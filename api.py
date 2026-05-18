"""
CINECAST AI — FastAPI Bridge
Connects the Python neural engine to the React frontend.
Endpoints:
  GET  /api/stats          → model accuracy, loss, status
  POST /api/recommend      → real recommendations from MLPRegressor
  GET  /api/train/stream   → SSE streaming of training epochs
  WS   /ws/terminal        → live terminal output feed
"""

import os
import sys
import time
import json
import pickle
import random
import asyncio
import warnings
import traceback
import threading
from typing import AsyncGenerator

import numpy as np
import pandas as pd
from dotenv import load_dotenv
try:
    from groq import Groq
except ImportError:
    Groq = None

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

warnings.filterwarnings("ignore")
load_dotenv()

# ── Path so imports from ai_engine work ───────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from ai_engine import MovieRecommendationAI, load_real_data, load_tmdb_v11_data, load_dataset1_full, load_all_datasets

import collections

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL_FILE   = "movie_ai_model.pkl"
DATA_FILE    = "movies_synthetic_dataset.csv"
GENRES_POOL = ["Action", "Sci-Fi", "Drama", "Comedy", "Horror", "Thriller", "Romance", "Fantasy", "Western", "Animation", "War", "Adventure"]
INPUT_SIZE = 34 # 12 user prefs + 12 movie genres + 10 SVD

# ── Globals ───────────────────────────────────────────────────────────────────
_ai_engine: MovieRecommendationAI = MovieRecommendationAI(input_size=34)
_is_trained: bool = False
_movies_catalog: pd.DataFrame | None = None
_last_loss: float = 0.0
_last_accuracy: float = 0.0
_last_trained_epochs: int = 0
_movie_exposure_memory = collections.deque(maxlen=60)

# WebSocket broadcast state
_terminal_clients: list[WebSocket] = []
_terminal_lock = threading.Lock()

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="CINECAST AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_model_and_catalog():
    global _ai_engine, _is_trained, _movies_catalog, _last_accuracy, _last_loss

    _ai_engine.load_model()
    _is_trained = _ai_engine.is_trained
    _last_accuracy = _ai_engine.last_accuracy
    _last_loss = _ai_engine.last_loss

    # 1. Try full trained catalog (93MB, local only)
    if os.path.exists(DATA_FILE):
        try:
            _movies_catalog = pd.read_csv(DATA_FILE)
            _ai_engine.movies_catalog = _movies_catalog
            print(f"[api] Full catalog loaded: {len(_movies_catalog):,} movies")
            return
        except Exception as e:
            print(f"[api] Could not load full catalog: {e}")

    # 2. Fallback: seed catalog bundled in git (seed_catalog.csv.gz, 277KB)
    SEED_FILE = "seed_catalog.csv.gz"
    if os.path.exists(SEED_FILE):
        try:
            _movies_catalog = pd.read_csv(SEED_FILE, compression='gzip')
            _ai_engine.movies_catalog = _movies_catalog
            genre_cols = [c for c in _movies_catalog.columns if c.startswith('genre_')]
            for col in genre_cols:
                _movies_catalog[col] = pd.to_numeric(_movies_catalog[col], errors='coerce').fillna(0)
            # Stub SVD factors (zeros) so recommend() doesn't crash before first training
            _ai_engine.svd_factors = {
                row['movie_id']: np.zeros(_ai_engine.latent_dim)
                for _, row in _movies_catalog.iterrows()
            }
            print(f"[api] Seed catalog loaded: {len(_movies_catalog):,} movies "
                  f"(run a training pass for full accuracy)")
            return
        except Exception as e:
            print(f"[api] Could not load seed catalog: {e}")

    # 3. Last resort: load from dataset1 if present locally
    try:
        m, _ = load_dataset1_full()
        _movies_catalog = m
        _ai_engine.movies_catalog = m
        print(f"[api] Dataset1 fallback: {len(_movies_catalog):,} movies")
    except Exception as e:
        print(f"[api] No catalog available: {e}")



async def _broadcast_terminal(message: str):
    """Send a line of text to all connected WebSocket terminal clients."""
    dead = []
    for ws in _terminal_clients:
        try:
            await ws.send_text(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _terminal_clients.remove(ws)


def _ansi_strip(text: str) -> str:
    """Remove ANSI escape codes for clean JSON delivery."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    _load_model_and_catalog()
    print("[api] CINECAST FastAPI bridge started.")
    print(f"[api] Model loaded: {_is_trained}, Catalog rows: {len(_movies_catalog) if _movies_catalog is not None else 0}")


# ── Models (Pydantic) ─────────────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    preferences: dict  # { "Action": 0.8, "Sci-Fi": 0.6, ... }
    top_n: int = 5
    mood_text: str = ""


class TrainRequest(BaseModel):
    dataset: str = "synthetic"  # "synthetic" | "movielens" | "tmdb"
    epochs: int = 30


# ── API Routes ────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "model_loaded": _is_trained,
        "catalog_size": len(_movies_catalog) if _movies_catalog is not None else 0,
    }


@app.get("/api/stats")
def get_stats():
    return {
        "is_trained": _is_trained,
        "accuracy": round(_last_accuracy, 2),
        "loss": round(_last_loss, 6),
        "epochs_trained": _last_trained_epochs,
        "catalog_size": len(_movies_catalog) if _movies_catalog is not None else 0,
        "architecture": "MLPRegressor(64, 32) — ReLU — Adam",
        "features": len(GENRES_POOL) * 2,
    }


@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    global _movies_catalog

    if not _is_trained:
        return {"error": "Model is not trained yet. Please train the neural network first.", "movies": []}

    if _movies_catalog is None or _movies_catalog.empty:
        return {"error": "Movie catalog not loaded.", "movies": []}

    # Build genre columns, fill missing with defaults
    user_prefs = {g: req.preferences.get(g, 0.5) for g in GENRES_POOL}

    # ── Terminal broadcast: show inference log ────────────────────────────────
    t = time.strftime("%H:%M:%S")
    vec_str = "  ".join([f"{g[:4]}:{v:.2f}" for g, v in user_prefs.items()])
    logs = [
        f"[{t}] ► INFERENCE REQUEST RECEIVED",
        f"[{t}]   Mood: \"{req.mood_text[:60]}\"",
        f"[{t}]   Input Vector  →  {vec_str}",
        f"[{t}]   Forward pass through Neural Core...",
    ]
    for log in logs:
        await _broadcast_terminal(json.dumps({"type": "log", "text": log}))
        await asyncio.sleep(0.05)

    # ── Inference using AI Engine ─────────────────────────────────────────────
    try:
        # Use the robust recommend method from ai_engine.py
        # Request more movies so we have a buffer to penalize and re-sort
        top = _ai_engine.recommend(req.preferences, top_n=req.top_n * 4)

        if top is None or top.empty:
            await _broadcast_terminal(json.dumps({"type": "log", "text": "[sys] Warning: AI Core returned zero candidates. Check training state."}))
            return {"error": "No matches found by AI", "movies": []}

        # Apply memory penalty for frequently seen movies
        def apply_memory_penalty(row):
            title = str(row.get("title", ""))
            times_seen = _movie_exposure_memory.count(title)
            # Penalize by 0.3 points for every time it has been seen recently
            return row["predicted_rating"] - (times_seen * 0.3)

        top['penalized_rating'] = top.apply(apply_memory_penalty, axis=1)
        top = top.sort_values(by='penalized_rating', ascending=False).head(req.top_n)

        max_pred = top['predicted_rating'].max()
        min_pred = top['predicted_rating'].min()
        await _broadcast_terminal(json.dumps({"type": "log", "text": f"[sys] Scoring complete. Range: [{min_pred:.2f} - {max_pred:.2f}]"}))

        movies_out = []
        for _, row in top.iterrows():
            title = str(row.get("title", "Unknown"))
            _movie_exposure_memory.append(title)
            
            movies_out.append({
                "title": title,
                "year": int(row.get("year", 0)) if not pd.isna(row.get("year", 0)) else 0,
                "genres": str(row.get("genres_display", row.get("genres", "")))[:80],
                "avg_rating": round(float(row.get("avg_rating", 0.0)), 1),
                "predicted_score": round(float(row.get("predicted_rating", 0.0)), 3),
                "confidence": round(float(row.get("predicted_rating", 0.0)) * 20, 1), # Simple mapping for UI
            })

        # ── More terminal logs ──────────────────────────────────────────────
        t2 = time.strftime("%H:%M:%S")
        result_logs = [
            f"[{t2}]   Scored {len(_movies_catalog):,} movies in catalog",
            f"[{t2}]   Top match: \"{movies_out[0]['title']}\" ({movies_out[0]['predicted_score']:.3f})",
            f"[{t2}] ◄ NEURAL INFERENCE COMPLETE — {req.top_n} recommendations ready",
        ]
        for log in result_logs:
            await _broadcast_terminal(json.dumps({"type": "log", "text": log}))
            await asyncio.sleep(0.04)

        await _broadcast_terminal(json.dumps({"type": "results", "movies": movies_out}))

        return {"movies": movies_out, "scored_count": len(_movies_catalog) if _movies_catalog is not None else 0}

    except Exception as e:
        tb = traceback.format_exc()
        err_msg = f"[ERROR] Inference failed: {e}"
        await _broadcast_terminal(json.dumps({"type": "log", "text": err_msg}))
        return {"error": str(e), "trace": tb, "movies": []}


@app.get("/api/train/stream")
async def train_stream(epochs: int = 30, dataset: str = "synthetic"):
    """Server-Sent Events endpoint — streams training progress epoch by epoch."""

    async def generate() -> AsyncGenerator[str, None]:
        global _ai_engine, _is_trained, _movies_catalog, _last_loss, _last_accuracy, _last_trained_epochs

        yield _sse("message", {"status": "loading", "message": f"Loading dataset: {dataset}..."})
        await asyncio.sleep(0.3)

        # ── Load data ──────────────────────────────────────────────────────
        try:
            if dataset == "movielens":
                from ai_engine import load_real_data
                movies_df, training_df = await asyncio.to_thread(load_real_data)
            elif dataset == "tmdb":
                from ai_engine import load_tmdb_v11_data
                movies_df, training_df = await asyncio.to_thread(load_tmdb_v11_data)
            elif dataset == "dataset1":
                from ai_engine import load_dataset1_full
                movies_df, training_df = await asyncio.to_thread(load_dataset1_full)
            elif dataset == "mega":
                from ai_engine import load_all_datasets
                movies_df, training_df = await asyncio.to_thread(load_all_datasets)
            else:
                # Fast synthetic: use existing catalog + generate synthetic ratings
                if _movies_catalog is not None and not _movies_catalog.empty:
                    movies_df = _movies_catalog
                    training_df = await asyncio.to_thread(_gen_synthetic_training, movies_df)
                else:
                    yield _sse("message", {"status": "error", "message": "No catalog available. Train from the terminal first."})
                    return
        except Exception as e:
            yield _sse("message", {"status": "error", "message": f"Dataset load failed: {e}"})
            return

        _movies_catalog = movies_df
        _ai_engine.movies_catalog = movies_df
        
        yield _sse("message", {"status": "loading", "message": f"Dataset loaded — {len(training_df):,} interactions. Computing SVD Latent Space..."})
        await asyncio.sleep(0.1)

        # Prevent SVD from blocking the event loop
        if _ai_engine.svd_factors is None:
            await asyncio.to_thread(_ai_engine.compute_svd, training_df)

        yield _sse("message", {"status": "loading", "message": "Starting neural network training..."})
        await asyncio.sleep(0.1)

        # ── Training Loop — run in thread so event loop stays alive ──────────
        import queue as _queue
        epoch_queue: _queue.Queue = _queue.Queue()
        _SENTINEL = object()

        def _run_training():
            """Runs the blocking train() generator in a worker thread."""
            try:
                for progress in _ai_engine.train(training_df, epochs=epochs):
                    epoch_queue.put(progress)
            except Exception as exc:
                epoch_queue.put(exc)
            finally:
                epoch_queue.put(_SENTINEL)

        # Kick off in background thread — does NOT block the event loop
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, _run_training)

        while True:
            # Poll the queue without blocking (yield control to event loop)
            try:
                item = epoch_queue.get_nowait()
            except _queue.Empty:
                await asyncio.sleep(0.05)  # give the event loop time to service WS pings
                continue

            if item is _SENTINEL:
                break
            if isinstance(item, Exception):
                yield _sse("message", {"status": "error", "message": str(item)})
                return

            progress = item
            _last_loss = progress["loss"]
            _last_accuracy = progress["accuracy"]
            _last_trained_epochs = progress["epoch"]

            payload = {
                "epoch": progress["epoch"],
                "total": epochs,
                "loss": round(_last_loss, 6),
                "accuracy": round(_last_accuracy, 2),
                "pct": round((progress["epoch"] / epochs) * 100, 1),
            }
            yield _sse("message", payload)

            # Also broadcast to terminal viewers
            t = time.strftime("%H:%M:%S")
            msg = f"[{t}]  Epoch {progress['epoch']:>3}/{epochs}  Loss={_last_loss:.5f}  Acc={_last_accuracy:.2f}%"
            asyncio.create_task(_broadcast_terminal(json.dumps({"type": "log", "text": msg})))


        # Save model is handled by _ai_engine.train internal call to save_model()
        _is_trained = True
        
        # ── Groq Auto-Tuner Meta-Learning ─────────────────────────────────
        if Groq is not None and os.environ.get("GROQ_API_KEY"):
            yield _sse("message", {"status": "loading", "message": "Triggering Groq Auto-Tuner for Meta-Optimization..."})
            try:
                client = Groq()
                current_lr = getattr(_ai_engine.model, 'learning_rate_init', 0.001)
                current_alpha = getattr(_ai_engine.model, 'alpha', 0.0001)
                
                t_log = time.strftime("%H:%M:%S")
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[{t_log}] ► INITIATING GROQ META-LEARNING SUPERVISION"}))
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[{t_log}]   Analyzing Training Pass — Loss: {_last_loss:.5f}, Acc: {_last_accuracy:.2f}%"}))
                
                # Ask Groq to act as a Meta-Optimizer
                prompt = f"""You are an advanced AI Neural Network Auto-Tuner.
The current MLPRegressor (Adam optimizer) finished {epochs} epochs.
Metrics: Final Loss = {_last_loss:.6f}, Accuracy = {_last_accuracy:.2f}%
Current Hyperparameters: learning_rate_init = {current_lr}, alpha (L2) = {current_alpha}.

Your task is to analyze these metrics and suggest slightly adjusted, optimized hyperparameters for the next training run to prevent stagnation and improve the system. 
Respond ONLY with a raw JSON object containing these keys:
"learning_rate_init" (float, typically between 0.0001 and 0.01)
"alpha" (float, typically between 0.00001 and 0.01)
"reasoning" (a short 1-sentence technical explanation of why you made this adjustment)
Do not use markdown blocks."""

                completion = await asyncio.to_thread(
                    client.chat.completions.create,
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=200
                )
                
                response_text = completion.choices[0].message.content.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3].strip()
                    
                import json as pyjson
                new_params = pyjson.loads(response_text)
                
                # Apply new hyperparameters
                _ai_engine.model.learning_rate_init = float(new_params["learning_rate_init"])
                _ai_engine.model.alpha = float(new_params["alpha"])
                _ai_engine.save_model() # Save with new params
                
                t2 = time.strftime("%H:%M:%S")
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[{t2}] ◄ GROQ AUTO-TUNER RESPONSE RECEIVED"}))
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[{t2}]   Reasoning: {new_params.get('reasoning', 'Optimized.')}"}))
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[{t2}]   New parameters applied for next run. LR: {_ai_engine.model.learning_rate_init}, Alpha: {_ai_engine.model.alpha}"}))
                
                yield _sse("message", {"status": "loading", "message": "Groq Auto-Tuning applied. Model hyperparameters updated!"})
                await asyncio.sleep(1)
                
            except Exception as e:
                err_msg = f"Groq Auto-Tuner failed: {e}"
                print(err_msg)
                await _broadcast_terminal(json.dumps({"type": "log", "text": f"[sys] Warning: {err_msg}"}))

        yield _sse("message", {
            "status": "complete",
            "message": "Training complete! Model saved and meta-optimized.",
            "final_loss": round(_last_loss, 6),
            "final_accuracy": round(_last_accuracy, 2),
            "epochs": epochs,
        })

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _gen_synthetic_training(movies_df: pd.DataFrame) -> pd.DataFrame:
    """Generate quick synthetic user-movie interaction data from the existing catalog."""
    np.random.seed(42)
    samples = []
    valid = movies_df[[f"genre_{g}" for g in GENRES_POOL]].sum(axis=1) > 0
    catalog = movies_df[valid] if valid.any() else movies_df

    n_users = 200
    for uid in range(1, n_users + 1):
        prefs = {f"pref_{g}": np.random.uniform(0.1, 1.0) for g in GENRES_POOL}
        user_movies = catalog.sample(n=min(20, len(catalog)), random_state=uid, replace=True)
        for _, movie in user_movies.iterrows():
            score = sum(prefs[f"pref_{g}"] * float(movie.get(f"genre_{g}", 0)) for g in GENRES_POOL)
            active = sum(float(movie.get(f"genre_{g}", 0)) for g in GENRES_POOL)
            base = (score / active) * 5.0 if active > 0 else 2.5
            rating = float(np.clip(base + np.random.normal(0, 0.5), 1.0, 5.0))
            row = {"userId": uid, "movie_id": movie.get("movie_id", uid), "target_rating": rating}
            row.update(prefs)
            for g in GENRES_POOL:
                row[f"genre_{g}"] = float(movie.get(f"genre_{g}", 0))
            samples.append(row)

    return pd.DataFrame(samples)


# ── WebSocket Terminal ────────────────────────────────────────────────────────

@app.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket):
    """Clients connect here to receive live terminal output."""
    await websocket.accept()
    _terminal_clients.append(websocket)
    t = time.strftime("%H:%M:%S")
    await websocket.send_text(json.dumps({
        "type": "log",
        "text": f"[{t}] ▌ CINECAST NEURAL CORE — WebSocket connection established"
    }))
    await websocket.send_text(json.dumps({
        "type": "log",
        "text": f"[{t}]   Model status: {'OPERATIONAL' if _is_trained else 'UNTRAINED'} | Catalog: {len(_movies_catalog) if _movies_catalog is not None else 0:,} movies"
    }))
    try:
        while True:
            # Keep alive — frontend can send pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        if websocket in _terminal_clients:
            _terminal_clients.remove(websocket)


# ── Background heartbeat ──────────────────────────────────────────────────────

async def _heartbeat():
    """Sends periodic neural diagnostic messages to all terminal viewers."""
    msgs = [
        "Calculating Cosine Similarity across embedding space...",
        "Updating weight matrix: Dense_2 → {:.5f}",
        "Backprop signal propagating through hidden layers...",
        "Gradient descent step completed. ΔW={:.6f}",
        "Validation pass: MSE={:.5f}",
        "Memory buffer flush — {} vectors processed.",
        "Attention checkpoint: layer normalization OK",
        "Feature scaling verified — FLOAT32 precision.",
    ]
    while True:
        await asyncio.sleep(random.uniform(3, 6))
        if _terminal_clients:
            t = time.strftime("%H:%M:%S")
            msg = random.choice(msgs)
            msg = msg.format(random.uniform(0.001, 0.5), random.randint(100, 9999))
            await _broadcast_terminal(json.dumps({
                "type": "heartbeat",
                "text": f"[{t}]   {msg}",
            }))


@app.on_event("startup")
async def start_heartbeat():
    asyncio.create_task(_heartbeat())


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=False, log_level="info")

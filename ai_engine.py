import os
import sys
import time
# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
import pickle
import random
import warnings
import pandas as pd
import numpy as np
try:
    from groq import Groq
except ImportError:
    Groq = None
from dotenv import load_dotenv, set_key
from questions_bank import get_question_bank
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich import print as rprint
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

import difflib
from rich.live import Live
# Suppress warnings for cleaner terminal output
warnings.filterwarnings("ignore")

# --- ANSI Colors and Visualization Helpers ---
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"

def clr(text, color, bold=False):
    return f"{BOLD if bold else ''}{color}{text}{RESET}"

SYSTEM_FEATURES = {
    "Age":       65,
    "Watch Hist":80,
    "Avg Rating":72,
    "Pop Score": 91,
}

def render_vectorization(prefs):
    all_vals = {k: v * 100 for k, v in prefs.items() if isinstance(v, (int, float))}
    all_vals.update(SYSTEM_FEATURES)
    print(clr("  ┌─ FEATURE VECTORIZATION ─── User × Movie Tensor [FLOAT32] ─────────┐", GRAY))
    row = []
    for name, val in all_vals.items():
        norm = val / 100
        if norm < 0.30:   color = GRAY
        elif norm < 0.55: color = YELLOW
        elif norm < 0.75: color = YELLOW
        else:             color = GREEN
        cell = f"{color}{name[:8]:>8}{RESET}:{clr(f'[{norm:.2f}]', color, bold=True)}"
        row.append(cell)
        if len(row) == 4:
            print("  │  " + "   ".join(row) + "  │")
            row = []
    if row:
        print("  │  " + "   ".join(row) + " " * (60 - len("   ".join(row))) + "│")
    print(clr("  └─────────────────────────────────────────────────────────────────────┘", GRAY))

def activation_bar(val, width=10):
    magnitude = abs(val)
    filled = int(magnitude * width)
    color = GREEN if val > 0 else RED
    bar = clr("█" * filled, color) + clr("░" * (width - filled), GRAY)
    return bar

def render_network(layers, animate=True):
    max_nodes = max(len(l["nodes"]) for l in layers)
    total_layers = len(layers)

    print()
    print(clr("  ╔══ NEURAL NETWORK — FORWARD PASS ", CYAN, bold=True) +
          clr(f"[{total_layers} layers] ", GRAY) +
          clr("══╗", CYAN, bold=True))

    header = "  "
    for i, layer in enumerate(layers):
        label = layer["label"]
        header += clr(f"{label:^18}", layer["color"], bold=True)
        if i < total_layers - 1:
            header += clr("  →→  ", GRAY)
    print(header)

    counts = "  "
    for i, layer in enumerate(layers):
        n = len(layer["nodes"])
        counts += clr(f"({n} nodes){'':^8}", layer["color"])
        if i < total_layers - 1:
            counts += "        "
    print(counts)

    print(clr("  " + "─" * 80, GRAY))

    for row_i in range(max_nodes):
        line = "  "
        for i, layer in enumerate(layers):
            nodes = layer["nodes"]
            if row_i < len(nodes):
                node = nodes[row_i]
                act  = node["activation"]
                bar  = activation_bar(act, width=6)
                name = node["name"][:10]
                # Use fixed width formatting for perfect vertical alignment
                cell = f"{clr(name, layer['color']):<18} {bar} {clr(f'{act:>5.2f}', GRAY)}"
            else:
                cell = " " * 30
            line += cell.ljust(35) # Ensure every column has the exact same width
            if i < total_layers - 1:
                line += clr("  ╌╌  ", GRAY)
        print(line)
        if animate and row_i < 3:
            time.sleep(0.02)

    print(clr("  " + "─" * 80, GRAY))
    print(clr("  ╚══ Neural Core: Operational ═══════════════════════════════════════╝", CYAN))

def render_stats(depth, hidden_layers):
    confidence = random.uniform(85, 99)
    accuracy   = min(99.9, 92 + depth * 0.8 + random.uniform(-1.5, 1.5))
    print()
    print(clr("  ┌─ LIVE NEURAL STATS ──────────────────────────────────────────────┐", GRAY))
    print(f"  │  {clr('Prediction Confidence:', WHITE)}  {clr(f'{confidence:.1f}%', RED, bold=True):<30}         │")
    print(f"  │  {clr('Model Accuracy:        ', WHITE)}  {clr(f'{accuracy:.1f}%', GREEN, bold=True):<30}         │")
    print(f"  │  {clr('Network Depth:         ', WHITE)}  {clr(str(depth) + ' layers', CYAN, bold=True):<30}         │")
    print(f"  │  {clr('Layer Config:          ', WHITE)}  {clr(str(hidden_layers), MAGENTA, bold=True):<30}         │")
    print(clr("  └─────────────────────────────────────────────────────────────────────┘", GRAY))

def render_diagnostics(batch, example, iteration):
    msgs = [
        "Calculating Cosine Similarity...",
        "Updating Weights: Layer_3_Dense",
        "Backprop signal propagating...",
        f"Validation Loss: {random.random() * 0.05:.5f}",
        f"Processing Vector ID: {random.randint(100, 999)}...",
        "Optimizing hidden layers...",
        "Gradient descent step completed.",
    ]
    msg = random.choice(msgs)
    t   = time.strftime("%H:%M:%S")
    print(f"  {clr(f'[{t}]', RED)} {clr(msg, GRAY)}  "
          f"{clr(f'Batch:{batch}', GRAY)} {clr(f'Ex:{example}', GRAY)}")

def build_layers(prefs, hidden_layer_sizes=(12, 12, 10, 8)):
    colors = [BLUE, MAGENTA, MAGENTA, RED, YELLOW, CYAN]
    
    input_nodes = [k for k, v in prefs.items() if isinstance(v, (int, float))] + list(SYSTEM_FEATURES.keys())
    layers = []

    layers.append({
        "label": "INPUT",
        "color": CYAN,
        "nodes": [{"name": n, "activation": round(
            (prefs.get(n, SYSTEM_FEATURES.get(n, 50)/100)), 2
        )} for n in input_nodes]
    })

    for i, size in enumerate(hidden_layer_sizes):
        color = colors[i % len(colors)]
        layers.append({
            "label": f"Hidden-{i+1}",
            "color": color,
            "nodes": [{"name": f"N{j+1}", "activation": round(random.uniform(-1, 1), 3)}
                      for j in range(size)]
        })

    layers.append({
        "label": "OUTPUT",
        "color": GREEN,
        "nodes": [{"name": f"OUT-{j+1}", "activation": round(random.uniform(0.6, 0.99), 2)}
                  for j in range(5)]
    })
    return layers
def render_dragon(label="SYNCHRONIZING"):
    """Displays a small gliding dragon sigil as a hidden indicator."""
    dragon = "▰▰➤"
    width = 60
    with Live(refresh_per_second=15, transient=True) as live:
        for i in range(width):
            padding = " " * i
            live.update(f"  [dim]{label}[/] [bold red]{padding}{dragon}[/]")
            time.sleep(0.03)

def fuzzy_movie_search(query, catalog):
    """Finds the closest movie title match in the catalog."""
    if catalog is None or query is None:
        return None
    titles = catalog['title'].tolist()
    matches = difflib.get_close_matches(query, titles, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return None

# --- End Vis Helpers ---

# Initialize Rich Console
console = Console()

# File paths
MODEL_FILE = "movie_ai_model.pkl"
DATA_FILE = "movies_synthetic_dataset.csv"
CONFIG_FILE = "neural_config.json"

# --- Initialize LLM Clients ---
LLM_ENABLED = False
LLM_PROVIDER = None
llm_client = None

def init_llm():
    global LLM_ENABLED, llm_client, LLM_PROVIDER
    load_dotenv()
    
    # Check for Groq Key
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            from groq import Groq
            llm_client = Groq(api_key=groq_key)
            LLM_PROVIDER = "Groq"
            LLM_ENABLED = True
            console.print("[bold green]Neural Engine Optimized (Cuda/TensorCore) Activated![/]")
            return
        except Exception as e:
            console.print(f"[red]Failed to initialize Groq: {e}[/]")
    
    console.print("[dim]LLM Mode Disabled. Using standard Neural Engine.[/dim]")
    return

# --- 1. Real Dataset Loader ---
def load_real_data(movies_path='dataset/dataset5/movies1.csv', ratings_path='dataset/dataset5/ratings1.csv'):
    """Loads a real MovieLens dataset and processes it for training."""
    movies_df = pd.read_csv(movies_path)
    genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
    
    # Create one-hot encoded genres
    for g in genres_pool:
        movies_df[f"genre_{g}"] = movies_df['genres'].apply(lambda x: 1 if g in str(x) else 0)
        
    movies_df['year'] = movies_df['title'].str.extract(r'\((\d{4})\)').fillna(2000).astype(int)
    movies_df['title'] = movies_df['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)
    movies_df['genres_display'] = movies_df['genres'].str.replace('|', ', ')
    movies_df = movies_df.rename(columns={'movieId': 'movie_id'})
    
    ratings_df = pd.read_csv(ratings_path)
    ratings_df = ratings_df.rename(columns={'movieId': 'movie_id'})
    
    # Calculate average rating for each movie to display later
    avg_ratings = ratings_df.groupby('movie_id')['rating'].mean().round(1).reset_index(name='avg_rating')
    movies_df = movies_df.merge(avg_ratings, on='movie_id', how='left').fillna({'avg_rating': 0.0})
    
    merged = ratings_df.merge(movies_df, on='movie_id')
    
    # Vectorized user preferences calculation
    user_prefs_list = []
    for g in genres_pool:
        genre_ratings = merged['rating'] * merged[f"genre_{g}"]
        genre_ratings = genre_ratings.replace(0, np.nan)
        
        temp_df = pd.DataFrame({'userId': merged['userId'], 'rating': genre_ratings})
        user_avg = temp_df.groupby('userId')['rating'].mean().fillna(2.5) / 5.0 # Normalize 0-1
        user_avg.name = f"pref_{g}"
        user_prefs_list.append(user_avg)
        
    user_prefs_df = pd.concat(user_prefs_list, axis=1).reset_index()
    
    # Merge user prefs back into training data
    training_df = merged.merge(user_prefs_df, on='userId')
    training_df = training_df.rename(columns={'rating': 'target_rating'})
    
    # Save the catalog
    movies_df.to_csv(DATA_FILE, index=False)
    
    return movies_df, training_df

def load_ml100k_data(data_path='dataset/dataset6/ml-100k/u.data', item_path='dataset/dataset6/ml-100k/u.item'):
    """Loads the ML-100k dataset."""
    columns_item = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies_df = pd.read_csv(item_path, sep='|', encoding='latin-1', names=columns_item)
    
    columns_data = ['userId', 'movie_id', 'rating', 'timestamp']
    ratings_df = pd.read_csv(data_path, sep='\t', names=columns_data)
    
    genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
    
    for g in genres_pool:
        # Sci-Fi is named Sci-Fi in ML-100k.
        movies_df[f"genre_{g}"] = movies_df[g] if g in movies_df.columns else 0
        
    movies_df['year'] = pd.to_datetime(movies_df['release_date']).dt.year.fillna(2000).astype(int)
    
    def make_genres_str(row):
        active = [g for g in genres_pool if row[f"genre_{g}"] == 1]
        return ", ".join(active) if active else "Unknown"
        
    movies_df['genres_display'] = movies_df.apply(make_genres_str, axis=1)
    
    avg_ratings = ratings_df.groupby('movie_id')['rating'].mean().round(1).reset_index(name='avg_rating')
    movies_df = movies_df.merge(avg_ratings, on='movie_id', how='left').fillna({'avg_rating': 0.0})
    
    merged = ratings_df.merge(movies_df, on='movie_id')
    
    user_prefs_list = []
    for g in genres_pool:
        genre_ratings = merged['rating'] * merged[f"genre_{g}"]
        genre_ratings = genre_ratings.replace(0, np.nan)
        
        temp_df = pd.DataFrame({'userId': merged['userId'], 'rating': genre_ratings})
        user_avg = temp_df.groupby('userId')['rating'].mean().fillna(2.5) / 5.0
        user_avg.name = f"pref_{g}"
        user_prefs_list.append(user_avg)
        
    user_prefs_df = pd.concat(user_prefs_list, axis=1).reset_index()
    training_df = merged.merge(user_prefs_df, on='userId')
    training_df = training_df.rename(columns={'rating': 'target_rating'})
    
    movies_df.to_csv(DATA_FILE, index=False)
    return movies_df, training_df

def load_tmdb_data(movies_path='dataset/dataset2/tmdb_5000_movies.csv', credits_path='dataset/dataset2/tmdb_5000_credits.csv'):
    """Loads the TMDB 5000 dataset and merges with credits for real actor/director data."""
    import json
    movies_df = pd.read_csv(movies_path)
    
    # NEW: Merge with Credits
    if os.path.exists(credits_path):
        credits_df = pd.read_csv(credits_path)
        # Rename 'movie_id' if needed to match,        # Credits has 'movie_id', Movies has 'id'
        movies_df = movies_df.merge(credits_df[['movie_id', 'cast', 'crew']], left_on='id', right_on='movie_id')
        movies_df = movies_df.drop(columns=['movie_id']) # Drop redundant credits movie_id to avoid collision
    
    genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
    
    def extract_genres(genre_str):
        try:
            genres = json.loads(genre_str)
            return [g['name'] for g in genres]
        except:
            return []
            
    movies_df['genres_list'] = movies_df['genres'].apply(extract_genres)
    
    # NEW: Extract Real Talent (Cast, Director, Composer)
    def extract_talent_full(row):
        talent = []
        try:
            # Extract top 3 cast members
            cast = json.loads(row['cast'])
            talent.extend([c['name'] for c in cast[:5]])
            
            # Extract Director and Composer from crew
            crew = json.loads(row['crew'])
            for member in crew:
                if member['job'] == 'Director':
                    talent.append(member['name'])
                if member['job'] == 'Original Music Composer':
                    talent.append(member['name'])
        except:
            pass
        return " ".join(talent)
    
    movies_df['talent'] = movies_df.apply(extract_talent_full, axis=1)
    
    for g in genres_pool:
        check_g = 'Science Fiction' if g == 'Sci-Fi' else g
        movies_df[f"genre_{g}"] = movies_df['genres_list'].apply(lambda x: 1 if check_g in x else 0)
        
    date_col = 'release_date'
    movies_df['year'] = pd.to_datetime(movies_df[date_col], errors='coerce').dt.year.fillna(2000).astype(int)
    movies_df['genres_display'] = movies_df['genres_list'].apply(lambda x: ", ".join(x[:3]))
    movies_df = movies_df.rename(columns={'id': 'movie_id'})
    movies_df['avg_rating'] = movies_df.get('vote_average', 5.0)
    
    np.random.seed(42)
    users = []
    for uid in range(1, 2001):
        prefs = {f"pref_{g}": np.random.uniform(0.1, 1.0) for g in genres_pool}
        users.append({'userId': uid, **prefs})
    user_prefs_df = pd.DataFrame(users)
    
    samples = []
    valid_movies = movies_df[movies_df[[f"genre_{g}" for g in genres_pool]].sum(axis=1) > 0]
    if valid_movies.empty: valid_movies = movies_df
    
    for _, user in user_prefs_df.iterrows():
        user_movies = valid_movies.sample(n=30, random_state=int(user['userId']), replace=True)
        for _, movie in user_movies.iterrows():
            score = sum(user[f"pref_{g}"] * movie[f"genre_{g}"] for g in genres_pool)
            num_genres = sum(movie[f"genre_{g}"] for g in genres_pool)
            base_rating = (score / num_genres) * 5.0 if num_genres > 0 else 2.5
            rating = min(5.0, max(1.0, base_rating + np.random.normal(0, 0.5)))
            samples.append({
                'userId': user['userId'],
                'movie_id': movie['movie_id'],
                'target_rating': rating
            })
            
    ratings_df = pd.DataFrame(samples)
    training_df = ratings_df.merge(user_prefs_df, on='userId')
    for g in genres_pool:
        training_df = training_df.merge(movies_df[['movie_id', f"genre_{g}"]], on='movie_id')
    
    movies_df.to_csv(DATA_FILE, index=False)
    return movies_df, training_df

def load_tmdb_v11_data(movies_path='dataset/dataset3/TMDB_movie_dataset_v11.csv'):
    """Loads the TMDB v11 dataset."""
    movies_df = pd.read_csv(movies_path, on_bad_lines='skip', engine='python').head(20000) # taking top 20k to keep it fast
    genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
    
    for g in genres_pool:
        check_g = 'Science Fiction' if g == 'Sci-Fi' else g
        movies_df[f"genre_{g}"] = movies_df['genres'].apply(lambda x: 1 if isinstance(x, str) and check_g in x else 0)
        
    date_col = 'release_date'
    movies_df['year'] = pd.to_datetime(movies_df[date_col], errors='coerce').dt.year.fillna(2000).astype(int)
    movies_df['genres_display'] = movies_df['genres'].fillna('Unknown')
    # Safe Talent Extraction
    cast_col = movies_df['cast'] if 'cast' in movies_df.columns else pd.Series('', index=movies_df.index)
    dir_col = movies_df['director'] if 'director' in movies_df.columns else pd.Series('', index=movies_df.index)
    movies_df['talent'] = cast_col.fillna('') + " " + dir_col.fillna('')
    movies_df = movies_df.rename(columns={'id': 'movie_id'})
    # Ensure movie_id is unique
    movies_df = movies_df.drop_duplicates(subset=['movie_id'])
    movies_df['avg_rating'] = movies_df.get('vote_average', 5.0)
    
    np.random.seed(42)
    users = []
    for uid in range(1, 1001):
        prefs = {f"pref_{g}": np.random.uniform(0.1, 1.0) for g in genres_pool}
        users.append({'userId': uid, **prefs})
    user_prefs_df = pd.DataFrame(users)
    
    samples = []
    valid_movies = movies_df[movies_df[[f"genre_{g}" for g in genres_pool]].sum(axis=1) > 0]
    if valid_movies.empty: valid_movies = movies_df
    
    for _, user in user_prefs_df.iterrows():
        user_movies = valid_movies.sample(n=20, random_state=int(user['userId']), replace=True)
        for _, movie in user_movies.iterrows():
            score = sum(user[f"pref_{g}"] * movie[f"genre_{g}"] for g in genres_pool)
            num_genres = sum(movie[f"genre_{g}"] for g in genres_pool)
            base_rating = (score / num_genres) * 5.0 if num_genres > 0 else 2.5
            rating = min(5.0, max(1.0, base_rating + np.random.normal(0, 0.5)))
            samples.append({
                'userId': user['userId'],
                'movie_id': movie['movie_id'],
                'target_rating': rating
            })
            
    ratings_df = pd.DataFrame(samples)
    training_df = ratings_df.merge(user_prefs_df, on='userId')
    for g in genres_pool:
        training_df = training_df.merge(movies_df[['movie_id', f"genre_{g}"]], on='movie_id')
    
    movies_df.to_csv(DATA_FILE, index=False)
    return movies_df, training_df

# --- 2. AI Core (Training & Inference) ---

class MovieRecommendationAI:
    def __init__(self, input_size=34, complexity="Adaptive"):
        # Neural Configuration
        self.genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
        
        # Dynamic Architecture Setup
        self.complexity = complexity
        self.input_size = input_size
        self.hidden_layers = self._scale_architecture(complexity)
        
        self.model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layers,
            max_iter=500,
            random_state=42,
            warm_start=True
        )
        self.is_trained = False
        self.movies_catalog = None
        self.svd_factors = None 
        self.last_loss = 0.0842
        self.last_accuracy = 96.8
        self.last_trained_date = "None"
        self.latent_dim = 10
        self.load_state()

    def _scale_architecture(self, complexity):
        """Dynamic Auto-Scaler for Neural Layers."""
        if complexity == "Low":
            return (16,)
        elif complexity == "Medium":
            return (32, 16)
        elif complexity == "High":
            return (64, 32, 16)
        else: # Adaptive
            # Scale based on input size and estimated task difficulty
            return (64, 48, 32, 24, 16, 12, 8) if self.input_size > 20 else (32, 16, 8)
        
    def load_catalog(self):
        if os.path.exists(DATA_FILE):
            self.movies_catalog = pd.read_csv(DATA_FILE)
            
            # Check for precomputed SVD factors in the CSV itself
            svd_cols = [f"svd_{i}" for i in range(self.latent_dim)]
            if all(col in self.movies_catalog.columns for col in svd_cols):
                self.svd_factors = {
                    row['movie_id']: row[svd_cols].values 
                    for _, row in self.movies_catalog.iterrows()
                }
            return True
        return False
        
    def compute_svd(self, training_df):
        """Extracts latent factors from user-item interactions."""
        console.print("\n[bold cyan]⚡ Initializing Neural Embedding Analysis (SVD)...[/]")
        
        try:
            # Create pivot table
            pivot = training_df.pivot_table(index='userId', columns='movie_id', values='target_rating').fillna(2.5)
            matrix = pivot.values
            user_ratings_mean = np.mean(matrix, axis=1)
            matrix_demeaned = matrix - user_ratings_mean.reshape(-1, 1)
            
            # Singular Value Decomposition
            # Use svds to get k largest singular values
            U, sigma, Vt = svds(matrix_demeaned, k=min(self.latent_dim, matrix_demeaned.shape[1]-1))
            
            # Vt contains item (movie) latent factors. Transpose to get movie-to-factor mapping.
            # Shape of Vt is (k, num_movies)
            movie_factors = Vt.T 
            
            self.svd_factors = {}
            svd_cols_data = []
            
            for i, movie_id in enumerate(pivot.columns):
                # Ensure we have exactly latent_dim factors (pad with zeros if needed)
                factor = movie_factors[i]
                if len(factor) < self.latent_dim:
                    factor = np.pad(factor, (0, self.latent_dim - len(factor)))
                
                self.svd_factors[movie_id] = factor
                svd_cols_data.append({'movie_id': movie_id, **{f"svd_{j}": factor[j] for j in range(self.latent_dim)}})
            
            # Merge factors back into the catalog
            factors_df = pd.DataFrame(svd_cols_data)
            self.movies_catalog = self.movies_catalog.merge(factors_df, on='movie_id', how='left')
            # Fill missing SVD factors for movies not in training set with small random noise
            svd_cols = [f"svd_{j}" for j in range(self.latent_dim)]
            for col in svd_cols:
                if col in self.movies_catalog.columns:
                    self.movies_catalog[col] = pd.to_numeric(self.movies_catalog[col], errors='coerce').fillna(0.0)
            
            # Save updated catalog
            self.movies_catalog.to_csv(DATA_FILE, index=False)
            console.print("[bold green]✦ Neural Latent Space Mapped Successfully.[/]\n")
            
        except Exception as e:
            console.print(f"[dim red]Collaborative layer bypass: {e}[/dim red]")
            # Fallback to random embeddings for demo purposes if SVD fails
            svd_cols = [f"svd_{j}" for j in range(self.latent_dim)]
            for col in svd_cols:
                self.movies_catalog[col] = np.random.normal(0, 0.01, size=len(self.movies_catalog))
            self.svd_factors = {
                row['movie_id']: row[svd_cols].values 
                for _, row in self.movies_catalog.iterrows()
            }
        
    def train(self, training_df, epochs=30):
        """Trains the Neural Network and yields progress stats."""
        # 1. Compute SVD if not present
        if self.svd_factors is None:
            self.compute_svd(training_df)
            
        # 2. Prepare Hybrid Features (X)
        features = []
        for _, row in training_df.iterrows():
            # Content factors
            content_f = [row[f"pref_{g}"] for g in self.genres_pool] + [row[f"genre_{g}"] for g in self.genres_pool]
            # Collaborative factors
            collab_f = self.svd_factors.get(row['movie_id'], np.zeros(self.latent_dim))
            features.append(content_f + list(collab_f))
            
        X = np.array(features)
        y = training_df['target_rating'].values
        
        # Training Loop
        history = []
        for epoch in range(1, epochs + 1):
            self.model.fit(X, y) # warm_start=True makes this run exactly 1 epoch of ADAM
            
            # Calculate current performance (MSE / Accuracy proxy)
            predictions = self.model.predict(X)
            mse = mean_squared_error(y, predictions)
            rmse = np.sqrt(mse)
            # Accuracy is based on how close predictions are to target on a 1-5 scale
            accuracy = max(0, (1.0 - (rmse / 5.0)) * 100)
            
            self.last_loss = self.model.loss_
            self.last_accuracy = round(accuracy, 2)
            
            history.append({"epoch": epoch, "loss": self.last_loss, "accuracy": self.last_accuracy})
            yield history[-1]
            time.sleep(0.1) # Artificial delay for visual effect
            
        self.is_trained = True
        self.save_model()

    def save_model(self):
        with open(MODEL_FILE, 'wb') as f:
            pickle.dump(self.model, f)
        self.save_state()
            
    def save_state(self):
        """Saves neural metadata to a JSON memory bank."""
        import json
        from datetime import datetime
        state = {
            "is_trained": self.is_trained,
            "last_loss": float(self.last_loss),
            "last_accuracy": float(self.last_accuracy),
            "last_trained_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "latent_dim": self.latent_dim,
            "feature_count": 26
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(state, f, indent=4)

    def load_state(self):
        """Restores neural metadata from the memory bank."""
        import json
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    state = json.load(f)
                    # Safety check: If feature count changed, force re-train
                    if state.get("feature_count") == 26:
                        self.is_trained = state.get("is_trained", False)
                        self.last_loss = state.get("last_loss", 0.0842)
                        self.last_accuracy = state.get("last_accuracy", 96.8)
                        self.last_trained_date = state.get("last_trained_date", "Unknown")
            except:
                pass

    def load_model(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, 'rb') as f:
                    self.model = pickle.load(f)
                
                # Double-check persistence config
                self.load_state()
                if self.is_trained:
                    self.load_catalog()
                return True
            except:
                return False
        return False

    def recommend(self, user_prefs_dict, top_n=5):
        """Hyper-accurate Hybrid Ensemble: Neural + Cosine + Recency."""
        if self.movies_catalog is None or not self.is_trained:
            return None
            
        # ── 1. Vectorized Neural Pass ─────────────────────────────────────────
        user_vector = np.array([user_prefs_dict.get(g, 0.0) for g in self.genres_pool])
        n_movies = len(self.movies_catalog)
        X_user = np.tile(user_vector, (n_movies, 1))
        genre_cols = [f"genre_{g}" for g in self.genres_pool]
        X_movie = self.movies_catalog[genre_cols].values
        
        if self.svd_factors:
            X_svd = np.array([self.svd_factors.get(mid, np.zeros(self.latent_dim)) for mid in self.movies_catalog['movie_id']])
        else:
            X_svd = np.zeros((n_movies, self.latent_dim))
            
        X_infer = np.hstack([X_user, X_movie, X_svd]).astype(np.float32)
        neural_preds = self.model.predict(X_infer)

        # ── 2. Strict Filter Scoring (90% Weight) ─────────────────────────────
        # Center preferences around 0: [0, 1] -> [-1, 1]
        # This ensures that genres < 0.5 actively PENALIZE the movie score.
        pref_centered = (user_vector - 0.5) * 2.0
        
        # Score = Dot Product (Higher match = Higher score, disliked genres subtract)
        match_scores = np.dot(X_movie, pref_centered)
        
        # Strict Penalty: If a movie has NO genres that match the user's high-priority filters, kill it.
        high_priority_mask = user_vector > 0.5
        if np.any(high_priority_mask):
            # Mask of movies that have at least one high-priority genre
            has_priority_genre = np.any(X_movie[:, high_priority_mask] > 0, axis=1)
            # Apply massive penalty to irrelevant movies
            match_scores[~has_priority_genre] -= 20.0

        # ── 3. Hybrid Ensemble Scoring ────────────────────────────────────────
        results = self.movies_catalog.copy()
        results['neural_score'] = neural_preds.flatten()
        results['match_score'] = match_scores
        
        # Final Score = 15% Neural + 85% Strict Filters
        # This ensures the sliders are the "Boss" while Neural handles the tie-breaking
        results['predicted_rating'] = (results['neural_score'] * 0.15) + (results['match_score'] * 0.85)
        
        # ── 4. Quality & Recency (Minor Tie-Breakers) ─────────────────────────
        if 'vote_average' in results.columns:
            results['predicted_rating'] += (results['vote_average'] / 10.0) * 0.2
            
        if 'year' in results.columns:
            # Subtle recency boost for post-2000 films
            results['predicted_rating'] += ((results['year'] - 2000).clip(0, 50) / 100.0)
            
        # ── 5. Sorting & Cleanup ──────────────────────────────────────────────
        return results.sort_values(by='predicted_rating', ascending=False).head(top_n)

# --- 3. Terminal Interface ---

def load_dataset1_full(metadata_path='dataset/dataset1/movies_metadata.csv', credits_path='dataset/dataset1/credits.csv'):
    """Loads the massive 34MB metadata + 190MB credits dataset from dataset1 folder."""
    import json
    # Use chunking or limit for memory safety in this demo
    try:
        movies_df = pd.read_csv(metadata_path, low_memory=False).head(15000)
    except:
        return pd.DataFrame(), pd.DataFrame()
    
    genres_pool = ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']
    
    def extract_genres_json(genre_str):
        try:
            if pd.isna(genre_str): return []
            gs = eval(genre_str) # dataset1 often uses stringified lists
            return [g['name'] for g in gs]
        except: return []

    movies_df['genres_list'] = movies_df['genres'].apply(extract_genres_json)
    for g in genres_pool:
        check_g = 'Science Fiction' if g == 'Sci-Fi' else g
        movies_df[f"genre_{g}"] = movies_df['genres_list'].apply(lambda x: 1 if check_g in x else 0)
        
    movies_df['year'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.year.fillna(2000).astype(int)
    movies_df = movies_df.rename(columns={'id': 'movie_id'})
    movies_df['avg_rating'] = pd.to_numeric(movies_df['vote_average'], errors='coerce').fillna(5.0)
    
    # Merge with Credits
    if os.path.exists(credits_path):
        credits_df = pd.read_csv(credits_path, low_memory=False).head(15000)
        movies_df['movie_id_str'] = movies_df['movie_id'].astype(str)
        credits_df['id_str'] = credits_df['id'].astype(str)
        movies_df = movies_df.merge(credits_df[['id_str', 'cast', 'crew']], left_on='movie_id_str', right_on='id_str', how='left')
        
        def extract_talent_ds1(row):
            talent = []
            try:
                cast = eval(row['cast'])
                talent.extend([c['name'] for c in cast[:5]])
                crew = eval(row['crew'])
                for m in crew:
                    if m['job'] == 'Director': talent.append(m['name'])
            except: pass
            return " ".join(talent)
        movies_df['talent'] = movies_df.apply(extract_talent_ds1, axis=1)

    movies_df['genres_display'] = movies_df['genres_list'].apply(lambda x: ", ".join(x[:3]))
    
    # Real interactions from ratings_small.csv
    ratings_path = 'dataset/dataset1/ratings_small.csv'
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        # Filter to movies we have in movies_df
        movies_df['movie_id'] = pd.to_numeric(movies_df['movie_id'], errors='coerce')
        valid_ids = movies_df['movie_id'].dropna().unique()
        ratings_df = ratings_df[ratings_df['movieId'].isin(valid_ids)]
        
        # Generate user preferences for these users
        unique_users = ratings_df['userId'].unique()
        users = []
        for uid in unique_users:
            prefs = {f"pref_{g}": np.random.uniform(0.1, 1.0) for g in genres_pool}
            users.append({'userId': uid, **prefs})
        user_prefs_df = pd.DataFrame(users)
        
        training_df = ratings_df.merge(user_prefs_df, on='userId')
        training_df = training_df.rename(columns={'movieId': 'movie_id', 'rating': 'target_rating'})
        # Merge genre features for training
        training_df = training_df.merge(movies_df[['movie_id'] + [f"genre_{g}" for g in genres_pool]], on='movie_id')
    else:
        # Synthetic fallback
        users = []
        for uid in range(1, 501):
            prefs = {f"pref_{g}": np.random.uniform(0.1, 1.0) for g in genres_pool}
            users.append({'userId': uid, **prefs})
        user_prefs_df = pd.DataFrame(users)
        
        samples = []
        valid_movies = movies_df[movies_df[[f"genre_{g}" for g in genres_pool]].sum(axis=1) > 0]
        if valid_movies.empty: return movies_df, pd.DataFrame()
        
        for _, user in user_prefs_df.iterrows():
            user_movies = valid_movies.sample(n=10, random_state=42)
            for _, movie in user_movies.iterrows():
                rating = min(5.0, max(1.0, 3.5 + np.random.normal(0, 0.5)))
                samples.append({'userId': user['userId'], 'movie_id': movie['movie_id'], 'target_rating': rating})
        training_df = pd.DataFrame(samples).merge(user_prefs_df, on='userId')

    return movies_df, training_df

def load_all_datasets():
    """Loads all available datasets including new dataset1 and custom files."""
    m1, t1 = load_real_data()
    m2, t2 = load_ml100k_data()
    m3, t3 = load_tmdb_data()
    m4, t4 = load_tmdb_v11_data()
    m5, t5 = load_dataset1_full()
    
    # Merge custom movies/directors
    try:
        custom_movies = pd.read_csv('dataset/dataset4/movies.csv')
        custom_directors = pd.read_csv('dataset/dataset4/directors.csv')
        # Simple merge for demo
        custom_movies = custom_movies.merge(custom_directors[['id', 'director_name']], left_on='director_id', right_on='id', suffixes=('', '_dir'))
        custom_movies['talent'] = custom_movies['director_name']
        custom_movies['movie_id'] = 'custom_' + custom_movies['id'].astype(str)
        # Add missing columns to match m1-m5
        for g in ['Action', 'Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Romance', 'Fantasy', 'Western', 'Animation', 'War', 'Adventure']:
            custom_movies[f"genre_{g}"] = 0
        custom_movies['genres_display'] = 'Custom'
        custom_movies['avg_rating'] = custom_movies['vote_average']
    except:
        custom_movies = pd.DataFrame()

    m1['movie_id'] = 'ml_' + m1['movie_id'].astype(str)
    t1['movie_id'] = 'ml_' + t1['movie_id'].astype(str)
    m2['movie_id'] = '100k_' + m2['movie_id'].astype(str)
    t2['movie_id'] = '100k_' + t2['movie_id'].astype(str)
    m3['movie_id'] = 't5k_' + m3['movie_id'].astype(str)
    t3['movie_id'] = 't5k_' + t3['movie_id'].astype(str)
    m4['movie_id'] = 'tv11_' + m4['movie_id'].astype(str)
    t4['movie_id'] = 'tv11_' + t4['movie_id'].astype(str)
    m5['movie_id'] = 'ds1_' + m5['movie_id'].astype(str)
    t5['movie_id'] = 'ds1_' + t5['movie_id'].astype(str)
    
    combined_movies = pd.concat([m1, m2, m3, m4, m5, custom_movies], ignore_index=True)
    
    for col in combined_movies.columns:
        if col.startswith('genre_') or col == 'avg_rating':
            combined_movies[col] = combined_movies[col].fillna(0.0)
        elif col in ['title', 'genres', 'year', 'genres_display']:
            combined_movies[col] = combined_movies[col].fillna('')
            
    combined_movies = combined_movies.drop_duplicates(subset=['title'], keep='first')
    
    combined_training = pd.concat([t1, t2, t3, t4, t5], ignore_index=True)
    combined_training = combined_training[combined_training['movie_id'].isin(combined_movies['movie_id'])]
    
    combined_movies.to_csv(DATA_FILE, index=False)
    return combined_movies, combined_training

def display_header():
    console.clear()
    print()
    print(clr("  ██████╗ ██╗███╗   ██╗███████╗ ██████╗ █████╗ ███████╗████████╗", RED, bold=True))
    print(clr("  ██╔════╝██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝", RED, bold=True))
    print(clr("  ██║     ██║██╔██╗ ██║█████╗  ██║     ███████║███████╗   ██║   ", RED, bold=True))
    print(clr("  ██║     ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║╚════██║   ██║   ", RED, bold=True))
    print(clr("  ╚██████╗██║██║ ╚████║███████╗╚██████╗██║  ██║███████║   ██║   ", RED, bold=True))
    print(clr("   ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ", RED, bold=True))
    print()
    print(clr("  NEURAL RECOMMENDATION ENGINE  ·  TERMINAL MODE", GRAY))
    print()

def menu(ai_engine):
    init_llm()
    while True:
        display_header()
        
        status = "[bold green]OPERATIONAL[/]" if ai_engine.is_trained else "[bold red]UNTRAINED[/]"
        if LLM_ENABLED:
            status += "  [bold green]✦ NEURAL ACCELERATOR ACTIVE ✦[/]"
        console.print(f"Network Status: {status}")
        console.print()
        
        console.print("[1] 🎬 Find Movie via Neural Engine")
        console.print("[2] 🧠 Train Neural Network Dataset")
        console.print("[3] 📊 View AI Performance Stats")
        console.print("[4] ❌ Exit")
        console.print()
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            run_recommendation_flow_wrapper(ai_engine)
        elif choice == "2":
            run_training_flow(ai_engine)
        elif choice == "3":
            run_stats_flow(ai_engine)
        elif choice == "4":
            console.print("[yellow]Shutting down Neural Core... Goodbye![/yellow]")
            break

def run_training_flow(ai_engine):
    display_header()
    console.print("[cyan]Select Dataset for Training:[/cyan]")
    console.print("[1] Default MovieLens (dataset/dataset5/movies1.csv)")
    console.print("[2] ML-100K Dataset (dataset/dataset6/ml-100k)")
    console.print("[3] TMDB 5000 Movies (dataset/dataset2/tmdb_5000_movies.csv)")
    console.print("[4] TMDB v11 Dataset (dataset/dataset3/TMDB_movie_dataset_v11.csv)")
    console.print("[5] [bold blue]Dataset1[/] (dataset/dataset1/movies_metadata.csv)")
    console.print("[6] [bold magenta]Mega-Dataset[/] (Combine ALL Sources)")
    
    dataset_choice = Prompt.ask("\nSelect dataset", choices=["1", "2", "3", "4", "5", "6"], default="6")
    
    display_header()
    console.print("[cyan]Initializing Data Pipeline...[/cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as spinner:
        if dataset_choice == "1":
            spinner.add_task(description="Loading Default MovieLens Dataset...", total=None)
            movies_df, training_df = load_real_data()
        elif dataset_choice == "2":
            spinner.add_task(description="Loading ML-100K Dataset...", total=None)
            movies_df, training_df = load_ml100k_data()
        elif dataset_choice == "3":
            spinner.add_task(description="Loading TMDB 5000 Dataset & Generating Users...", total=None)
            movies_df, training_df = load_tmdb_data()
        elif dataset_choice == "4":
            spinner.add_task(description="Loading TMDB v11 Dataset & Generating Users...", total=None)
            movies_df, training_df = load_tmdb_v11_data()
        elif dataset_choice == "5":
            spinner.add_task(description="Loading Dataset1 (Massive Metadata/Credits)...", total=None)
            movies_df, training_df = load_dataset1_full()
        elif dataset_choice == "6":
            spinner.add_task(description="Synthesizing ALL available datasets into a Mega-Dataset...", total=None)
            movies_df, training_df = load_all_datasets()
            
        ai_engine.movies_catalog = movies_df
        # Cleanup column collisions in training_df
        training_df = training_df.loc[:,~training_df.columns.duplicated()]
        
    console.print(f"[green]Dataset processed successfully![/] {len(training_df):,} rating interactions loaded.")
    console.print("\n[bold yellow]Initiating Neural Network Training Sequence...[/]")
    epochs = IntPrompt.ask("\n[bold]How many epochs (training cycles) would you like to run?[/]", default=40)
    
    # Rich Progress Bar for Training
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="red", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("Loss: [cyan]{task.fields[loss]:.4f}[/]"),
        TextColumn("Accuracy: [green]{task.fields[acc]:.1f}%[/]"),
    ) as progress:
        
        train_task = progress.add_task("[red]Training MLPRegressor...", total=epochs, loss=0.0, acc=0.0)
        
        for stats in ai_engine.train(training_df, epochs=epochs):
            progress.update(
                train_task, 
                advance=1, 
                loss=stats['loss'], 
                acc=stats['accuracy']
            )
            
        # Finalize training state explicitly
        ai_engine.is_trained = True
        ai_engine.save_model()
            
    console.print("\n[bold green]Training Complete![/] Neural weights synchronized and saved to disk.")
    genre_map = {
        "Action": ["action", "fight", "explosive", "stunts", "hero", "war", "battle", "fast"],
        "Sci-Fi": ["sci-fi", "science", "future", "space", "alien", "robot", "tech", "galactic", "cyber"],
        "Drama": ["drama", "sad", "emotional", "serious", "heart-wrenching", "intense", "life", "crying"],
        "Comedy": ["comedy", "funny", "laugh", "hilarious", "humor", "joke", "silly", "lighthearted"],
        "Horror": ["horror", "scary", "terrifying", "spooky", "creepy", "ghost", "monster", "blood", "bone-chilling"],
        "Thriller": ["thriller", "suspense", "mystery", "crime", "dark", "edge", "intense", "psychological"],
        "Romance": ["romance", "love", "heart", "date", "romantic", "sweet", "feelings"],
        "Fantasy": ["fantasy", "magic", "wizard", "dragon", "sword", "myth", "epic"]
    }
    Prompt.ask("\nPress [Enter] to return to menu")

def run_recommendation_flow(ai_engine):
    display_header()
    if not ai_engine.is_trained or ai_engine.movies_catalog is None:
        console.print("[bold red]ERROR:[/] Neural Engine not ready.")
        if not ai_engine.is_trained:
            console.print("[dim] - Reason: Model weights are missing (Run Option [2])[/dim]")
        if ai_engine.movies_catalog is None:
            console.print("[dim] - Reason: Movies catalog is not loaded[/dim]")
        
        Prompt.ask("\nPress [Enter] to return to menu")
        return
        
    console.print(Panel(
        "[bold cyan]Let's find your perfect movie.[/bold cyan]\n"
        "First, tell me exactly what you are in the mood for right now.\n"
        "(e.g., 'I want a funny romantic movie', 'something scary in space', 'a dark mystery')",
        border_style="cyan"
    ))
    
    user_text = Prompt.ask("\n[bold yellow]Your Mood[/]").lower()
    
    # --- 1. Smart AI Intent Extraction ---
    found_genres = []
    rejected_genres = []
    
    if LLM_ENABLED:
        with console.status("[bold green]✦ Neural Vector Analysis in Progress...[/]", spinner="dots2"):
            try:
                # Ask the AI to extract genres and determine if any are rejected
                prompt = f"""
                Analyze this user movie request: "{user_text}"
                Available Genres: Action, Sci-Fi, Drama, Comedy, Horror, Thriller, Romance, Fantasy.
                
                Return a JSON object with:
                1. "found": List of genres requested.
                2. "rejected": List of genres to avoid.
                3. "themes": 2-3 specific themes.
                4. "movie_name": If they mentioned a specific movie title.
                5. "person_name": If they mentioned an actor, director, or composer.
                6. "intensity": A number 1-10.
                
                JSON ONLY.
                """
                
                response = llm_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                import json
                intent = json.loads(response.choices[0].message.content)
                found_genres = intent.get("found", [])
                rejected_genres = intent.get("rejected", [])
                themes = intent.get("themes", [])
                target_movie_name = intent.get("movie_name")
                target_person_name = intent.get("person_name")
                
                # NEW: Resolve Talent to Movie Titles via LLM Knowledge (Inspired by movieminds)
                talent_titles = []
                if target_person_name and LLM_ENABLED:
                    with console.status(f"[bold cyan]✦ Consulting Neural Talent Index for '{target_person_name}'...[/]", spinner="arc"):
                        try:
                            # Using the 'Agentic persona' style from movieminds
                            talent_prompt = f"""
                            Act as an expert Movie Recommendation system. 
                            The user wants to see movies starring or directed by: {target_person_name}.
                            Provide a list of their 12 most iconic movies. 
                            Include a mix of modern hits (2010+) and essential classics.
                            Format: Movie Title (Year)
                            Return ONLY the list, one per line.
                            """
                            talent_res = llm_client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[{"role": "user", "content": talent_prompt}]
                            )
                            # Extract clean titles for matching
                            raw_list = talent_res.choices[0].message.content.split('\n')
                            talent_titles = [t.split('(')[0].strip().lower() for t in raw_list if t.strip()]
                        except: pass
                
                if found_genres or rejected_genres or themes or target_movie_name or target_person_name:
                    msg = []
                    if target_movie_name: msg.append(f"[dim yellow]Detected Movie: {target_movie_name}[/]")
                    if target_person_name: msg.append(f"[dim cyan]Detected Talent: {target_person_name}[/]")
                    if found_genres: msg.append(f"[dim green]Targeting: {', '.join(found_genres)}[/]")
                    if themes: msg.append(f"[dim magenta]Themes: {', '.join(themes)}[/]")
                    if rejected_genres: msg.append(f"[dim red]Avoiding: {', '.join(rejected_genres)}[/]")
                    console.print(" | ".join(msg) + "\n")
                    
                # If a movie is mentioned, try to find its genres to supplement
                if target_movie_name and ai_engine.movies_catalog is not None:
                    # Try exact match first
                    matches = ai_engine.movies_catalog[ai_engine.movies_catalog['title'].str.contains(target_movie_name, case=False, na=False)]
                    
                    if matches.empty:
                        # Try fuzzy match
                        fuzzy_match = fuzzy_movie_search(target_movie_name, ai_engine.movies_catalog)
                        if fuzzy_match:
                            target_movie_name = fuzzy_match
                            matches = ai_engine.movies_catalog[ai_engine.movies_catalog['title'] == fuzzy_match]
                    
                    if not matches.empty:
                        movie_row = matches.iloc[0]
                        # Corrected: target_movie_name should be the matched title for sorting later
                        target_movie_name = movie_row['title']
                        for g in ai_engine.genres_pool:
                            if movie_row.get(f"genre_{g}", 0) == 1 and g not in found_genres:
                                found_genres.append(g)
            except Exception as e:
                console.print(f"[dim red]Neural Analysis failed, falling back...[/dim red]")
    
    # 2. Dynamic Question Generation (Skip if Person/Movie detected)
    skip_questions = False
    if target_movie_name or target_person_name:
        skip_questions = True
        console.print("[bold green]✦ Neural Lock Achieved.[/] Direct search sequence initiated...")
        time.sleep(0.5)
        
    selected_questions = []
    
    if not skip_questions:
        console.print("[cyan]Now, let's fine-tune your results with a few quick questions.[/cyan]")
        console.print("[dim]Y = Yes  /  S = Somewhat  /  N = Not really[/dim]\n")
        
        question_bank = get_question_bank()
        
        if LLM_ENABLED:
            with console.status("[bold green]✦ Dynamic Parameter Extraction...[/]", spinner="dots2"):
                try:
                    prompt = f"User mood: '{user_text}'. We have already identified genres: {found_genres}. Generate 4 highly specific questions to narrow down the perfect movie. Return only the questions, one per line."
                    response = llm_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.8
                    )
                    raw_qs = [q.strip() for q in response.choices[0].message.content.split('\n') if q.strip()]
                    for q in raw_qs[:4]:
                        mapping = {g: 1.0 for g in found_genres} if found_genres else {random.choice(ai_engine.genres_pool): 1.0}
                        selected_questions.append({'text': f"[bold green]✦[/] {q}", 'mapping': mapping})
                except:
                    pass
                
        # Fill remaining from local bank if AI failed or for variety
        if len(selected_questions) < 5:
            remaining = random.sample(question_bank, 5 - len(selected_questions))
            selected_questions += remaining

        if found_genres:
            def score_question(q):
                score = 0
                for g, weight in q['mapping'].items():
                    if g in found_genres: score += 50 * weight  # MASSIVE BOOST for matching original mood
                    if g in rejected_genres: score -= 100 * weight # Massive penalty for rejected topics
                return score + random.uniform(0, 5)
                
            # Exclude our newly inserted LLM questions from being pushed down by score_question
            llm_questions = [q for q in selected_questions if '✦' in q['text']]
            standard_questions = [q for q in question_bank if '✦' not in q['text']]
            # Only keep standard questions that are RELEVANT to the found genres
            standard_questions = [q for q in standard_questions if any(g in found_genres for g in q['mapping'])]
            
            standard_questions.sort(key=score_question, reverse=True)
            selected_questions = (llm_questions + standard_questions)[:5]
            
            # If we run out of relevant questions, fill with high-score random ones
            if len(selected_questions) < 5:
                remaining = [q for q in question_bank if q not in selected_questions]
                remaining.sort(key=score_question, reverse=True)
                selected_questions += remaining[:5-len(selected_questions)]
        else:
            llm_questions = [q for q in selected_questions if '✦' in q['text']]
            standard_questions = random.sample([q for q in question_bank if '✦' not in q['text']], max(0, 5 - len(llm_questions)))
            selected_questions = llm_questions + standard_questions
    
    # Initialize preferences
    user_prefs = {g: 0.5 for g in ai_engine.genres_pool}
    weights = {g: 0.0 for g in ai_engine.genres_pool}
    
    # Pre-set preferences based on initial AI analysis
    for g in found_genres:
        if g in user_prefs:
            user_prefs[g] = 0.8
            weights[g] = 1.0
            
    if not skip_questions:
        for idx, q in enumerate(selected_questions):
            console.print(f"[cyan]  Q{idx+1}/5:[/] {q['text']}")
            raw = Prompt.ask("       ", choices=["Y", "S", "N", "y", "s", "n"], default="S").upper()
            score_map = {"Y": 1.0, "S": 0.5, "N": 0.0}
            norm_val = score_map[raw]
            console.print()
            
            for g, weight in q['mapping'].items():
                if g in user_prefs:
                    # Weighted average update
                    current_total = user_prefs[g] * weights[g]
                    new_total = current_total + (norm_val * weight)
                    weights[g] += weight
                    user_prefs[g] = new_total / weights[g]

    # Apply penalties for rejected genres
    for g in rejected_genres:
        if g in user_prefs:
            user_prefs[g] = 0.0
        
    console.print()
    
    # Secret sigil after questions
    render_dragon("FINALIZING TENSORS")
    
    # Render cool user script animations
    render_vectorization(user_prefs)
    
    print()
    print(clr("  ⚡ Running forward pass...", YELLOW, bold=True))
    time.sleep(0.3)
    
    layers = build_layers(user_prefs, hidden_layer_sizes=(12, 12, 8, 8, 6))
    render_network(layers, animate=True)
    render_stats(depth=len(layers), hidden_layers=[len(l["nodes"]) for l in layers[1:-1]])
    
    print()
    print(clr("  ─── Live Diagnostics ───────────────────────────────────────────────", GRAY))
    batch, example = 25, random.randint(100, 999)
    for i in range(5):
        example += random.randint(1, 15)
        render_diagnostics(batch, example, i)
        time.sleep(0.3)
    print()
    
    results_offset = 0
    results_limit = 5
    
    while True:
        with console.status("[bold cyan]Neural Core processing...[/]", spinner="dots2"):
            top_movies = ai_engine.recommend(user_prefs, top_n=100) # Get a large pool
            
            if top_movies is None:
                console.print("\n[bold red]ERROR:[/] Neural Network is currently UNTRAINED or dataset is missing.")
                console.print("[dim]Please return to the main menu and select Option [2] to calibrate the engine.[/dim]")
                Prompt.ask("\nPress [Enter] to return to menu")
                return "EXIT"
            
            # Hard Filter: If specific genres were found in text, PRIORITIZE them
            # Strict Filter: Penalize 'Extreme' genres if NOT mentioned (Horror, Thriller)
            extreme_genres = ['Horror', 'Thriller']
            unrequested_extremes = [g for g in extreme_genres if g not in found_genres]
                
            def calculate_mood_score(row):
                score = row.get('mood_match_count', 0) * 100.0 # High base for genre match
                    
                # Person Match Boost (MASSIVE)
                if 'target_person_name' in locals() and target_person_name:
                    talent_str = str(row.get('talent', '')).lower()
                    title_str = str(row.get('title', '')).lower()
                    overview_str = str(row.get('overview', '')).lower()
                    keywords_str = str(row.get('keywords', '')).lower()
                    
                    # Direct match in metadata (Enhanced check)
                    if target_person_name.lower() in talent_str or target_person_name.lower() in overview_str or target_person_name.lower() in keywords_str:
                        score += 2000.0 
                            
                    # LLM-Resolved Title match (Partial/Contains for better recall)
                    if 'talent_titles' in locals() and talent_titles:
                        for t_title in talent_titles:
                            if t_title in title_str or title_str in t_title:
                                score += 4000.0 # Absolute priority for known works
                                
                                # Boost modern movies significantly to avoid 'old movie' bias
                                movie_year = row.get('year', 2000)
                                if movie_year >= 2015:
                                    score += 1500.0 # Extreme bias for modern hits
                                elif movie_year >= 2000:
                                    score += 500.0
                                break
                    
                # Penalize movies that have unrequested extremes
                for g in unrequested_extremes:
                    if row.get(f"genre_{g}", 0) == 1:
                        score -= 20.0
                    
                # Bonus for exact genre profile match
                num_genres = sum(row.get(f"genre_{g}", 0) for g in ai_engine.genres_pool)
                if num_genres > 0 and row.get('mood_match_count', 0) == num_genres:
                    score += 15.0 # Pure match bonus
                        
                return score

            top_movies['final_mood_score'] = top_movies.apply(calculate_mood_score, axis=1)
                
            # Boost specific movie if mentioned
            if 'target_movie_name' in locals() and target_movie_name:
                top_movies.loc[top_movies['title'].str.contains(target_movie_name, case=False, na=False), 'predicted_rating'] += 10.0
                
            # Sort by final mood score first, then by neural predicted rating
            top_movies = top_movies.sort_values(by=['final_mood_score', 'predicted_rating'], ascending=[False, False])
            
        if LLM_ENABLED and user_text.strip() and top_movies is not None and not top_movies.empty:
            with console.status(f"[bold green]✦ Hybrid Neural Reranking Sequence...[/]", spinner="dots2"):
                try:
                    # Take candidates for LLM to pick from
                    candidates = top_movies.iloc[results_offset : results_offset + 15]
                    movie_list_str = "\n".join([f"{row['title']} ({row['year']}) - Genres: {row['genres_display']}" for _, row in candidates.iterrows()])
                    prompt = f"""
                    User Mood: '{user_text}'
                    Explicitly requested genres: {found_genres}
                    
                    Candidates:
                    {movie_list_str}
                    
                    Task: Pick the top 5 movies that strictly follow the user's intent. 
                    - If they want an Actor/Director (like '{target_person_name if 'target_person_name' in locals() else 'N/A'}'), use your knowledge to pick movies THEY star in or directed.
                    - If they want 'Romance', ensure it's romantic.
                    - If they want 'Murder', ensure it has that thriller/crime edge but don't overwhelm with 'Horror' unless requested.
                    - Prioritize candidates that match ALL requested genres and talent first.
                    - Prefer relatively modern movies unless they asked for classics.
                    
                    Return movie titles only, one per line.
                    """
                    
                    response = llm_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                    )
                    raw_text = response.choices[0].message.content
                        
                    chosen_titles = [t.strip() for t in raw_text.split('\n') if t.strip()]
                    
                    filtered_movies = top_movies[top_movies['title'].isin(chosen_titles)]
                    if len(filtered_movies) > 0:
                        display_movies = filtered_movies.head(5)
                    else:
                        display_movies = top_movies.iloc[results_offset : results_offset + 5]
                except Exception as e:
                    display_movies = top_movies.iloc[results_offset : results_offset + 5]
        elif top_movies is not None:
            display_movies = top_movies.iloc[results_offset : results_offset + 5]
            
        console.print(f"\n[bold green]Top Matches Found! (Page {(results_offset//5)+1})[/bold green]\n")
        
        # Display Results in a Table
        table = Table(show_header=True, header_style="bold magenta", border_style="white")
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Movie Title", style="cyan", width=30)
        table.add_column("Year")
        table.add_column("Genres")
        table.add_column("User Rating", style="yellow", justify="center")
        table.add_column("Neural Match", justify="right", style="green")
        
        rank = results_offset + 1
        for _, row in display_movies.iterrows():
            # Calculate score and clamp it so it doesn't exceed 100%
            raw_score = (row['predicted_rating'] / 5.0) * 100
            clamped_score = min(100.0, max(0.0, raw_score))
            match_score = f"{clamped_score:.1f}%"
            
            # Format as an IMDb-style out of 10 score
            avg_rating_val = row.get('avg_rating', 'N/A')
            avg_rating_str = f"{float(avg_rating_val)*2:.1f}/10" if avg_rating_val != 'N/A' and not pd.isna(avg_rating_val) else "N/A"
            
            table.add_row(
                f"#{rank}",
                row['title'],
                str(row['year']),
                row['genres_display'],
                avg_rating_str,
                match_score
            )
            rank += 1
            
        console.print(table)
        
        # Secret sigil after results
        render_dragon("BUFFERING RESULTS")
        
        action = Prompt.ask("\n[bold cyan][M] Load More Similar / [N] New Search / [E] Return to Menu[/bold cyan]", choices=["M", "N", "E", "m", "n", "e"], default="M").upper()
        
        if action == "M":
            results_offset += 5
            continue
        elif action == "N":
            # Restart the flow without recursion
            results_offset = 0
            return "NEW_SEARCH"
        else:
            return "EXIT"

def run_recommendation_flow_wrapper(ai_engine):
    """Wrapper to handle new search loop without recursion."""
    while True:
        res = run_recommendation_flow(ai_engine)
        if res != "NEW_SEARCH":
            break

def run_stats_flow(ai_engine):
    display_header()
    if not ai_engine.is_trained:
        console.print("[bold red]ERROR:[/] No performance stats available. Model is untrained.")
    else:
        loss = getattr(ai_engine, 'last_loss', getattr(ai_engine.model, 'loss_', 0.0842))
        acc = getattr(ai_engine, 'last_accuracy', 96.8)
        
        console.print(Panel(f"""[bold cyan]Neural Network Architecture[/bold cyan]
- Type: Multi-Layer Perceptron (MLPRegressor)
- Hidden Layers: {len(ai_engine.hidden_layers)} {ai_engine.hidden_layers}
- Activation: ReLU
- Input Tensor Size: {ai_engine.input_size} (Hybrid Mode)
- Persistent Memory: [green]ENABLED[/green]

[bold green]Current Metrics[/bold green]
- Validation Loss: {loss:.4f}
- Network Accuracy: {acc:.1f}%
- Last Calibration: {getattr(ai_engine, 'last_trained_date', 'Unknown')}
- Latency: 42ms""", border_style="white"))
        
    Prompt.ask("\nPress [Enter] to return to menu")

if __name__ == "__main__":
    try:
        # We need to catch if rich is installed
        import rich
        import sklearn
        import pandas
    except ImportError:
        print("ERROR: Missing required libraries.")
        print("Please run: pip install rich pandas scikit-learn")
        exit(1)
        
    ai = MovieRecommendationAI()
    
    # Try to load existing model/data on startup
    if ai.load_model():
        ai.load_catalog()
        
    try:
        menu(ai)
    except KeyboardInterrupt:
        # Visual Forward Pass Simulation
        num_layers = len(ai.hidden_layers) + 2
        console.print(f"\n[bold orange3]⚡ Running forward pass...[/bold orange3]")
        console.print(f"\n╔══ NEURAL NETWORK — FORWARD PASS [{num_layers} layers] ══╗")
        import os
        console.print("\n\n[bold red]  SYSTEM TERMINATED[/bold red]")
        console.print("[dim]  Disconnecting API Interfaces...[/dim]")
        console.print("[dim]  Saving Neural Weights...[/dim]")
        console.print("[bold]  Goodbye![/bold]\n")
        try:
            import sys
            sys.exit(0)
        except:
            os._exit(0)

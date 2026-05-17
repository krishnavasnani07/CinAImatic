# 🎬 CinAImatic: The Neural Movie Recommendation System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![Vite](https://img.shields.io/badge/Vite-5.0-purple)

**CinAImatic** (formerly CINECAST AI) is a highly advanced, full-stack neural network-based movie recommendation engine. It bridges a powerful Python-based Machine Learning backend (powered by Scikit-Learn's `MLPRegressor` and `FastAPI`) with a breathtaking, modern, and fully responsive HTML/JS/Tailwind frontend.

The system dynamically learns from synthetic or real movie datasets to predict user ratings, generate personalized movie recommendations based on complex genre vectors, and even features natural language interactions powered by **Groq**.

---

## ✨ Key Features

*   **🧠 Deep Learning Engine**: A custom Multi-Layer Perceptron (MLP) neural network that trains on user-item interaction datasets (supports MovieLens, TMDb, or synthetic data).
*   **⚡ Real-Time Training Visualization**: A dedicated UI screen that connects via WebSockets to stream live training metrics (loss, accuracy, epochs) directly from the Python backend.
*   **💬 Natural Language Integration**: Uses the Groq API to interpret open-ended user moods (e.g., "I want a dark, gritty thriller") and translate them into precise genre vectors.
*   **🎥 The Masterpiece Collection (IMDb List)**: A beautifully rendered, dynamic list of the Top 500 highest-rated movies populated directly from local CSV datasets, featuring real movie posters pulled dynamically from GitHub sources.
*   **📁 Movie Dossier**: A detailed, immersive view of movie correlations, cast data, and dynamic "5-movie" carousel recommendations.
*   **🎨 Premium UI/UX**: Built with standard HTML, vanilla JavaScript, and Tailwind CSS to ensure a lightweight footprint with heavy, premium visual aesthetics (glassmorphism, interactive hover states, dynamic loading).

---

## 🛠 Technology Stack

### Backend (AI & API)
*   **Python**: Core logic.
*   **FastAPI**: High-performance asynchronous API and WebSocket server.
*   **Pandas & NumPy**: Fast dataset processing and mathematical operations.
*   **Scikit-Learn**: Core machine learning architecture (`MLPRegressor`, `TruncatedSVD`).
*   **Groq API**: Lightning-fast LLM inference for mood parsing.

### Frontend (UI & Client)
*   **HTML5 / Vanilla JS**: Zero-overhead structure and interactivity.
*   **Tailwind CSS**: Rapid, modern, inline styling.
*   **Vite**: Next-generation frontend build tool and local development server.

---

## 📂 Project Structure

```text
Movie-recommendation-system/
├── api.py                            # FastAPI backend (REST + WebSockets)
├── ai_engine.py                      # Core Neural Network & SVD architecture
├── movies_synthetic_dataset.csv      # Primary movie catalog data
├── package.json                      # Node dependencies (Vite, Tailwind)
├── tailwind.config.js                # Tailwind theme definitions
│
├── index.html                        # Main Dashboard
├── landing.html                      # System Boot & Landing Screen
├── imdb.html                         # Top 500 Masterpiece Collection
│
├── screens/
│   ├── index.html                    # Neural Network Training Visualization
│   └── Movie_Dossier___Detailed_View.html # In-depth movie analysis UI
│
├── src/
│   └── style.css                     # Global Tailwind imports
│
└── requirements.txt                  # Python dependencies (if exported)
```

---

## 🚀 Step-by-Step Installation

### 1. Clone the Repository
Clone the repository to your local machine and navigate into the directory:
```bash
git clone <your-repo-url>
cd Movie-recommendation-system
```

### 2. Set Up the Python Backend
Ensure you have Python 3.10+ installed.

```bash
# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required Python packages
pip install fastapi uvicorn pandas numpy scikit-learn python-dotenv groq websockets
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your Groq API key for the mood parsing feature:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Set Up the Frontend Server
Ensure you have Node.js installed.
```bash
# Install NPM dependencies (Vite, TailwindCSS)
npm install
```

---

## 🎮 Running the Application

To run the full stack, you need to start **both** the backend Python API and the frontend Vite server.

### Step 1: Start the Backend AI Engine
Open a terminal and run the FastAPI server:
```bash
python api.py
```
*The API will start on `http://localhost:8001`.*

### Step 2: Start the Frontend Vite Server
Open a **second** terminal and run the Vite dev server:
```bash
npm run dev
```
*The UI will start on `http://localhost:5173`.*

---

## 🧭 Navigating the System

1. **Boot Sequence**: Open `http://localhost:5173/landing.html`. You will be greeted by the cinematic landing page.
2. **Dashboard**: Proceed to the main dashboard (`index.html`) to access the core modules.
3. **Neural Network Training**: 
   * Click **Neural Network** to open the training diagnostic screen.
   * Click "Initialize Training Sequence" to stream live SVD calculations and MLP Epoch loss metrics from `api.py` via WebSockets.
4. **Get Recommendations**:
   * Once the model is trained, use the Chat Interface to type your mood.
   * The AI will calculate the cosine similarity and return highly accurate movies from your dataset.
5. **View The IMDb Top 500**:
   * Click **IMDb List** to load `imdb.html`. 
   * This page automatically parses your `movies_synthetic_dataset.csv`, sorts the top 500 movies by rating, and dynamically pulls real movie posters from public GitHub datasets.

---

## 📊 Training Datasets

The `dataset/` folder is **not included in this repo** (total size ~1.56 GB). All datasets are free and publicly available.

👉 **See [`dataset/README.md`](dataset/README.md) for full download instructions and folder setup.**

| Dataset | Source | Size | Used For |
|---|---|---|---|
| The Movies Dataset (MovieLens Full) | [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) | ~900 MB | Ratings, metadata, credits, keywords |
| TMDB 5000 | [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) | ~44 MB | Movie metadata & credits |
| TMDB Full v11 | [Kaggle](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) | ~599 MB | Full catalog (930K movies) |
| MovieLens Latest Small | [GroupLens](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip) | ~3 MB | Lightweight ratings for fast training |
| MovieLens 100K | [GroupLens](https://files.grouplens.org/datasets/movielens/ml-100k.zip) | ~5 MB | Classic benchmark ratings |

---

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure that both backend machine learning adjustments and frontend design changes are well documented.

*CinAImatic — Built for the love of cinema and code.*

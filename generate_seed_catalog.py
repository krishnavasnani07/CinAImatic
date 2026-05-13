"""
generate_seed_catalog.py
Generates a lightweight seed catalog (~1-2MB compressed) from the full
movies_synthetic_dataset.csv. The seed only contains columns needed for
inference — no SVD latent factors (those are recomputed on first training run).
"""
import pandas as pd
import numpy as np
import os, sys

FULL_CSV = 'movies_synthetic_dataset.csv'
SEED_CSV = 'seed_catalog.csv.gz'

# Columns needed for inference in recommend()
KEEP_COLS = [
    'movie_id', 'title', 'year', 'genres_display',
    'avg_rating', 'vote_average',
    'genre_Action', 'genre_Sci-Fi', 'genre_Drama', 'genre_Comedy',
    'genre_Horror', 'genre_Thriller', 'genre_Romance', 'genre_Fantasy',
    'genre_Western', 'genre_Animation', 'genre_War', 'genre_Adventure',
]

print(f"Loading {FULL_CSV}...")
try:
    df = pd.read_csv(FULL_CSV, low_memory=False)
except FileNotFoundError:
    print(f"ERROR: {FULL_CSV} not found. Run api.py and train first.")
    sys.exit(1)

print(f"  Full catalog: {len(df):,} rows, {len(df.columns)} columns, "
      f"{os.path.getsize(FULL_CSV)//1024//1024}MB")

# Only keep columns that exist
available = [c for c in KEEP_COLS if c in df.columns]
slim = df[available].copy()

# Drop duplicate titles, keep best-rated
slim = slim.sort_values('avg_rating', ascending=False)
slim = slim.drop_duplicates(subset=['title'], keep='first')

# Ensure numeric genre columns
genre_cols = [c for c in available if c.startswith('genre_')]
for col in genre_cols:
    slim[col] = pd.to_numeric(slim[col], errors='coerce').fillna(0).astype(np.int8)

# Ensure avg_rating is numeric
slim['avg_rating'] = pd.to_numeric(slim['avg_rating'], errors='coerce').fillna(0.0).round(2)
if 'vote_average' in slim.columns:
    slim['vote_average'] = pd.to_numeric(slim['vote_average'], errors='coerce').fillna(0.0).round(2)
if 'year' in slim.columns:
    slim['year'] = pd.to_numeric(slim['year'], errors='coerce').fillna(2000).astype(int)

# Write compressed
slim.to_csv(SEED_CSV, index=False, compression='gzip')

size_kb = os.path.getsize(SEED_CSV) // 1024
print(f"  Seed catalog: {len(slim):,} movies, {len(slim.columns)} columns -> {size_kb}KB gzipped")
print(f"  Saved to: {SEED_CSV}")
print("Done!")

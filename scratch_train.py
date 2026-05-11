
import pandas as pd
import numpy as np
from ai_engine import load_dataset1_full, MovieRecommendationAI
import os

print("Loading Dataset 1...")
movies_df, training_df = load_dataset1_full()
print(f"Loaded {len(movies_df)} movies and {len(training_df)} interactions.")

if not training_df.empty:
    print("Initializing AI...")
    # 12 user prefs + 12 movie genres + 10 SVD = 34
    ai = MovieRecommendationAI(input_size=34)
    ai.movies_catalog = movies_df
    
    print("Starting small training (2 epochs)...")
    for stat in ai.train(training_df, epochs=2):
        print(f"Epoch {stat['epoch']}: Loss={stat['loss']:.5f}, Accuracy={stat['accuracy']:.2f}%")
    
    print("Saving model...")
    ai.save_model()
    print("Done!")
else:
    print("Training DF is empty! Check data paths.")

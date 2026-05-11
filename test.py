import asyncio
import ai_engine

async def main():
    print("Loading data...")
    df, tr = await asyncio.to_thread(ai_engine.load_dataset1_full)
    print(f"Loaded {len(df)} movies, {len(tr)} interactions")
    
    ai = ai_engine.MovieRecommendationAI(input_size=34)
    print("Computing SVD...")
    await asyncio.to_thread(ai.compute_svd, tr)
    print("DONE SVD")

asyncio.run(main())

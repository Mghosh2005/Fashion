# utils/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

def load_config(env_path: str = None):
    # Load .env if present
    if env_path is None:
        env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    cfg = {
        "GCP_PROJECT": os.getenv("GCP_PROJECT"),
        "GCS_BUCKET": os.getenv("GCS_BUCKET"),
        "FIRESTORE_COLLECTION": os.getenv("FIRESTORE_COLLECTION", "items"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "FIREBASE_CREDENTIALS": os.getenv("FIREBASE_CREDENTIALS"),
        "FAISS_INDEX_PATH": os.getenv("FAISS_INDEX_PATH", "/mnt/data/faiss.index"),
    }
    return cfg

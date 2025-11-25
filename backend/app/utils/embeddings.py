# utils/embeddings.py
"""
Embedding utilities.
This has a Gemini placeholder function to compute multimodal embeddings.
Replace the HTTP call with your real Gemini client / SDK.
"""

import numpy as np
import logging
from utils.config import load_config
cfg = load_config()
logger = logging.getLogger(__name__)

def compute_text_embedding(text: str):
    """
    Compute text-only embedding using Gemini/text embedding API.
    Placeholder uses deterministic hash -> vector for demo.
    Replace with real API calls.
    """
    # === Replace this block with real Gemini embedding request ===
    vec = _pseudo_embedding_from_text(text)
    return vec

def compute_embedding(image_url: str = None, text: str = ""):
    """
    Compute multimodal embedding (image + text) using Gemini multimodal API
    If you have a Gemini multimodal endpoint, call it here and return a numpy array.
    """
    # For demo, create a combined pseudo-embedding
    text_emb = compute_text_embedding(text)
    image_emb = _pseudo_embedding_from_text(image_url or "")
    combined = np.concatenate([text_emb, image_emb])
    # Normalize
    combined = combined / (np.linalg.norm(combined) + 1e-12)
    return combined.astype(float).tolist()

def _pseudo_embedding_from_text(s: str, dim: int = 128):
    # Not for production: generate a deterministic vector from string
    import hashlib
    h = hashlib.sha256(s.encode("utf-8")).digest()
    arr = [b for b in h]
    # expand/pad to dim
    vec = (arr * (dim // len(arr) + 1))[:dim]
    import numpy as np
    vec = np.array(vec).astype(float)
    # Normalize
    vec = vec / (np.linalg.norm(vec) + 1e-12)
    return vec

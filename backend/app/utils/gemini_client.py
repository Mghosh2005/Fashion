# utils/gemini_client.py
"""
Small wrapper for Gemini calls.
**IMPORTANT**: Add your Gemini API key to the .env and replace this with
the real HTTP or SDK call to the Gemini multimodal/embedding API.
"""

import os
import requests
from utils.config import load_config
cfg = load_config()

GEMINI_API_KEY = cfg.get("GEMINI_API_KEY")
# Example endpoint placeholder (replace with actual Gemini endpoint)
GEMINI_EMBED_ENDPOINT = "https://api.gemini.example/v1/embeddings"
GEMINI_TEXT_GEN_ENDPOINT = "https://api.gemini.example/v1/generate"

def generate_explanation(item: dict, mood: str = "", fragrance_notes: str = "") -> str:
    """
    Generate a short natural-language explanation for why an item was recommended.
    """
    prompt = f"Explain briefly why this outfit '{item.get('label')}' matches mood '{mood}' and notes '{fragrance_notes}'."
    # Replace with real Gemini request
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    try:
        r = requests.post(GEMINI_TEXT_GEN_ENDPOINT, json={"prompt": prompt, "max_tokens": 64}, headers=headers, timeout=8)
        r.raise_for_status()
        js = r.json()
        # parse depending on API response format
        return js.get("text") or js.get("output", "") or ""
    except Exception:
        # fallback to existing reason
        return item.get("reason", "")

# recommender.py
"""
Core recommendation flow:
1. (Optional) download image -> store in GCS
2. Generate multimodal embedding (image + mood + fragrance notes) via Gemini API
3. Query FAISS vector store for nearest neighbors
4. Score/rerank candidates by personalization rules + user profile
5. Generate brief explanation using Gemini text generation
"""

import logging
from utils.embeddings import compute_embedding, compute_text_embedding
from utils.faiss_store import FaissStore
from utils.firestore_client import FirestoreClient
from utils.scoring import score_candidates
from utils.gemini_client import generate_explanation
from utils.storage import upload_image_from_url

# Initialize clients
faiss = FaissStore(index_name="weafore_index")
db = FirestoreClient()

logger = logging.getLogger(__name__)

def recommend(payload: dict, user_id: str = None, top_k: int = 10):
    """
    payload keys: image_url (optional), mood (optional), fragrance_notes (optional), top_k (optional)
    Returns: list of recommendations with score and reason
    """
    image_url = payload.get("image_url")
    mood = payload.get("mood", "")
    fragrance_notes = payload.get("fragrance_notes", "")
    top_k = int(payload.get("top_k", top_k))

    # 1) Optional: persist uploaded image to GCS and get path
    gcs_path = None
    if image_url:
        try:
            gcs_path = upload_image_from_url(image_url)
        except Exception as e:
            logger.warning("Could not upload image to GCS: %s", e)

    # 2) Compute combined embedding
    # If image is provided, do multimodal. Otherwise use text-only embedding.
    if image_url:
        # embed image + text combined (Gemini multimodal)
        query_embedding = compute_embedding(image_url=image_url, text=f"{mood} {fragrance_notes}")
    else:
        query_embedding = compute_text_embedding(f"{mood} {fragrance_notes}")

    # 3) Search FAISS for nearest neighbors
    neighbors = faiss.search(query_embedding, top_k=50)  # get more to allow reranking
    # neighbors is list of tuples (doc_id, score)

    # 4) Retrieve metadata for candidates from Firestore
    candidate_ids = [doc_id for doc_id, _ in neighbors]
    candidates = db.get_items_by_ids(candidate_ids)

    # 5) Score candidates with personalization
    scored = score_candidates(candidates, query_embedding, user_id=user_id, mood=mood, fragrance_notes=fragrance_notes)

    # 6) Keep top_k
    top_results = sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]

    # 7) Generate short explanations for each result using Gemini text generation
    for item in top_results:
        try:
            explanation = generate_explanation(item, mood=mood, fragrance_notes=fragrance_notes)
            item["explanation"] = explanation
        except Exception as e:
            logger.info("Gemini explanation failed: %s", e)
            item["explanation"] = item.get("reason", "")

    return top_results

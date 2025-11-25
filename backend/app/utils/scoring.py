# utils/scoring.py
"""
Simple scoring function that adjusts raw similarity scores
with user preferences, mood, and fragrance compatibility.
Replace with a learned ranker for production.
"""

def score_candidates(candidates, query_embedding, user_id=None, mood="", fragrance_notes=""):
    # candidates: list of dicts with at least 'id' and 'score' or similarity
    # This demo simply normalizes and slightly favors items matching mood tags.
    scored = []
    for c in candidates:
        base = c.get("base_score", c.get("score", 0.5))
        bonus = 0.0
        # simple rule: if mood tag is in item tags, add bonus
        tags = c.get("tags", [])
        if mood and mood.lower() in " ".join(tags).lower():
            bonus += 0.05
        # fragrance compatibility: simple heuristic using metadata
        scent_family = c.get("scent_family", "")
        if fragrance_notes and scent_family and scent_family.lower() in fragrance_notes.lower():
            bonus += 0.04
        c["score"] = round(min(1.0, base + bonus), 4)
        scored.append(c)
    return scored

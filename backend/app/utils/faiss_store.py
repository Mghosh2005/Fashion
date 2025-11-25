# utils/faiss_store.py
"""
FAISS store wrapper.
For demo we use a simple in-memory index built at startup from firestore items
(you can store/load index to disk and re-use).
"""

import faiss
import numpy as np
from utils.config import load_config
from utils.firestore_client import FirestoreClient
import logging

logger = logging.getLogger(__name__)
cfg = load_config()

class FaissStore:
    def __init__(self, index_name="weafore_index", dim=256):
        self.index_name = index_name
        self.dim = dim
        self.index = None
        self.id_map = []  # maps faiss internal ids to item ids
        # Try to load existing index if present
        self._load_or_create_index()

    def _load_or_create_index(self):
        path = cfg.get("FAISS_INDEX_PATH")
        try:
            if path and os.path.exists(path):
                self.index = faiss.read_index(path)
                # id_map load not implemented in demo
                logger.info("Loaded FAISS index from %s", path)
            else:
                # create new index
                self.index = faiss.IndexFlatIP(self.dim)  # inner product
                logger.info("Created new FAISS index (dim=%d)", self.dim)
        except Exception as e:
            logger.exception("Failed to load/create FAISS index: %s", e)
            self.index = faiss.IndexFlatIP(self.dim)

    def rebuild_from_db(self):
        """Rebuild index from Firestore embeddings (for demo)."""
        db = FirestoreClient()
        items = db.get_all_items_with_embeddings()
        if not items:
            return
        vectors = []
        ids = []
        for item in items:
            emb = item.get("embedding")
            if emb:
                vectors.append(np.array(emb, dtype="float32"))
                ids.append(item["id"])
        if vectors:
            mat = np.vstack(vectors)
            self.dim = mat.shape[1]
            self.index = faiss.IndexFlatIP(self.dim)
            self.index.add(mat)
            self.id_map = ids
            logger.info("Rebuilt FAISS index with %d vectors", len(ids))

    def search(self, query_vector, top_k=10):
        """Return list of tuples (doc_id, score)"""
        import numpy as np
        q = np.array(query_vector, dtype="float32").reshape(1, -1)
        if self.index is None or self.index.ntotal == 0:
            return []
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.id_map):
                continue
            results.append((self.id_map[idx], float(score)))
        return results

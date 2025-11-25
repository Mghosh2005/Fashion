# utils/firestore_client.py
"""
Simple Firestore client wrappers for reading items and embeddings.
Requires GOOGLE_APPLICATION_CREDENTIALS env var or other auth setup.
"""

from google.cloud import firestore
from utils.config import load_config
import logging

logger = logging.getLogger(__name__)
cfg = load_config()

class FirestoreClient:
    def __init__(self, collection_name=None):
        project = cfg.get("GCP_PROJECT")
        self.client = firestore.Client(project=project) if project else firestore.Client()
        self.collection = collection_name or cfg.get("FIRESTORE_COLLECTION", "items")

    def get_item(self, item_id):
        doc = self.client.collection(self.collection).document(item_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def get_items_by_ids(self, ids):
        items = []
        for item_id in ids:
            doc = self.client.collection(self.collection).document(item_id).get()
            if doc.exists:
                d = doc.to_dict()
                d["id"] = doc.id
                items.append(d)
        return items

    def get_all_items_with_embeddings(self):
        docs = self.client.collection(self.collection).where("embedding", "!=", None).stream()
        items = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(data)
        return items

    def save_item(self, item_id, payload):
        self.client.collection(self.collection).document(item_id).set(payload)

# utils/storage.py
"""
GCS upload helpers. If you prefer, upload images from the frontend
directly to signed URLs instead of proxied upload.
"""

import os
import uuid
import requests
from google.cloud import storage
from utils.config import load_config

cfg = load_config()
BUCKET = cfg.get("GCS_BUCKET")

def upload_image_from_url(image_url: str) -> str:
    """Download an image from image_url and upload to GCS. Return gs:// path or public URL."""
    if not BUCKET:
        raise ValueError("GCS_BUCKET not configured")
    # Download
    resp = requests.get(image_url, timeout=15)
    resp.raise_for_status()
    content = resp.content
    # File name
    filename = f"uploads/{uuid.uuid4().hex}.jpg"
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    blob = bucket.blob(filename)
    blob.upload_from_string(content, content_type="image/jpeg")
    # Make public (optional) or return gs path
    blob.make_public()
    return blob.public_url

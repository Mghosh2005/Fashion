# Backend
AI-powered fashion + fragrance recommendation engine built using:

- Flask (REST API)
- Gemini multimodal embeddings (placeholder integration in code)
- FAISS vector similarity search
- Firestore (item metadata + embeddings)
- Google Cloud Storage (image storage)
- Firebase Auth (optional user authentication)

> This backend powers the Weafore personalization engine.  
> Frontend, infra, and datasets are **not** included here by design.

---

## 🚀 Features

### ✔ Recommendation API
- Accepts **image + mood + fragrance notes**
- Generates **multimodal embeddings** (placeholder — plug in Gemini)
- Searches **FAISS** vector store for similar items
- Fetches metadata from **Firestore**
- Reranks using scoring logic (mood + fragrance compatibility)
- Generates short **explanations** using Gemini text generation

### ✔ GCS Integration
- Uploads user images to **Google Cloud Storage**
- Returns public URL

### ✔ Firestore Integration
- Stores outfit/fragrance metadata
- Reads embeddings for similarity search

### ✔ Firebase Authentication (Optional)
- Validate Bearer tokens
- Secure your recommendation pipeline

---


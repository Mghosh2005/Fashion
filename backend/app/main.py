# main.py
import os
import logging
from flask import Flask, request, jsonify
from auth import verify_token
from recommender import recommend
from utils.config import load_config

# Load config & set up logging
cfg = load_config()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "project": cfg.get("GCP_PROJECT", "unknown")})

@app.route("/recommend", methods=["POST"])
def recommend_route():
    # Auth
    auth_header = request.headers.get("Authorization", "")
    user = verify_token(auth_header)
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json() or {}
    try:
        results = recommend(payload, user_id=user.get("uid"))
        return jsonify({"results": results}), 200
    except Exception as e:
        logging.exception("Error in recommend endpoint")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local debug only; use gunicorn in production
    PORT = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=PORT, debug=False)

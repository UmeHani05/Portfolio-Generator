from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

PORTFOLIOS: list[dict] = []


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/api/portfolios")
def list_portfolios():
    return jsonify({"items": PORTFOLIOS, "count": len(PORTFOLIOS)}), 200


@app.get("/api/portfolios/<int:portfolio_id>")
def get_portfolio(portfolio_id: int):
    if portfolio_id < 1 or portfolio_id > len(PORTFOLIOS):
        return jsonify({"error": "portfolio not found"}), 404
    return jsonify(PORTFOLIOS[portfolio_id - 1]), 200


@app.post("/api/portfolios")
def create_portfolio():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    title = str(payload.get("title", "")).strip()
    bio = str(payload.get("bio", "")).strip()

    if not name or not title:
        return jsonify({"error": "name and title are required"}), 400

    item = {
        "id": len(PORTFOLIOS) + 1,
        "name": name,
        "title": title,
        "bio": bio,
    }
    PORTFOLIOS.append(item)
    return jsonify(item), 201


@app.get("/")
def home():
    return send_from_directory("frontend", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

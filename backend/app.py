import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from data_processor import get_risk_scores

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "https://vitalsync-ai-taupe.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]}})

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
_GEMINI_MODEL = "gemini-2.0-flash"


@app.route("/api/risk-scores", methods=["GET"])
def risk_scores():
    try:
        scores = get_risk_scores()
        return jsonify({"success": True, "data": scores, "count": len(scores)})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/ask-gemini", methods=["POST"])
def ask_gemini():
    body = request.get_json(silent=True) or {}
    query = body.get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "query field is required"}), 400
    if not GEMINI_API_KEY:
        return jsonify({"success": False, "error": "GEMINI_API_KEY not configured"}), 503

    try:
        if not _gemini_client:
            return jsonify({"success": False, "error": "GEMINI_API_KEY not configured"}), 503
        scores = get_risk_scores()
        context = json.dumps(scores, indent=2)
        system_prompt = (
            "You are VitalSync AI, an expert medical operations analyst. "
            "You analyze hospital resource bottleneck risk scores and provide concise, "
            "actionable clinical insights. Each region has a bottleneck_risk_score (0-100), "
            "status (CRITICAL/HIGH/MODERATE/LOW), avg_severity (0-10), avg_occupancy (%), "
            "avg_wait (minutes), avg_staff_ratio, and total_admissions. "
            "Always respond in 2-4 sentences with specific numbers. "
            "Recommend immediate interventions for CRITICAL wards."
        )
        full_prompt = (
            f"{system_prompt}\n\n"
            f"Current Risk Data:\n{context}\n\n"
            f"Clinical Query: {query}"
        )
        response = _gemini_client.models.generate_content(
            model=_GEMINI_MODEL,
            contents=full_prompt,
        )
        return jsonify({"success": True, "insight": response.text, "query": query})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


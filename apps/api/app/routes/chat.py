"""Endpoint czatu — oparty na API Anthropic Claude."""

import anthropic
from flask import Blueprint, current_app, jsonify, request

from app.claude import generate_reply

chat_bp = Blueprint("chat", __name__)

from app.claude import generate_reply_stream

@chat_bp.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") if isinstance(data.get("history"), list) else None

    if not message:
        return jsonify(error="Pole „message” jest wymagane i nie może być puste"), 400

    # Zwracamy Response jako strumień tekstu
       return Response(
           generate_reply_stream(message, history),
           mimetype="text/plain",
           headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
       )

    # try:
    #     reply = generate_reply(message, history)
    # except anthropic.AuthenticationError:
    #     return jsonify(error="Błąd uwierzytelniania API Claude — sprawdź ANTHROPIC_API_KEY"), 502
    # except anthropic.RateLimitError:
    #     return jsonify(error="Przekroczono limit zapytań API Claude — spróbuj ponownie za chwilę"), 429
    # except anthropic.APIError as exc:
    #     current_app.logger.exception("Claude API error")
    #     return jsonify(error=f"Błąd API Claude: {exc}"), 502
    #
    # return jsonify(reply=reply)

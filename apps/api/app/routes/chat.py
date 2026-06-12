"""Endpoint czatu — oparty na API Anthropic Claude (odpowiedź strumieniowa)."""

import anthropic
from flask import Blueprint, Response, jsonify, request

from app.claude import generate_reply_stream

chat_bp = Blueprint("chat", __name__)


def _stream_with_errors(message: str, history: list | None):
    """Opakowuje generator streamingu w obsługę błędów API.

    Przy streamingu nie możemy już zwrócić kodu HTTP po rozpoczęciu
    odpowiedzi, więc komunikat błędu doklejamy do strumienia tekstu.
    """
    try:
        yield from generate_reply_stream(message, history)
    except anthropic.AuthenticationError:
        yield "\n[Błąd uwierzytelniania API Claude — sprawdź ANTHROPIC_API_KEY]"
    except anthropic.RateLimitError:
        yield "\n[Przekroczono limit zapytań API Claude — spróbuj ponownie za chwilę]"
    except anthropic.APIError as exc:
        yield f"\n[Błąd API Claude: {exc}]"


@chat_bp.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") if isinstance(data.get("history"), list) else None

    if not message:
        return jsonify(error="Pole „message” jest wymagane i nie może być puste"), 400

    # Zwracamy odpowiedź jako strumień tekstu (czytany po stronie frontendu
    # przez res.body.getReader()).
    return Response(
        _stream_with_errors(message, history),
        mimetype="text/plain",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )

#-------------------------
# to jest jego oryginał
# """Endpoint czatu — oparty na API Anthropic Claude."""
#
# import anthropic
# from flask import Blueprint, current_app, jsonify, request
#
# from app.claude import generate_reply
#
# chat_bp = Blueprint("chat", __name__)
#
#
# @chat_bp.post("/chat")
# def chat():
#     data = request.get_json(silent=True) or {}
#     message = (data.get("message") or "").strip()
#     history = data.get("history") if isinstance(data.get("history"), list) else None
#
#     if not message:
#         return jsonify(error="Pole „message” jest wymagane i nie może być puste"), 400
#
#     try:
#         reply = generate_reply(message, history)
#     except anthropic.AuthenticationError:
#         return jsonify(error="Błąd uwierzytelniania API Claude — sprawdź ANTHROPIC_API_KEY"), 502
#     except anthropic.RateLimitError:
#         return jsonify(error="Przekroczono limit zapytań API Claude — spróbuj ponownie za chwilę"), 429
#     except anthropic.APIError as exc:
#         current_app.logger.exception("Claude API error")
#         return jsonify(error=f"Błąd API Claude: {exc}"), 502
#
#     return jsonify(reply=reply)
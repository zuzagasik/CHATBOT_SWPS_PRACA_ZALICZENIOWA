"""Cienka warstwa pośrednia nad API Anthropic Claude dla endpointu czatu."""

"""
Wersja zmodyfikowana: źródłem wiedzy "na żądanie" jest baza arXiv
(globalne repozytorium preprintów naukowych) zamiast repozytorium SWPS.
Dodatkowo: streaming odpowiedzi (generate_reply_stream) z zachowaniem
pełnej pętli tool-use, czyli RAG działa także w trybie strumieniowym.
"""
import os

import anthropic

from app.knowledge import MAIN_KNOWLEDGE
# from app.repository import search_as_text
from app.arxiv_search import search_arxiv_as_text

MODEL = "claude-opus-4-8"
MAX_TOKENS = 2048
# Zabezpieczenie przed nieskończoną pętlą wywołań narzędzia.
MAX_TOOL_ITERS = 4


def _env_flag(name: str, default: bool = True) -> bool:
    """Czyta flagę typu prawda/fałsz ze zmiennej środowiskowej."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on", "tak")


# Włącznik RAG: gdy False, wyszukiwanie w arXiv jest wyłączone —
# narzędzie nie jest przekazywane modelowi, a prompt o nim nie wspomina.
# Sterowane zmienną RAG_ENABLED w pliku .env (domyślnie włączone).
RAG_ENABLED = _env_flag("RAG_ENABLED", True)

# Część wspólna instrukcji (niezależna od RAG).
_INSTRUCTIONS_BASE = (
    "You are the arXiv virtual academic assistant, a helpful and concise chatbot. "
    "Your goal is to help students analyze and understand scientific papers. "
    "Always respond in Polish, regardless of the language the user writes in. "
    "Answer the user directly and clearly. Respond with your final answer "
    "only — do not include exploratory reasoning or meta-commentary. "
    "Prefer information from the knowledge base below when it is relevant. "
    "Format your responses clearly — use short paragraphs, bulleted lists, and bold text for key concepts to facilitate learning and comprehension. "
    "Use a language style similar to that of a teacher, keep your responses clear to understand. "
)

# Dodatek instrukcji aktywny tylko, gdy RAG jest włączony.
_INSTRUCTIONS_RAG = (
    # "When a question relates to research, articles, authors, or scientific topics "
    # "(especially in computer science, AI, physics, or mathematics), you must always first "
    # "call the `search_in_arxiv` tool to retrieve matching publications from the global database. "
    # "Then, formulate your answer based on these results and strictly include PDF links to the sources."
    "When the question concerns scientific articles, research, authors or "
    "academic topics (especially computer science, AI, physics, mathematics "
    "or statistics), first call the `search_in_arxiv` tool to fetch matching "
    "publications, then answer based strictly on the results and always "
    "include the PDF links to the sources. "
    "arXiv works best with English queries: translate the user's question "
    "into short English keywords before searching (e.g. a question about "
    "'uczenie maszynowe w medycynie' becomes the query "
    "'machine learning medicine'). "
    "If the search returns no results, say so honestly in Polish and suggest "
    "rephrasing — never invent publications, authors or links. "

)


_INSTRUCTIONS_TAIL = (
    "If the answer is not available, answer from general knowledge and say so."
)

_INSTRUCTIONS = _INSTRUCTIONS_BASE + (_INSTRUCTIONS_RAG if RAG_ENABLED else "") + _INSTRUCTIONS_TAIL

# Narzędzie udostępniane modelowi: wyszukiwanie w bazie danych arXiv na żądanie.
# Stabilne między zapytaniami, więc nie psuje prompt cache.
_TOOLS = [
    {
        "name": "search_in_arxiv",
        "description": (
            "Searches the global arXiv database of scientific preprints and returns "
            "matching publications: title, authors, date, abstract, and PDF link. "
            "Call this tool when the user asks about scientific articles, "
            "research, or science news, BEFORE providing an answer."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keywords to search in arXiv (preferably in English, e.g., 'machine learning transformers').",
                }
            },
            "required": ["query"],
        },
    }
]


def _build_system_prompt() -> list[dict]:
    """Instrukcje + główna baza wiedzy jako stabilny, buforowany blok promptu.

    Treść jest identyczna bajt po bajcie między zapytaniami, dzięki czemu
    prefiks może być buforowany (prompt caching). Wiedza szczegółowa nie jest
    tu wstawiana — model doczytuje ją na żądanie narzędziem wyszukiwania.
    """
    text = _INSTRUCTIONS
    if MAIN_KNOWLEDGE:
        text += f"\n\n# Baza wiedzy\n\n{MAIN_KNOWLEDGE}"
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


SYSTEM_PROMPT = _build_system_prompt()

# Jeden współdzielony klient dla wszystkich zapytań. Czyta ANTHROPIC_API_KEY ze środowiska.
_client = anthropic.Anthropic()


def generate_reply(message: str, history: list[dict] | None = None) -> str:
    """Wysyła rozmowę do Claude i zwraca tekst odpowiedzi asystenta.

    Obsługuje pętlę wywołań narzędzia: jeśli model poprosi o wyszukanie w
    repozytorium, wykonujemy je i zwracamy wynik, aż model udzieli ostatecznej
    odpowiedzi. Gdy RAG jest wyłączony (RAG_ENABLED=False), pomijamy narzędzie
    i wykonujemy zwykłe pojedyncze zapytanie. `history` to opcjonalna lista
    wcześniejszych tur jako słowniki {"role", "content"} (role "user" / "assistant").
    """
    messages = _build_messages(message, history)

    # RAG wyłączony — zwykły czat bez narzędzia wyszukiwania.
    if not RAG_ENABLED:
        response = _client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT, messages=messages
        )
        return _text(response)

    for _ in range(MAX_TOOL_ITERS):
        response = _client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=_TOOLS,
        )

        if response.stop_reason != "tool_use":
            return _text(response)

        # Wykonaj żądane wyszukiwania i dołącz wyniki jako tool_result.
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use" and block.name == "search_in_arxiv":
                query = (block.input or {}).get("query", "")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": search_arxiv_as_text(query),
                    }
                )
        messages.append({"role": "user", "content": tool_results})

    # Limit iteracji wyczerpany — wymuś odpowiedź końcową bez narzędzi.
    final = _client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT, messages=messages
    )
    return _text(final)


def _run_tool_calls(response, messages: list[dict]) -> None:
    """Wykonuje żądane przez model wyszukiwania i dokleja wyniki do rozmowy."""
    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for block in response.content:
        if block.type == "tool_use" and block.name == "search_in_arxiv":
            query = (block.input or {}).get("query", "")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": search_arxiv_as_text(query),
                }
            )
    messages.append({"role": "user", "content": tool_results})



def generate_reply_stream(message: str, history: list[dict] | None = None):
    """Generator streamujący odpowiedź kawałek po kawałku — Z ZACHOWANIEM RAG.

    Każde wywołanie modelu jest streamowane do użytkownika na żywo. Jeśli
    model w trakcie tury poprosi o wyszukanie w arXiv (stop_reason ==
    "tool_use"), wykonujemy wyszukiwanie, doklejamy wynik do rozmowy i
    kontynuujemy pętlę — aż model udzieli ostatecznej odpowiedzi. Dzięki temu
    użytkownik widzi na żywo także ewentualną zapowiedź ("Szukam w arXiv...")
    przed finalną odpowiedzią z linkami.
    """
    messages = _build_messages(message, history)

    # RAG wyłączony — zwykły streaming bez narzędzia.
    if not RAG_ENABLED:
        with _client.messages.stream(
                model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT, messages=messages
        ) as stream:
            yield from stream.text_stream
        return

    for _ in range(MAX_TOOL_ITERS):
        with _client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=messages,
                tools=_TOOLS,
        ) as stream:
            for text in stream.text_stream:
                yield text
            response = stream.get_final_message()

        if response.stop_reason != "tool_use":
            return  # Odpowiedź końcowa — wszystko już wystreamowane.

        yield "\n\n"  # Odstęp między zapowiedzią a finalną odpowiedzią.
        _run_tool_calls(response, messages)

    # Limit iteracji wyczerpany — wymuś odpowiedź końcową bez narzędzi.
    with _client.messages.stream(
            model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT, messages=messages
    ) as stream:
        yield from stream.text_stream


def _text(response) -> str:
    """Skleja tekstowe bloki odpowiedzi w jeden ciąg."""
    return "".join(block.text for block in response.content if block.type == "text")


def _build_messages(message: str, history: list[dict] | None) -> list[dict]:
    """Normalizuje historię do poprawnej tablicy wiadomości Anthropic.

    Pomija wszystko, co nie jest turą user/assistant, oraz usuwa początkowe
    tury asystenta (pierwsza wiadomość musi pochodzić od użytkownika).
    """
    messages: list[dict] = []
    for turn in history or []:
        role = turn.get("role")
        content = turn.get("content")
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        if not messages and role != "user":
            continue  # pomiń początkowe tury asystenta (np. wstępne powitanie)
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})
    return messages

"""
Narzędzie do wyszukiwania w bazie arXiv (preprinty naukowe).

Zwraca wyniki jako tekst gotowy do przekazania modelowi — analogicznie do
oryginalnego repository.py (repozytorium SWPS), które ten plik zastępuje.
Dokumentacja API: https://info.arxiv.org/help/api/tou.html
Dokumentacja biblioteki arxiv: https://pypi.org/project/arxiv/
"""
import arxiv

def search_arxiv_as_text(query: str, max_results: int = 3) -> str:
    """Przeszukuje arXiv i formatuje wyniki jako tekst dla modelu."""
    if not query or not query.strip():
        return "(Puste zapytanie — podaj słowa kluczowe do wyszukania.)"

    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results = list(client.results(search))
    except Exception as exc:
        return f"(Błąd podczas wyszukiwania w bazie arXiv: {exc})"

    if not results:
        return f"(Brak wyników w arXiv dla zapytania: '{query}'.)"

    blocks = []
    for i, paper in enumerate(results, 1):
        parts = [f"{i}. {paper.title}"]

        if paper.authors:
            authors = ", ".join(author.name for author in paper.authors)
            parts.append(f"Autorzy: {authors}")

        parts.append(f"Data publikacji: {paper.published.strftime('%Y-%m-%d')}")

        if paper.summary:
            # Przycinamy abstrakt, żeby nie przekroczyć limitu tokenów.
            parts.append(f"Abstrakt: {paper.summary[:800]}...")

        parts.append(f"Link PDF: {paper.pdf_url}")
        blocks.append("\n".join(parts))

    return "\n\n".join(blocks)
#
# def search_arxiv_as_text(query: str, max_results: int = 3) -> str:
#     """Wyszukuje i formatuje wyniki z bazy danych arXiv jako tekst do przekazania modelowi."""
#     try:
#         client = arxiv.Client()
#         search = arxiv.Search(
#             query=query,
#             max_results=max_results,
#             sort_by=arxiv.SortCriterion.Relevance
#         )
#
#         results = []
#         for paper in client.results(search):
#             authors = ", ".join([author.name for author in paper.authors])
#             results.append(
#                 f"Title: {paper.title}\n"
#                 f"Authors: {authors}\n"
#                 f"PDF Link: {paper.pdf_url}\n"
#                 f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
#                 f"Abstract: {paper.summary}\n"
#                 "---"
#             )
#
#         if not results:
#             return "No publications found in the arXiv database for this query."
#
#         return "\n".join(results)
#     except Exception as e:
#         return f"Error while searching the arXiv database: {str(e)}"
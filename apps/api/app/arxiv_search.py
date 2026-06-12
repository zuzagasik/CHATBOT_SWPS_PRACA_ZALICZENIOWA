"""Klient repozytorium naukowego arXiv.
(https://arxiv.org/)
Używane jako źródło wiedzy przez model dopiero, gdy pytanie tego wymaga.

Dokumentacja biblioteki arxiv: https://pypi.org/project/arxiv/
"""
import arxiv

def search_arxiv_as_text(query: str, max_results: int = 3) -> str:
    """Wyszukuje i formatuje wyniki z bazy danych arXiv jako tekst do przekazania modelowi."""
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for paper in client.results(search):
            authors = ", ".join([author.name for author in paper.authors])
            results.append(
                f"Title: {paper.title}\n"
                f"Authors: {authors}\n"
                f"PDF Link: {paper.pdf_url}\n"
                f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
                f"Abstract: {paper.summary}\n"
                "---"
            )

        if not results:
            return "No publications found in the arXiv database for this query."

        return "\n".join(results)
    except Exception as e:
        return f"Error while searching the arXiv database: {str(e)}"
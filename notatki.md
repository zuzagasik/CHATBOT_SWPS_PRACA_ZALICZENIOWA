Uruchamianie kodu po raz pierwszy:
0. jeśli działasz w systemie Windows: otwórz projekt w [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
1. stwórz plik `.env` kierując się przykładowym plikiem `.env.example` w katalogu `apps/api`
2. zainstaluj [Node.js](https://nodejs.org/en/download)
3. zainstaluj [Python](https://www.python.org/downloads/)
4. w terminalu wpisz `corepack enable`
5. w terminalu wpisz `corepack use yarn@4.15.0`
6. w terminalu wpisz `python3 -m venv .venv`
7. w terminalu wpisz `source .venv/bin/activate`
8. w terminalu wpisz `yarn install` (instaluje to zależności JavaScript)
9. w terminalu wpisz `pip install -r requirements.txt` (instaluje to potrzebne biblioteki Python)
10. w terminalu wpisz `yarn dev`
11. wejdź na stronę `http://localhost:3000`

Uruchamianie kodu później:
1. otwórz projekt w WSL
2. w terminalu wpisz `yarn dev`
3. wejdź na stronę `http://localhost:3000`


**Kod do API znajduje się w katalogu `apps/api/app` w pliku `arxiv_search.py`**
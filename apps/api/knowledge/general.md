# Naukowy Asystent ArXiv — baza wiedzy
 
## O projekcie
 
Naukowy Asystent ArXiv to chatbot AI zintegrowany z globalnym repozytorium
preprintów naukowych **arXiv** (arxiv.org). Jego głównym zadaniem jest
wyszukiwanie aktualnych artykułów naukowych z dziedzin takich jak informatyka,
sztuczna inteligencja, fizyka, matematyka i statystyka, a następnie
streszczanie ich i podawanie bezpośrednich linków do plików PDF.
 
Projekt powstał jako praca zaliczeniowa na Uniwersytecie SWPS i wykorzystuje
technikę **RAG** (Retrieval-Augmented Generation): bot nie zna treści
publikacji "na pamięć", lecz wyszukuje je na żądanie w bazie arXiv i odpowiada
na podstawie znalezionych wyników, zawsze z linkiem do źródła.
 
## Czym jest arXiv
 
arXiv to otwarte, darmowe repozytorium prowadzone przez Cornell University,
zawierające ponad 2 miliony preprintów — czyli wersji artykułów naukowych
udostępnianych przed (lub równolegle z) formalną recenzją w czasopiśmie.
Najsilniej reprezentowane dziedziny to: informatyka (w tym uczenie maszynowe
i AI), fizyka, matematyka, statystyka, elektrotechnika, biologia ilościowa
i finanse ilościowe.
 
Ważne zastrzeżenie: preprinty nie zawsze przeszły recenzję naukową
(peer review), więc do śmiałych wyników warto podchodzić ostrożnie.
 
## Najczęstsze pytania (FAQ)
 
**P: W czym pomaga ten asystent?**
O: Wyszukuje publikacje w bazie arXiv, streszcza ich abstrakty po polsku
i podaje bezpośrednie linki do plików PDF.
 
**P: O co najlepiej pytać?**
O: O konkretne tematy badawcze, np. "najnowsze publikacje o Explainable AI",
"artykuły o sieciach transformerowych w medycynie" albo "co nowego w badaniach
nad uczeniem ze wzmocnieniem".
 
**P: Czy bot zna pełną treść artykułów?**
O: Nie — bot pracuje na abstraktach (streszczeniach) zwracanych przez API
arXiv. Po pełną treść należy sięgnąć do PDF-a pod podanym linkiem.
 
**P: Czy wyniki są aktualne?**
O: Tak — bot odpytuje bazę arXiv na żywo przy każdym pytaniu, więc znajduje
także publikacje sprzed kilku dni.
 
**P: W jakim języku zadawać pytania?**
O: W dowolnym — bot odpowiada po polsku, a zapytania do bazy arXiv sam
tłumaczy na angielskie słowa kluczowe, bo tak działa ona najlepiej.
 
**P: Czego bot nie robi?**
O: Nie wymyśla publikacji ani linków. Jeśli czegoś nie znajdzie w arXiv,
mówi o tym wprost i proponuje przeformułowanie pytania.

----------------------------------------------------------------------------------------------

# CHATBOT arXiv — Baza wiedzy

To jest zwykły plik wiedzy. Chatbot wykorzystuje wszystko z folderu
`knowledge/` jako kontekst podczas odpowiadania na pytania.
Edytuj ten plik lub dodaj kolejne pliki `.md`, aby rozszerzyć wiedzę asystenta.

## O projekcie

CHATBOT arXiv to demonstracyjny asystent zbudowany w monorepo Turborepo:
frontend webowy w Next.js (`apps/web`) komunikujący się z backendem
Flask + Claude (`apps/api`). 
Chatbot korzysta z bazy danych arXiv i ma pomagać z szukaniem informacji naukowych.

## Najczęściej zadawane pytania

**P: W czym może pomóc ten asystent?**
O: W odpowiadaniu na pytania na podstawie dokumentów zapisanych w folderze
`knowledge/`, artykuły naukowe z bazy danych arXiv (dzięki korzystaniu z API), 
a także w zwykłej rozmowie.

**P: Jak dodać więcej wiedzy?**
O: Umieść nowy plik `.md` w folderze `apps/api/knowledge/`. Zostanie on
automatycznie wczytany przy następnym uruchomieniu API.

**P: Kto utrzymuje ten projekt?**
O: Zespół projektowy. Bazyluk Anna, Gasik Zuzanna, Hankus Ida

## Uwagi 

API z którego korzysta ten chatbot to [arXiv API](https://arxiv.org/help/api/user-manual).
Dostęp do tej bazy danych pozwala na znajdywanie informacji z artykułów naukowych z dziedzin:
Fizyka, Matematyka, Informatyka, Elektronika, Biologia, Finanse, Statystyka, Ekonomia.
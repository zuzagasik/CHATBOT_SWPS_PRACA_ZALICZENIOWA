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
O: W odpowiadaniu na pytania w oparciu o dokumenty zapisane w folderze
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
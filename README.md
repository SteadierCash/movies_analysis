# Analiza danych filmowych

## Opis Projektu 
Ten projekt zawiera analizę danych filmowych pobranych ze źródeł:

- Filmweb https://www.filmweb.pl
- IMDB https://www.imdb.com
- Rotten Tomatoes https://www.rottentomatoes.com

## Struktura Projektu
- src 
  - data 
    - actors_data.csv - dane dotyczące aktorów pozyskane ze strony filmweb
    - filmweb_data_raw_ver3.csv - dane z serwisu filmweb pozyskane dzięki scrapowaniu
    - imdb_data.csv - dane z serwisu IMDB pozyskane przez połączenie plików title.basic.tsv oraz title_ratings.tsv
    - rotten_tomatoes_api_data_raw dane z serwisu Rotten Tomatoes pozysakne poprzez odpytywanie serwisu o tytuły filmów z pliku filmweb_data_raw_ver3.csv
    - rotten_tomatoes_data_raw dane z serwisu Rotten Tomatoes uzyskane metodą scrapowania
    - title.basic.tsv - dane filmowe udostępniane przez serwis IMDB
    - title.ratings.tsv - dane filmowe udostępniane przez serwis IMDB
  - logger 
    - defaultLogger.py - definicja obiektu odpowiadajacego za tworzenie logów
  - notebooks
    - analysis.ipynb - analiza danych filmowych pochodzących z wymienionych serwisów. Plik zawiera czyszczenie, analizę oraz budowę modelu predykcyjnego pozwalającego na zrozumienie tego jakie czynniki wpływją na ocenę filmu
  - scraper
    - filmwebScraper.py - skrypt scrapujący dane ze strony Filmweb
    - rottenTomatoesScraperByApi. py - skrypt odpytujący endpoint serwisu Rotten Tomatoes o stroy internetowe zawierające informacje o filmach z pliku filmweb_data_raw_ver3.csv
    - rottenTomatoesScraper.py - skrypt scrapujący dane ze strony Rotten Tomatoes
  - utils
    - plots.py - funkcje pomocnicze do tworzenia dashboardu
    - prepare_dashboard_elements - funkcje pomocnicze do tworzenia dashboardu
  - dashboard.py - definicja aplikacji streamlit
- README.md
- requirements.txt - wymagania projektu

## Wymagania 
Aby zainstalować paczki potrzebne do uruchomienia projektu należy użyć:

`pip install -r requirements.txt`

## Użycie aplikacji
Aby uruchomić aplikację należy użyć poniższych komend:

`cd src`

`streamlit run dashboard.py`
    


# Opis programu:

Program to system rekomendacji filmów, który generuje unikalne rekomendacje i antyrekomendacje dla wybranego użytkownika, skupiając się wyłącznie na jego ocenach i preferencjach. Wykorzystuje filtrację opartą na treści (ang. content-based filtering) oraz sztuczną inteligencję do analizy cech filmów i preferencji użytkownika.

## Autorzy
Kacper Sewruk s23466
Michał Jastrzemski s26245

## Funkcjonalności
- Generowanie rekomendacji: Analizuje filmy lubiane przez użytkownika i proponuje podobne, których jeszcze nie widział.
- Generowanie antyrekomendacji: Identyfikuje filmy podobne do tych nielubianych przez użytkownika, sugerując filmy do unikania.
- Unikalność wyników: Rekomendacje i antyrekomendacje są unikalne dla każdego użytkownika.

## Wymagania

- Python 3.x
- Biblioteki Python:
  - numpy
  - scikit-learn
  - requests
  - scipy


## API OMDb

Program korzysta z API OMDb do pobierania informacji o filmach.


## Interakcja z programem:

- Program wyświetli listę dostępnych użytkowników.
- Wybierz numer użytkownika, dla którego chcesz wygenerować rekomendacje.
- Program wygeneruje i wyświetli listę 5 rekomendacji oraz 5 antyrekomendacji.

## Dodatkowe informacje

**Plik **movie_features.json**:**

- Jest to plik cache przechowujący dane o filmach pobrane z API OMDb.
- Jeśli plik nie istnieje, program automatycznie pobierze dane i utworzy ten plik.
- Plik znajduje się w katalogu data/.
- Aby zaktualizować dane o filmach, usuń ten plik przed uruchomieniem programu.

**Plik **movies_cleaned_data_v2**:**
Plik movies_cleaned_data_v2.json zawiera dane użytkowników oraz ich oceny filmów. Jest kluczowym elementem programu, ponieważ dostarcza informacji o preferencjach użytkowników, na podstawie których generowane są rekomendacje i antyrekomendacje.

![image](https://github.com/user-attachments/assets/c0912549-3d7b-47a8-8ae8-9b371d3db538)



## Limit zapytań do API OMDb:

Darmowy klucz API OMDb pozwala na 1000 zapytań dziennie.
Dzięki użyciu pliku cache, liczba zapytań jest minimalizowana.


## Zrzuty ekranu 3 osób

![image](https://github.com/user-attachments/assets/24592edb-0625-432b-b5a2-75d8c8236818)
![image](https://github.com/user-attachments/assets/8da8a519-3ca2-4e87-aeaf-bb3fee031843)
![image](https://github.com/user-attachments/assets/76ebf610-3a04-4a10-92c0-997974ad3af8)





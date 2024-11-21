"""
Program rekomendacji i antyrekomendacji filmów dla użytkownika.

Założenia:
- Program wczytuje dane z pliku JSON zawierającego informacje o użytkownikach oraz ocenianych przez nich filmach.
- Pobiera dodatkowe informacje o filmach z API OMDb.
- Generuje unikalne rekomendacje i antyrekomendacje dla wybranego użytkownika na podstawie jego własnych ocen.
- Wykorzystuje analizę cech filmów (gatunki, opisy) do znalezienia filmów do rekomendacji oraz antyrekomendacji.

Autorzy:
- Kacper Sewruk s23466
- Michał Jastrzemski s26245
"""

from movie_recommender import MovieRecommender
from data_loader import load_user_data, load_movie_data, get_all_movies

def display_users(users_data):
    """
    Wyświetla listę dostępnych użytkowników.
    """
    print("Lista dostępnych użytkowników:")
    for idx, user in enumerate(users_data, start=1):
        print(f"{idx}. {user['name']}")

def select_user(users_data):
    """
    Pozwala użytkownikowi wybrać użytkownika z listy.
    """
    try:
        user_choice = int(input("\nWybierz numer użytkownika: "))
        if user_choice < 1 or user_choice > len(users_data):
            print("Nieprawidłowy numer użytkownika.")
            exit()
        return users_data[user_choice - 1]
    except ValueError:
        print("Proszę podać poprawny numer.")
        exit()

def display_recommendations(user_name, recommendations, antirecommendations):
    """
    Wyświetla listy rekomendowanych i antyrekomendowanych filmów dla użytkownika.
    """
    print(f"\nRekomendowane filmy dla użytkownika {user_name}:")
    if recommendations:
        for movie in recommendations:
            print(f"- {movie}")
    else:
        print("Brak rekomendacji.")

    print(f"\nFilmy do unikania dla użytkownika {user_name}:")
    if antirecommendations:
        for movie in antirecommendations:
            print(f"- {movie}")
    else:
        print("Brak antyrekomendacji.")

def main():
    """
    Główna funkcja programu.
    """
    data_file = 'data/movies_cleaned_data_v2.json'
    api_key = '2b7fdcd9'

    users_data = load_user_data(data_file)
    display_users(users_data)
    user_data = select_user(users_data)
    user_name = user_data['name']

    all_movies = get_all_movies(users_data)
    movie_data = load_movie_data(all_movies, api_key)

    recommender = MovieRecommender(users_data, movie_data)
    recommendations, antirecommendations = recommender.generate_recommendations(user_data)

    display_recommendations(user_name, recommendations, antirecommendations)

if __name__ == "__main__":
    main()

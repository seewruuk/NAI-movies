import json
import os
import requests

def load_user_data(data_file):
    """
    Wczytuje dane użytkowników z pliku JSON.
    """
    with open(data_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_movie_data(all_movies, api_key):
    """
    Wczytuje dane o filmach z pliku cache lub pobiera je z API OMDb.
    """
    cache_file = 'data/movie_features.json'
    movie_data = {}

    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            movie_data = json.load(f)
    else:
        movie_data = fetch_movie_data(all_movies, api_key)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(movie_data, f, ensure_ascii=False, indent=4)

    return movie_data

def fetch_movie_data(all_movies, api_key):
    """
    Pobiera dane o filmach z API OMDb.
    """
    movie_data = {}
    for movie_title in all_movies:
        params = {
            't': movie_title,
            'apikey': api_key
        }
        response = requests.get('http://www.omdbapi.com/', params=params)
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                movie_data[movie_title] = data
            else:
                print(f"Błąd pobierania danych dla {movie_title}: {data['Error']}")
        else:
            print(f"Błąd HTTP {response.status_code} dla {movie_title}")
    return movie_data

def get_all_movies(users_data):
    """
    Pobiera zestaw wszystkich filmów z danych użytkowników.
    """
    movies = set()
    for user in users_data:
        for movie in user['movies']:
            movies.add(movie['title'])
    return movies

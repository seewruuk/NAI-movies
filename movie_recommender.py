import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

class MovieRecommender:
    """
    Generuje rekomendacje i antyrekomendacje filmów dla użytkownika z użyciem filtracji opartej na treści.
    """

    def __init__(self, users_data, movie_data):
        """
        Inicjalizuje obiekt klasy MovieRecommender.
        """
        self.users_data = users_data
        self.movie_data = movie_data
        self.all_movies = set(movie_data.keys())
        self.movie_features = None
        self.movie_title_to_index = {}
        self.movie_index_to_title = {}
        self.process_movie_features()

    def process_movie_features(self):
        """
        Przetwarza dane filmów i tworzy wektory cech dla każdego filmu.
        """
        genres_list = []
        plots = []
        movie_titles = []
        for title, data in self.movie_data.items():
            genres = data.get('Genre', '')
            genres_list.append([g.strip() for g in genres.split(',')])
            plot = data.get('Plot', '')
            plots.append(plot)
            movie_titles.append(title)

        mlb = MultiLabelBinarizer()
        genres_encoded = mlb.fit_transform(genres_list)

        tfidf = TfidfVectorizer(stop_words='english')
        plots_tfidf = tfidf.fit_transform(plots)

        self.movie_features = hstack([genres_encoded, plots_tfidf]).tocsr()

        self.movie_title_to_index = {title: idx for idx, title in enumerate(movie_titles)}
        self.movie_index_to_title = {idx: title for idx, title in enumerate(movie_titles)}

    def generate_recommendations(self, user_data):
        """
        Generuje listy rekomendacji i antyrekomendacji na podstawie ocen użytkownika.
        """
        user_movies = user_data['movies']
        liked_movies = [movie['title'] for movie in user_movies if movie['rating'] >= 7.0]
        disliked_movies = [movie['title'] for movie in user_movies if movie['rating'] <= 4.0]
        seen_movies = set(movie['title'] for movie in user_movies)
        unseen_movies = self.all_movies - seen_movies

        liked_indices = [self.movie_title_to_index[title] for title in liked_movies if title in self.movie_title_to_index]
        disliked_indices = [self.movie_title_to_index[title] for title in disliked_movies if title in self.movie_title_to_index]
        unseen_indices = [self.movie_title_to_index[title] for title in unseen_movies if title in self.movie_title_to_index]

        if not liked_indices:
            print("Brak wystarczającej liczby ocenionych pozytywnie filmów do wygenerowania rekomendacji.")
            return [], []

        # Oblicza podobieństwo między niewidzianymi filmami a lubianymi
        unseen_features = self.movie_features[unseen_indices]
        liked_features = self.movie_features[liked_indices]
        similarity_to_liked = cosine_similarity(unseen_features, liked_features)
        mean_similarity_to_liked = np.mean(similarity_to_liked, axis=1)

        # Oblicza podobieństwo między niewidzianymi filmami a nielubianymi
        if disliked_indices:
            disliked_features = self.movie_features[disliked_indices]
            similarity_to_disliked = cosine_similarity(unseen_features, disliked_features)
            mean_similarity_to_disliked = np.mean(similarity_to_disliked, axis=1)
        else:
            mean_similarity_to_disliked = np.zeros(len(unseen_indices))

        # Oblicza różnicę podobieństw
        scores = mean_similarity_to_liked - mean_similarity_to_disliked

        # Sortuje filmy według uzyskanych ocen
        top_indices = np.argsort(-scores)
        bottom_indices = np.argsort(scores)

        recommendations = []
        antirecommendations = []
        movies_already_picked = set()

        # Wybiera 5 najlepszych rekomendacji
        for idx in top_indices:
            if len(recommendations) >= 5:
                break
            movie_idx = unseen_indices[idx]
            movie_title = self.movie_index_to_title[movie_idx]
            if movie_title not in movies_already_picked:
                recommendations.append(movie_title)
                movies_already_picked.add(movie_title)

        # Wybiera 5 antyrekomendacji
        for idx in bottom_indices:
            if len(antirecommendations) >= 5:
                break
            movie_idx = unseen_indices[idx]
            movie_title = self.movie_index_to_title[movie_idx]
            if movie_title not in movies_already_picked:
                antirecommendations.append(movie_title)
                movies_already_picked.add(movie_title)

        return recommendations, antirecommendations

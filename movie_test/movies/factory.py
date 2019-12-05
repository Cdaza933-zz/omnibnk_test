# Classes for implementation using only Services and Helpers
from movies.methods import get_recommended_movies_by_title_search, get_recommended_movies_by_year_search, \
    get_recommended_movies_by_genre_search


class MovieRecomendationsHandlerFactory:

    FILTER_METHOD = {
        'title': get_recommended_movies_by_title_search,
        'genres': get_recommended_movies_by_genre_search,
        'release_date': get_recommended_movies_by_year_search
    }

    def __init__(self, user_searches, type_of_search):
        self.user_searches = user_searches
        self.type_of_search = type_of_search

    def get_recommended_movies(self):
        recommend_func = MovieRecomendationsHandlerFactory.FILTER_METHOD.get(self.type_of_search)
        response = recommend_func(self.user_searches)
        return response



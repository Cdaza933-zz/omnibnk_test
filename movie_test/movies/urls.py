from django.conf.urls import url
from django.urls import path

from movies.views import GetMoviesView, GetUserRecommendedMovies

app_name = 'movierecomendation'

urlpatterns = [
    url(r'^search_movies$', GetMoviesView.as_view(), name='search_movies'),
    url(r'^recommended_movies', GetUserRecommendedMovies.as_view(), name='recommended_movies'),
]
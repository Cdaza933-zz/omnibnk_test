import operator
from functools import reduce

from django.db.models import Sum, Q

from movies.models import Movie, Genre
from user.models import UserSearchHistory


def get_recommended_movies_by_title_search(user_searched_titles):
    # get users that have searched similar movies than the user
    users_search = {}
    total_searches = user_searched_titles.aggregate(Sum('number_of_searches'))['number_of_searches__sum']
    user = user_searched_titles.first().user
    for title in user_searched_titles:
        users_with_similar_tates = UserSearchHistory.objects.filter(
            search_data__iexact=title.search_data).exclude(user=user).order_by('-number_of_searches')
        for similar_taste_user in users_with_similar_tates:
            try:
                users_search[similar_taste_user.user.id] += title.number_of_searches / total_searches
            except KeyError:
                users_search[similar_taste_user.user.id] = title.number_of_searches / total_searches
    most_matched_users = sorted(users_search, key=users_search.__getitem__, reverse=True)[:10]
    if most_matched_users:
        recommended_titles = UserSearchHistory.objects.filter(type_of_search__slug='title',
                                                              user__id__in=most_matched_users
                                                              ).values_list('search_data', flat=True)
        search = None
        for x in recommended_titles:
            if not search:
                search = Q(title__icontains=x)
            else:
                search = search | Q(title__icontains=x)
        return Movie.objects.filter(search)
    else:
        recommended_titles = UserSearchHistory.objects.filter(type_of_search__slug='title',
                                                              user=user).values_list('search_data', flat=True)
        search = None
        for x in recommended_titles:
            if not search:
                search = Q(title__icontains=x)
            else:
                search = search | Q(title__icontains=x)
        return Movie.objects.filter(search)


def get_recommended_movies_by_genre_search(user_most_searched_genre):
    genre = Genre.objects.get(name=user_most_searched_genre.first().search_data)
    return genre.genre_movies.all().order_by('-rate')


def get_recommended_movies_by_year_search(user_most_searched_genre):
    movies = Movie.objects.filter(release_date=user_most_searched_genre.first().search_data).order_by('-rate')
    return movies

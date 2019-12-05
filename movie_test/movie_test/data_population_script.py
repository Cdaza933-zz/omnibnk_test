import requests

# populate genre table
from movies.models import Genre, Movie
from user.models import TypeOfSearch, UserSearchHistory


def populate_data_base():
    genre_dict = {}
    base_url = 'https://api.themoviedb.org/3'
    genre_resp = requests.get(base_url + '/genre/movie/list?api_key=1a4d240b7b1426f488fb03ba70cb3649&language=es-CO')
    if genre_resp.status_code == 200:
        for genre in genre_resp.json()['genres']:
            genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
            genre_dict[genre['id']] = genre_obj

    # populate movie table
    for page in range(1, 10):
        movies_resp = requests.get(
            base_url + '/movie/popular?api_key=1a4d240b7b1426f488fb03ba70cb3649&language=es-CO&page={}'.format(page))
        if movies_resp.status_code == 200:
            for movie in movies_resp.json()['results']:
                movie_obj, _ = Movie.objects.get_or_create(title=movie["title"],
                                                           rate=movie["vote_average"],
                                                           overview=movie["overview"],
                                                           release_date=movie["release_date"])
                for genre in movie['genre_ids']:
                    movie_obj.genres.add(genre_dict[genre])


def simulate_multiple_genre_searches(user):
    type_of_search, created = TypeOfSearch.objects.get_or_create(name='Genre Filter', slug='genres')
    UserSearchHistory.objects.get_or_create(user=user,
                                            type_of_search=type_of_search,
                                            search_data='Terror',
                                            number_of_searches=50)


def simulate_multiple_year_searches(user):
    type_of_search, created = TypeOfSearch.objects.get_or_create(name='Release Date Filter',
                                                                 slug='release_date')
    UserSearchHistory.objects.get_or_create(user=user,
                                            type_of_search=type_of_search,
                                            search_data='2019-12-18',
                                            number_of_searches=50)


def simulate_title_searches(users, user):
    type_of_search, created = TypeOfSearch.objects.get_or_create(name='Title Filter',
                                                                 slug='title')
    title_search = ['frozen', 'star', 'it', 'Terminator', 'bastardos', 'spider', 'Aladdín', 'Fast']
    for i in range(0, len(title_search)):
        user_position = i % 4
        if i % 3:
            number_of_searches = 90 if i == 0 else 90/i
            UserSearchHistory.objects.get_or_create(user=user,
                                                    type_of_search=type_of_search,
                                                    search_data=title_search[i],
                                                    number_of_searches=number_of_searches)
            for t_user in users:
                UserSearchHistory.objects.get_or_create(user=t_user,
                                                        type_of_search=type_of_search,
                                                        search_data=title_search[i],
                                                        number_of_searches=i)
        else:
            UserSearchHistory.objects.get_or_create(user=users[user_position],
                                                    type_of_search=type_of_search,
                                                    search_data=title_search[i],
                                                    number_of_searches=i)

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from movie_test.data_population_script import populate_data_base, simulate_title_searches, \
    simulate_multiple_year_searches, simulate_multiple_genre_searches


class SearchMovieTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.url = '/movies/search_movies'
        self.headers = {'Content-Type': 'application/json'}
        populate_data_base()

    def test_user_search_by_title(self):
        response = self.client.get(self.url + '?title={}'.format('star'),
                                    format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 4)
        self.assertEquals(response.json()[0]['title'], "Star Wars: El ascenso de Skywalker")

    def test_user_search_by_release_date(self):
        response = self.client.get(self.url + '?release_date={}'.format('2019-12-18'),
                                    format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['title'], "Star Wars: El ascenso de Skywalker")

    def test_user_search_by_one_genre(self):
        response = self.client.get(self.url + '?genres={}'.format('Drama'),
                                    format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 50)
        self.assertEquals(response.json()[0]['title'], "El irlandés")

    def test_user_search_by_list_of_genres(self):
        response = self.client.get(self.url + '?genres={}'.format('Drama,Aventura,Comedia'),
                                    format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 148)
        self.assertEquals(response.json()[0]['title'], "El irlandés")


class RecommendedMovieTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.url = '/movies/recommended_movies'
        self.headers = {'Content-Type': 'application/json'}
        populate_data_base()

    def test_user_recommend_by_title(self):
        users = [User.objects.create_superuser('admin{}'.format(i),
                                               'admin{}@admin.com'.format(i), 'admin123') for i in range(1, 5)]
        simulate_title_searches(users, self.user)
        response = self.client.get(self.url, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 28)
        self.assertEquals(response.json()[0]['title'], "Sense, Sensibility & Snowmen")

    def test_user_recomend_by_release_date(self):
        simulate_multiple_year_searches(self.user)
        response = self.client.get(self.url, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['title'], "Star Wars: El ascenso de Skywalker")

    def test_user_search_by_one_genre(self):
        simulate_multiple_genre_searches(self.user)
        response = self.client.get(self.url, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 11)
        self.assertEquals(response.json()[0]['title'], "Handjob Cabin")

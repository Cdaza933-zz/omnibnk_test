from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.factory import MovieRecomendationsHandlerFactory
from movies.filters import MovieFilter
from movies.models import Movie
from movies.serializers import MovieSerializer
from user.models import UserSearchHistory


class GetMoviesView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_class = MovieFilter
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class GetUserRecommendedMovies(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_search_data = UserSearchHistory.objects.filter(user=user).order_by('-number_of_searches')
        if user_search_data.exists():
            type_of_search = user_search_data.first().type_of_search
            user_search_data = user_search_data.filter(type_of_search=type_of_search)
            movies = MovieRecomendationsHandlerFactory(user_search_data, type_of_search.slug).get_recommended_movies()
        else:
            movies = Movie.objects.all()
        movies = movies.order_by('-rate')[:100]
        return Response(MovieSerializer(movies,many=True).data, status=status.HTTP_200_OK)


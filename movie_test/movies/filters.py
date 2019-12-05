import django_filters

from movies.models import Movie, Genre
from user.models import TypeOfSearch, UserSearchHistory


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='title_filter')
    release_date = django_filters.DateFilter(method='release_date_filter')
    genres = django_filters.Filter(method='genre_filter')



    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'genres']

    def genre_filter(self, queryset, args, value):
        type_of_search, created = TypeOfSearch.objects.get_or_create(name='Genre Filter', slug='genres')
        id_list = []
        for genre in value.split(','):
            history, h_created = UserSearchHistory.objects.get_or_create(user=self.request.user,
                                                                         type_of_search=type_of_search,
                                                                         search_data=genre)
            genre_obj = Genre.objects.get(name=genre)
            genre_obj.searches += 1
            genre_obj.save()
            id_list.extend(genre_obj.genre_movies.all().values_list('id',flat=True))
            history.number_of_searches += 1
            history.save()
        return queryset.filter(id__in=id_list)

    def release_date_filter(self, queryset, args, value):
        type_of_search, created = TypeOfSearch.objects.get_or_create(name='Release Date Filter',
                                                                     slug='release_date')

        history, h_created = UserSearchHistory.objects.get_or_create(user=self.request.user,
                                                                     type_of_search=type_of_search,
                                                                     search_data=value)
        history.number_of_searches += 1
        history.save()
        return queryset.filter(release_date=value)

    def title_filter(self, queryset, args, value):
        type_of_search, created = TypeOfSearch.objects.get_or_create(name='Title Filter',
                                                                     slug='title')

        history, h_created = UserSearchHistory.objects.get_or_create(user=self.request.user,
                                                                     type_of_search=type_of_search,
                                                                     search_data=value)
        history.number_of_searches += 1
        history.save()
        return queryset.filter(title__icontains=value)



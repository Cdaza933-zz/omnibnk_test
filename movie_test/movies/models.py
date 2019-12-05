from django.db import models
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    searches = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    searches = models.IntegerField(default=0, blank=False, null=False)
    genres = models.ManyToManyField(Genre, related_name='genre_movies')
    release_date = models.DateField(null=False, blank=False)
    overview = models.TextField(max_length=255, null=False, blank=False)
    rate = models.FloatField(default=0.0, null=False, blank=False)

    def __str__(self):
        return self.title

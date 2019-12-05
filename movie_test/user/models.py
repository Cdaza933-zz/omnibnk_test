from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TypeOfSearch(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, related_name='user_search', null=False, on_delete=models.CASCADE)
    type_of_search = models.ForeignKey(TypeOfSearch, null=False, on_delete=models.CASCADE)
    number_of_searches = models.IntegerField(default=0, null=False, blank=False)
    search_data = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return ' '.join([str(self.user), str(self.type_of_search), str(self.number_of_searches)])

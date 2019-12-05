from django.conf.urls import url

from user.views import ObtainAuthToken

app_name = 'users'


urlpatterns = [
    url(r'^api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
]

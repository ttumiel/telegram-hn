from django.conf.urls import url

from .views import CommandReceiveView

app_name = 'telegram'
urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]
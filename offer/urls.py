from django.urls import path

from . import api


urlpatterns = [
    path('create/', api.offer_create, name='post_create'),
]
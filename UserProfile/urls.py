# core/urls.py

from django.urls import path
from .views import create_post_view

app_name = 'user'
urlpatterns = [
    path('create_post/', create_post_view, name='create_post'),
]

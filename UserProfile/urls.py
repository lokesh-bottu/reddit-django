# core/urls.py

from django.urls import path
from .views import create_post_view,like_post

app_name = 'user'
urlpatterns = [
    path('create_post/', create_post_view, name='create_post'),
    path('like_post/', like_post, name='like_post'),
]

# core/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_post_view,like_post,add_comment,like_post_2

app_name = 'user'
urlpatterns = [
    path('create_post/', create_post_view, name='create_post'),
    path('like_post/', like_post, name='like_post'),
    path('add_comment/', add_comment, name='add_comment'),
    path('like_post_2/', like_post_2, name='like_post_2'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



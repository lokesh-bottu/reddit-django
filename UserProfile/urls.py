# core/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_post_view,like_post,add_comment,like_post_2,comment_view,post_comment_view,like_comment,profile_view

app_name = 'user'
urlpatterns = [
    path('create_post/', create_post_view, name='create_post'),
    path('like_post/', like_post, name='like_post'),
    path('add_comment/', add_comment, name='add_comment'),
    path('like_post_2/', like_post_2, name='like_post_2'),
    path('popup_comment/<int:id>', comment_view, name='popup_comment'),
    path('post_comment_view/<int:id>', post_comment_view, name='post_comment_view'),
    path('like_comment/', like_comment, name='like_comment'),
    path('profile/', profile_view, name='profile'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin

from .models import Post,Comment,UserProfile,Replies
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Replies)
# admin.site.register(Followings)
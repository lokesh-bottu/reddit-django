
#IMPLEMENTING THE LIKES


# from django.contrib.auth.models import User
# from django.db import models

# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     caption = models.CharField(max_length=255)
#     description = models.TextField()
#     # image = models.ImageField(upload_to='post_images/', blank=True, null=True)
#     likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
#     comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.created_at}"


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()





from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)


    newlikes = models.ManyToManyField(User, related_name='newliked_posts', blank=True)
    newdislikes = models.ManyToManyField(User, related_name='newdisliked_posts', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.caption} - {self.created_at}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    # parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.post_id.caption} - {self.created_at}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username




# class Followings(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
#     followers = models.ManyToManyField(User, related_name='followers', blank=True)
#     follow = models.ManyToManyField(User, related_name='follow', blank=True)



    # def __str__(self):
    #     return f'{self.follow} follows {self.followers}'

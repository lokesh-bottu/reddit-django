
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
    likesposts = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikesposts = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.caption} - {self.created_at}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    # commentlikes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.post_id.caption} - {self.created_at}"

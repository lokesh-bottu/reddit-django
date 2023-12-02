
from django.shortcuts import  redirect, render


from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User

def create_post_view(request):


    all_posts = {}
    for post in Post.objects.all():
        post_id = post.id
        all_posts[post_id] = {
                'post_caption': post.caption,
                'post_description': post.description,
                'post_likes': post.likes.count(),
            }

        context = {'all_posts': all_posts}

    if(request.method == "POST"):
        caption = request.POST['caption']
        description = request.POST['description']
        post = Post.objects.create(
        user=request.user,
        caption = caption,
        description = description
        )
        post.save()
        return redirect('user:create_post')
    else:
        
        return render(request, 'authentication/index1.html', context)
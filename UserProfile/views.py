
from django.shortcuts import  redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse,JsonResponse
from .models import Post
from django.contrib.auth.models import User
from .forms import LikeForm
import json

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
    

@csrf_exempt  
def like_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            form = LikeForm(data)
            if form.is_valid():
                post_id = form.cleaned_data['post_id']
                post = Post.objects.get(pk=post_id)
                post.likes.add(request.user)
                likes_count = post.likes.count()
                print(f"Post {post_id} liked by {request.user.username}. New likes count: {likes_count}")
                return JsonResponse({'likes_count': likes_count})
            else:
                print("Form not valid:", form.errors)
        except json.JSONDecodeError:
            print("Invalid JSON data")
    print("Invalid request")
    return JsonResponse({'error': 'Invalid request'})

from django.shortcuts import  redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse,JsonResponse
from .models import Post,Comment
from django.contrib.auth.models import User
from .forms import LikeForm
import json

def create_post_view(request):
    all_posts = {}
    for post in Post.objects.all():
        post_id = post.id
        id_comment = post.id
        comments_list = []
        for com in Comment.objects.filter(post_id = Post.objects.get(id = id_comment)):
            com_string = str(com.user)+"--"+str(com.text)
            comments_list.append(com_string)

        all_posts[post_id] = {
                'post_caption': post.caption,
                'post_description': post.description,
                'post_likes': post.likes.count(),
                'post_comments':comments_list
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
                user = request.user

                # Check if the user has already liked the post
                if user in post.likes.all():
                    # If yes, remove the like
                    post.likes.remove(user)
                    liked = False
                else:
                    # If no, add the like
                    post.likes.add(user)
                    liked = True

                likes_count = post.likes.count()
                print(f"Post {post_id} {'liked' if liked else 'unliked'} by {user.username}. New likes count: {likes_count}")
                return JsonResponse({'likes_count': likes_count, 'liked': liked})
            else:
                print("Form not valid:", form.errors)
        except json.JSONDecodeError:
            print("Invalid JSON data")
    print("Invalid request")
    return JsonResponse({'error': 'Invalid request'})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Import this decorator
from .models import Comment
import json

@csrf_exempt  # Add this decorator to exempt CSRF token for simplicity (don't use in production)
def add_comment(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            text = data.get('text', '')
            
            # Assuming you have the 'Comment' model with fields 'user', 'post', 'text'
            # Add some debug statements
            print(f"Received comment for post {post_id} with text: {text}")
            
            Comment.objects.create(
                user=request.user,
                post_id=post_id,
                text=text
            )
            
            print("Comment successfully added to the database.")
            
            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            print("Invalid JSON data. Error:", e)
    
    print("Invalid request or failed to add comment.")
    return JsonResponse({'error': 'Invalid request or failed to add comment'})









@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            post_id = data.get('post_id', None)
            text = data.get('text', '')

            if post_id is not None:
                post = Post.objects.get(pk=post_id)

                Comment.objects.create(
                    user=request.user,
                    post_id=post,  # Corrected from `post` to `post_id`
                    text=text
                )

                print(f"Comment for post {post_id} added successfully.")
                return JsonResponse({'success': True})
            else:
                print("Invalid request. Post ID is missing.")
        except json.JSONDecodeError as e:
            print("Invalid JSON data. Error:", e)
        except Post.DoesNotExist:
            print(f"Post with ID {post_id} does not exist.")
    print("Invalid request or failed to add comment.")
    return JsonResponse({'error': 'Invalid request or failed to add comment'})

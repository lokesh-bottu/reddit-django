
from django.shortcuts import  redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse,JsonResponse
from .models import Post,Comment,Replies,UserProfile
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
        
        image_url = ''
    
        if post.image:
            image_url = request.build_absolute_uri(post.image.url)
            print("this is image url", image_url)
            

        user_image = get_object_or_404(UserProfile, user=post.user)
        all_posts[post_id] = {
                'post_caption': post.caption,
                'post_description': post.description,
                'post_likes': post.likes.count(),
                'post_comments':comments_list,
                'user_name':post.user,
                'comments_count':len(comments_list),
                'newlikes':post.newlikes.count(),
                'newdislikes':post.newdislikes.count(),
                'alllikes':(post.newlikes.count()-post.newdislikes.count()),
                'image': image_url,
                'user_image':user_image
                
        }


    context = {'all_posts': all_posts}
    if(request.method == "POST"):
        caption = request.POST['caption']
        description = request.POST['description']
        image = request.FILES.get('image_database')
        post = Post.objects.create(
        user=request.user,
        caption = caption,
        description = description,
        image = image
        
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



# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .forms import LikeForm

@csrf_exempt
# views.py

def like_post_2(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            post_id = data.get('post_id')
            action = data.get('action')
            post = Post.objects.get(pk=post_id)
            user = request.user

            if action == 1:  # Like
                post.newlikes.add(user)
                post.newdislikes.remove(user)
            elif action == 0:  # Dislike
                post.newdislikes.add(user)
                post.newlikes.remove(user)

            count = {
                'likes_count': post.newlikes.count(),
                'dislikes_count': post.newdislikes.count(),
            }

            print(f"Post {post_id} {'liked' if action == 1 else 'disliked'} by {user.username}. New counts: {count}")
            return JsonResponse(count)
        except json.JSONDecodeError:
            print("Invalid JSON data")

    print("Invalid request")
    return JsonResponse({'error': 'Invalid request'})



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





def post_comment_view(request,id):
    print("function callled",id)
    if id is not None:
        post = Post.objects.get(pk=id)
        user_name = request.user

        Comment.objects.create(
            user=user_name,
            post_id=post,
            text=request.POST.get('comment_text')
        )

    return redirect(request.META.get('HTTP_REFERER'))



def add_reply(request,id):
    print("reply fucntion called")
    if id is not None:
        comment_inst = Comment.objects.get(pk=id)
        loggeduser_name = request.user
        Replies.objects.create(
            user=loggeduser_name,
            comment_id = comment_inst,
            text=request.POST.get('reply')
        )
    return redirect(request.META.get('HTTP_REFERER'))




def comment_view(request,id):
    post = Post.objects.get(pk=id)
    comments = {}
    for com  in Comment.objects.filter(post_id = Post.objects.get(id = id)):

        # user_image = get_object_or_404(UserProfile, user=com.user)

        comments[com.id] = {'username':com.user,
                            'text':com.text,
                            'created_at':com.created_at,
                            'alllikes':(com.likes.count() - com.dislikes.count()),
                            # 'image':user_image
                            }
        reps={} 
        for replies in Replies.objects.filter(comment_id = com):
            # reply_image = get_object_or_404(UserProfile,user = replies.user)   #'image':reply_image
            reps[replies.id]= {'user':str(replies.user),'text':replies.text}
        comments[com.id]['replies'] = reps
            
    return render(request, 'userposts/multicomments.html', {'post':post, 'comments':comments,'post_id':id})




# def comment_view(request, id):
#     post = Post.objects.get(pk=id)
#     comments = Comment.objects.filter(post_id_id=id, parent_comment__isnull=True)
#     nested_comments = Comment.objects.filter(post_id_id=id, parent_comment__isnull=False)

#     context = {'post': post, 'comments': comments, 'nested_comments': nested_comments}
#     return render(request, 'userposts/multicomments.html', context)




def like_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            comment_id = data.get('comment_id')
            action = data.get('action')
            com_instance = Comment.objects.get(pk=comment_id)
            user = request.user

            if action == 1:  # Like
                com_instance.likes.add(user)
                com_instance.dislikes.remove(user)
            elif action == 0:  # Dislike
                com_instance.dislikes.add(user)
                com_instance.likes.remove(user)

            count = {
                'likes_count': com_instance.likes.count(),
                'dislikes_count': com_instance.dislikes.count(),
            }

            print(f"Comment {comment_id} {'liked' if action == 1 else 'disliked'} by {user.username}. New counts: {count}")
            return JsonResponse(count)
        except json.JSONDecodeError:
            print("Invalid JSON data")

    print("Invalid request")
    return JsonResponse({'error': 'Invalid request'})







def editprofile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.save()

        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.image = request.FILES.get('image', profile.image)
        profile.save()

    user = request.user
    posts = Post.objects.all().count()
    context = {'user':user,
               'posts':posts,
               }
    return render(request, 'userposts/editprofile.html',context)


def viewprofile(request, username):

    
    # print(username)
    # post = get_object_or_404(UserProfile, user__username='lokesh')
    # print(post)
    # print(user_obj)   #'image':reply_image     #,'user_image':user_obj
    context = {'user': username}

    return render(request, 'userposts/viewprofile.html', context)









    
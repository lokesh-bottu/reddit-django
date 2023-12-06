
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
# from .models import UserDetails
from UserProfile.models import Post,Comment,UserProfile


def home(request):
    return render(request,'authentication/signin.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,"Your Account has been successfully created.")
        return redirect('signin')
    return render(request,'authentication/signup.html')



def signin(request):    
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username = username,password = password)

        if user is not None:
            login(request,user)
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
                }


            context = {'all_posts': all_posts}
            return render(request,'authentication/index1.html',context)
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('home')
        
    return render(request,'authentication/signin.html')

def signout(request):
    return render(request,'authentication/signin.html')





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

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('editprofile')

    return render(request, 'authentication/editprofile.html')


from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
# from .models import UserDetails
from UserProfile.models import Post

# Create your views here.
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
                all_posts[post_id] = {
                        'post_caption': post.caption,
                        'post_description': post.description,
                        'post_likes': (post.likesposts.count() - post.dislikesposts.count()),
                }

            context = {'all_posts': all_posts,'username':username}
            return render(request,'authentication/index1.html',context)
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('home')
        
    return render(request,'authentication/signin.html')

def signout(request):
    return render(request,'authentication/signin.html')




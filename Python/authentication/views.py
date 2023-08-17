from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method=="POST":
            username=request.POST['username']
            fname=request.POST['firstname']
            lname=request.POST['lastname']
            email=request.POST['email']
            password1=request.POST['password']
            password2=request.POST['cpassword']

            myuser = User.objects.create_user(username,email,password1)
            myuser.first_name = fname
            myuser.last_name = lname
            
            myuser.save()

            messages.success(request, "Successful")

            return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html",{'fname':fname})
        else:
            messages.error(request, "bad credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('home')


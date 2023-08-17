from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import User

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("log_in")
    else:
        return render(request, "login.html")
    
def signup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        Cpassword = request.POST.get("cpass")

        User = get_user_model()
        if password == Cpassword:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "Username/Email already exists")
                return redirect("signup")
            else:
                obj = User.objects.create(
                    fname=fname,
                    lname=lname,
                    username=username,
                    email=email,
                    password=password
                )
                return redirect("log_in")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
    return render(request, "signup.html")

def home(request):
    return render(request, "home.html")

def loggout(request):
    logout(request)
    return redirect("home")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials! please try again")
            return redirect('login')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        uid = request.POST.get("uid")
        password = request.POST.get("pass")
        Cpassword = request.POST.get("cpass")

        if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
        ):
            messages.error(request, "Email Already Exists")
            return render(request, "signup.html", {"email": username})
        else:
            user = User.objects.create_user(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password,
                uid=uid
            )
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
    else:
        return render(request, "signup.html")



def home(request):
    return render(request, "home.html")


def loggout(request):
    logout(request)
    return redirect("home")

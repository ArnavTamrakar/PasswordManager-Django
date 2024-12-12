from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Password
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from django.urls import reverse

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY)



def sign_up(request):
    if request.method =="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password != password2:
            msg = "Password doesn't match!"
            messages.error(request, msg)
            return HttpResponseRedirect(request.path)
        # if username exists
        if User.objects.filter(username=username).exists():
            msg = f"{username} already exists!"
            messages.error(request, msg)
            return HttpResponseRedirect(request.path)
        # if email exists
        elif User.objects.filter(email=email).exists():
            msg = f"{email} already exists!"
            messages.error(request, msg)
            return HttpResponseRedirect(request.path)
        else:
            User.objects.create_user(username, email,password)
            new_user=authenticate(request, username = username, password = password2)
            if new_user is not None:
                login(request, new_user)
                msg = f"{username} Welcome"
                messages.success(request, msg)
                return redirect('home')
    return render(request, "Manager/signup.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    passwords = Password.objects.filter(user=request.user)
    return render(request, 'Manager/passmanager.html', {'passwords': passwords})

def add_password(request):
    if request.method == "POST":
        # Retrieve form data
        url = request.POST.get("url")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Encrypt the email and password
        encrypted_email = fernet.encrypt(email.encode())
        encrypted_password = fernet.encrypt(password.encode())

        # Retrieve the title and icon
        try:
            br.open(url)
            title = br.title()
        except:
            title = url
        try:
            icon = favicon.get(url)[0].url
        except:
            icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"

        # Save to the Password model
        Password.objects.create(
            user=request.user,
            name=title,
            logo=icon,
            email=encrypted_email.decode(),
            password=encrypted_password.decode(),
        )

        msg = f"{title} added successfully."
        messages.success(request, msg)
        

    elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return redirect("home")

    # Decrypt passwords before rendering
    if request.user.is_authenticated:
        try:
            passwords = Password.objects.filter(user=request.user)
            for password in passwords:
                password.email = fernet.decrypt(password.email.encode()).decode()
                password.password = fernet.decrypt(password.password.encode()).decode()
                password.save()
        except Exception as e:
            print(f"Decryption Error: {e}")
            print(f"Problematic Email: {password.email}")
            print(f"Problematic Password: {password.password}")

    return render(request, "Manager/add_password.html", {"passwords":passwords,})



def login_view(request):
    if request.method == "POST":
        if 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "Manager/passmanager.html", {
                    "code": code,
                    "user": new_login,
                })

        elif "confirm" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                messages.error(request, msg)
                return render(request, "Manager/login.html")
            else:
                login(request, User.objects.get(username=user))
                msg = f"Welcome {request.user}!!"
                messages.success(request, msg)
                return HttpResponseRedirect(reverse('home'))

    return render(request, "Manager/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')

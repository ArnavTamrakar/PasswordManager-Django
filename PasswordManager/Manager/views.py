from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Password
from cryptography.fernet import Fernet, InvalidToken
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
from django.views.decorators.http import require_POST
import re

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY)

# Dictionary of known social media favicons
SOCIAL_MEDIA_ICONS = {
    'instagram.com': 'https://cdn-icons-png.flaticon.com/512/174/174855.png',
    'facebook.com': 'https://cdn-icons-png.flaticon.com/512/174/174848.png',
    'twitter.com': 'https://cdn-icons-png.flaticon.com/512/3256/3256013.png',
    'x.com': 'https://cdn-icons-png.flaticon.com/512/3256/3256013.png',
    'youtube.com': 'https://cdn-icons-png.flaticon.com/512/174/174883.png',
    'linkedin.com': 'https://cdn-icons-png.flaticon.com/512/174/174857.png',
    'github.com': 'https://cdn-icons-png.flaticon.com/512/733/733609.png',
    'reddit.com': 'https://cdn-icons-png.flaticon.com/512/3670/3670157.png',
    'discord.com': 'https://cdn-icons-png.flaticon.com/512/3670/3670157.png',
    'snapchat.com': 'https://cdn-icons-png.flaticon.com/512/174/174863.png',
    'tiktok.com': 'https://cdn-icons-png.flaticon.com/512/3938/3938056.png',
    'whatsapp.com': 'https://cdn-icons-png.flaticon.com/512/174/174879.png',
    'telegram.org': 'https://cdn-icons-png.flaticon.com/512/174/174857.png',
    'spotify.com': 'https://cdn-icons-png.flaticon.com/512/174/174872.png',
    'netflix.com': 'https://cdn-icons-png.flaticon.com/512/174/174836.png',
    'amazon.com': 'https://cdn-icons-png.flaticon.com/512/174/174836.png',
    'google.com': 'https://cdn-icons-png.flaticon.com/512/2991/2991148.png',
    'gmail.com': 'https://cdn-icons-png.flaticon.com/512/552/552489.png',
    'outlook.com': 'https://cdn-icons-png.flaticon.com/512/552/552489.png',
    'yahoo.com': 'https://cdn-icons-png.flaticon.com/512/552/552489.png',
}

def get_favicon_url(url):
    """
    Get favicon URL with improved logic for social media sites
    """
    # Clean and format the URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Extract domain for social media lookup
    domain = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if domain:
        domain = domain.group(1).lower()
        
        # Check if it's a known social media site
        for social_domain, icon_url in SOCIAL_MEDIA_ICONS.items():
            if social_domain in domain:
                return icon_url
    
    # Try to get favicon using the favicon library
    try:
        icons = favicon.get(url)
        if icons and len(icons) > 0:
            # Prefer PNG or ICO formats, fall back to first available
            for icon in icons:
                if icon.format in ['png', 'ico']:
                    return icon.url
            return icons[0].url
    except Exception as e:
        print(f"Favicon fetch error for {url}: {e}")
    
    # Fallback to default icon
    return "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"

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
        
        # Use the improved favicon function
        icon = get_favicon_url(url)

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

@require_POST
def delete_password(request):
    password_id = request.POST.get("password-id")
    if not password_id:
        messages.error(request, "Missing password ID.")
        return redirect("home")
    
    try:
        password_obj = Password.objects.get(id=password_id, user=request.user)
        name = password_obj.name
        password_obj.delete()
        messages.success(request, f"{name} deleted.")
    except Password.DoesNotExist:
        messages.error(request, "Password not found or you don't have permission to delete it.")
    
    return redirect("home")

def update_password(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        password_obj = Password.objects.get(id=id, user=request.user)
    except Password.DoesNotExist:
        messages.error(request, "Password not found.")
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and Password are required.")
            return redirect(request.path)

        password_obj.email = fernet.encrypt(email.encode()).decode()
        password_obj.password = fernet.encrypt(password.encode()).decode()
        password_obj.save()

        messages.success(request, f"{password_obj.name} updated successfully.")
        return redirect("home")

    # # Decrypt for pre-filled form
    # password_obj.email = fernet.decrypt(password_obj.email.encode()).decode()
    # password_obj.password = fernet.decrypt(password_obj.password.encode()).decode()

    return render(request, "Manager/update_password.html", {"password": password_obj})

    


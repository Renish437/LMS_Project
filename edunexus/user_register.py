from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout,authenticate, login as auth_login

def register(request):
    # Initialize context with empty defaults
    context = {'username': '', 'email': ''}

    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # Keep submitted values in context
        context['username'] = username
        context['email'] = email
       
        if not username :
            messages.warning(request, "Username is required")
            return render(request, 'registration/register.html', context)
        if not email :
            messages.warning(request, "Email is required")
            return render(request, 'registration/register.html', context)
        if not password :
            messages.warning(request, "password is required")
            return render(request, 'registration/register.html', context)
        # Check email
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return render(request, 'registration/register.html', context)

        # Check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return render(request, 'registration/register.html', context)

        # Create user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'registration/register.html', context)



def login(request):
    context = {'username': ''}

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        context['username'] = username  # Keep username filled in the form

        # Validation
        if not username:
            messages.warning(request, "Username is required")
            return render(request, 'registration/login.html', context)
        if not password:
            messages.warning(request, "Password is required")
            return render(request, 'registration/login.html', context)

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'registration/login.html', context)

    return render(request, 'registration/login.html', context)



def logout_user(request):
    logout(request)  # This clears the session
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def auth_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            # Login logic
            email = request.POST.get('email')  # Fetch email from the form
            password = request.POST.get('password')  # Fetch password from the form

            try:
                # Find the user by email
                user = User.objects.get(email=email)
                # Authenticate using the username (Django requires `username`)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('landing')  # Redirect to dashboard or any desired page
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')

        elif 'signup' in request.POST:
            # Signup logic
            username = request.POST.get('username')  # Fetch username (full name)
            email = request.POST.get('email')  # Fetch email
            password = request.POST.get('password')  # Fetch password

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            else:
                # Create the user and save
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)  # Automatically log the user in after signup
                return redirect('landing')  # Redirect to dashboard or any desired page

    return render(request, 'accounts/auth.html')

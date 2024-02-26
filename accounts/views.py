from accounts.forms import LoginForm, RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db import IntegrityError

@csrf_protect
def login_view(request):
    user = request.user
    context = {}
    context["errors"] = None
    if user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        form = LoginForm()
        context["form"] = form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context["form"] = form

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            form_has_errors = False

            existing_user = User.objects.filter(username=username)
            if not existing_user:
                form.add_error('username', f"No user with username \"{username}\" found.")
                form_has_errors = True

            user = authenticate(request, username=username, password=password)
            if not user:
                form.add_error('username', f"Username and password do not match.")
                form_has_errors = True

            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('/')

    context["errors"] = form.errors
    return render(request, 'login.html', context=context)

@csrf_protect
def register_view(request):
    context = {}
    context["errors"] = None
    if request.method == 'GET':
        form = RegistrationForm()
        context["form"] = form
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context["form"] = form
        if form.is_valid():

            # Set flag
            form_has_errors = False

            # Extract form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            existing_user = User.objects.filter(username=username)
            if existing_user:
                error_message = "Username is already taken. Please choose a different one."
                form.add_error('username', error_message)
                form_has_errors = True

            if password1 != password2:
                error_message = "Passwords do not match. Remember, passwords are cAsE sEnSiTiVe!"
                form.add_error('password2', error_message)
                form_has_errors = True

            if not form_has_errors:
                # Create the account
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Log the user in
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)

                return redirect('/')

    context["errors"] = form.errors
    return render(request, 'register.html', context=context)

def logout_view(request):
    messages.info(request, "Logging out...")
    if request.method == 'GET':
        user = request.user
        logout(request)
        return redirect('/')


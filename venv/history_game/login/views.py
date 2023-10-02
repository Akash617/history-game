from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from game.models import User
from login.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password

# Create your views here.
def login(request):
    # There is a logged in user already
    if "_auth_user_id" in request.session.keys():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        selection = request.POST.getlist('switch')
        if "login" in selection:
            return HttpResponseRedirect(reverse('login'))
        if "register" in selection:
            return HttpResponseRedirect(reverse('register'))

        form = LoginForm(request.POST)

        if form.is_valid() and login_form_is_valid(request, form):
            user = User.objects.get(username=form.cleaned_data["username"])
            auth_login(request, user)
            return HttpResponseRedirect(reverse('play'))

    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context=context)


def register(request):
    # There is a logged in user already
    if "_auth_user_id" in request.session.keys():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        selection = request.POST.getlist('switch')
        if "login" in selection:
            return HttpResponseRedirect(reverse('login'))
        if "register" in selection:
            return HttpResponseRedirect(reverse('register'))

        form = RegisterForm(request.POST)

        if form.is_valid() and register_form_is_valid(request, form):
            create_user(request, form)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context=context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


def register_form_is_valid(request, form):
    username = form.cleaned_data["username"]
    username_qs = User.objects.filter(username=username)
    if username_qs.exists():
        messages.error(request, "Username already exists")
        return False

    email = form.cleaned_data["email"]
    email_qs = User.objects.filter(email=email)
    if email_qs.exists():
        messages.error(request, "Email already exists")
        return False

    password = form.cleaned_data["password"]
    password1 = form.cleaned_data["password1"]
    if password and password1 and (password != password1):
        messages.error(request, "Passwords do not match")
        return False

    messages.error(request, "Account has been created")
    return True


def login_form_is_valid(request, form):
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    username_qs = User.objects.filter(username=username)

    if not username_qs.exists():
        messages.error(request, "Username/password is incorrect")
        return False

    user = authenticate(username=username, password=password)
    if user == None:
        messages.error(request, "Username/password is incorrect")
        return False

    return True


def create_user(request, form):
    user = User.objects.create_user(username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"])
    user.save()
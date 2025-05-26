from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .constants import MESSAGES
from .forms import SignUpForm, LoginForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password1'],
                                            )
            login(request, user)
            return render(request, 'registration/successful_registration.html')

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            return render(request,
                          'registration/failed_login.html',
                          context={'error': MESSAGES.get('user_error', '')})

        user = authenticate(request,
                            username=username,
                            password=password)
        if user:
            login(request, user)
            return redirect('main')

        return render(request,
                      'registration/failed_login.html',
                      context={'error':  MESSAGES.get('password_error', '')})

    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def log_out(request):
    logout(request)
    return render(request, 'main.html')

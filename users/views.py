from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, login_form_builder, registration_form_builder

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, 'users/form_builder.html', {'form': registration_form_builder})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'kitchen':
                return redirect('kitchen_dashboard')
            else:
                return redirect('user_dashboard')
        else: login_form_builder['warnline'] = 'Неправильный логин или пароль!'
    
    return render(request, 'users/form_builder.html', {'form': login_form_builder})

def logout_view(request):
    logout(request)
    return redirect('/')

from django.contrib.auth.decorators import login_required

@login_required
def kitchen_dashboard(request):
    return render(request, 'kitchen_dashboard.html')

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'kitchen':
                return redirect('kitchen_dashboard')
            else:
                return redirect('user_dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def kitchen_dashboard(request):
    return render(request, 'kitchen_dashboard.html')

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

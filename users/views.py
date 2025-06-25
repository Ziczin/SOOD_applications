from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .form_builder import form_builder
from .forms import builder_data

registration_form = form_builder(builder_data['registration'])
login_form = form_builder(builder_data['login'])

def register(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = registration_form()

    return render(request, 'users/form_builder.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.service == 'kitchen':
                return redirect('kitchen_dashboard')
            else:
                return redirect('user_dashboard')
    
    return render(request, 'users/form_builder.html', {'form': login_form})

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

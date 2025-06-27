from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .form_builder import form_builder

from .forms import login_form_data, registration_form_data

import json

registration_form = form_builder(registration_form_data)
login_form = form_builder(login_form_data)

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
            return redirect('dashboard')
            
    return render(request, 'users/form_builder.html', {'form': login_form})

def logout_view(request):
    logout(request)
    return redirect('/')



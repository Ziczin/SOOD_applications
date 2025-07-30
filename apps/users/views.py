from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from apps.users.models import CustomUser
from apps.forms.forms import login_form_data, registration_form_data

from apps.forms.form_builder import form_builder

registration_form = form_builder(registration_form_data)
login_form = form_builder(login_form_data)

def register(request):
    errors = []
    if request.method == 'POST':
        if CustomUser.objects.filter(username=request.POST["username"]).exists():
            errors.append('Пользователь с таким логином уже существует!')
        if request.POST['password1'] != request.POST['password2']:
            errors.append('Пароли не совпадают!')
        form = registration_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = registration_form()

    return render(request, 'application/make_example.html', {'form': form, 'errors': errors})
    return render(request, 'forms/form_builder.html', {'form': form, 'errors': errors})

def login_view(request):
    errors = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = login_form(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/applications/dashboard')
        else:
            errors.append("Неправильный логин или пароль!")
    else:
        form = login_form()
    return render(request, 'forms/form_builder.html', {'form': form, 'errors': errors})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def change_role(request):
    username = request.POST['username']
    new_role = request.POST['role']
    user = CustomUser.objects.get(username=username)
    user.role = new_role
    user.save()
    return JsonResponse({'status': 'success', 'message': 'Роль успешно изменена.'})




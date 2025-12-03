from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from apps.users.models import CustomUser, UserRole, Department
from apps.forms.forms import login_form_data, registration_form_data
from apps.forms.form_checker import form_checker

def register(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if CustomUser.objects.filter(username=username).exists():
            errors.append({
                'text':'Пользователь с таким логином уже существует!',
                'desc': 'Кто-то уже занял этот логин, попробуйте добавить в конец 1 или написать логин как-то по другому.'})
        if password1 != password2:
            errors.append({
                'text': 'Пароли не совпадают!',
                'desc': 'Проверьте внимательней или нажмите на значок глаза чтобы сравнить пароли в открытом виде.'
            })
        if len(password1) < 8 or len(password2) < 8:
            errors.append({
                'text': 'Пароль слишком короткий!',
                'desc': 'Пароль и его повтор должны быть не короче 8 символов.'
            })
        if not errors:
            CustomUser.objects.create_user(
                username=username,
                password=password1,
                fullname=request.POST.get('fullname', ''),
                department=Department.objects.order_by('id')[int(request.POST.get('department', 0))],
                role=UserRole.USER
            )
            return redirect('login')

    data = form_checker(registration_form_data)
    data['_errors'] = errors
    return render(request, 'forms/form_builder.html', {'form_data': data})

def login_view(request):
    errors = []
    data = form_checker(login_form_data)
    data["_errors"] = errors
    return render(request, 'forms/form_builder.html', {"form_data": data})

def logout_view(request):
    logout(request)
    return redirect('/')

def change_role(request):
    username = request.POST['username']
    new_role = request.POST['role']
    user = CustomUser.objects.get(username=username)
    user.role = new_role
    user.save()
    return JsonResponse({'status': 'success', 'message': 'Роль успешно изменена.'})

def permission_denied_view(request):
    resp = render(request, 'users/403.html')
    return resp

def wnauthorized_view(request):
    resp = render(request, 'users/401.html')
    return resp

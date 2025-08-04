from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Form
from apps.users.models import CustomUser, UserRole

@login_required
def dashboard(request):
    forms_list = list(Form.objects.all().values())
    user_data = CustomUser.objects.get(username=request.user)
    users = CustomUser.objects.filter(department=user_data.department)
    roles = UserRole.choices
    
    return render(
        request, 'application/builder.html',
        {
            'variant': 'dashboard',
            'data': {'forms': forms_list, 'user': user_data, 'users': users, 'roles': roles}
        }
    )

@login_required
def form_manager(request):
    forms_list = list(Form.objects.all().values())
    
    return render(
        request, 'application/builder.html',
        {
            'variant': 'form_manager',
            'data': {'forms': forms_list}
        }
    )

@login_required
def demo_1(request):
    return render(request, 'application/test.html',)

@login_required
def demo_2(request):
    return render(request, 'application/test2.html',)

@login_required
def demo_3(request):
    return render(request, 'application/test3.html',)
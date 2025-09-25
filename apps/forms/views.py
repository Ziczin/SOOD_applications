from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import form_create_form_data
from .form_checker import form_checker

from .models import Field, FieldType, ServiceGroup, Service, Form

@login_required
def get_forms_by_user_department(request):
    dept = request.user.department
    qs = Form.objects.filter(department=dept, available=True)
    data = list(qs.values(
        'id', 'form_name'
    ))
    return JsonResponse({'forms': data})

@login_required
def get_service_groups_by_form_id(request):
    form_name = request.GET.get('form_name')
    groups = ServiceGroup.objects.filter(form_name=form_name)
    data = [
        {
            'name': g.name,
            'available': g.available
        }
        for g in groups
    ]
    return JsonResponse({'service_groups': data})

@login_required
def form_creation(request):
    errors = []
    if request.method == 'POST':
        form = request.POST
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'forms/form_builder.html', {'form': form_checker(form), 'errors': errors})

@login_required
def get_form_data(request):
    form_name = request.GET['form_name']
    form = Form.objects.get(form_name=form_name)

    # Получаем базу формы
    data = {
        'form': {
            'page_label': form.page_label,
            'form_label': form.form_label,
            'confirm_button_text': form.confirm_button_text,
            #'sub_button_link_text': 'Вернуться к списку форм',
            #'sub_button_link_route': '/applications/dashboard/',
        }
    }
    # Получаем поля и их типы
    data['field_types'] = [elem.name for elem in FieldType.objects.filter()] # type: ignore
    data['fields'] = [{ # type: ignore
        'label': field.label,
        'selected_type': field.type.name,
        'enum_tag': field.enum_tag
    } for field in Field.objects.filter(form=form)]

    # Получаем группы сервисов
    data['service_groups'] = {
        'selected': [elem.name for elem in ServiceGroup.objects.filter(form=form, available=True)],
        'available': [elem.name for elem in ServiceGroup.objects.filter(form=form)],
    }

    return JsonResponse(data)



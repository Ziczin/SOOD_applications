from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import form_create_form_data
from .form_builder import form_builder

from .models import Field, FieldType, Form
from application.models import ServiceGroup

form_create_form = form_builder(form_create_form_data)

@login_required
def form_creation(request):
    errors = []
    if request.method == 'POST':
        form = form_create_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = form_create_form()
    return render(request, 'forms/form_builder.html', {'form': form, 'errors': errors})

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
    data['fields'] = [{
            'label': field.label,
            'type': {
                'selected': field.type.name,
                'list': [elem.name for elem in FieldType.objects.filter()],
            },
            'enum_tag': field.enum_tag
        } for field in Field.objects.filter(form=form)]

    # Получаем группы сервисов
    data['service_groups'] = {
        'selected': [elem.name for elem in ServiceGroup.objects.filter(form=form, available=True)],
        'available': [elem.name for elem in ServiceGroup.objects.filter(form=form)],
    }

    return JsonResponse(data)

@login_required
def field_type_creation(request):
    pass

@login_required
def enum_tag_creation(request):
    pass

@login_required
def enum_elem_creation(request):
    pass

@login_required
def field_creation(request):
    pass



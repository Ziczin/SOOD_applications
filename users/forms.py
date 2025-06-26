from django.forms import PasswordInput as PassIn
from django.forms import TextInput as TextIn
from .models import CustomUser, Department
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm

builder_data = {
    'registration': {
        'form_object_name': 'RegistrationForm',
        'css': 'deps/css/style.css',
        'model': CustomUser,
        'parent': UserCreationForm,
        'title': 'Регистрация',
        'form_name': 'Регистрация',
        'btn_confirm': 'Зарегистрироваться',
        'sub_btn_link': '/auth/login',
        'sub_btn_link_text': 'Уже есть аккаунт? Войти',
        'fields': [
            {
                'id': 'username', 'type': TextIn,
                'label': 'Имя пользователя',
                'placeholder': 'Например IvanovAV',
            },
            {
                'id': 'password1', 'type': PassIn,
                'label': 'Пароль',
                'placeholder': 'Введите пароль',
            },
            {
                'id': 'password2', 'type': PassIn,
                'label': 'Повторите пароль',
                'placeholder': 'Введите пароль. Снова',
            },
            {
                'id': 'full_name', 'type': TextIn,
                'label': 'Полное имя',
                'placeholder': 'Например: Иванов Иван Иванович',
                'required': True,
            },
            {
                'id': 'department', 'type': [Department, ],
                'label': 'Выберите ваш отдел',
                'placeholder': 'Без отдела',
                'required': True,
            },
        ],
        'services': [
            {
                'count': int,
                'data': 
                {
                    'name': 'Наименование услуги',
                    'description': 'Описание услуги',
                    'price': 10
                }
            },
            {
                'count': int,
                'data': 
                {
                    'name': 'Наименование услуги2',
                    'description': 'Описание услуги2',
                    'some_field': int,
                    'some_field2': '<datetime>'
                }
            }
        ],
        'services_agregation': [
            {
                'label': 'К оплате',
                'field': 'price',
                'escape_null': None, # if skip, or <default value>
                'func': sum,
            },
        ],
    },
    'login': {
        'form_object_name': 'LoginForm',
        'css': 'deps/css/style.css',
        'model': CustomUser,
        'parent': ModelForm,
        'title': 'Вход',
        'form_name': 'Вход',
        'btn_confirm': 'Войти',
        'sub_btn_link': '/auth/register',
        'sub_btn_link_text': 'Нет аккаунта? Зарегистрироваться',
        'fields': [
            {
                'id': 'username', 'type': TextIn,
                'label': 'Имя пользователя',
                'placeholder': 'Введите логин',
            },
            {
                'id': 'password', 'type': PassIn,
                'label': 'Пароль',
                'placeholder': 'Введите пароль',
            },
        ]
    }
}


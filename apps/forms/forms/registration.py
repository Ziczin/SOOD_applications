from django.contrib.auth.forms import UserCreationForm

from apps.users.models import CustomUser, Department

from django.forms import PasswordInput
from django.forms import TextInput

registration_form_data = {
    'meta': {
        'name': 'Registration',
        'css': 'deps/css/bright.css',
        'model': CustomUser,
        'parent': UserCreationForm,
    },
    'form': {
        'page_title': 'Регистрация',
        'form_title': 'Регистрация',
        'btn_confirm': 'Зарегистрироваться',
        'sub_btn_link': '/users/login',
        'sub_btn_link_text': 'Уже есть аккаунт? Войти',
    },
    'fields': [
        {
            'id': 'username', 'type': TextInput,
            'label': 'Имя пользователя',
            'placeholder': 'Например IvanovAV',
        },
        {
            'id': 'password1', 'type': PasswordInput,
            'label': 'Пароль',
            'placeholder': 'Введите пароль',
        },
        {
            'id': 'password2', 'type': PasswordInput,
            'label': 'Повторите пароль',
            'placeholder': 'Введите пароль. Снова',
            'error_messages': {'password_mismatch': 'Gfhj'},
        },
        {
            'id': 'full_name', 'type': TextInput,
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
}

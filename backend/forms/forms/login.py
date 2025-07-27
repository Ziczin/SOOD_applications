from django.forms import ModelForm

from users.models import CustomUser

from django.forms import PasswordInput
from django.forms import TextInput

login_form_data = {
    'meta': {
        'name': 'Login',
        'css': 'deps/css/bright.css',
        'model': CustomUser,
        'parent': ModelForm,
    },
    'form': {
        'page_title': 'Вход',
        'form_title': 'Вход',
        'btn_confirm': 'Войти',
        'sub_btn_link': '/users/register',
        'sub_btn_link_text': 'Нет аккаунта? Зарегистрироваться',
    },
    'fields': [
        {
            'id': 'username', 'type': TextInput,
            'label': 'Имя пользователя',
            'placeholder': 'Например IvanovAV',
        },
        {
            'id': 'password', 'type': PasswordInput,
            'label': 'Пароль',
            'placeholder': 'Введите пароль',
        },
    ],
}

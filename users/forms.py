from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'department', 'full_name']

# form builders
registration_form_builder = {
    'css': 'deps/css/styles.css',
    'title': 'Регистрация',
    'name': 'Регистрация',
    'fields': [
        {
            'id':'username',
            'label':'Имя пользователя',
            'placeholder':'Например IvanovAV'
        },
        {
            'id':'password1',
            'type':'password',
            'label':'Пароль',
            'placeholder':''
        },
        {
            'id':'password2',
            'type':'password',
            'label':'Повторите пароль',
            'placeholder':''
        },
        {
            'id':'full_name',
            'label':'Ваше ФИО полностью',
            'placeholder':'Например: Иванов Иван Иванович'
        },
        {
            'id':'department',
            'label':'Введите ваше отделение',
            'placeholder':'Например ОГШ №1'
        },
        

    ],
    'confirm_btn_text': 'Зарегистрироваться',
    'redirect': {
        'text': 'Уже есть аккаунт? Войти',
        'route': "/auth/login"
    },
}

login_form_builder = {
    'css': 'deps/css/styles.css',
    'title': 'Вход',
    'name': 'Вход',
    'fields': [
        {
            'id':'username',
            'label':'Имя пользователя',
            'placeholder':'Введите имя пользователя'
        },
        {
            'id':'password',
            'type':'password',
            'label':'Пароль',
            'placeholder':'Введите пароль'
        }
    ],
    'confirm_btn_text': 'Войти',
    'redirect': {
        'text': 'Нет аккаунта? Зарегистрироваться',
        'route': "/auth/register"
    },
}

# add types to fields on form builders
for builder in (
    registration_form_builder,
    login_form_builder,
):
    for field in builder['fields']:
        if not 'type' in field:
            field['type'] = 'text'




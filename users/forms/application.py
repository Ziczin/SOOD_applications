from django.forms import ModelForm

from users.models import CustomUser, Department

from django.forms import Textarea
from django.forms import TextInput

application = {
    'meta': {
        'name': 'Application',
        'css': 'deps/css/style.css',
        'model': CustomUser,
        'parent': ModelForm,
    },
    'form': {
        'page_title': 'Заявка',
        'form_title': 'Заявка',
        'btn_confirm': 'Отправить',
        'sub_btn_link': '/auth/register',
        'sub_btn_link_text': 'Нет аккаунта? Зарегистрироваться',
    },
    'fields': [
        {
            'id': 'department', 'type': [Department, ],
            'label': 'Заявка: ',
        },
        {
            'id': 'office', 'type': TextInput,
            'label': 'Кабинет',
            'placeholder': 'Например: Каб. 535',
        },
        {
            'id': 'password', 'type': Textarea,
            'label': 'Описание заявки',
            'placeholder': '',
        },
    ],
}

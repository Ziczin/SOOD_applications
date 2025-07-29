from django.forms import ModelForm

from apps.forms.models import Form

from django.forms import Textarea
from django.forms import TextInput
from django.forms import HiddenInput

form_create_form_data = {
    'meta': {
        'name': 'Form_Creation',
        'css': 'deps/css/style.css',
        'model': Form,
        'parent': ModelForm,
    },
    'form': {
        'page_title': 'Создание формы',
        'form_title': 'Создание формы',
        'btn_confirm': 'Создать',
        'sub_btn_link': '/applications/dashboard',
        'sub_btn_link_text': 'Вернуться в аккаунт',
    },
    'fields': [
        {
            'id': 'department', 'type': HiddenInput,
            'label': 'Заявка:',
        },
        {
            'id': 'form_name', 'type': TextInput,
            'label': ': Имя формы:',
        },
        {
            'id': 'page_label', 'type': TextInput,
            'label': ': Заголовок страницы:',
        },
        {
            'id': 'form_label', 'type': TextInput,
            'label': ': Заголовок формы:',
        },
        {
            'id': 'confirm_button_text', 'type': TextInput,
            'label': ': Текст кнопки подтверждения:',
        },
    ],
}
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOOD_applications.settings')
django.setup()

from django.contrib.auth import get_user_model

from apps.users.models import Department, UserRole
from apps.forms.models import Enum, EnumTag, FieldType
from apps.application.models import Field, Form, Application, ApplicationField

from itertools import product

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='toster').exists():
        print("Создание суперюзера...")
        User.objects.create_superuser(username='toster', password='imposter', email='toster@example.com')

    super_user = User.objects.get(username='toster')
    super_user.fullname = 'SUPERUSER'
    super_user.role = UserRole.ADMIN
    super_user.verified = True
    super_user.proxy = True
    super_user.save()

    if not User.objects.filter(username='000').exists():
        print("Создание 2 суперюзера...")
        User.objects.create_superuser(username='000', password='000', email='000@example.com')

    super_user = User.objects.get(username='000')
    super_user.fullname = 'SUPERUSER'
    super_user.role = UserRole.ADMIN
    super_user.verified = True
    super_user.proxy = True
    super_user.save()

def on_test_setup():
    prog_dep, c = Department.objects.get_or_create(name='Отдел программирования')
    rem_dep, c = Department.objects.get_or_create(name='Отдел сетевой поддержки')

    User = get_user_model()
    users = [UserRole.USER, UserRole.MODERATOR, UserRole.ADMIN]
    deps = [prog_dep, rem_dep]
    usrs = [p for p in product(deps, users) for _ in range(3)]
    for i, us in enumerate(usrs):
        User.objects.create_user(
            username=str(i), password=str(i), fullname=str(i),
            department=us[0], role=us[1], verified=bool(i%2), proxy=i>3,
        ).save()
    
    print("-- Создание тэгов перечислений")
    obj1, c = EnumTag.objects.get_or_create(name='Принтер', department=rem_dep, shared=True)
    obj2, c = EnumTag.objects.get_or_create(name='Блюда')
    obj3, c = EnumTag.objects.get_or_create(name='Компьютеры', department=prog_dep)


    print("-- Создание элементов перечислений")
    Enum.objects.get_or_create(value='Принтер п-1', enum_tag=obj1)
    Enum.objects.get_or_create(value='Принтер Lenovo', enum_tag=obj1)
    Enum.objects.get_or_create(value='Мьясо', enum_tag=obj2)
    Enum.objects.get_or_create(value='Пирожки с пирожками', enum_tag=obj2)
    Enum.objects.get_or_create(value='OIDI-123', enum_tag=obj3)
    Enum.objects.get_or_create(value='UZI-1', enum_tag=obj3)
    Enum.objects.get_or_create(value='UZI-2', enum_tag=obj3)
    Enum.objects.get_or_create(value='kpo-866', enum_tag=obj3)

    print("-- Создание типов полей")
    type_names = [
        ('numeric', "Число", False),
        ('int', "Целое число", False),
        ('float', "Дробное число", False),
        ('text', "Строка", False),
        ('bigtext', "Текст", False),
        ('date', "Дата", False),
        ('time', "Время", False),
        ('enum', "Перечисление", True),
        ('phone', "Телефон", False),
    ]
    types = {tn[0]: FieldType.objects.get_or_create(name=tn[0], label=tn[1], allow_tags=tn[2])[0] for tn in type_names}

    print("-- Создание форм")
    form1, c = Form.objects.get_or_create(
        form_name='TestForm1',
        department=rem_dep,
        page_label='Test',
        form_label='Testovaya Forma',
        confirm_button_text='Confirm Button Text',
        sub_button_link_text='#',
        sub_button_link_route='#',
        )
    
    form2, c = Form.objects.get_or_create(
        form_name='Testovaya forma2',
        department=rem_dep,
        page_label='TestTestTest',
        form_label='ttt',
        confirm_button_text='Confirm Button Text',
        sub_button_link_text='#',
        sub_button_link_route='#',
        )
    
    print("-- Создание примеров полей")
    fields = [
        {"label": "Количество", "type": types['int']},
        {"label": "Новое количество", "type": types['int']},
        {"label": "Цена", "type": types['numeric']},
        {"label": "Стоимость", "type": types['numeric']},
        {"label": "Наименование", "type": types['text']},
        {"label": "Описание", "type": types['bigtext']},
        {"label": "Компьютер", "type": types['enum'], "tag": obj3},
        {"label": "Принтер", "type": types['enum'], "tag": obj1},
        {"label": "Технологические пирожки", "type": types['enum'], "tag": obj2},
    ]

    for i, f in enumerate(fields):
        Field.objects.get_or_create(**f, department=deps[i%2])

    print("-- Создание тестовой заявки")
    app, c = Application.objects.get_or_create(
        user=User.objects.get(username='toster'),
        form=form1,
    )

    ApplicationField.objects.get_or_create(
        application=app,
        field=Field.objects.get(label='Цена'),
        value='14.5',
    )

    ApplicationField.objects.get_or_create(
        application=app,
        field=Field.objects.get(label='Наименование'),
        value='Тестовое наименование',
    )

    print("База данных заполнена начальными данными!")

if __name__ == '__main__':
    on_test_setup()

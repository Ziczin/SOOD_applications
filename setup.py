import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOOD_applications.settings')
django.setup()

from django.contrib.auth import get_user_model

from apps.users.models import Department, UserRole
from apps.forms.models import Enum, EnumTag, FieldType
from apps.application.models import Field, Form

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

def on_test_setup():
    prog_dep, created = Department.objects.get_or_create(name='prog', label='Отдел программирования')
    rem_dep, created = Department.objects.get_or_create(name='net', label='Отдел сетевой поддержки')

    User = get_user_model()
    usrs = [
        [prog_dep, UserRole.USER],
        [prog_dep, UserRole.USER],
        [prog_dep, UserRole.MODERATOR],
        [prog_dep, UserRole.ADMIN],
        [rem_dep, UserRole.USER],
        [rem_dep, UserRole.ADMIN],
    ]
    for i, us in enumerate(usrs):
        User.objects.create_user(
            username=str(i), password=str(i), fullname=str(i),
            department=us[0], role=us[1], verified=bool(i), proxy=i>3,
        ).save()
    
    print("-- Создание тэгов перечислений")
    obj1, created = EnumTag.objects.get_or_create(name='Принтер')
    obj2, created = EnumTag.objects.get_or_create(name='Блюда')

    print("-- Создание элементов перечислений")
    Enum.objects.get_or_create(value='Принтер п-1', enum_tag=obj1)
    Enum.objects.get_or_create(value='Принтер Lenovo', enum_tag=obj1)
    Enum.objects.get_or_create(value='Мьясо', enum_tag=obj2)
    Enum.objects.get_or_create(value='Пирожки с пирожками', enum_tag=obj2)

    print("-- Создание типов полей")
    t1, created = FieldType.objects.get_or_create(name='Int')
    t2, created = FieldType.objects.get_or_create(name='Float')
    t3, created = FieldType.objects.get_or_create(name='Str')
    t4, created = FieldType.objects.get_or_create(name='Enum')

    print("-- Создание форм")
    form1, created = Form.objects.get_or_create(
        form_name='TestForm1',
        department=rem_dep,
        page_label='Test',
        form_label='Testovaya Forma',
        confirm_button_text='Confirm Button Text',
        sub_button_link_text='#',
        sub_button_link_route='#',
        )
    
    print("-- Создание примеров полей")
    f1, created = Field.objects.get_or_create(label='Количество', type=t1, form=form1)
    f2, created = Field.objects.get_or_create(label='Новое количество', type=t1)
    f3, created = Field.objects.get_or_create(label='Цена', type=t2, form=form1)
    f4, created = Field.objects.get_or_create(label='Стоимость', type=t2)
    f5, created = Field.objects.get_or_create(label='Наименование', type=t3, form=form1)
    f6, created = Field.objects.get_or_create(label='Описание', type=t3, form=form1)
    f7, created = Field.objects.get_or_create(label='Отдел', type=t4, enum_tag=obj1)
    f8, created = Field.objects.get_or_create(label='Имя принтера', type=t4, enum_tag=obj2)

    print("База данных заполнена начальными данными!")

if __name__ == '__main__':
    on_test_setup()

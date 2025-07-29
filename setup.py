import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOOD_applications.settings')
django.setup()

from django.contrib.auth import get_user_model
# from django.forms import ModelForm

from apps.users.models import Department, UserRole # CustomUser
# from apps.application.models import Application, ApplicationField, ApplicationService
from apps.forms.models import Enum, EnumTag, FieldType
from apps.application.models import Field, Form
# from apps.application.models import Service, ServiceValue


def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='toster').exists():
        print("Создание суперюзера...")
        User.objects.create_superuser(username='toster', password='imposter', email='toster@example.com')

    super_user = User.objects.get(username='toster')
    super_user.full_name = 'SUPERUSER'
    super_user.role = UserRole.ADMIN
    super_user.save()

def on_test_setup():
    user_department, created = Department.objects.get_or_create(name='User')
    remont_department, created = Department.objects.get_or_create(name='Remont')

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
        department=remont_department,
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

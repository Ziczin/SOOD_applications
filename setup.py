import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.forms import ModelForm

from users.models import CustomUser, Department
from application.models import Application, ApplicationField, ApplicationService
from forms.models import Enum, EnumTag, FieldType
from application.models import Field, Form
from application.models import Service, ServiceValue

def create_superuser_and_populate():
    User = get_user_model()
    
    user_department, created = Department.objects.get_or_create(name='User')
    remont_department, created = Department.objects.get_or_create(name='Remont')

    if not User.objects.filter(username='toster').exists():
        print("Создание суперюзера...")
        User.objects.create_superuser(username='toster', password='imposter', email='toster@example.com')
    
    print("Загрузка предустановленных значений...")

    CustomUser.objects.get_or_create(
        username='testuser',
        password='test',
        full_name='test simple user',
        department=user_department,
    )
    CustomUser.objects.get_or_create(
        username='testremont',
        password='test',
        full_name='test remont manager',
        department=remont_department,
    )
        
    obj1, created = EnumTag.objects.get_or_create(name='Принтер')
    obj2, created = EnumTag.objects.get_or_create(name='Блюда')

    Enum.objects.get_or_create(value='Принтер п-1', enum_tag=obj1)
    Enum.objects.get_or_create(value='Принтер Lenovo', enum_tag=obj1)
    Enum.objects.get_or_create(value='Мьясо', enum_tag=obj2)
    Enum.objects.get_or_create(value='Пирожки с пирожками', enum_tag=obj2)

    t1, created = FieldType.objects.get_or_create(name='Int')
    t2, created = FieldType.objects.get_or_create(name='Float')
    t3, created = FieldType.objects.get_or_create(name='Str')
    t4, created = FieldType.objects.get_or_create(name='Enum')

    f1, created = Field.objects.get_or_create(label='Количество', field_type=t1)
    f2, created = Field.objects.get_or_create(label='Новое количество', field_type=t1)
    f3, created = Field.objects.get_or_create(label='Цена', field_type=t2)
    f4, created = Field.objects.get_or_create(label='Стоимость', field_type=t2)
    f5, created = Field.objects.get_or_create(label='Наименование', field_type=t3)
    f6, created = Field.objects.get_or_create(label='Описание', field_type=t3)
    f7, created = Field.objects.get_or_create(label='Отдел', field_type=t4, enum_tag=obj1)
    f8, created = Field.objects.get_or_create(label='Имя принтера', field_type=t4, enum_tag=obj2)

    form1, created = Form.objects.get_or_create(
        form_name='TestForm1',
        department=remont_department,
        page_label='Test',
        form_label='Testovaya Forma',
        confirm_button_text='Confirm Button Text',
        sub_button_link_text='#',
        sub_button_link_route='#',
        )

    print("База данных заполнена начальными данными.")

if __name__ == '__main__':
    create_superuser_and_populate()

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import CustomUser, Department

def create_superuser_and_populate():
    User = get_user_model()
    
    user_department, created = Department.objects.get_or_create(name='User')
    kitchen_department, created = Department.objects.get_or_create(name='Kitchen')

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
        username='testkitchen',
        password='test',
        full_name='test kitchen manager',
        department=kitchen_department,
    )
        
    print("База данных заполнена начальными данными.")

if __name__ == '__main__':
    create_superuser_and_populate()

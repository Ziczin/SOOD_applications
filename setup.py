import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import CustomUser, Service

def create_superuser_and_populate():
    User = get_user_model()
    
    user_service, created = Service.objects.get_or_create(name='User')
    kitchen_service, created = Service.objects.get_or_create(name='Kitchen')

    if not User.objects.filter(username='toster').exists():
        print("Создание суперюзера...")
        User.objects.create_superuser(username='toster', password='imposter', email='toster@example.com')
    
    print("Загрузка предустановленных значений...")

    CustomUser.objects.get_or_create(
        username='testuser',
        password='test',
        department='user',
        full_name='test simple user',
        service=user_service,
    )
    CustomUser.objects.get_or_create(
        username='testkitchen',
        password='test',
        department='kitchen',
        full_name='test kitchen manager',
        service=kitchen_service,
    )
        
    print("База данных заполнена начальными данными.")

if __name__ == '__main__':
    create_superuser_and_populate()

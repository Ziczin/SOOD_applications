import os
import django

# Установите настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import CustomUser

def create_superuser_and_populate():
    

    User = get_user_model()
    
    if not User.objects.filter(username='toster').exists():
        print("Загрузка предустановленных значений...")
        User.objects.create_superuser(username='toster', password='imposter', email='toster@example.com')
        CustomUser.objects.create(
            username='testuser',
            password='test',
            department='user',
            full_name='test simple user',
            role='user',
            )
        CustomUser.objects.create(
            username='testkitchen',
            password='test',
            department='kitchen',
            full_name='test kitchen manager',
            role='kitchen',
            )
        print("База данных заполнена начальными данными.")
        
if __name__ == '__main__':
    create_superuser_and_populate()

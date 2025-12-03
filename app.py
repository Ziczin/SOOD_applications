import os
import sys
import glob
import argparse
from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

from setup import create_field_types

def setup_django():
    """Настраивает окружение Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOOD_applications.settings')
    sys.path.insert(0, os.getcwd())
    try:
        import django
        django.setup()
    except ImportError as e:
        raise ImportError(f"Не удалось настроить Django. Проверьте структуру проекта.\n{e}")

def remove_migrations():
    """Удаляет все файлы миграций, кроме __init__.py."""
    for migrations_dir in glob.glob('**/migrations', recursive=True):
        for file in glob.glob(os.path.join(migrations_dir, '*.py')):
            if os.path.basename(file) != '__init__.py':
                os.remove(file)
                print(f"Удалён: {file}")

def reset_database():
    """Сбрасывает базу данных в зависимости от типа."""
    if not settings.configured:
        setup_django()
    
    db_engine = settings.DATABASES['default']['ENGINE']
    db_name = settings.DATABASES['default']['NAME']
    
    # Для SQLite
    if db_engine == 'django.db.backends.sqlite3':
        if os.path.exists(db_name):
            try:
                os.remove(db_name)
                print(f"Удалена SQLite база: {db_name}")
            except PermissionError:
                print(f"Ошибка: Нет прав для удаления {db_name}")
    
    # Для MSSQL и других баз данных
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute("exec dropall")
                print("Выполнена процедура dropall")
        except Exception as e:
            print(f"Ошибка при выполнении dropall: {e}")

def main():
    parser = argparse.ArgumentParser(description='Управление Django проектом')
    parser.add_argument('--reset', action='store_true', help='Полный сброс миграций и БД и установка базовых значений')
    parser.add_argument('--model-recover', action='store_true', help='Полный сброс миграций и БД')
    parser.add_argument('--run', action='store_true', help='Запустить сервер разработки')
    parser.add_argument('--apps-10000', action='store_true', help='Вбить в сервис 10000 заявок')
    parser.add_argument('--flush', action='store_true', help='Только создать суперюзера и выйти')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    setup_django()

    from setup import on_test_setup, create_superuser

    from setup import on_test_setup, create_superuser
    if args.reset or args.model_recover or args.flush:
        print("\n=== ПОЧИНКА БАЗЫ ===")
        remove_migrations()
        reset_database()
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        create_superuser()
        create_field_types()
        if args.flush: return

        if args.reset:
            print("Загрузка предустановленных значений...")
            on_test_setup(args.apps_10000)
        print("=== БАЗА ПОЧИНЕНА ===\n")

    if args.run:
        print("\n=== ЗАПУСК СЕРВЕРА РАЗРАБОТКИ ===")
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5051'])

if __name__ == '__main__':
    main()
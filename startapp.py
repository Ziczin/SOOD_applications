import subprocess
import os
import sys
import signal
import argparse
import shutil
import socket
import time
from threading import Thread
from queue import Queue, Empty

project_dir = os.path.dirname(os.path.abspath(__file__))

class ProcessMonitor(Thread):
    """Мониторинг вывода процессов в реальном времени с улучшенной поддержкой кодировок"""
    def __init__(self, process, name):
        super().__init__(daemon=True)
        self.process = process
        self.name = name
        self.output = Queue()
        
    def run(self):
        while True:
            raw_line = self.process.stdout.readline()
            if not raw_line:
                break
            
            # Пробуем разные кодировки
            decoded = None
            for encoding in ['utf-8', 'cp1251', 'cp866', sys.getfilesystemencoding()]:
                try:
                    decoded = raw_line.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if decoded is None:
                decoded = raw_line.decode('utf-8', errors='replace')
            
            self.output.put(f"[{self.name}] {decoded.strip()}")
            sys.stdout.write(f"[{self.name}] {decoded}")
            sys.stdout.flush()
            
    def get_output(self):
        lines = []
        while True:
            try:
                lines.append(self.output.get_nowait())
            except Empty:
                break
        return "\n".join(lines)

def run_nginx(prod_mode=False):
    """Запускает Nginx с правильной конфигурацией"""
    nginx_dir = os.path.join(project_dir, 'nginx')
    nginx_exe = os.path.join(nginx_dir, 'nginx.exe')
    
    if not os.path.exists(nginx_exe):
        print(f"❌ Ошибка: nginx.exe не найден в {nginx_dir}")
        print("👉 Скачайте nginx для Windows: https://nginx.org/en/download.html")
        print(f"👉 Распакуйте в папку: {nginx_dir}")
        return None

    # Останавливаем предыдущий экземпляр Nginx
    stop_nginx()
    
    # Генерируем конфиг
    conf_content = generate_nginx_conf(prod_mode)
    conf_path = os.path.join(nginx_dir, 'generated.conf')
    with open(conf_path, 'w', encoding='utf-8') as f:
        f.write(conf_content)
    
    # Запускаем процесс
    try:
        proc = subprocess.Popen(
            [nginx_exe, '-c', conf_path],
            cwd=nginx_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )
        print(f"🚀 Nginx запущен с конфигом: {conf_path}")
        return proc
    except Exception as e:
        print(f"❌ Ошибка запуска Nginx: {e}")
        return None

def generate_nginx_conf(prod_mode=False):
    """Упрощённый и надёжный конфиг Nginx"""
    django_static = os.path.join(project_dir, 'backend', 'staticfiles').replace('\\', '/')
    react_static = os.path.join(project_dir, 'backend', 'static').replace('\\', '/')
    log_dir = os.path.join(project_dir, 'nginx', 'logs').replace('\\', '/')
    
    if prod_mode:
        return f"""
worker_processes 1;

events {{
    worker_connections 1024;
}}

http {{
    include       mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    keepalive_timeout 65;
    server_tokens off;
    
    access_log {log_dir}/access.log;
    error_log {log_dir}/error.log;

    server {{
        listen 80;
        server_name _;
        
        # Статика Django (все файлы из staticfiles)
        location /static/ {{
            alias {django_static}/;
            expires 30d;
        }}
        
        # Статика React (из отдельной папки)
        location /sood-applications/ {{
            alias {react_static}/;
            expires 30d;
        }}

        # Все остальные запросы - в Django
        location / {{
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
"""
    else:
        return f"""
worker_processes 1;

events {{
    worker_connections 1024;
}}

http {{
    include       mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    keepalive_timeout 65;
    server_tokens off;
    
    access_log {log_dir}/access.log;
    error_log {log_dir}/error.log;

    server {{
        listen 80;
        server_name _;
        
        # Статика Django (все файлы)
        location /static/ {{
            proxy_pass http://localhost:8000/static/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }}

        # API Django
        location /api/ {{
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}

        # Все остальные запросы - в React
        location / {{
            proxy_pass http://localhost:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }}
    }}
}}
"""

def stop_nginx():
    """Останавливает Nginx"""
    nginx_dir = os.path.join(project_dir, 'nginx')
    nginx_exe = os.path.join(nginx_dir, 'nginx.exe')
    
    if os.path.exists(nginx_exe):
        try:
            subprocess.run(
                [nginx_exe, '-s', 'stop'],
                cwd=nginx_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("🛑 Nginx остановлен")
        except Exception as e:
            print(f"⚠️ Ошибка при остановке Nginx: {e}")

def run_frontend():
    """Запускает React-приложение"""
    frontend_dir = os.path.join(project_dir, 'frontend')
    try:
        # Для корректного отображения русского текста в выводе
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['NODE_ENV'] = 'development'
        
        proc = subprocess.Popen(
            'npm start',
            cwd=frontend_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            env=env
        )
        print("🚀 React приложение запущено")
        return proc
    except Exception as e:
        print(f"❌ Ошибка запуска React: {e}")
        return None

def build_frontend():
    """Собирает React-приложение"""
    frontend_dir = os.path.join(project_dir, 'frontend')
    print("🔧 Сборка React-приложения...")
    
    try:
        # Устанавливаем переменные окружения для корректной сборки
        env = os.environ.copy()
        env['PUBLIC_URL'] = './'
        env['GENERATE_SOURCEMAP'] = 'false'
        
        proc = subprocess.Popen(
            'npm run build',
            cwd=frontend_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            env=env
        )
        
        # Мониторинг вывода в реальном времени
        while True:
            output = proc.stdout.readline()
            if not output and proc.poll() is not None:
                break
            if output:
                decoded = None
                for encoding in ['utf-8', 'cp1251', 'cp866']:
                    try:
                        decoded = output.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if decoded is None:
                    decoded = output.decode('utf-8', errors='replace')
                
                sys.stdout.write(decoded)
                sys.stdout.flush()
        
        if proc.returncode == 0:
            print("✅ React-приложение успешно собрано")
            
            # Копируем сборку
            build_dir = os.path.join(frontend_dir, 'build')
            static_dir = os.path.join(project_dir, 'backend', 'static')
            
            # Очищаем папку
            if os.path.exists(static_dir):
                shutil.rmtree(static_dir)
            shutil.copytree(build_dir, static_dir)
            print(f"📁 Сборка скопирована в {static_dir}")
            return True
        else:
            print("❌ Ошибка сборки React!")
            return False
    except Exception as e:
        print(f"❌ Ошибка при сборке React: {e}")
        return False

def run_backend(flush=False):
    """Запускает Django-сервер"""
    backend_dir = os.path.join(project_dir, 'backend')
    cmd = [sys.executable, 'run.py']
    
    if flush:
        cmd.append('--flush')
    
    try:
        # Для корректного отображения русского текста
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        proc = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            env=env
        )
        print("🚀 Django сервер запущен")
        return proc
    except Exception as e:
        print(f"❌ Ошибка запуска Django: {e}")
        return None

def build_backend():
    """Выполняет collectstatic для Django"""
    backend_dir = os.path.join(project_dir, 'backend')
    print("🔧 Сборка Django (collectstatic)...")
    
    try:
        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        proc = subprocess.Popen(
            [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            env=env
        )
        
        # Мониторинг вывода в реальном времени
        while True:
            output = proc.stdout.readline()
            if not output and proc.poll() is not None:
                break
            if output:
                decoded = None
                for encoding in ['utf-8', 'cp1251', 'cp866']:
                    try:
                        decoded = output.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if decoded is None:
                    decoded = output.decode('utf-8', errors='replace')
                
                sys.stdout.write(decoded)
                sys.stdout.flush()
        
        if proc.returncode == 0:
            print("✅ Django collectstatic выполнен успешно")
            return True
        else:
            print("❌ Ошибка collectstatic!")
            return False
    except Exception as e:
        print(f"❌ Ошибка при выполнении collectstatic: {e}")
        return False

def terminate_process(proc, name):
    """Безопасное завершение процесса"""
    if proc and proc.poll() is None:
        try:
            if os.name == 'nt':
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                proc.terminate()
            
            try:
                proc.wait(timeout=5)
                print(f"🛑 {name} остановлен")
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"⚠️ {name} принудительно завершен")
        except Exception as e:
            print(f"⚠️ Ошибка при остановке {name}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Запуск Django + React + Nginx")
    parser.add_argument('--flush', action='store_true', help='Сброс миграций и базы данных')
    parser.add_argument('--prod', action='store_true', help='Production режим (сборка React)')
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOOD_applications.settings')
    
    # Останавливаем все предыдущие процессы
    stop_nginx()
    
    nginx_proc = None
    frontend_proc = None
    backend_proc = None
    monitors = []
    
    try:
        # Production режим: сборка приложений
        if args.prod:
            print("🏗️  Запуск в PRODUCTION режиме")
            if not build_frontend():
                print("❌ Сборка фронтенда не удалась, выход")
                sys.exit(1)
                
            if not build_backend():
                print("⚠️ Ошибка collectstatic, продолжение без статики")
        else:
            print("👨‍💻 Запуск в DEVELOPMENT режиме")
        
        # Запуск Nginx
        nginx_proc = run_nginx(args.prod)
        if not nginx_proc:
            print("❌ Не удалось запустить Nginx, выход")
            sys.exit(1)
            
        # Мониторинг вывода Nginx
        nginx_monitor = ProcessMonitor(nginx_proc, "NGINX")
        nginx_monitor.start()
        monitors.append(nginx_monitor)
        
        # Запуск React (только в development режиме)
        if not args.prod:
            frontend_proc = run_frontend()
            if frontend_proc:
                frontend_monitor = ProcessMonitor(frontend_proc, "REACT")
                frontend_monitor.start()
                monitors.append(frontend_monitor)
            else:
                print("❌ Не удалось запустить React, выход")
                sys.exit(1)
        
        # Запуск Django
        backend_proc = run_backend(args.flush)
        if backend_proc:
            backend_monitor = ProcessMonitor(backend_proc, "DJANGO")
            backend_monitor.start()
            monitors.append(backend_monitor)
        else:
            print("❌ Не удалось запустить Django, выход")
            sys.exit(1)
        
        # Ожидание завершения основного процесса (Django)
        backend_proc.wait()
        print("\n🔚 Django процесс завершен")
        
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал Ctrl+C, остановка приложений...")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        # Остановка процессов в правильном порядке
        if frontend_proc:
            terminate_process(frontend_proc, "React")
        
        if backend_proc:
            terminate_process(backend_proc, "Django")
        
        stop_nginx()
        
        # Сбор диагностики
        print("\n📋 Диагностическая информация:")
        if monitors:
            print("\nПоследние сообщения процессов:")
            for monitor in monitors:
                print(f"\n{monitor.name}:\n{monitor.get_output()}")
        
        print("\n✅ Все процессы остановлены. Выход.")
        sys.exit(0)
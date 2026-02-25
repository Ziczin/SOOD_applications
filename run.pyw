import subprocess
import pystray
from PIL import Image, ImageDraw, ImageFont
import sys
import os
import threading
import time
import psutil

img = Image.new('RGB', (64, 64), 'green')
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arialbd.ttf", 50)
except:
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()

draw.text((10, 5), 'D', fill='white', font=font)

# Глобальная переменная для хранения процесса
proc = None

def is_process_alive(pid):
    """Проверяет, существует ли процесс с заданным PID"""
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

def start_process():
    """Запуск процесса waitress-serve"""
    global proc
    try:
        # Используем subprocess.Popen без shell=True для лучшего контроля
        proc = subprocess.Popen(
            ['waitress-serve', '--listen=0.0.0.0:5051', 'SOOD_applications.wsgi:application'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        )
        print(f"Сервис запущен с PID: {proc.pid}")
        # Запускаем поток для отслеживания вывода
        threading.Thread(target=monitor_output, args=(proc,), daemon=True).start()
    except Exception as e:
        print(f"Ошибка при запуске сервиса: {e}")

def monitor_output(process):
    """Мониторинг вывода процесса"""
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        # Проверяем stderr после завершения stdout
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"STDERR: {stderr_output}")
    except Exception as e:
        print(f"Ошибка при мониторинге вывода: {e}")

def stop_process():
    """Остановка процесса waitress-serve"""
    global proc
    if proc is not None:
        try:
            # Сначала проверяем, жив ли процесс
            if proc.poll() is None:  # Процесс все еще работает
                print(f"Останавливаем процесс с PID: {proc.pid}")
                
                # Для Windows используем специальный флаг
                if sys.platform == "win32":
                    import ctypes
                    ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, proc.pid)
                else:
                    proc.terminate()  # SIGTERM для Unix
                
                # Ждем завершения
                try:
                    proc.wait(timeout=5)
                    print("Процесс корректно завершен")
                except subprocess.TimeoutExpired:
                    print("Процесс не завершился вовремя, принудительная остановка...")
                    proc.kill()  # SIGKILL для Unix
                    proc.wait()
                    print("Процесс принудительно завершен")
                
                # Дополнительная проверка через psutil
                try:
                    if is_process_alive(proc.pid):
                        print(f"Процесс {proc.pid} все еще жив, завершаем...")
                        parent = psutil.Process(proc.pid)
                        # Завершаем дочерние процессы
                        for child in parent.children(recursive=True):
                            try:
                                child.terminate()
                            except:
                                pass
                        # Завершаем родительский процесс
                        parent.terminate()
                        gone, alive = psutil.wait_procs([parent], timeout=3)
                        for p in alive:
                            p.kill()
                except:
                    pass
            else:
                print("Процесс уже завершился самостоятельно")
        except Exception as e:
            print(f"Ошибка при остановке сервиса: {str(e)}")
        finally:
            proc = None

def restart_action(icon, item):
    """Действие при перезагрузке"""
    print("Перезагрузка сервиса...")
    stop_process()
    time.sleep(2)  # Увеличиваем задержку перед запуском
    start_process()
    print("Сервис перезапущен")

def exit_action(icon, item):
    """Действие при выходе"""
    stop_process()
    icon.stop()
    sys.exit(0)

# Запускаем процесс при старте
start_process()

icon = pystray.Icon(
    'SOOD Applications Service',
    img,
    'SOOD Applications Service',
    menu=pystray.Menu(
        pystray.MenuItem('Перезагрузить', restart_action),
        pystray.MenuItem('Выход', exit_action)
    )
)

# Запускаем иконку в трее в отдельном потоке
if __name__ == '__main__':
    try:
        print("Сервис запущен. Иконка в трее активна.")
        print("Для выхода используйте меню иконки в трее.")
        icon.run()
    except KeyboardInterrupt:
        print("\nПолучен сигнал прерывания...")
        exit_action(None, None)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        exit_action(None, None)
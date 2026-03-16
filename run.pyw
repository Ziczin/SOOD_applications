import subprocess
import pystray
from PIL import Image, ImageDraw, ImageFont
import sys
import os
import threading
import time
import psutil
import signal

# Скрываем консоль на Windows
if sys.platform == "win32":
    import ctypes
    wh = ctypes.windll.kernel32.GetConsoleWindow()
    if wh:
        ctypes.windll.user32.ShowWindow(wh, 0)  # 0 = SW_HIDE

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

# Глобальные переменные
proc = None

def kill_process_tree(pid):
    """Убивает процесс и все его дочерние процессы"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Сначала завершаем дочерние процессы
        for child in children:
            try:
                child.terminate()
            except:
                pass
        
        # Ждем завершения дочерних процессов
        gone, alive = psutil.wait_procs(children, timeout=3)
        
        # Принудительно завершаем оставшиеся
        for p in alive:
            try:
                p.kill()
            except:
                pass
        
        # Завершаем родительский процесс
        try:
            parent.terminate()
            parent.wait(timeout=3)
        except:
            try:
                parent.kill()
            except:
                pass
    except:
        pass

def find_waitress_processes():
    """Находит все процессы waitress-serve"""
    waitress_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = proc.cmdline()
                if any('waitress-serve' in cmd for cmd in cmdline):
                    waitress_processes.append(proc)
        except:
            pass
    return waitress_processes

def start_process():
    """Запуск процесса waitress-serve"""
    global proc
    try:
        # Запускаем процесс с подавлением вывода
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
        
        proc = subprocess.Popen(
            ['waitress-serve', '--listen=0.0.0.0:5051', 'SOOD_applications.wsgi:application'],
            stdout=subprocess.DEVNULL,   # Подавляем stdout
            stderr=subprocess.DEVNULL,   # Подавляем stderr
            stdin=subprocess.DEVNULL,    # Подавляем stdin
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            # Не используем shell=True
        )
    except Exception as e:
        # Ничего не выводим в консоль
        pass

def stop_process():
    """Остановка процесса waitress-serve и всех его потомков"""
    global proc
    
    # Останавливаем основной процесс
    if proc is not None:
        try:
            if proc.poll() is None:
                kill_process_tree(proc.pid)
        except:
            pass
        finally:
            proc = None
    
    # Ищем и завершаем все оставшиеся процессы waitress
    waitress_processes = find_waitress_processes()
    for wp in waitress_processes:
        try:
            kill_process_tree(wp.pid)
        except:
            pass

def restart_action(icon, item):
    """Действие при перезагрузке"""
    stop_process()
    time.sleep(2)
    start_process()

def exit_action(icon, item):
    """Действие при выходе"""
    stop_process()
    icon.stop()
    sys.exit(0)

# Запускаем процесс при старте
start_process()

# Создаем иконку в трее
icon = pystray.Icon(
    'SOOD Applications Service',
    img,
    'SOOD Applications Service',
    menu=pystray.Menu(
        pystray.MenuItem('Перезагрузить', restart_action),
        pystray.MenuItem('Выход', exit_action)
    )
)

# Запускаем без консоли
if __name__ == '__main__':
    try:
        icon.run()
    except:
        try:
            stop_process()
        except:
            pass
        sys.exit(0)
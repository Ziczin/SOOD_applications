import subprocess
import os
import sys
import signal

project_dir = os.path.dirname(os.path.abspath(__file__))

def run_frontend():
    frontend_dir = os.path.join(project_dir, 'frontend')
    return subprocess.Popen(
        'npm start',
        cwd=frontend_dir,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr
    )

def run_backend():
    backend_dir = os.path.join(project_dir, 'backend')
    return subprocess.Popen(
        [sys.executable, 'run.py'],
        cwd=backend_dir,
        stdout=sys.stdout,
        stderr=sys.stderr
    )

if __name__ == '__main__':
    try:
        frontend_proc = run_frontend()
        backend_proc = run_backend()
        frontend_proc.wait()
        backend_proc.wait()
    except KeyboardInterrupt:
        print('\nОстановка приложений по Ctrl+C...')
        for p in (frontend_proc, backend_proc):
            if p.poll() is None:
                try:
                    p.send_signal(signal.CTRL_BREAK_EVENT if os.name == 'nt' else signal.SIGTERM)
                except Exception:
                    p.terminate()
        sys.exit(0)

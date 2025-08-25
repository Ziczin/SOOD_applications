import os
import sys
import pyperclip  # Добавлен импорт для работы с буфером обмена

def collect_files(start_path, file_list):
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return
    for entry in entries:
        path = os.path.join(start_path, entry)
        if os.path.isdir(path):
            collect_files(path, file_list)
        elif entry.lower().endswith(('.js', '.css', '.py', '.html')):  # Регистронезависимая проверка расширений
            file_list.append(path)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = []
    collect_files(script_dir, files)
    
    clipboard_content = []
    for i, file_path in enumerate(files):
        if i > 0:
            clipboard_content.append('\n\n')  # Два переноса между файлами
        
        rel_path = os.path.relpath(file_path, script_dir)
        clipboard_content.append(f"{rel_path}\n")  # Относительный путь с переносом
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                clipboard_content.append(f.read())
        except Exception as e:
            error_msg = f"Ошибка чтения файла: {str(e)}"
            sys.stderr.write(error_msg + '\n')
            clipboard_content.append(error_msg)
    
    # Копируем собранный контент в буфер обмена
    pyperclip.copy(''.join(clipboard_content))
    print("Содержимое файлов скопировано в буфер обмена.")

if __name__ == "__main__":
    main()
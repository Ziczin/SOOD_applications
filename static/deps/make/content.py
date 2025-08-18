import os
import sys

def collect_js_files(start_path, file_list):
    """Рекурсивно собирает .js файлы в список."""
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return
    for entry in entries:
        path = os.path.join(start_path, entry)
        if os.path.isdir(path):
            collect_js_files(path, file_list)
        elif entry.endswith('.js') or entry.endswith('.css'):
            file_list.append(path)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    js_files = []
    collect_js_files(script_dir, js_files)
    js_files.sort()  # Сортируем файлы в алфавитном порядке
    
    with open('content.txt', 'w', encoding='utf-8') as output_file:
        for i, file_path in enumerate(js_files):
            # Пустая строка между файлами (кроме первого)
            if i > 0:
                output_file.write('\n')
                output_file.write('\n')
            
            # Записываем относительный путь
            rel_path = os.path.relpath(file_path, script_dir)
            output_file.write(rel_path + '\n')
            
            # Записываем содержимое файла
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    output_file.write(f.read())
            except Exception as e:
                error_msg = f"Ошибка чтения файла: {str(e)}"
                sys.stderr.write(error_msg + '\n')
                output_file.write(error_msg + '\n')

if __name__ == "__main__":
    main()

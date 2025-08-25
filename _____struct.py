import os
import json
import pyperclip

def get_file_structure(start_path):
    file_structure = {}
    allowed_extensions = ['.py', '.js', '.css', '.json']
    
    for root, dirs, files in os.walk(start_path):
        # Исключаем ненужные директории
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
        
        relative_path = os.path.relpath(root, start_path)
        if relative_path == '.':
            relative_path = ''
        
        # Фильтруем файлы по расширению с учетом регистра
        filtered_files = [
            f for f in files 
            if os.path.splitext(f)[1].lower() in allowed_extensions
        ]
        
        file_structure[relative_path] = filtered_files
    
    return file_structure

def main():
    start_path = os.path.dirname(os.path.abspath(__file__))
    file_structure = get_file_structure(start_path)
    json_structure = json.dumps(file_structure, indent=4)
    pyperclip.copy(json_structure)
    print("Структура файлов скопирована в буфер обмена.")

if __name__ == "__main__":
    main()
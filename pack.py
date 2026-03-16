import os
import zipfile
import sys
from pathlib import Path

def create_pack_archive(items_to_pack, output_filename='pack.zip', folder_in_archive='SOOD_applications'):
    if not items_to_pack:
        print("Ошибка: Список файлов для упаковки пуст!")
        return False
    
    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item_path in items_to_pack:
                path = Path(item_path)
                
                if not path.exists():
                    print(f"Предупреждение: {item_path} не найден, пропускаем...")
                    continue
                
                print(f"Добавляем: {item_path}")
                
                if path.is_file():
                    arcname = f"{folder_in_archive}/{path.name}"
                    zipf.write(path, arcname)
                    
                elif path.is_dir():
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = Path(root) / file
                            rel_path = file_path.relative_to(path.parent)
                            arcname = f"{folder_in_archive}/{rel_path}"
                            zipf.write(file_path, arcname)
                
        print(f"\nАрхив успешно создан: {output_filename}")
        print(f"Файлы помещены в папку: {folder_in_archive}")
        
        archive_size = os.path.getsize(output_filename)
        print(f"Размер архива: {archive_size:,} байт ({archive_size/1024/1024:.2f} МБ)")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при создании архива: {e}")
        return False

def main():
    items_to_pack = [
        "apps",
        "files",
        "media",
        "SOOD_applications",
        "static",
        "__init__.py",
        "app.py",
        "run.py",
        "run.pyw",
        "manage.py",
        "setup.py",
        "requirements.txt"
    ]
    
    output_archive = "SOOD_applications.zip"
    folder_in_archive = "SOOD_applications"
    
    print("=" * 50)
    print("Упаковщик файлов в ZIP архив")
    print("=" * 50)
    
    success = create_pack_archive(items_to_pack, output_archive, folder_in_archive)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
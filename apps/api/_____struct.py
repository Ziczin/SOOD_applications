import os
import pyperclip


def get_file_structure_with_content(start_path):
    result = []

    for root, dirs, files in os.walk(start_path):
        # Исключаем системные директории
        dirs[:] = [
            d
            for d in dirs
            if d not in ["__pycache__", ".git", ".venv", "venv", "node_modules"]
        ]

        for file in files:
            # Пропускаем некоторые системные файлы
            if file in [".gitignore", ".env", ".DS_Store", "__init__.py"]:
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, start_path)

            # Добавляем путь к файлу
            result.append(f"/{relative_path}")

            try:
                # Пытаемся прочитать содержимое файла
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                result.append(content)
            except UnicodeDecodeError:
                # Если не текстовый файл, пропускаем содержимое
                result.append("<binary file - content skipped>")
            except Exception as e:
                # В случае других ошибок
                result.append(f"<error reading file: {str(e)}>")

            # Добавляем разделитель между файлами
            result.append("\n" + "=" * 50 + "\n")

    return "\n".join(result)


def main():
    start_path = os.path.dirname(os.path.abspath(__file__))
    structure_with_content = get_file_structure_with_content(start_path)
    pyperclip.copy(structure_with_content)
    print("Структура файлов с содержимым скопирована в буфер обмена.")
    print(f"Обработано примерно {len(structure_with_content)} символов.")


if __name__ == "__main__":
    main()

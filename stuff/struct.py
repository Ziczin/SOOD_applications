#!/usr/bin/env python3
import os

EXCLUDE = {".git", "__pycache__"}

def tree(dir_path, prefix=""):
    try:
        names = sorted(n for n in os.listdir(dir_path) if n not in EXCLUDE)
    except PermissionError:
        return
    for i, name in enumerate(names):
        path = os.path.join(dir_path, name)
        branch = "└── " if i == len(names)-1 else "├── "
        print(prefix + branch + name)
        if os.path.isdir(path):
            extension = "    " if i == len(names)-1 else "│   "
            tree(path, prefix + extension)

if __name__ == "__main__":
    # папка, где лежит script.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # её родитель
    parent = os.path.dirname(script_dir)
    print(parent)
    tree(parent)

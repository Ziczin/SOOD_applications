#!/usr/bin/env python3
import os
from collections import defaultdict

ALLOWED = {'py', 'js', 'html'}

def valid_extension(name):
    if '.' not in name:
        return None
    ext = name.rsplit('.', 1)[1].lower()
    return ext if ext in ALLOWED else None

def is_hidden(name):
    return name.startswith('.')

def file_nonempty(path):
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            if any(b for b in chunk):
                return True
    return False

def count_nonblank_lines(path):
    cnt = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip():
                cnt += 1
    return cnt

def walk_and_count(start_path='.'):
    total_files = 0
    total_dirs = 0
    total_lines = 0
    ext_lines = defaultdict(int)
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d != 'migrations' and not is_hidden(d)]
        total_dirs += 1
        for name in files:
            if is_hidden(name):
                continue
            ext = valid_extension(name)
            if ext is None:
                continue
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                continue
            if not file_nonempty(path):
                continue
            lines = count_nonblank_lines(path)
            total_files += 1
            total_lines += lines
            ext_lines[ext] += lines
    return total_files, total_dirs, total_lines, ext_lines

if __name__ == '__main__':
    files, dirs, lines, ext_lines = walk_and_count('.')
    if ext_lines:
        top_ext = max(ext_lines.items(), key=lambda x: x[1])[0]
    else:
        top_ext = ''
    print(files, dirs, lines, top_ext)

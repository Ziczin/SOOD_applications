#!/usr/bin/env python3
import os
from collections import defaultdict

ALLOWED = {'py', 'js', 'html', 'css'}

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
    ext_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
    
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
            ext_stats[ext]['files'] += 1
            ext_stats[ext]['lines'] += lines
            
    return total_files, total_dirs, total_lines, ext_stats

if __name__ == '__main__':
    files, dirs, lines, ext_stats = walk_and_count('.')
    print()
    print(f"  Total files: {files}")
    print(f"  Total dirs: {dirs}")
    print(f"  Total lines: {lines}")
    print("\n  Statistics by extension:")
    print(" ", "-" * 40)
    
    for ext in sorted(ext_stats.keys()):
        stats = ext_stats[ext]
        print(f"  {ext.upper():<6} - Files: {stats['files']:>4}, Lines: {stats['lines']:>6}")
    
while True: pass
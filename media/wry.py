#!/usr/bin/env python3
from PIL import Image
from pathlib import Path
import shutil

TARGET_SIZE = (64, 64)
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

def process_folder(folder: Path):
    for p in folder.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMAGE_EXTS:
            continue

        backup = p.with_name(f"original_{p.name}")
        if backup.exists():
            continue

        try:
            shutil.copy2(p, backup)
            with Image.open(p) as im:
                im = im.convert('RGBA') if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info) else im.convert('RGB')
                im = im.resize(TARGET_SIZE, resample=Image.LANCZOS)
                if p.suffix.lower() in ('.jpg', '.jpeg') and im.mode == 'RGBA':
                    im = im.convert('RGB')
                im.save(p)
        except Exception:
            if backup.exists():
                shutil.move(str(backup), str(p))

if __name__ == '__main__':
    process_folder(Path.cwd())

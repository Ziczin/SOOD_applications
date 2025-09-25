from PIL import Image
import os, re

PATTERN = re.compile(r'^orig_(.+)\.png$', re.IGNORECASE)
TARGET_SIZE = (64, 64)

for fname in os.listdir('.'):
    m = PATTERN.match(fname)
    if not m:
        continue
    out_name = f"{m.group(1)}.png"
    with Image.open(fname) as im:
        im = im.resize(TARGET_SIZE, Image.LANCZOS)
        im.save(out_name, format='PNG', optimize=True)
    print(f"Saved: {out_name}")

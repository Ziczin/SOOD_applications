#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys

EXCLUDE_DIRS = {"sandbox", "test", "node_modules", "staticfiles"}


def collect_js_contents(root: Path) -> str:
    parts = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel_dir.parts):
            dirnames.clear()
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in sorted(filenames):
            if fname.lower().endswith((".js", ".py", ".css", ".html")):
                fpath = Path(dirpath) / fname
                rel = fpath.relative_to(root)
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                parts.append(f"{rel}\n{content}\n")
    return "\n".join(parts)


def write_txt_with_bom(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8-sig"))


def copy_to_clipboard_windows(text: str):
    p = subprocess.Popen(
        ["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value $input"],
        stdin=subprocess.PIPE,
    )
    p.communicate(input=text.encode("utf-8"))


if __name__ == "__main__":
    root = Path(".").resolve()
    result = collect_js_contents(root)
    out = Path("collected.txt")
    write_txt_with_bom(out, result)
    copy_to_clipboard_windows(result)
    sys.stdout.write(
        f"Скопировано {len(result.encode('utf-8'))} байт в буфер обмена и записано в {out}\n"
    )

import os,shutil,subprocess,pathlib,sys

SRC_DIR = r"C:\Users\korneevas\Desktop\proj\apps\Apps\SOOD_applications\static\deps"
OUT_DIR = r"C:\Users\korneevas\Desktop\proj\apps\Apps\SOOD_applications\static\deps_min"
TGZ = r"C:\Users\korneevas\Desktop\terser-5.19.0.tgz"

def find(x):
    return shutil.which(x) or None

def ensure_terser():
    t = find("terser") or find("terser.cmd")
    if t: return t
    npm = find("npm") or find("npm.cmd")
    if not npm:
        raise SystemExit("npm не найден")
    if not os.path.isfile(TGZ):
        raise SystemExit("TGZ не найден: " + TGZ)
    subprocess.check_call([npm, "install", TGZ, "--no-audit", "--no-fund"])
    local = os.path.join("node_modules", ".bin", "terser")
    if os.path.exists(local) or os.path.exists(local + ".cmd"):
        return local
    raise SystemExit("terser не установлен")

terser = ensure_terser()

for root, _, files in os.walk(SRC_DIR):
    for f in files:
        if not f.endswith(".js"): continue
        src = os.path.join(root, f)
        rel = os.path.relpath(src, SRC_DIR)
        out = os.path.join(OUT_DIR, os.path.splitext(rel)[0] + ".min.js")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            subprocess.check_call([terser, src, "--compress", "--mangle", "--toplevel", "--output", out])
            print("ok", rel)
        except subprocess.CalledProcessError:
            print("err", rel)

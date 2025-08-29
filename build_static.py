#!/usr/bin/env python3
"""
build_with_esbuild.py

Автоматический инициатор сборки через build-esbuild.js.

Usage:
  python build_with_esbuild.py            # выполнить сборку (требуется node/npm)
  python build_with_esbuild.py --watch    # запустить режим наблюдения
  python build_with_esbuild.py --skip-install           # пропустить npm install/esbuild
  python build_with_esbuild.py --skip-node-install     # не проверять/не требовать node/npm
  python build_with_esbuild.py --force    # перезаписать build-esbuild.js placeholder, если нужно
  python build_with_esbuild.py --out DIR  # изменить выходную папку (default: static/collected)
  python build_with_esbuild.py --entry PATH # явно указать entry (default: ./make.js)
"""

from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Tuple, Optional

ROOT = Path.cwd()
PACKAGE_JSON = ROOT / "package.json"
BUILD_JS = ROOT / "build-esbuild.js"
DEFAULT_ENTRY = ROOT / "make.js"
DEFAULT_OUT = ROOT / "static" / "collected"

BUILD_JS_PLACEHOLDER = """// build-esbuild.js
// Minimal esbuild bundler for this project. Place this file in project root (next to make.js).
// It will bundle `ENTRY` (default: ./make.js) into OUT_DIR and write manifest.json.
// You can replace this with your own build script — this placeholder will only be created if missing.

const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

const ENTRY = process.env.ENTRY || path.resolve(__dirname, 'make.js'); // override with env var
const OUT_DIR = process.env.OUT_DIR || path.resolve(__dirname, 'static', 'collected');

(async () => {
  try {
    if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });
    const tmpOut = path.join(OUT_DIR, 'static.tmp.js');
    const result = await esbuild.build({
      entryPoints: [ENTRY],
      bundle: true,
      minify: true,
      sourcemap: false,
      metafile: true,
      splitting: false,
      format: 'iife',
      globalName: 'AppBundle',
      platform: 'browser',
      target: ['es2018'],
      outfile: tmpOut,
    });

    // move/rename js to fixed name (no hash)
    const finalName = `static.js`;
    const finalPath = path.join(OUT_DIR, finalName);
    if (fs.existsSync(finalPath)) fs.unlinkSync(finalPath);
    fs.renameSync(tmpOut, finalPath);

    // handle css output (if any) - fixed name static.css
    let cssFinal = null;
    const cssOutputs = Object.keys(result.metafile.outputs || {}).filter(p => p.endsWith('.css'));
    if (cssOutputs.length) {
      const cssPath = path.resolve(cssOutputs[0]);
      if (fs.existsSync(cssPath)) {
        const cssName = `static.css`;
        const cssFinalPath = path.join(OUT_DIR, cssName);
        if (fs.existsSync(cssFinalPath)) fs.unlinkSync(cssFinalPath);
        fs.renameSync(cssPath, cssFinalPath);
        cssFinal = cssName;
      }
    }

    const manifest = {
      "static.js": path.relative(process.cwd(), finalPath).replace(/\\\\/g, '/')
    };
    if (cssFinal) manifest['static.css'] = path.relative(process.cwd(), path.join(OUT_DIR, cssFinal)).replace(/\\\\/g, '/');

    fs.writeFileSync(path.join(OUT_DIR, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
    console.log('Build finished:', manifest);
  } catch (e) {
    console.error('Build failed', e);
    process.exit(1);
  }
})();
"""

# Choose npm executable name per-platform
NPM = "npm.cmd" if os.name == "nt" else "npm"

# Helper utilities
def sh(cmd: list[str], check=True, capture_output=False, env=None) -> subprocess.CompletedProcess:
    print("> " + " ".join(cmd))
    return subprocess.run(cmd, check=check, capture_output=capture_output, env=env)

def which_prog(name: str) -> Optional[str]:
    return shutil.which(name)

def node_npm_present() -> Tuple[bool, bool]:
    node = which_prog("node")
    npm = which_prog(NPM)
    return (node is not None, npm is not None)

def npm_init_if_needed():
    if not PACKAGE_JSON.exists():
        print("package.json not found — running: npm init -y")
        sh([NPM, "init", "-y"])
    else:
        print("package.json found.")

def ensure_build_js(force: bool):
    if BUILD_JS.exists() and not force:
        print("build-esbuild.js already exists — leaving unchanged.")
        return
    print("Writing build-esbuild.js placeholder (overwrite=%s)..." % bool(force))
    BUILD_JS.write_text(BUILD_JS_PLACEHOLDER, encoding="utf-8")
    try:
        BUILD_JS.chmod(0o755)
    except Exception:
        pass

def ensure_package_scripts():
    try:
        pj = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    except Exception:
        print("Failed to read package.json — aborting script modification.")
        return
    scripts = pj.get("scripts", {})
    changed = False
    if "build" not in scripts:
        scripts["build"] = "node build-esbuild.js"
        changed = True
    if "watch" not in scripts:
        scripts["watch"] = "node build-esbuild.js --watch"
        changed = True
    if changed:
        pj["scripts"] = scripts
        PACKAGE_JSON.write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
        print("Updated package.json with build/watch scripts.")
    else:
        print("package.json already contains build/watch scripts.")

def npm_install_esbuild(skip_install: bool) -> bool:
    if skip_install:
        print("Skipping npm install (per flag).")
        return True
    print("Installing esbuild (dev dependency)...")
    try:
        sh([NPM, "install", "--save-dev", "esbuild"])
        return True
    except subprocess.CalledProcessError as e:
        print("npm install failed:", e)
        return False

def run_build(watch: bool, entry: Optional[str], out_dir: str):
    env = os.environ.copy()
    if entry:
        env['ENTRY'] = str(entry)
    if out_dir:
        env['OUT_DIR'] = str(out_dir)
    cmd = [NPM, "run", "watch" if watch else "build"]
    print("Running:", " ".join(cmd))
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    try:
        for line in proc.stdout:
            print(line, end="")
    except KeyboardInterrupt:
        print("Interrupted by user, terminating child process...")
        proc.terminate()
        proc.wait()
    return proc.wait()

def ensure_gitignore_collected():
    gitignore = ROOT / ".gitignore"
    try:
        if gitignore.exists():
            txt = gitignore.read_text(encoding='utf-8')
            if "static/collected/" not in txt:
                gitignore.write_text(txt + "\n# build outputs\nstatic/collected/\n", encoding='utf-8')
                print("Appended 'static/collected/' to .gitignore")
        else:
            gitignore.write_text("# build outputs\nstatic/collected/\n", encoding='utf-8')
            print("Created .gitignore with static/collected/ entry")
    except Exception:
        pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true", help="Run watch after setup")
    ap.add_argument("--skip-install", action="store_true", help="Skip npm install/esbuild")
    ap.add_argument("--skip-node-install", action="store_true", help="Do not require/check node/npm")
    ap.add_argument("--force", action="store_true", help="Overwrite build-esbuild.js placeholder if exists")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory for bundles (default: static/collected)")
    ap.add_argument("--entry", default=str(DEFAULT_ENTRY), help="Entry JS file (default: ./make.js)")
    args = ap.parse_args()

    if not args.skip_node_install:
        node_present, npm_present = node_npm_present()
        if not (node_present and npm_present):
            print("Node/npm not available. Please install Node.js and npm manually and re-run the script:")
            print("  https://nodejs.org/")
            print("You can re-run with --skip-node-install to bypass this check.")
            sys.exit(1)
        else:
            print("Node and npm detected.")
    else:
        print("Skipping Node/npm presence check (per flag).")

    # 2) package.json and build-esbuild.js placeholder
    npm_init_if_needed()
    ensure_build_js(force=args.force)
    ensure_package_scripts()

    installed = npm_install_esbuild(skip_install=args.skip_install)
    if not installed:
        print("esbuild installation failed or skipped. If esbuild is already installed, you can continue with --skip-install.")
        if not args.skip_install:
            sys.exit(1)

    out_dir = Path(args.out).resolve()
    ensure_gitignore_collected()

    entry = Path(args.entry).resolve()
    if not entry.exists():
        print(f"Warning: entry file {entry} not found. The build may fail. You can specify entry with --entry.")
    code = run_build(watch=args.watch, entry=str(entry), out_dir=str(out_dir))
    if code == 0:
        print("Build finished successfully.")
    else:
        print("Build exited with code", code)
        sys.exit(code)

if __name__ == "__main__":
    main()

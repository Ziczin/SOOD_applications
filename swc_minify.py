import os
import json
import subprocess
import sys
import glob
from pathlib import Path
import shutil
import hashlib
import argparse


class SWCMinifier:
    def __init__(self, config_path, no_cache=False):
        self.config_path = Path(config_path)
        self.project_root = self.config_path.parent
        self.config = self._load_config()
        self.node_modules = self.project_root / "node_modules"
        # Меняем путь на JS скрипт
        self.swc_script = self.project_root / "swc-minify.js"
        self.temp_config = None
        self.hashes_file = self.project_root / "minify-hashes.json"
        self.no_cache = no_cache
        self.file_hashes = self._load_hashes()

    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Конфиг не найден: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        if "entries" not in config or "output_dir" not in config:
            raise ValueError("Конфиг должен содержать 'entries' и 'output_dir'")

        expanded = []
        for pattern in config["entries"]:
            exclude = pattern.startswith("!")
            clean = pattern[1:] if exclude else pattern
            matches = glob.glob(str(self.project_root / clean), recursive=True)
            resolved = [str(Path(f).resolve()) for f in matches]

            if exclude:
                expanded = [f for f in expanded if f not in resolved]
            else:
                expanded.extend(resolved)

        config["entries"] = list(set(expanded))
        config["output_dir"] = str((self.project_root / config["output_dir"]).resolve())
        return config

    def _load_hashes(self):
        if self.no_cache or not self.hashes_file.exists():
            return {}
        try:
            with open(self.hashes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_hashes(self):
        try:
            with open(self.hashes_file, "w", encoding="utf-8") as f:
                json.dump(self.file_hashes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Не удалось сохранить хеши: {e}")

    def _file_hash(self, path):
        try:
            with open(path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None

    def _relative_path(self, path):
        path = Path(path).resolve()
        root = self.project_root.resolve()
        try:
            return str(path.relative_to(root))
        except ValueError:
            return path.name

    def _display_path(self, path):
        path = Path(path).resolve()
        cwd = Path.cwd().resolve()
        try:
            return str(path.relative_to(cwd))
        except ValueError:
            return str(path)

    def _get_output_path(self, input_file):
        rel = self._relative_path(input_file)
        if rel.startswith(("static/deps/", "static\\deps\\")):
            rel = rel.split(os.sep, 2)[-1]
        return Path(self.config["output_dir"]) / Path(rel).with_suffix(".js")

    def _needs_minification(self, file_path):
        current = self._file_hash(file_path)
        if current is None:
            return True

        rel = self._relative_path(file_path)

        if self.no_cache:
            self.file_hashes[rel] = current
            return True

        if rel in self.file_hashes and self.file_hashes[rel] == current:
            out = self._get_output_path(file_path)
            if out.exists():
                print(f"\n⏭️ Пропускаем {self._display_path(file_path)} (без изменений)")
                return False

        self.file_hashes[rel] = current
        return True

    def _check_node_npm(self):
        node = shutil.which("node") or shutil.which("node.exe")
        npm = shutil.which("npm") or shutil.which("npm.cmd")

        if not node or not npm:
            for base in [
                os.environ.get("ProgramFiles", "C:\\Program Files"),
                os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
                os.path.expanduser("~\\AppData\\Roaming\\nvm"),
                os.path.expanduser("~\\AppData\\Local\\Programs\\nodejs"),
            ]:
                if "nvm" in base:
                    node_candidates = glob.glob(os.path.join(base, "v*", "node.exe"))
                else:
                    node_candidates = [os.path.join(base, "nodejs", "node.exe")]
                for cand in node_candidates:
                    if os.path.exists(cand):
                        node = cand
                        npm = os.path.join(os.path.dirname(cand), "npm.cmd")
                        if os.path.exists(npm):
                            break
                if node and npm:
                    break

        if node and npm:
            try:
                node_ver = subprocess.run(
                    [node, "--version"], capture_output=True, text=True
                )
                npm_ver = subprocess.run(
                    [npm, "--version"], capture_output=True, text=True
                )
                if node_ver.returncode == 0 and npm_ver.returncode == 0:
                    print(
                        f"✅ Node {node_ver.stdout.strip()}, npm {npm_ver.stdout.strip()}"
                    )
                    return True
            except Exception:
                pass
        return False

    def _install_swc(self):
        print("\n📦 Устанавливаем SWC...")
        npm = shutil.which("npm") or shutil.which("npm.cmd")
        if not npm:
            print("❌ npm не найден")
            return False

        pkg = self.project_root / "package.json"
        if not pkg.exists():
            with open(pkg, "w", encoding="utf-8") as f:
                json.dump({"name": "swc-minify", "private": True}, f)

        subprocess.run(
            f'"{npm}" config set strict-ssl false', shell=True, capture_output=True
        )
        subprocess.run(
            f'"{npm}" config set registry https://registry.npmmirror.com', shell=True
        )

        result = subprocess.run(
            f'"{npm}" install --save-dev @swc/core --no-audit --no-fund',
            cwd=self.project_root,
            shell=True,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ SWC установлен")
            return True
        else:
            print(f"❌ Ошибка установки SWC: {result.stderr[:200]}")
            return False

    def _create_swc_script(self):
        """Создает JS скрипт для минификации через SWC API"""
        opts = self.config.get("options", {})
        compress = opts.get("compress", {})
        mangle = opts.get("mangle", {})

        script_content = f"""
const swc = require('@swc/core');
const fs = require('fs');
const path = require('path');

async function minifyFile(inputFile, outputFile) {{
    try {{
        const code = fs.readFileSync(inputFile, 'utf8');
        
        const result = await swc.transform(code, {{
            jsc: {{
                parser: {{
                    syntax: 'ecmascript',
                    dynamicImport: true,
                    importMeta: true
                }},
                target: 'es2020',
                minify: {{
                    compress: {json.dumps(compress)},
                    mangle: {json.dumps(mangle)},
                    format: {{
                        comments: false
                    }}
                }}
            }},
            minify: true,
            sourceMaps: false
        }});
        
        fs.mkdirSync(path.dirname(outputFile), {{ recursive: true }});
        fs.writeFileSync(outputFile, result.code);
        console.log(JSON.stringify({{ success: true, output: outputFile }}));
    }} catch (error) {{
        console.log(JSON.stringify({{ 
            success: false, 
            error: error.message,
            input: inputFile 
        }}));
    }}
}}

const inputFile = process.argv[2];
const outputFile = process.argv[3];
minifyFile(inputFile, outputFile);
"""

        script_path = self.project_root / "swc-minify.js"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        return script_path

    def ensure_dependencies(self):
        print("🔍 Проверяем зависимости...")
        if not self._check_node_npm():
            print("❌ Node.js/npm не найдены. Установите Node.js с https://nodejs.org/")
            sys.exit(1)

        # Проверяем наличие @swc/core в node_modules
        swc_core = self.node_modules / "@swc" / "core"
        if not swc_core.exists():
            print("⚠️ @swc/core не найден, устанавливаем...")
            if not self._install_swc():
                print(
                    "❌ Не удалось установить @swc/core. Попробуйте вручную: npm install --save-dev @swc/core"
                )
                sys.exit(1)

        # Создаем JS скрипт
        self._create_swc_script()

        print("✅ Все зависимости готовы\n")

    def minify_file(self, input_file):
        output = self._get_output_path(input_file)
        output.parent.mkdir(parents=True, exist_ok=True)

        node = shutil.which("node") or shutil.which("node.exe")
        cmd = f'"{node}" "{self.swc_script}" "{input_file}" "{output}"'

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, encoding="utf-8"
            )

            # Парсим JSON ответ от скрипта
            try:
                response = json.loads(result.stdout.strip())
                if response.get("success"):
                    return True, output, None
                else:
                    return False, input_file, response.get("error", "Unknown error")
            except Exception:
                return False, input_file, result.stderr or result.stdout

        except Exception as e:
            return False, input_file, str(e)

    def run(self):
        self.ensure_dependencies()

        print("🚀 Запуск минификации...")
        print(f"📁 Проект: {self.project_root}")
        print(f"📄 Файлов в конфиге: {len(self.config['entries'])}")
        print(f"📂 Папка вывода: {self.config['output_dir']}")
        print(
            "💾 Кэш:",
            "отключен (--no-cache)"
            if self.no_cache
            else f"включен ({self.hashes_file})",
        )
        print("-" * 50)

        os.makedirs(self.config["output_dir"], exist_ok=True)

        to_process = []
        skipped = 0
        for entry in self.config["entries"]:
            if not os.path.exists(entry):
                print(f"\n⚠️ Файл не найден: {self._display_path(entry)}")
                continue
            if self._needs_minification(entry):
                to_process.append(entry)
            else:
                skipped += 1

        if skipped:
            print(f"\n⏭️ Пропущено без изменений: {skipped}")

        if not to_process:
            print("\n✨ Все файлы актуальны!")
            return True

        print(f"\n🔨 Обрабатываем {len(to_process)} файлов...\n")

        success = []
        failed = []
        sizes_before = {}
        sizes_after = {}

        for i, file in enumerate(to_process, 1):
            sizes_before[file] = os.path.getsize(file)
            print(f"[{i}/{len(to_process)}] {self._display_path(file)}")
            ok, out_or_file, err = self.minify_file(file)
            if ok:
                sizes_after[file] = os.path.getsize(out_or_file)
                success.append(file)
                print(f"   ✅ Сохранено в {self._display_path(out_or_file)}")
            else:
                failed.append((file, err))
                print(f"   ❌ Ошибка: {err[:150]}...")

        self._save_hashes()

        print("\n" + "=" * 50)
        print(f"✅ Успешно: {len(success)}")
        if success:
            total_before = sum(sizes_before[f] for f in success)
            total_after = sum(sizes_after[f] for f in success)
            for f in success:
                before = sizes_before[f]
                after = sizes_after[f]
                savings = (1 - after / before) * 100 if before else 0
                print(
                    f"   {self._display_path(f)}: {before / 1024:.1f}КБ → {after / 1024:.1f}КБ ({savings:.1f}%)"
                )
            print(
                f"\n   📦 Всего: {total_before / 1024:.1f}КБ → {total_after / 1024:.1f}КБ ({(1 - total_after / total_before) * 100:.1f}%)"
            )

        if failed:
            print(f"\n❌ Ошибок: {len(failed)}")
            for f, e in failed[:3]:
                print(f"   - {self._display_path(f)}: {e[:100]}...")
            if len(failed) > 3:
                print(f"   ... и еще {len(failed) - 3}")

        # Очищаем временный скрипт
        if self.swc_script.exists():
            os.unlink(self.swc_script)

        return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(description="SWC Минификатор с кэшированием")
    parser.add_argument(
        "config",
        nargs="?",
        default="minify_config.json",
        help="Путь к конфигу (по умолчанию: minify_config.json)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Игнорировать существующие хеши, но сохранить новые",
    )
    args = parser.parse_args()

    try:
        m = SWCMinifier(args.config, no_cache=args.no_cache)
        sys.exit(0 if m.run() else 1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

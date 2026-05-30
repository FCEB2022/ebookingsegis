# Script to create comprehensive translations for all languages
# Run this after updating templates with gettext markers

import subprocess
import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PYTHON = sys.executable
PYBABEL_EXECUTABLE = os.path.join(ROOT_DIR, '.venv', 'Scripts', 'pybabel.exe')
if os.path.exists(PYBABEL_EXECUTABLE):
    PYBABEL = [PYBABEL_EXECUTABLE]
else:
    PYBABEL = [PYTHON, '-m', 'pybabel']

print("=" * 60)
print("ACTUALIZANDO TRADUCCIONES")
print("=" * 60)
print()

# 1. Extract new strings from templates
print("1. Extrayendo strings traducibles...")
result = subprocess.run(
    PYBABEL + [
        "extract",
        "-F", "babel.cfg",
        "-k", "_",
        "-k", "_l",
        "-k", "gettext",
        "-k", "ngettext",
        "-k", "lazy_gettext",
        "-o", "messages.pot",
        "."
    ],
    cwd=ROOT_DIR,
    capture_output=True,
    text=True
)
print(f"   {result.stdout}")
if result.returncode == 0:
    print("   [OK] Strings extraídos")
else:
    print(f"   [ERROR] Error: {result.stderr}")
print()

# 2. Update existing catalogs
print("2. Actualizando catálogos existentes...")
for lang in ['en', 'fr']:
    result = subprocess.run(
        PYBABEL + [
            "update",
            "-i", "messages.pot",
            "-d", os.path.join("app", "translations"),
            "-l", lang
        ],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"   [OK] Catálogo {lang} actualizado")
    else:
        print(f"   [ERROR] Error en {lang}: {result.stderr}")
print()

# 3. Apply translations
print("3. Aplicando traducciones automáticas...")
result = subprocess.run(
    [PYTHON, os.path.join(ROOT_DIR, 'add_translations.py')],
    cwd=ROOT_DIR,
    capture_output=True,
    text=True
)
print(result.stdout)
print()

# 4. Compile translations
print("4. Compilando traducciones...")
result = subprocess.run(
    PYBABEL + [
        "compile",
        "-d",
        os.path.join("app", "translations")
    ],
    cwd=ROOT_DIR,
    capture_output=True,
    text=True
)
print(f"   {result.stdout}")
if result.returncode == 0:
    print("   [OK] Traducciones compiladas")
else:
    print(f"   [ERROR] Error: {result.stderr}")
print()

print("============================================================\n[OK] PROCESO COMPLETADO\n============================================================")
print()
print("Las traducciones han sido actualizadas y compiladas.")
print("Reinicia el servidor para ver los cambios:")
print("  1. Detener servidor (CTRL+C)")
print("  2. Ejecutar: .\\run.ps1")

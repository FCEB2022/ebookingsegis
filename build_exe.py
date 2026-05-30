import os
import subprocess
import sys
import shutil


def get_python():
    """Return the Python executable from .venv if it exists, otherwise use system Python."""
    venv_python_win = os.path.join(".venv", "Scripts", "python.exe")
    venv_python_unix = os.path.join(".venv", "bin", "python")
    if os.path.exists(venv_python_win):
        print(f"Using virtual environment Python: {venv_python_win}")
        return os.path.abspath(venv_python_win)
    elif os.path.exists(venv_python_unix):
        print(f"Using virtual environment Python: {venv_python_unix}")
        return os.path.abspath(venv_python_unix)
    else:
        print(f"No .venv found, using system Python: {sys.executable}")
        return sys.executable


def get_installed_packages(python_exe):
    """Return a set of installed package names (lowercase)."""
    result = subprocess.run(
        [python_exe, "-m", "pip", "list", "--format=freeze"],
        capture_output=True, text=True
    )
    packages = set()
    for line in result.stdout.splitlines():
        if "==" in line:
            pkg_name = line.split("==")[0].strip().lower().replace("-", "_")
            packages.add(pkg_name)
            # Also add with hyphens
            packages.add(line.split("==")[0].strip().lower())
    return packages


def build():
    print("Starting build process for EquaHome...")
    print("=" * 60)

    python_exe = get_python()

    # 1. Install PyInstaller in the target environment if needed
    try:
        subprocess.check_call(
            [python_exe, "-c", "import PyInstaller"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Installing PyInstaller...")
        subprocess.check_call([python_exe, "-m", "pip", "install", "pyinstaller"])

    # 2. Clean previous build artifacts
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"Removing old '{folder}' folder...")
            shutil.rmtree(folder, ignore_errors=True)
    for spec in ["EquaHome_App.spec", "EquaHome.spec"]:
        if os.path.exists(spec):
            os.remove(spec)

    # Windows path separator
    separator = ";"

    assets = [
        ("app/templates", "app/templates"),
        ("app/static", "app/static"),
        ("app/translations", "app/translations"),
    ]

    hidden_imports = [
        "flask_migrate",
        "flask_sqlalchemy",
        "flask_login",
        "flask_mail",
        "flask_wtf",
        "flask_babel",
        "email_validator",
        "alembic",
        "sqlalchemy.sql.default_comparator",
        "flask_sqlalchemy.extension",
        "PIL",
        "dotenv",
        "python_dotenv",
        "wtforms",
        "babel",
        "babel.dates",
        "babel.numbers",
    ]

    cmd = [
        python_exe,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--console",
        "--name", "EquaHome_App",
    ]

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    for src, dst in assets:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src}{separator}{dst}"])
        else:
            print(f"Warning: Asset path '{src}' not found. Skipping.")

    # --collect-all for packages that use importlib.metadata at runtime
    # This fixes: PackageNotFoundError: No package metadata was found for werkzeug
    collect_packages = ["werkzeug", "flask", "jinja2", "markupsafe", "click",
                        "babel", "flask_babel"]
    for pkg in collect_packages:
        cmd.extend(["--collect-all", pkg])

    # --copy-metadata only for packages confirmed installed (avoids build errors)
    installed = get_installed_packages(python_exe)
    copy_meta_candidates = [
        ("flask_sqlalchemy", "flask_sqlalchemy"),
        ("flask-sqlalchemy", "flask_sqlalchemy"),
        ("sqlalchemy", "sqlalchemy"),
        ("flask_login", "flask_login"),
        ("flask-login", "flask_login"),
        ("flask_wtf", "flask_wtf"),
        ("flask-wtf", "flask_wtf"),
        ("flask_mail", "flask_mail"),
        ("flask-mail", "flask_mail"),
        ("flask_migrate", "flask_migrate"),
        ("flask-migrate", "flask_migrate"),
        ("alembic", "alembic"),
    ]

    added_meta = set()
    for check_name, meta_name in copy_meta_candidates:
        if check_name in installed and meta_name not in added_meta:
            cmd.extend(["--copy-metadata", meta_name])
            added_meta.add(meta_name)

    # Entry point
    cmd.append("run.py")

    # 3. Execute PyInstaller
    print(f"\nRunning PyInstaller (this may take several minutes)...\n")
    subprocess.check_call(cmd)

    # 4. Post-build: Create uploads folder so it exists on first run
    dist_path = os.path.join("dist", "EquaHome_App")
    uploads_path = os.path.join(dist_path, "app", "static", "uploads")
    os.makedirs(uploads_path, exist_ok=True)
    print(f"Created uploads folder: {uploads_path}")

    # 5. Post-build: Copy .env.example as .env for the user to configure
    env_dest = os.path.join(dist_path, ".env")
    if os.path.exists(".env.example") and not os.path.exists(env_dest):
        print(f"Creating default .env from .env.example...")
        shutil.copy2(".env.example", env_dest)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"Executable: dist/EquaHome_App/EquaHome_App.exe")
    print("Copy the entire 'EquaHome_App' folder to deploy on another machine.")
    print("=" * 60)


if __name__ == "__main__":
    build()

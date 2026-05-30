import os
import sys
import traceback
from dotenv import load_dotenv

# Monkey-patch importlib.metadata for bundled executable stability
import importlib.metadata
try:
    importlib.metadata.version('werkzeug')
except (importlib.metadata.PackageNotFoundError, ImportError):
    orig_version = importlib.metadata.version
    def patched_version(package_name):
        try:
            return orig_version(package_name)
        except (importlib.metadata.PackageNotFoundError, ImportError):
            fallbacks = {
                'werkzeug': '3.0.0',
                'flask': '3.0.1',
                'flask-sqlalchemy': '3.1.1',
                'jinja2': '3.1.3'
            }
            return fallbacks.get(package_name, '0.0.0')
    importlib.metadata.version = patched_version

# Load environment variables
load_dotenv()

# Setup logging for the packaged executable - only log critical errors to file
if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
    log_path = os.path.join(basedir, 'error_log.txt')
    # We will keep the default stdout/stderr for the console but write errors to file too

def log_critical(msg):
    if getattr(sys, 'frozen', False):
        log_path = os.path.join(os.path.dirname(sys.executable), 'error_log.txt')
        with open(log_path, 'a') as f:
            f.write(f"\n[{datetime.now()}] CRITICAL: {msg}\n")
    print(msg)

try:
    from app import create_app, db
    from app.models import Usuario, Oferta, Contacto, Queja, Favorito, HistorialOferta
    from datetime import datetime
except Exception as e:
    log_critical(f"ERROR AL IMPORTAR MÓDULOS: {str(e)}")
    traceback.print_exc()
    input("\nPresiona ENTER para cerrar...")
    sys.exit(1)

# Create the Flask app
try:
    app = create_app(os.getenv('FLASK_ENV') or 'development')
except Exception as e:
    log_critical(f"ERROR AL CREAR LA APP: {str(e)}")
    traceback.print_exc()
    input("\nPresiona ENTER para cerrar...")
    sys.exit(1)


# Shell context for flask shell command
@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell"""
    return {
        'db': db,
        'Usuario': Usuario,
        'Oferta': Oferta,
        'Contacto': Contacto,
        'Queja': Queja,
        'Favorito': Favorito,
        'HistorialOferta': HistorialOferta
    }


# CLI command to create an admin user
@app.cli.command()
def create_admin():
    """Create an admin user"""
    from werkzeug.security import generate_password_hash
    
    admin = Usuario(
        nombre='Administrador',
        email='admin@equahome.gq',
        telefono='+240123456789',
        rol='admin',
        password_hash=generate_password_hash('admin123')
    )
    
    db.session.add(admin)
    db.session.commit()
    print('Admin user created successfully!')
    print('Email: admin@equahome.gq')
    print('Password: admin123')
    print('Please change the password after first login.')


# CLI command to seed the database with sample data
@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from werkzeug.security import generate_password_hash
    from datetime import datetime
    
    # Create sample users
    users = [
        Usuario(
            nombre='Admin User',
            email='admin@equahome.gq',
            telefono='+240111111111',
            rol='admin',
            password_hash=generate_password_hash('admin123')
        ),
        Usuario(
            nombre='Juan Pérez',
            email='juan@example.com',
            telefono='+240222222222',
            rol='usuario',
            password_hash=generate_password_hash('user123')
        ),
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print('Database seeded successfully!')


if __name__ == '__main__':
    # Determine if we should run in debug mode
    debug_mode = not getattr(sys, 'frozen', False)
    
    # Initialize database if it doesn't exist
    with app.app_context():
        print("Initializing database tables...")
        db.create_all()
        print("Database initialized.")
    
    # Diagnostic info
    print(f"Base Directory: {os.path.abspath(os.path.dirname(sys.executable))}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Run on all network interfaces (0.0.0.0) to allow remote access
    # Access locally: http://localhost:5000
    # Access remotely: http://YOUR_IP_ADDRESS:5000
    print(f"Starting EquaHome server on port 5000 (Debug: {debug_mode})...")
    try:
        app.run(host='0.0.0.0', port=5000, debug=debug_mode)
    except Exception as e:
        print(f"\nERROR DE EJECUCIÓN: {str(e)}")
        traceback.print_exc()
    
    input("\nServidor detenido. Presiona ENTER para salir...")

# Script para crear usuario administrador
from app import create_app, db
from app.models import Usuario

# Crear aplicación
app = create_app('development')

with app.app_context():
    # Verificar si ya existe un admin
    existing_admin = Usuario.query.filter_by(email='admin@equahome.gq').first()
    
    if existing_admin:
        print('El usuario admin ya existe.')
        print(f'Email: {existing_admin.email}')
        print(f'Username: {existing_admin.username}')
    else:
        # Crear nuevo admin
        admin = Usuario(
            nombre='Administrador',
            username='admin',
            email='admin@equahome.gq',
            telefono='+240123456789',
            rol='admin',
            activo=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print('✓ Usuario administrador creado exitosamente!')
        print('')
        print('Credenciales:')
        print('  Usuario: admin')
        print('  Email: admin@equahome.gq')
        print('  Contraseña: admin123')
        print('')
        print('⚠️  IMPORTANTE: Cambia la contraseña después del primer login.')

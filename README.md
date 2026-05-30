# EquaHome - Portal Inmobiliario para Guinea Ecuatorial

Sistema web desarrollado en Flask para gestionar ofertas de alquiler y venta de viviendas en Guinea Ecuatorial. El sistema actúa como intermediario donde administradores publican ofertas, clientes exploran y contactan, y las negociaciones se realizan fuera de la plataforma.

## 🚀 Características Principales

- **Autenticación y Roles**: Sistema de usuarios con roles (Admin, Usuario Registrado, Visitante)
- **Gestión de Ofertas**: CRUD completo de propiedades con imágenes, videos y ubicación GPS
- **Búsqueda Avanzada**: Filtros por precio, ubicación, tipo, características
- **Contacto y Quejas**: Formularios de contacto y sistema de quejas
- **Favoritos**: Los usuarios registrados pueden guardar propiedades favoritas
- **Dashboard Administrativo**: Estadísticas y gestión centralizada
- **Responsive Design**: Interfaz adaptable a todos los dispositivos
- **Integración de Mapas**: Leaflet.js para mostrar ubicaciones

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

## 🛠️ Instalación

### 1. Clonar el repositorio o descargar el código

```bash
cd PROYECTO_SEGIS
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env` y configurar:

```bash
copy .env.example .env
```

Editar `.env` con tus configuraciones:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///equahome.db
```

### 5. Inicializar la base de datos

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Crear usuario administrador

```bash
flask create-admin
```

Esto creará un usuario administrador con:
- **Email**: admin@equahome.gq
- **Contraseña**: admin123 (¡cambiar después del primer login!)

### 7. (Opcional) Poblar base de datos con datos de prueba

```bash
flask seed-db
```

## ▶️ Ejecutar la Aplicación

### Modo Desarrollo

```bash
flask run
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

### Modo Producción

Para producción, usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 📁 Estructura del Proyecto

```
PROYECTO_SEGIS/
├── app/
│   ├── __init__.py              # Inicialización de la app
│   ├── models.py                # Modelos de base de datos
│   ├── forms.py                 # Formularios WTForms
│   ├── auth/                    # Blueprint de autenticación
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/                    # Blueprint principal (público)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/                   # Blueprint de administración
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── user/                    # Blueprint de usuario
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/                # Capa de servicios
│   │   ├── file_service.py      # Manejo de archivos
│   │   └── email_service.py     # Envío de emails
│   ├── templates/               # Plantillas Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── main/
│   │   ├── admin/
│   │   ├── user/
│   │   └── errors/
│   └── static/                  # Archivos estáticos
│       ├── css/
│       ├── js/
│       └── uploads/
├── migrations/                   # Migraciones de base de datos
├── config.py                     # Configuración
├── run.py                        # Punto de entrada
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

## 🔑 Usuarios y Roles

### Visitante (No autenticado)
- Buscar y ver propiedades
- Ver detalles de propiedades

### Usuario Registrado
- Todas las funciones de visitante
- Guardar favoritos
- Enviar formularios de contacto
- Enviar quejas

### Administrador
- Todas las funciones de usuario registrado
- Crear, editar y eliminar ofertas
- Gestionar contactos recibidos
- Gestionar quejas
- Ver estadísticas
- Exportar datos

## 🗺️ Rutas Principales

### Rutas Públicas
- `/` - Página de inicio
- `/alquiler` - Propiedades en alquiler
- `/venta` - Propiedades en venta
- `/oferta/<id>` - Detalle de propiedad
- `/buscar` - Búsqueda con filtros

### Autenticación
- `/auth/register` - Registro de usuario
- `/auth/login` - Inicio de sesión
- `/auth/logout` - Cerrar sesión

### Usuario (Requiere login)
- `/user/favoritos` - Mis favoritos
- `/user/quejas` - Mis quejas
- `/user/perfil` - Mi perfil

### Administración (Requiere rol admin)
- `/admin/dashboard` - Panel de administración
- `/admin/ofertas` - Gestión de ofertas
- `/admin/ofertas/nueva` - Nueva oferta
- `/admin/ofertas/editar/<id>` - Editar oferta
- `/admin/buzon` - Buzón de contactos
- `/admin/quejas` - Gestión de quejas
- `/admin/buzon/exportar` - Exportar contactos a CSV

## 📧 Configuración de Email

Para habilitar el envío de emails, configurar en `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=noreply@equahome.gq
```

> **Nota**: Para Gmail, necesitas crear una "Contraseña de aplicación" en la configuración de seguridad de Google.

## 🎨 Personalización

### Colores del diseño
Los colores están basados en la bandera de Guinea Ecuatorial y se pueden modificar en `app/static/css/style.css`:

```css
:root {
    --verde: #009E49;  /* Verde de la bandera */
    --azul: #3A75C4;   /* Azul de la bandera */
    --rojo: #D21034;   /* Rojo de la bandera */
    --blanco: #FFFFFF;
}
```

## 🔒 Seguridad

- **CSRF Protection**: Habilitado en todos los formularios
- **Password Hashing**: Werkzeug para hash seguro de contraseñas
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Session Security**: Cookies HttpOnly y Secure
- **File Upload Validation**: Validación de tipo y tamaño de archivos

## 📝 Comandos CLI Útiles

```bash
# Iniciar shell interactivo con contexto de la app
flask shell

# Crear migraciones
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Volver atrás una migración
flask db downgrade

# Crear administrador
flask create-admin

# Poblar base de datos
flask seed-db
```

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Database not found"
```bash
flask db init
flask db migrate
flask db upgrade
```

### Las imágenes no se cargan
Verifica que la carpeta `app/static/uploads` existe y tiene permisos de escritura.

### Error de CSRF token
Asegúrate de que las cookies estén habilitadas en tu navegador.

## 🚀 Próximos Pasos

- [ ] Implementar internacionalización (ES/EN) con Flask-Babel
- [ ] Agregar CAPTCHA en formularios
- [ ] Integración con WhatsApp para notificaciones
- [ ] Sistema de reportes avanzados
- [ ] Integración con AWS S3 para almacenamiento de archivos
- [ ] API REST para aplicación móvil
- [ ] Tests unitarios y de integración

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👥 Contacto

Para preguntas o soporte, contactar a: admin@equahome.gq

---

**Versión**: 1.0.0  
**Última actualización**: Noviembre 2025

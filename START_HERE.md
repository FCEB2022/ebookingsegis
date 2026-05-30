✅ **SISTEMA EQUAHOME - LISTO PARA USAR**

## 🎉 Instalación Completada

La base de datos y el usuario administrador se han creado exitosamente.

---

## 🚀 Cómo Iniciar la Aplicación

### Opción 1: Usar el script PowerShell (Recomendado)
```powershell
.\run.ps1
```

### Opción 2: Comando manual
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask run
```

### Opción 3: Ejecutar directamente run.py
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" run.py
```

---

## 🌐 Acceder a la Aplicación

Una vez iniciado el servidor, abre tu navegador en:

**http://127.0.0.1:5000**

---

## 🔑 Credenciales de Administrador

Para acceder al panel de administración:

- **URL**: http://127.0.0.1:5000/auth/login
- **Email**: `admin@equahome.gq`
- **Contraseña**: `admin123`

> ⚠️ **IMPORTANTE**: Cambia la contraseña después del primer login

---

## 📍 Rutas Disponibles

### Públicas (sin login)
- **Homepage**: http://127.0.0.1:5000/
- **Alquiler**: http://127.0.0.1:5000/alquiler
- **Venta**: http://127.0.0.1:5000/venta
- **Registro**: http://127.0.0.1:5000/auth/register

### Requieren Login
- **Favoritos**: http://127.0.0.1:5000/user/favoritos
- **Quejas**: http://127.0.0.1:5000/user/quejas
- **Perfil**: http://127.0.0.1:5000/user/perfil

### Solo Administradores
- **Dashboard**: http://127.0.0.1:5000/admin/dashboard
- **Gestión de Ofertas**: http://127.0.0.1:5000/admin/ofertas
- **Nueva Oferta**: http://127.0.0.1:5000/admin/ofertas/nueva
- **Buzón**: http://127.0.0.1:5000/admin/buzon
- **Quejas**: http://127.0.0.1:5000/admin/quejas

---

## 💡 Primeros Pasos

1. **Inicia el servidor**:
   ```powershell
   .\run.ps1
   ```

2. **Abre el navegador** en http://127.0.0.1:5000

3. **Inicia sesión como admin** con las credenciales de arriba

4. **Crea tu primera oferta**:
   - Ve a "Admin" → "Nueva Oferta"
   - Completa el formulario
   - Sube imágenes
   - Publica

5. **Prueba como usuario**:
   - Cierra sesión (logout)
   - Regístrate como nuevo usuario
   - Explora propiedades
   - Agrega favoritos
   - Envía formulario de contacto

---

## 🛑 Detener el Servidor

Presiona **CTRL + C** en la terminal donde está corriendo el servidor.

---

## 🔧 Comandos Útiles

### Recrear base de datos
```powershell
Remove-Item equahome.db -ErrorAction SilentlyContinue
Remove-Item -Recurse migrations -ErrorAction SilentlyContinue
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db init
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db migrate -m "Initial migration"
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db upgrade
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" create_admin.py
```

### Ver rutas de la aplicación
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask routes
```

### Entrar a shell interactivo
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask shell
```

---

## 📦 Archivos Creados

- ✅ **Base de datos**: `equahome.db` (SQLite)
- ✅ **Migraciones**: `migrations/` 
- ✅ **Admin user**: admin@equahome.gq
- ✅ **Uploads folder**: `app/static/uploads/`

---

## 📚 Documentación Completa

- [README.md](README.md) - Documentación técnica completa
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida
- [walkthrough.md](../.gemini/antigravity/brain/.../walkthrough.md) - Resumen de implementación

---

## ✨ ¡Todo listo!

El sistema EquaHome está completamente funcional y listo para usar.

**Ejecuta ahora**:
```powershell
.\run.ps1
```

Y visita: **http://127.0.0.1:5000**

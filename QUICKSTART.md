# Guía Rápida de Inicio - EquaHome

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Activar entorno virtual
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/Activate.ps1"
```

### 2️⃣ Inicializar base de datos (solo primera vez)
```powershell
.\init_db.ps1
```

### 3️⃣ Ejecutar aplicación
```powershell
.\run.ps1
```

Abrir navegador en: **http://127.0.0.1:5000**

---

## 🔑 Credenciales de Administrador

- **Email**: admin@equahome.gq
- **Contraseña**: admin123

> ⚠️ Cambiar la contraseña después del primer login

---

## 📝 Comandos Útiles

### Instalar dependencias (si es necesario)
```powershell
pip install -r requirements.txt
```

### Recrear base de datos
```powershell
Remove-Item equahome.db -ErrorAction SilentlyContinue
Remove-Item -Recurse migrations -ErrorAction SilentlyContinue
.\init_db.ps1
```

### Poblar con datos de prueba
```powershell
python -m flask seed-db
```

### Ver rutas disponibles
```powershell
python -m flask routes
```

---

## 🌐 Rutas Principales

- **Homepage**: http://127.0.0.1:5000/
- **Alquiler**: http://127.0.0.1:5000/alquiler
- **Venta**: http://127.0.0.1:5000/venta
- **Login**: http://127.0.0.1:5000/auth/login
- **Registro**: http://127.0.0.1:5000/auth/register
- **Admin Dashboard**: http://127.0.0.1:5000/admin/dashboard

---

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```powershell
# Asegúrate de tener el entorno virtual activado
& "c:/PROYECTO SEGIS/.venv/Scripts/Activate.ps1"
pip install -r requirements.txt
```

### Error: "Database not found"
```powershell
.\init_db.ps1
```

### Puerto 5000 ocupado
Editar `run.ps1` y cambiar:
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask run --port 5001
```

---

## 📚 Documentación Completa

Ver [README.md](README.md) para documentación completa.

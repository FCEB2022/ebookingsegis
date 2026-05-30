# Guía de Despliegue en Render.com

## 📦 Archivos Creados para Deployment

Tu proyecto ya tiene todo lo necesario para desplegarse en Render.com:

- ✅ `requirements.txt` - Dependencias de Python
- ✅ `Procfile` - Comando de inicio
- ✅ `build.sh` - Script de construcción
- ✅ `render.yaml` - Configuración de Render
- ✅ `.gitignore` - Archivos a excluir de Git

---

## 🚀 Pasos para Desplegar

### Paso 1: Subir a GitHub

1. **Crea un repositorio en GitHub**:
   - Ve a: https://github.com/new
   - Nombre: `equahome` (o el que prefieras)
   - Visibilidad: Público o Privado
   - NO inicialices con README

2. **Inicializa Git local** (en PowerShell):
   ```powershell
   cd "C:\PROYECTO SEGIS"
   git init
   git add .
   git commit -m "Initial commit - EquaHome v1.0"
   ```

3. **Conecta con GitHub**:
   ```powershell
   git remote add origin https://github.com/TU_USUARIO/equahome.git
   git branch -M main
   git push -u origin main
   ```

---

### Paso 2: Conectar con Render.com

1. **Crea cuenta en Render**:
   - Ve a: https://render.com/
   - Sign up (usa GitHub para login fácil)

2. **Crear nuevo Web Service**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona `equahome`

3. **Configuración automática**:
   - Render detectará `render.yaml`
   - Todo se configurará automáticamente
   - Click en "Create Web Service"

4. **Espera el deploy** (~5 minutos):
   - Verás logs en tiempo real
   - Cuando termine: ✅ "Live"

---

### Paso 3: Obtener tu URL

Una vez desplegado:
```
https://equahome.onrender.com
```

**¡Esta URL es permanente!** Compártela con tus colaboradores.

---

## 🔄 Flujo de Trabajo de Desarrollo

### Para actualizar la app:

1. **Haces cambios localmente**
2. **Commit y push**:
   ```powershell
   git add .
   git commit -m "Descripción de cambios"
   git push
   ```
3. **Auto-deploy**: Render detecta el push y despliega automáticamente
4. **2-3 minutos**: Tus colaboradores ven los cambios

---

## 📊 Monitoreo

### Ver logs en tiempo real:
- Dashboard de Render → Tu servicio → "Logs"

### Métricas:
- CPU, memoria, requests
- Todo visible en tiempo real

---

## 🎯 Ventajas para tu Caso

✅ **Gratis permanentemente**
✅ **URL fija que no cambia**
✅ **Auto-deploy al hacer push**
✅ **Colaboradores ven cambios inmediatamente**
✅ **Base de datos PostgreSQL incluida gratis**
✅ **SSL/HTTPS automático**

---

## ⚙️ Configuración de Producción

El archivo `render.yaml` ya incluye:
- Base de datos PostgreSQL
- Variables de entorno seguras
- Auto-deploy habilitado

---

## 🆘 Solución de Problemas

### Build falla:
- Revisa logs en Render dashboard
- Verifica que `requirements.txt` esté completo

### App no inicia:
- Revisa que `gunicorn` esté en `requirements.txt`
- Verifica el `Procfile`

### Base de datos:
- Render migra automáticamente de SQLite a PostgreSQL
- El `build.sh` crea las tablas

---

## 📝 Notas

- **Primer deploy**: ~5-7 minutos
- **Deploys posteriores**: ~2-3 minutos
- **Inactividad**: App se "duerme" tras 15 min sin uso
- **Despertar**: ~60 segundos en primera visita

---

## 🔗 Enlaces Útiles

- **Dashboard**: https://dashboard.render.com/
- **Docs**: https://render.com/docs
- **Status**: https://status.render.com/

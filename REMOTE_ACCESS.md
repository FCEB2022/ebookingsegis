# EquaHome - Acceso Remoto con ngrok

## 🌍 Opciones para Acceso Remoto

### Opción 1: Script Python Automático (Recomendado)

**Paso 1: Instalar pyngrok**
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/pip.exe" install pyngrok
```

**Paso 2: Configurar authtoken (opcional pero recomendado)**
1. Crea cuenta en: https://dashboard.ngrok.com/signup
2. Copia tu authtoken
3. Ejecuta:
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m pyngrok config add-authtoken TU_TOKEN_AQUI
```

**Paso 3: Ejecutar**
```powershell
cd "c:/PROYECTO SEGIS"
& "./.venv/Scripts/python.exe" "run_with_ngrok.py"
```

La URL pública aparecerá en la consola. ¡Compártela con quien quieras!

---

### Opción 2: Script PowerShell

**Paso 1: Descargar ngrok**
1. Ve a: https://ngrok.com/download
2. Descarga ngrok para Windows
3. Extrae `ngrok.exe` a `C:\ngrok\`

**Paso 2: Configurar authtoken** (mismo que arriba)

**Paso 3: Ejecutar el script**
```powershell
cd "c:/PROYECTO SEGIS"
.\start_remote.ps1
```

---

### Opción 3: Manual (Dos terminales)

**Terminal 1 - Flask:**
```powershell
cd "c:/PROYECTO SEGIS"
& "./.venv/Scripts/python.exe" "run.py"
```

**Terminal 2 - ngrok:**
```powershell
C:\ngrok\ngrok.exe http 5000
```

---

## 📋 Cómo Compartir

1. Ejecuta cualquiera de las opciones anteriores
2. Copia la URL que empieza con `https://....ngrok-free.app`
3. Compártela con quien quieras
4. ¡Listo! Pueden acceder desde cualquier parte del mundo

## ⚠️ Notas Importantes

- **Cuenta Gratuita**: URL aleatoria que cambia cada vez
- **Límites**: 40 conexiones/minuto en plan gratuito
- **Seguridad**: No expongas datos sensibles sin autenticación
- **Producción**: Para uso comercial, considera un servidor en la nube

## 🔧 Solución de Problemas

**Error: "pyngrok no encontrado"**
```powershell
& "c:/PROYECTO SEGIS/.venv/Scripts/pip.exe" install pyngrok
```

**Error: "ngrok.exe no encontrado"**
- Descarga de: https://ngrok.com/download
- Extrae a: `C:\ngrok\`
- O ajusta la ruta en `start_remote.ps1`

**Página muestra "Visit Site"**
- Es normal en plan gratuito
- Click en "Visit Site" para continuar
- O configura authtoken para evitarlo

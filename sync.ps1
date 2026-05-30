# Script para sincronizar cambios con GitHub automáticamente
# Uso: .\sync.ps1 "Mensaje del cambio"

param (
    [string]$Message = "Actualización automática"
)

Write-Host "🔄 Sincronizando con GitHub..." -ForegroundColor Cyan

# Agregar todos los cambios
git add .

# Commit
git commit -m "$Message"

# Push
git push origin main

if ($?) {
    Write-Host "✅ Cambios subidos correctamente a GitHub" -ForegroundColor Green
}
else {
    Write-Host "❌ Error al subir cambios. Verifica tu conexión o credenciales." -ForegroundColor Red
}

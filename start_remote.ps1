# Script PowerShell para iniciar Flask con ngrok
# Asegúrate de tener ngrok descargado en C:\ngrok\ngrok.exe

Write-Host "🚀 Iniciando EquaHome con acceso remoto..." -ForegroundColor Green
Write-Host ""

# Ruta a ngrok (ajusta si está en otra ubicación)
$ngrokPath = "C:\ngrok\ngrok.exe"

# Verificar si ngrok existe
if (-not (Test-Path $ngrokPath)) {
    Write-Host "❌ ngrok no encontrado en $ngrokPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Descarga ngrok de: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "📁 Extrae ngrok.exe a: C:\ngrok\" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit
}

# Iniciar Flask en segundo plano
Write-Host "▶️  Iniciando servidor Flask..." -ForegroundColor Cyan
$flaskJob = Start-Job -ScriptBlock {
    Set-Location "c:/PROYECTO SEGIS"
    & "./.venv/Scripts/python.exe" "run.py"
}

# Esperar 3 segundos para que Flask inicie
Start-Sleep -Seconds 3

# Iniciar ngrok
Write-Host "🌍 Creando túnel ngrok..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ Servidor listo!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""
Write-Host "📋 La URL pública aparecerá en la ventana de ngrok" -ForegroundColor Yellow
Write-Host "⚠️  Presiona Ctrl+C en la ventana de ngrok para detener" -ForegroundColor Yellow
Write-Host ""

# Ejecutar ngrok (esto abrirá una nueva ventana)
& $ngrokPath http 5000

# Cuando ngrok se cierra, detener Flask
Write-Host ""
Write-Host "🛑 Deteniendo servidor Flask..." -ForegroundColor Cyan
Stop-Job -Job $flaskJob
Remove-Job -Job $flaskJob
Write-Host "✅ Servidor detenido" -ForegroundColor Green

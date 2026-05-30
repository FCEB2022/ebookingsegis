# Script para ejecutar la aplicación Flask
# Ejecutar con el entorno virtual activado

Write-Host "=== Iniciando EquaHome ===" -ForegroundColor Green
Write-Host "Servidor Flask iniciando en http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Presiona CTRL+C para detener el servidor`n" -ForegroundColor Yellow

# Configurar variables de entorno
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"

# Ejecutar la aplicación
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask run

# Script de inicialización de la base de datos
# Ejecutar con el entorno virtual activado

Write-Host "=== Inicializando Base de Datos EquaHome ===" -ForegroundColor Green

# 1. Inicializar Flask-Migrate
Write-Host "`n1. Inicializando Flask-Migrate..." -ForegroundColor Yellow
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db init
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Flask-Migrate inicializado" -ForegroundColor Green
} else {
    Write-Host "   (Ya existe o error - continuando...)" -ForegroundColor Gray
}

# 2. Crear migración inicial
Write-Host "`n2. Creando migración inicial..." -ForegroundColor Yellow
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db migrate -m "Initial migration"
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Migración creada" -ForegroundColor Green
} else {
    Write-Host "   ! Error en migración" -ForegroundColor Red
}

# 3. Aplicar migración
Write-Host "`n3. Aplicando migración..." -ForegroundColor Yellow
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask db upgrade
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Base de datos creada" -ForegroundColor Green
} else {
    Write-Host "   ! Error aplicando migración" -ForegroundColor Red
}

# 4. Crear usuario administrador
Write-Host "`n4. Creando usuario administrador..." -ForegroundColor Yellow
& "c:/PROYECTO SEGIS/.venv/Scripts/python.exe" -m flask create-admin
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Admin creado" -ForegroundColor Green
} else {
    Write-Host "   ! Error creando admin" -ForegroundColor Red
}

Write-Host "`n=== Inicialización Completada ===" -ForegroundColor Green
Write-Host "`nCredenciales de acceso:" -ForegroundColor Cyan
Write-Host "  Email: admin@equahome.gq" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host "`nPara iniciar la aplicación ejecuta:" -ForegroundColor Cyan
Write-Host "  .\run.ps1" -ForegroundColor White

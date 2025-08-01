# ANCAP RSS Reader PowerShell Launcher
# ANCAP RSS Reader Launcher Script para Windows PowerShell

# Obtener directorio del script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    python scripts/setup.py
}

# Activar entorno virtual y ejecutar la aplicación
if (Test-Path "venv\Scripts\python.exe") {
    & ".\venv\Scripts\python" "ancap_rss.py" $args
} else {
    Write-Host "Error: Virtual environment not properly configured" -ForegroundColor Red
    Write-Host "Please run: python scripts/setup.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

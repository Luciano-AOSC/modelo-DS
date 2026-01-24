@echo off
REM ========================================
REM FlightOnTime API - Script de Inicio
REM ========================================
setlocal

echo.
echo ======================================
echo  FLIGHTONTIME API - Iniciando...
echo ======================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encuentra main.py
    echo Asegurate de estar en la carpeta backend/
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
if not exist ".venv\\Scripts\\python.exe" (
    echo.
    echo  Creando entorno virtual...
    python -m venv .venv
)
set VENV_PY=.venv\\Scripts\\python.exe
set PYTHONIOENCODING=utf-8
%VENV_PY% -m pip install -r requirements.txt

echo [2/3] Verificando modelo...
if not exist "..\models\model.joblib" (
    echo.
    echo ERROR: Modelo no encontrado
    echo Ejecuta primero: python ..\train_model.py
    pause
    exit /b 1
)

echo [3/3] Iniciando API...
echo.
echo ======================================
echo  API corriendo en:
echo  http://localhost:8000
echo.
echo  Documentacion:
echo  http://localhost:8000/docs
echo ======================================
echo.
echo Presiona Ctrl+C para detener
echo.

%VENV_PY% main.py

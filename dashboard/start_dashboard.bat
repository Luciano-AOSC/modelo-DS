@echo off
REM ========================================
REM FlightOnTime Dashboard - Script Inicio
REM ========================================
setlocal

echo.
echo ======================================
echo  FLIGHTONTIME DASHBOARD - Iniciando...
echo ======================================
echo.

echo [1/3] Verificando dependencias...
if not exist ".venv\\Scripts\\python.exe" (
    echo.
    echo  Creando entorno virtual...
    python -m venv .venv
)
set VENV_PY=.venv\\Scripts\\python.exe
set PYTHONIOENCODING=utf-8
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
%VENV_PY% -m pip install -r requirements.txt

echo [2/3] Verificando estructura...
if not exist "app.py" (
    echo.
    echo ERROR: app.py no encontrado
    pause
    exit /b 1
)

echo [3/3] Iniciando dashboard...
echo.
echo ======================================
echo  Dashboard corriendo en:
echo  http://localhost:8501
echo.
echo  Navegacion:
echo  - Dashboard Principal
echo  - ROI Calculator
echo  - Predictive Simulator
echo  - 3D Routes Map
echo ======================================
echo.
echo Presiona Ctrl+C para detener
echo.

%VENV_PY% -m streamlit run app.py

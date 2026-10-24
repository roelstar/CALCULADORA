@echo off
title ROELSTAR TRADING - Evaluador de Rentabilidad
cd /d "%~dp0"

echo ==============================================
echo   ROELSTAR TRADING
echo   Evaluador de Rentabilidad e Inversiones
echo ==============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: No se encontro Python instalado.
    echo Instala Python desde https://www.python.org/downloads/
    echo Durante la instalacion marca "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if not exist "evaluador_rentabilidad.py" (
    echo ERROR: No se encontro evaluador_rentabilidad.py en esta carpeta.
    echo Deja este archivo BAT junto al archivo Python y el logo.
    echo.
    pause
    exit /b 1
)

if not exist "roelstar_logo.png" (
    echo AVISO: No se encontro roelstar_logo.png en esta carpeta.
    echo La aplicacion podria abrir sin mostrar el logo.
    echo.
)

python -m pip show streamlit >nul 2>nul
if errorlevel 1 (
    echo Instalando Streamlit por primera vez...
    python -m pip install streamlit
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo instalar Streamlit.
        pause
        exit /b 1
    )
)

echo Iniciando ROELSTAR...
echo Cuando termine de iniciar, se abrira en el navegador.
echo Para cerrar la aplicacion, vuelve a esta ventana y presiona Ctrl+C.
echo.
python -m streamlit run evaluador_rentabilidad.py

echo.
echo La aplicacion se ha detenido.
pause

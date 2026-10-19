@echo off
REM ============================================================
REM Steer Metabolic Engine - Windows One-Click Setup
REM ============================================================

echo.
echo ============================================================
echo   Setting up Steer Metabolic Engine (Windows)...
echo ============================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found on PATH. Please install Python 3.10+ from python.org.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

python setup_pipeline.py

echo.
echo ============================================================
echo  Setup finished! Run 'python run_pipeline.py --serve' to start.
echo ============================================================
echo.
pause

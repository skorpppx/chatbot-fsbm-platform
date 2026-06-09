@echo off
REM ============================================================================
REM  FSBM Platform — Installation complete (Windows)
REM  Installe les dépendances Python pour les micro-services + npm pour Angular
REM ============================================================================
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

echo ================================================================
echo   FSBM Platform — Installation complete
echo ================================================================
echo.

set ROOT=%~dp0..

echo [1/3] Installation des dependances chatbot-service...
cd /d "%ROOT%\services\chatbot-service"
if not exist venv (
    py -m venv venv
)
call venv\Scripts\activate.bat
py -m pip install --upgrade pip
pip install -r requirements.txt
call deactivate

echo.
echo [2/3] Installation des dependances academic-service...
cd /d "%ROOT%\services\academic-service"
if not exist venv (
    py -m venv venv
)
call venv\Scripts\activate.bat
py -m pip install --upgrade pip
pip install -r requirements.txt
call deactivate

echo.
echo [3/3] Installation des dependances frontend Angular...
cd /d "%ROOT%\frontend"
call npm install

echo.
echo ================================================================
echo   ✅ Installation terminee
echo ================================================================
echo.
echo Prochaines etapes :
echo   1. Configurer .env dans chaque service (copier .env.example)
echo   2. Charger la base MySQL ^(voir README.md^)
echo   3. Lancer : scripts\start-all.bat
echo ================================================================
pause

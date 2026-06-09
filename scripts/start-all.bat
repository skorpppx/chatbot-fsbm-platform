@echo off
REM ============================================================================
REM  FSBM Platform — Demarrage des services (Windows)
REM  3 fenetres : chatbot-service + academic-service + frontend Angular
REM ============================================================================
setlocal
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

set ROOT=%~dp0..

echo ================================================================
echo   FSBM Platform — Demarrage des services
echo ================================================================
echo.
echo Trois fenetres vont s'ouvrir :
echo   - chatbot-service  : http://localhost:5001
echo   - academic-service : http://localhost:5002
echo   - frontend Angular : http://localhost:4200
echo.
echo Pour arreter : Ctrl+C dans chaque fenetre.
echo ================================================================
echo.

start "FSBM-chatbot-service :5001" cmd /k "set PYTHONIOENCODING=utf-8 && cd /d ""%ROOT%\services\chatbot-service"" && py -m uvicorn app.main:app --reload --port 5001"

timeout /t 2 /nobreak >nul

start "FSBM-academic-service :5002" cmd /k "set PYTHONIOENCODING=utf-8 && cd /d ""%ROOT%\services\academic-service"" && py -m uvicorn app.main:app --reload --port 5002"

timeout /t 2 /nobreak >nul

start "FSBM-frontend :4200" cmd /k "cd /d ""%ROOT%\frontend"" && npm start"

echo ✅ Demarrage en cours...
echo Patientez 10-20 secondes que tout soit pret.
echo Le frontend ouvrira automatiquement http://localhost:4200
pause

@echo off
REM ============================================================================
REM  FSBM Platform — Configuration interactive des fichiers .env
REM  Demande le mot de passe MySQL et configure les 2 services
REM ============================================================================
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ================================================================
echo   FSBM Platform — Configuration des fichiers .env
echo ================================================================
echo.

set ROOT=%~dp0..

set /p MYSQL_USER=Utilisateur MySQL [defaut: root]:
if "!MYSQL_USER!"=="" set MYSQL_USER=root

set /p MYSQL_PWD=Mot de passe MySQL :
echo.

REM ─── Generer .env pour academic-service ─────────────────────────────────────
echo SERVICE_NAME=academic-service> "!ROOT!\services\academic-service\.env"
echo SERVICE_PORT=5002>> "!ROOT!\services\academic-service\.env"
echo ENV=development>> "!ROOT!\services\academic-service\.env"
echo DEBUG=true>> "!ROOT!\services\academic-service\.env"
echo DB_HOST=localhost>> "!ROOT!\services\academic-service\.env"
echo DB_PORT=3306>> "!ROOT!\services\academic-service\.env"
echo DB_NAME=fsbm_db>> "!ROOT!\services\academic-service\.env"
echo DB_USER=!MYSQL_USER!>> "!ROOT!\services\academic-service\.env"
echo DB_PASSWORD=!MYSQL_PWD!>> "!ROOT!\services\academic-service\.env"
echo CORS_ORIGINS=http://localhost:4200,http://localhost:5001>> "!ROOT!\services\academic-service\.env"
echo ✅ .env cree pour academic-service

REM ─── Generer .env pour chatbot-service ─────────────────────────────────────
echo SERVICE_NAME=chatbot-service> "!ROOT!\services\chatbot-service\.env"
echo SERVICE_PORT=5001>> "!ROOT!\services\chatbot-service\.env"
echo ENV=development>> "!ROOT!\services\chatbot-service\.env"
echo DEBUG=true>> "!ROOT!\services\chatbot-service\.env"
echo DB_HOST=localhost>> "!ROOT!\services\chatbot-service\.env"
echo DB_PORT=3306>> "!ROOT!\services\chatbot-service\.env"
echo DB_NAME=fsbm_db>> "!ROOT!\services\chatbot-service\.env"
echo DB_USER=!MYSQL_USER!>> "!ROOT!\services\chatbot-service\.env"
echo DB_PASSWORD=!MYSQL_PWD!>> "!ROOT!\services\chatbot-service\.env"
echo ACADEMIC_SERVICE_URL=http://localhost:5002>> "!ROOT!\services\chatbot-service\.env"
echo CONFIDENCE_THRESHOLD=0.15>> "!ROOT!\services\chatbot-service\.env"
echo MAX_HISTORY_MESSAGES=20>> "!ROOT!\services\chatbot-service\.env"
echo MAX_MESSAGE_LENGTH=500>> "!ROOT!\services\chatbot-service\.env"
echo CORS_ORIGINS=http://localhost:4200,http://localhost:3000>> "!ROOT!\services\chatbot-service\.env"
echo ✅ .env cree pour chatbot-service

echo.
echo ================================================================
echo   ✅ Configuration terminee
echo ================================================================
echo.
echo Tu peux maintenant lancer les services :
echo   scripts\start-all.bat
echo.
pause

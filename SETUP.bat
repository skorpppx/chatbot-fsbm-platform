@echo off
REM ============================================================================
REM  FSBM Platform — Setup ONE-CLICK
REM  Tout-en-un : config .env + install deps + init DB + lance les services
REM  Demande UNIQUEMENT le mot de passe MySQL
REM ============================================================================
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

cls
echo.
echo ================================================================
echo.
echo   ╔═══════════════════════════════════════════════════════════╗
echo   ║                                                           ║
echo   ║       🎓  FSBM Platform — Setup One-Click  🎓            ║
echo   ║                                                           ║
echo   ║   Faculté des Sciences Ben M'Sick — PFE 2025/2026         ║
echo   ║                                                           ║
echo   ╚═══════════════════════════════════════════════════════════╝
echo.
echo ================================================================
echo.
echo Ce script va :
echo   [1] Configurer les fichiers .env (mot de passe MySQL)
echo   [2] Installer les dependances Python (FastAPI, etc.)
echo   [3] Installer les dependances npm (Angular)
echo   [4] Initialiser la base MySQL (schema + donnees seed)
echo   [5] Lancer les 3 services (chatbot, academic, frontend)
echo.
echo ================================================================
echo.

REM ─── Detection MySQL ───────────────────────────────────────────────────────
set MYSQL_EXE=
for %%P in (
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
    "C:\xampp\mysql\bin\mysql.exe"
    "C:\wamp64\bin\mysql\mysql8.0.31\bin\mysql.exe"
    "C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe"
) do (
    if exist %%P (
        set "MYSQL_EXE=%%~P"
        goto :mysql_found
    )
)
where mysql >nul 2>&1
if !errorlevel! == 0 (
    set MYSQL_EXE=mysql
    goto :mysql_found
)
echo ❌ MySQL non trouve. Installe MySQL 8.0+ et relance ce script.
pause
exit /b 1

:mysql_found
echo ✅ MySQL detecte : !MYSQL_EXE!
echo.

REM ─── Demande mot de passe ──────────────────────────────────────────────────
set /p MYSQL_PWD=🔑 Entre ton mot de passe MySQL (utilisateur root) :
echo.

set ROOT=%~dp0
set "ROOT=%ROOT:~0,-1%"

REM ─── ÉTAPE 1 : Configurer .env ─────────────────────────────────────────────
echo ----------------------------------------------------------------
echo [1/5] Configuration des fichiers .env
echo ----------------------------------------------------------------

(
echo SERVICE_NAME=academic-service
echo SERVICE_PORT=5002
echo ENV=development
echo DEBUG=true
echo DB_HOST=localhost
echo DB_PORT=3306
echo DB_NAME=fsbm_db
echo DB_USER=root
echo DB_PASSWORD=!MYSQL_PWD!
echo CORS_ORIGINS=http://localhost:4200,http://localhost:5001
) > "%ROOT%\services\academic-service\.env"
echo    ✅ .env cree pour academic-service

(
echo SERVICE_NAME=chatbot-service
echo SERVICE_PORT=5001
echo ENV=development
echo DEBUG=true
echo DB_HOST=localhost
echo DB_PORT=3306
echo DB_NAME=fsbm_db
echo DB_USER=root
echo DB_PASSWORD=!MYSQL_PWD!
echo ACADEMIC_SERVICE_URL=http://localhost:5002
echo CONFIDENCE_THRESHOLD=0.15
echo MAX_HISTORY_MESSAGES=20
echo MAX_MESSAGE_LENGTH=500
echo CORS_ORIGINS=http://localhost:4200,http://localhost:3000
) > "%ROOT%\services\chatbot-service\.env"
echo    ✅ .env cree pour chatbot-service

REM ─── ÉTAPE 2 : Installer Python deps ───────────────────────────────────────
echo.
echo ----------------------------------------------------------------
echo [2/5] Installation des dependances Python
echo ----------------------------------------------------------------
echo    📦 academic-service ...
py -m pip install -q -r "%ROOT%\services\academic-service\requirements.txt" 2>nul
echo    📦 chatbot-service ...
py -m pip install -q -r "%ROOT%\services\chatbot-service\requirements.txt" 2>nul
echo    ✅ Dependances Python OK

REM ─── ÉTAPE 3 : Installer npm deps ──────────────────────────────────────────
echo.
echo ----------------------------------------------------------------
echo [3/5] Installation des dependances Angular (peut prendre 1-2 min)
echo ----------------------------------------------------------------
cd /d "%ROOT%\frontend"
if not exist node_modules (
    call npm install --silent 2>nul
) else (
    echo    ⏭️  node_modules existe deja
)
echo    ✅ Dependances Angular OK
cd /d "%ROOT%"

REM ─── ÉTAPE 4 : Initialiser MySQL ───────────────────────────────────────────
echo.
echo ----------------------------------------------------------------
echo [4/5] Initialisation de la base MySQL (fsbm_db)
echo ----------------------------------------------------------------
set MYSQL_DIR=%ROOT%\database\mysql

REM Regenerer les donnees si necessaire
if not exist "!MYSQL_DIR!\04_seed_data.sql" (
    echo    🔄 Generation des donnees seed (~3000 etudiants^)...
    cd /d "%ROOT%\database\seed"
    py generate_data.py >nul 2>&1
    cd /d "%ROOT%"
)

echo    📥 01_schema.sql ...
"!MYSQL_EXE!" -u root -p!MYSQL_PWD! < "!MYSQL_DIR!\01_schema.sql" 2>nul
if errorlevel 1 (
    echo    ❌ Echec de la connexion MySQL. Verifie le mot de passe.
    pause
    exit /b 1
)
echo    📥 02_seed_static.sql ...
"!MYSQL_EXE!" -u root -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\02_seed_static.sql" 2>nul
echo    📥 03_seed_modules.sql ...
"!MYSQL_EXE!" -u root -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\03_seed_modules.sql" 2>nul
echo    📥 04_seed_data.sql (peut prendre 30s^) ...
"!MYSQL_EXE!" -u root -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\04_seed_data.sql" 2>nul
echo    ✅ Base MySQL initialisee

REM ─── ÉTAPE 5 : Verification + Lancement ────────────────────────────────────
echo.
echo ----------------------------------------------------------------
echo [5/5] Verification + Lancement des services
echo ----------------------------------------------------------------
echo.
echo Statistiques de la base :
"!MYSQL_EXE!" -u root -p!MYSQL_PWD! -e "USE fsbm_db; SELECT 'Departements' AS Table_, COUNT(*) AS Count_ FROM departments UNION ALL SELECT 'Filieres', COUNT(*) FROM filieres UNION ALL SELECT 'Modules', COUNT(*) FROM modules UNION ALL SELECT 'Professeurs', COUNT(*) FROM professors UNION ALL SELECT 'Etudiants', COUNT(*) FROM students;" 2>nul

echo.
echo ----------------------------------------------------------------
echo   ✅ SETUP TERMINE — Lancement des 3 services...
echo ----------------------------------------------------------------
echo.

start "FSBM-academic :5002" cmd /k "set PYTHONIOENCODING=utf-8 && cd /d ""%ROOT%\services\academic-service"" && py -m uvicorn app.main:app --reload --port 5002"
timeout /t 3 /nobreak >nul

start "FSBM-chatbot :5001" cmd /k "set PYTHONIOENCODING=utf-8 && cd /d ""%ROOT%\services\chatbot-service"" && py -m uvicorn app.main:app --reload --port 5001"
timeout /t 3 /nobreak >nul

start "FSBM-frontend :4200" cmd /k "cd /d ""%ROOT%\frontend"" && npm start"

echo.
echo ================================================================
echo   🚀 SERVICES LANCES — Patiente 15-30 secondes
echo ================================================================
echo.
echo   🤖 Chatbot   API : http://localhost:5001/docs
echo   🎓 Academic  API : http://localhost:5002/docs
echo   🎨 Frontend  UI  : http://localhost:4200
echo.
echo Ouvre ton navigateur sur http://localhost:4200 dans 30 secondes.
echo ================================================================
pause

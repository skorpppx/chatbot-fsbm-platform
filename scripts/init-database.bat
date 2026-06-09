@echo off
REM ============================================================================
REM  FSBM Platform — Initialisation MySQL (auto-detection)
REM  Detecte MySQL meme s'il n'est pas dans le PATH
REM ============================================================================
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ================================================================
echo   FSBM Platform — Initialisation MySQL
echo ================================================================
echo.

REM ─── Auto-detection du client mysql.exe ────────────────────────────────────
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
        goto :found
    )
)

REM Verifier si mysql est dans le PATH
where mysql >nul 2>&1
if !errorlevel! == 0 (
    set MYSQL_EXE=mysql
    goto :found
)

echo ❌ MySQL non trouve. Verifiez l'installation.
echo.
echo Emplacements verifies :
echo   - C:\Program Files\MySQL\MySQL Server X.X\bin\
echo   - C:\xampp\mysql\bin\
echo   - C:\wamp64\bin\mysql\
echo   - C:\laragon\bin\mysql\
echo   - PATH systeme
pause
exit /b 1

:found
echo ✅ Client MySQL trouve :
echo    !MYSQL_EXE!
echo.

set /p MYSQL_USER=Utilisateur MySQL [defaut: root]:
if "!MYSQL_USER!"=="" set MYSQL_USER=root

set /p MYSQL_PWD=Mot de passe MySQL :

set ROOT=%~dp0..
set MYSQL_DIR=!ROOT!\database\mysql

echo.
echo [1/4] Creation du schema fsbm_db...
"!MYSQL_EXE!" -u !MYSQL_USER! -p!MYSQL_PWD! < "!MYSQL_DIR!\01_schema.sql"
if errorlevel 1 goto :error

echo [2/4] Donnees statiques ^(departements, filieres, masters^)...
"!MYSQL_EXE!" -u !MYSQL_USER! -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\02_seed_static.sql"
if errorlevel 1 goto :error

echo [3/4] Modules...
"!MYSQL_EXE!" -u !MYSQL_USER! -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\03_seed_modules.sql"
if errorlevel 1 goto :error

echo [4/4] Donnees generees ^(profs + etudiants^)...
if not exist "!MYSQL_DIR!\04_seed_data.sql" (
    echo Generation du fichier 04_seed_data.sql en cours...
    set PYTHONIOENCODING=utf-8
    cd /d "!ROOT!\database\seed"
    py generate_data.py
)
"!MYSQL_EXE!" -u !MYSQL_USER! -p!MYSQL_PWD! fsbm_db < "!MYSQL_DIR!\04_seed_data.sql"
if errorlevel 1 goto :error

echo.
echo ================================================================
echo   ✅ Base MySQL initialisee avec succes : fsbm_db
echo ================================================================
echo.
echo Verification rapide :
"!MYSQL_EXE!" -u !MYSQL_USER! -p!MYSQL_PWD! -e "USE fsbm_db; SELECT COUNT(*) AS departments FROM departments; SELECT COUNT(*) AS filieres FROM filieres; SELECT COUNT(*) AS modules FROM modules; SELECT COUNT(*) AS professors FROM professors; SELECT COUNT(*) AS students FROM students;"
echo.
pause
exit /b 0

:error
echo.
echo ❌ Erreur lors de l'execution d'un script SQL
echo Verifiez les credentials et l'etat du serveur MySQL.
pause
exit /b 1

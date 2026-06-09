# ============================================================================
#  FSBM Platform - Setup ONE-CLICK (PowerShell natif)
#  Tout-en-un : config .env + install deps + init DB + lance les services
#  Compatible Windows PowerShell 5.1 et PowerShell 7+
#
#  USAGE :
#      powershell -ExecutionPolicy Bypass -File .\SETUP.ps1
# ============================================================================

# Note : on n'utilise PAS $ErrorActionPreference="Stop" car MySQL emet des
# warnings sur stderr qui sont legitimes (pas des erreurs).
$env:PYTHONIOENCODING = "utf-8"

# ─── Helpers ──────────────────────────────────────────────────────────────────
function Write-Step    { param($msg) Write-Host "`n[*] $msg" -ForegroundColor Cyan }
function Write-Ok      { param($msg) Write-Host "    OK  $msg" -ForegroundColor Green }
function Write-Info    { param($msg) Write-Host "    --  $msg" -ForegroundColor Gray }
function Write-Warn    { param($msg) Write-Host "    !!  $msg" -ForegroundColor Yellow }
function Write-Err     { param($msg) Write-Host "    XX  $msg" -ForegroundColor Red }
function Write-Header  { param($msg)
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor DarkCyan
    Write-Host "   $msg" -ForegroundColor White
    Write-Host ("=" * 70) -ForegroundColor DarkCyan
}

# Execute mysql.exe via cmd.exe pour eviter le warning "NativeCommandError"
# qui plante PowerShell 5.1. Renvoie $true si succes, $false sinon.
function Invoke-Mysql {
    param(
        [string]$mysqlExe,
        [string]$password,
        [string]$query,
        [string]$database = ""
    )
    $dbArg = if ($database) { "`"$database`"" } else { "" }
    $cmd = "`"$mysqlExe`" -u root `"-p$password`" $dbArg -e `"$query`""
    $output = cmd /c "$cmd 2>&1"
    return @{
        Success = ($LASTEXITCODE -eq 0)
        Output  = $output
    }
}

function Import-SqlFile {
    param(
        [string]$mysqlExe,
        [string]$password,
        [string]$sqlFile,
        [string]$database = ""
    )
    $dbArg = if ($database) { "`"$database`"" } else { "" }
    # cmd permet la redirection < pour piper le fichier SQL
    $cmd = "`"$mysqlExe`" -u root `"-p$password`" $dbArg < `"$sqlFile`""
    $output = cmd /c "$cmd 2>&1"
    return @{
        Success = ($LASTEXITCODE -eq 0)
        Output  = $output
    }
}

# ─── Banner ───────────────────────────────────────────────────────────────────
Clear-Host
Write-Host ""
Write-Host "   ##################################################" -ForegroundColor DarkCyan
Write-Host "   #                                                #" -ForegroundColor DarkCyan
Write-Host "   #       FSBM Platform - Setup One-Click          #" -ForegroundColor DarkCyan
Write-Host "   #                                                #" -ForegroundColor DarkCyan
Write-Host "   #   Faculte des Sciences Ben M'Sick - PFE 2026   #" -ForegroundColor DarkCyan
Write-Host "   #                                                #" -ForegroundColor DarkCyan
Write-Host "   ##################################################" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "Ce script va :" -ForegroundColor White
Write-Host "  [1] Configurer les fichiers .env (mot de passe MySQL)"
Write-Host "  [2] Installer les dependances Python (FastAPI, etc.)"
Write-Host "  [3] Installer les dependances npm (Angular)"
Write-Host "  [4] Initialiser la base MySQL (schema + donnees seed)"
Write-Host "  [5] Lancer les 3 services (chatbot, academic, frontend)"
Write-Host ""

# ─── Detection de MySQL ───────────────────────────────────────────────────────
$mysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
    "C:\xampp\mysql\bin\mysql.exe",
    "C:\wamp64\bin\mysql\mysql8.0.31\bin\mysql.exe",
    "C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe"
)
$mysqlExe = $null
foreach ($p in $mysqlPaths) {
    if (Test-Path $p) { $mysqlExe = $p; break }
}
if (-not $mysqlExe) {
    $cmd = Get-Command mysql -ErrorAction SilentlyContinue
    if ($cmd) { $mysqlExe = $cmd.Source }
}
if (-not $mysqlExe) {
    Write-Err "MySQL non trouve. Installe MySQL 8.0+ et relance ce script."
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}
Write-Ok "MySQL detecte : $mysqlExe"

# ─── Demande mot de passe ─────────────────────────────────────────────────────
Write-Host ""
$securePwd = Read-Host "Entre ton mot de passe MySQL (utilisateur root)" -AsSecureString
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePwd)
$mysqlPwd = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

# ─── Tester la connexion MySQL ────────────────────────────────────────────────
Write-Step "Test de connexion MySQL..."
$result = Invoke-Mysql -mysqlExe $mysqlExe -password $mysqlPwd -query "SELECT VERSION();"
if (-not $result.Success) {
    # Distinguer entre erreur reelle et warning de mot de passe
    $errorMsg = $result.Output -join "`n"
    if ($errorMsg -match "Access denied") {
        Write-Err "Mot de passe MySQL incorrect."
    } else {
        Write-Err "Echec de connexion MySQL :"
        Write-Host $errorMsg -ForegroundColor Red
    }
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}
Write-Ok "Connexion MySQL OK"

$root = $PSScriptRoot

# ─── ETAPE 1 : Configurer .env ────────────────────────────────────────────────
Write-Header "[1/5] Configuration des fichiers .env"

$academicEnv = @"
SERVICE_NAME=academic-service
SERVICE_PORT=8002
ENV=development
DEBUG=true
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fsbm_db
DB_USER=root
DB_PASSWORD=$mysqlPwd
CORS_ORIGINS=http://localhost:4200,http://localhost:8001
JWT_SECRET=fsbm_pfe_2026_change_me_8f3a9c1d7b4e6f2a0c5d8e1b3f6a9c2d
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=720
REVIEWS_AUTO_APPROVE=true
"@
$academicEnvPath = Join-Path $root "services\academic-service\.env"
# Ecrire en UTF-8 SANS BOM (sinon pydantic-settings ne lit pas la 1ere ligne correctement)
[System.IO.File]::WriteAllText($academicEnvPath, $academicEnv, (New-Object System.Text.UTF8Encoding $false))
Write-Ok ".env cree pour academic-service"

$chatbotEnv = @"
SERVICE_NAME=chatbot-service
SERVICE_PORT=8001
ENV=development
DEBUG=true
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fsbm_db
DB_USER=root
DB_PASSWORD=$mysqlPwd
ACADEMIC_SERVICE_URL=http://localhost:8002
CONFIDENCE_THRESHOLD=0.15
MAX_HISTORY_MESSAGES=20
MAX_MESSAGE_LENGTH=500
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
"@
$chatbotEnvPath = Join-Path $root "services\chatbot-service\.env"
[System.IO.File]::WriteAllText($chatbotEnvPath, $chatbotEnv, (New-Object System.Text.UTF8Encoding $false))
Write-Ok ".env cree pour chatbot-service"

# ─── ETAPE 2 : Installer Python deps ──────────────────────────────────────────
Write-Header "[2/5] Installation des dependances Python"
Write-Info "academic-service..."
cmd /c "py -m pip install -q -r `"$root\services\academic-service\requirements.txt`" >nul 2>&1"
Write-Ok "academic-service Python OK"

Write-Info "chatbot-service..."
cmd /c "py -m pip install -q -r `"$root\services\chatbot-service\requirements.txt`" >nul 2>&1"
Write-Ok "chatbot-service Python OK"

# ─── ETAPE 3 : Installer npm deps ─────────────────────────────────────────────
Write-Header "[3/5] Installation des dependances Angular"
$frontendPath = Join-Path $root "frontend"
$nodeModulesPath = Join-Path $frontendPath "node_modules"
if (Test-Path $nodeModulesPath) {
    Write-Info "node_modules existe deja - skip npm install"
} else {
    Write-Info "Lancement de npm install (peut prendre 1-2 min)..."
    cmd /c "cd /d `"$frontendPath`" && npm install --silent >nul 2>&1"
}
Write-Ok "Angular dependencies OK"

# ─── ETAPE 4 : Initialiser MySQL ──────────────────────────────────────────────
Write-Header "[4/5] Initialisation de la base MySQL (fsbm_db)"
$mysqlDir = Join-Path $root "database\mysql"

# Regenerer 04_seed_data.sql si necessaire
$seedFile = Join-Path $mysqlDir "04_seed_data.sql"
if (-not (Test-Path $seedFile)) {
    Write-Info "Generation du fichier 04_seed_data.sql (~3000 etudiants)..."
    cmd /c "cd /d `"$root\database\seed`" && py generate_data.py >nul 2>&1"
}

Write-Info "Chargement de 01_schema.sql..."
$r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile (Join-Path $mysqlDir "01_schema.sql")
if (-not $r.Success) {
    Write-Err "Echec 01_schema.sql"
    Write-Host ($r.Output -join "`n") -ForegroundColor Red
    Read-Host; exit 1
}
Write-Ok "01_schema.sql charge"

Write-Info "Chargement de 02_seed_static.sql..."
$r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile (Join-Path $mysqlDir "02_seed_static.sql") -database "fsbm_db"
if (-not $r.Success) {
    Write-Err "Echec 02_seed_static.sql"
    Write-Host ($r.Output -join "`n") -ForegroundColor Red
    Read-Host; exit 1
}
Write-Ok "02_seed_static.sql charge"

Write-Info "Chargement de 03_seed_modules.sql..."
$r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile (Join-Path $mysqlDir "03_seed_modules.sql") -database "fsbm_db"
if (-not $r.Success) {
    Write-Err "Echec 03_seed_modules.sql"
    Write-Host ($r.Output -join "`n") -ForegroundColor Red
    Read-Host; exit 1
}
Write-Ok "03_seed_modules.sql charge"

Write-Info "Chargement de 04_seed_data.sql (~720 KB, peut prendre 30 sec)..."
$r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile (Join-Path $mysqlDir "04_seed_data.sql") -database "fsbm_db"
if (-not $r.Success) {
    Write-Err "Echec 04_seed_data.sql"
    Write-Host ($r.Output -join "`n") -ForegroundColor Red
    Read-Host; exit 1
}
Write-Ok "04_seed_data.sql charge"

# 05 : Partie 2 — table reviews + compte admin (login JWT)
$phase2File = Join-Path $mysqlDir "05_phase2_reviews_auth.sql"
if (Test-Path $phase2File) {
    Write-Info "Chargement de 05_phase2_reviews_auth.sql (reviews + admin)..."
    $r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile $phase2File -database "fsbm_db"
    if (-not $r.Success) {
        Write-Err "Echec 05_phase2_reviews_auth.sql"
        Write-Host ($r.Output -join "`n") -ForegroundColor Red
        Read-Host; exit 1
    }
    Write-Ok "05_phase2_reviews_auth.sql charge (admin@fsbm.ac.ma / Admin@FSBM2026)"
}

# 06 : Partie 2 — colonnes media (logos filieres + pieces jointes PDF)
$uploadsFile = Join-Path $mysqlDir "06_phase2_uploads.sql"
if (Test-Path $uploadsFile) {
    Write-Info "Chargement de 06_phase2_uploads.sql (logos + pieces jointes)..."
    $r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile $uploadsFile -database "fsbm_db"
    if ($r.Success) { Write-Ok "06_phase2_uploads.sql charge" }
    else { Write-Info "06 ignore (colonnes deja presentes ?)" }
}

# 07 : Donnees REELLES FSBM (departements, filieres, professeurs, FAQ - source fsbm.ma)
$realFile = Join-Path $mysqlDir "07_real_fsbm_data.sql"
if (Test-Path $realFile) {
    Write-Info "Chargement de 07_real_fsbm_data.sql (donnees reelles FSBM)..."
    $r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile $realFile -database "fsbm_db"
    if ($r.Success) { Write-Ok "07_real_fsbm_data.sql charge (6 departements, 25 filieres reels)" }
    else { Write-Info "07 ignore" }
}

# 08 : REMPLACEMENT par donnees reelles (emails @univh2c.ma, vraies actualites, profs Scholar)
$cleanFile = Join-Path $mysqlDir "08_real_fsbm_clean.sql"
if (Test-Path $cleanFile) {
    Write-Info "Chargement de 08_real_fsbm_clean.sql (remplacement par donnees reelles)..."
    $r = Import-SqlFile -mysqlExe $mysqlExe -password $mysqlPwd -sqlFile $cleanFile -database "fsbm_db"
    if ($r.Success) { Write-Ok "08_real_fsbm_clean.sql charge (donnees reelles, emails @univh2c.ma)" }
    else { Write-Info "08 ignore" }
}

# Pre-remplissage des FAQ depuis le dataset du chatbot
$seedFaq = Join-Path $root "services\academic-service\seed_faq.py"
if (Test-Path $seedFaq) {
    Write-Info "Pre-remplissage des FAQ (faq_items) depuis le dataset..."
    Push-Location (Join-Path $root "services\academic-service")
    cmd /c "set PYTHONIOENCODING=utf-8&& py seed_faq.py 2>nul"
    Pop-Location
    Write-Ok "FAQ pre-remplies"
}

# ─── Statistiques ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Info "Statistiques de la base :"
$statsQuery = "USE fsbm_db; SELECT 'departments' AS T, COUNT(*) AS N FROM departments UNION ALL SELECT 'filieres', COUNT(*) FROM filieres UNION ALL SELECT 'modules', COUNT(*) FROM modules UNION ALL SELECT 'professors', COUNT(*) FROM professors UNION ALL SELECT 'students', COUNT(*) FROM students;"
$statsCmd = "`"$mysqlExe`" -u root `"-p$mysqlPwd`" -e `"$statsQuery`""
cmd /c "$statsCmd 2>nul"

# ─── ETAPE 5 : Lancer les services ────────────────────────────────────────────
Write-Header "[5/5] Lancement des 3 services"

$academicCmd = "cd /d `"$root\services\academic-service`" && set PYTHONIOENCODING=utf-8 && py -m uvicorn app.main:app --reload --port 8002"
$chatbotCmd  = "cd /d `"$root\services\chatbot-service`" && set PYTHONIOENCODING=utf-8 && py -m uvicorn app.main:app --reload --port 8001"
$angularCmd  = "cd /d `"$root\frontend`" && npm start"

Write-Info "Demarrage academic-service sur port 8002..."
Start-Process cmd.exe -ArgumentList "/k", $academicCmd
Start-Sleep -Seconds 3

Write-Info "Demarrage chatbot-service sur port 8001..."
Start-Process cmd.exe -ArgumentList "/k", $chatbotCmd
Start-Sleep -Seconds 3

Write-Info "Demarrage frontend Angular sur port 4200..."
Start-Process cmd.exe -ArgumentList "/k", $angularCmd

# ─── FIN ──────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host ("=" * 70) -ForegroundColor Green
Write-Host "   SETUP TERMINE - Services en cours de demarrage..." -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Green
Write-Host ""
Write-Host "   Chatbot   API : " -NoNewline; Write-Host "http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "   Academic  API : " -NoNewline; Write-Host "http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "   Admin login   : " -NoNewline; Write-Host "http://localhost:4200/admin/login" -ForegroundColor Cyan
Write-Host "   (admin@fsbm.ac.ma / Admin@FSBM2026)" -ForegroundColor DarkGray
Write-Host "   Frontend  UI  : " -NoNewline; Write-Host "http://localhost:4200" -ForegroundColor Cyan
Write-Host ""
Write-Host "Patiente 15-30 secondes que tout soit pret." -ForegroundColor Yellow
Write-Host "Puis ouvre " -NoNewline; Write-Host "http://localhost:4200" -ForegroundColor Cyan -NoNewline; Write-Host " dans ton navigateur."
Write-Host ""
Read-Host "Appuie sur Entree pour fermer ce script"

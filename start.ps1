# ============================================================================
#  FSBM Platform - Lancement des 3 services (PowerShell)
#  USAGE :  powershell -ExecutionPolicy Bypass -File .\start.ps1
# ============================================================================

$root = $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   FSBM Platform - Lancement des services" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# ─── Verifier que les .env existent ──────────────────────────────────────────
$envAcad = Join-Path $root "services\academic-service\.env"
$envChat = Join-Path $root "services\chatbot-service\.env"

if (-not (Test-Path $envAcad)) {
    Write-Host "ERREUR : .env manquant pour academic-service." -ForegroundColor Red
    Write-Host "Lance d'abord : powershell -ExecutionPolicy Bypass -File .\SETUP.ps1" -ForegroundColor Yellow
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}
if (-not (Test-Path $envChat)) {
    Write-Host "ERREUR : .env manquant pour chatbot-service." -ForegroundColor Red
    Read-Host
    exit 1
}

Write-Host "[1/3] Demarrage academic-service sur port 8002..." -ForegroundColor Cyan
$cmdAcad = "cd /d `"$root\services\academic-service`" && set PYTHONIOENCODING=utf-8 && py -m uvicorn app.main:app --reload --port 8002"
Start-Process cmd.exe -ArgumentList "/k", $cmdAcad
Start-Sleep -Seconds 3

Write-Host "[2/3] Demarrage chatbot-service sur port 8001..." -ForegroundColor Cyan
$cmdChat = "cd /d `"$root\services\chatbot-service`" && set PYTHONIOENCODING=utf-8 && py -m uvicorn app.main:app --reload --port 8001"
Start-Process cmd.exe -ArgumentList "/k", $cmdChat
Start-Sleep -Seconds 3

Write-Host "[3/3] Demarrage frontend Angular sur port 4200..." -ForegroundColor Cyan
$cmdNg = "cd /d `"$root\frontend`" && npm start"
Start-Process cmd.exe -ArgumentList "/k", $cmdNg

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "   3 fenetres ouvertes - Services en demarrage..." -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "   Chatbot   API : " -NoNewline; Write-Host "http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "   Academic  API : " -NoNewline; Write-Host "http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "   Frontend  UI  : " -NoNewline; Write-Host "http://localhost:4200" -ForegroundColor Cyan
Write-Host "   Admin login   : " -NoNewline; Write-Host "http://localhost:4200/admin/login" -ForegroundColor Cyan
Write-Host ""
Write-Host "Attendre 15-30 secondes que tout soit pret, puis ouvrir le navigateur." -ForegroundColor Yellow
Write-Host ""
Read-Host "Appuie sur Entree pour fermer ce script (les services restent ouverts)"

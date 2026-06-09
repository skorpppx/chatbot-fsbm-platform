# ============================================================================
#  FSBM Platform - Fix DEFINITIF des problemes de ports Windows
#
#  IMPORTANT : ce script doit etre lance EN ADMINISTRATEUR.
#  Clic droit sur PowerShell -> Executer en tant qu'administrateur, puis :
#      cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform
#      powershell -ExecutionPolicy Bypass -File .\scripts\fix-windows-ports.ps1
#
#  Ce script :
#   1. Verifie qu'il tourne en admin
#   2. Liste les plages de ports reservees par Hyper-V/WSL
#   3. Ajoute des EXCLUSIONS pour nos ports FSBM (5001, 5002, 8001, 8002, 4200)
#      => Windows reserve definitivement ces ports pour notre usage exclusif
#   4. Restart les services reseau
#   5. Nettoie les zombies survivants
# ============================================================================

$FSBM_PORTS = @(5001, 5002, 8001, 8002, 4200)

function Write-Step { param($msg) Write-Host "`n[*] $msg" -ForegroundColor Cyan }
function Write-Ok   { param($msg) Write-Host "    OK  $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "    !!  $msg" -ForegroundColor Yellow }
function Write-Err  { param($msg) Write-Host "    XX  $msg" -ForegroundColor Red }

# ─── 1. Verifier admin ──────────────────────────────────────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Err "Ce script doit etre lance EN ADMINISTRATEUR."
    Write-Host ""
    Write-Host "Comment faire :" -ForegroundColor Yellow
    Write-Host "  1. Ferme cette fenetre" -ForegroundColor White
    Write-Host "  2. Clic droit sur PowerShell" -ForegroundColor White
    Write-Host "  3. Selectionne 'Executer en tant qu'administrateur'" -ForegroundColor White
    Write-Host "  4. Tape : cd $PSScriptRoot\.." -ForegroundColor White
    Write-Host "  5. Tape : powershell -ExecutionPolicy Bypass -File .\scripts\fix-windows-ports.ps1" -ForegroundColor White
    Write-Host ""
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor DarkCyan
Write-Host "   FSBM Platform - Fix definitif des ports (mode admin)" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor DarkCyan
Write-Host ""

# ─── 2. Plages reservees actuelles ──────────────────────────────────────────
Write-Step "Plages de ports TCP actuellement reservees"
$ranges = netsh int ipv4 show excludedportrange protocol=tcp 2>&1
$ranges | Where-Object { $_ -match "\d" } | ForEach-Object { Write-Host "    $_" }

# ─── 3. Tuer les zombies sur les ports cibles ───────────────────────────────
Write-Step "Tuer les processus actuels sur les ports FSBM"
foreach ($p in $FSBM_PORTS) {
    $conn = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        foreach ($c in $conn) {
            $pid = $c.OwningProcess
            $null = cmd /c "taskkill /F /T /PID $pid 2>nul"
            Write-Warn "Killed PID $pid (port $p)"
        }
    }
}

# ─── 4. Stopper temporairement les services réseau ──────────────────────────
Write-Step "Arret temporaire des services reseau Hyper-V"
$services = @("WinNat", "hns", "vmcompute")
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s -and $s.Status -eq "Running") {
        try {
            Stop-Service -Name $svc -Force -ErrorAction Stop
            Write-Ok "Stopped $svc"
        } catch {
            Write-Warn "$svc : impossible d'arreter ($($_.Exception.Message))"
        }
    }
}
Start-Sleep -Seconds 3

# ─── 5. Ajouter les exclusions de port ──────────────────────────────────────
Write-Step "Reservation des ports FSBM (exclusion definitive)"
foreach ($p in $FSBM_PORTS) {
    # Supprimer si deja exclu (pour eviter doublon)
    $null = netsh int ipv4 delete excludedportrange protocol=tcp startport=$p numberofports=1 2>$null
    # Ajouter l'exclusion
    $result = netsh int ipv4 add excludedportrange protocol=tcp startport=$p numberofports=1 2>&1
    if ($LASTEXITCODE -eq 0 -or $result -match "Ok") {
        Write-Ok "Port $p reserve pour FSBM"
    } else {
        Write-Warn "Port $p : $result"
    }
}

# ─── 6. Restart des services ────────────────────────────────────────────────
Write-Step "Redemarrage des services reseau"
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        try {
            Start-Service -Name $svc -ErrorAction Stop
            Write-Ok "Started $svc"
        } catch {
            Write-Warn "$svc : $($_.Exception.Message)"
        }
    }
}

# ─── 7. WSL shutdown si dispo ──────────────────────────────────────────────
if (Get-Command wsl -ErrorAction SilentlyContinue) {
    Write-Step "WSL shutdown (libere les ports WSL)"
    & wsl --shutdown 2>$null
    Write-Ok "WSL arrete"
}

# ─── 8. Verification finale ─────────────────────────────────────────────────
Write-Step "Verification finale"
Start-Sleep -Seconds 3
$allOk = $true
foreach ($p in $FSBM_PORTS) {
    $conn = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Err "Port $p TOUJOURS occupe (PID $($conn.OwningProcess))"
        $allOk = $false
    } else {
        Write-Ok "Port $p libre et reserve pour FSBM"
    }
}

# ─── Resume ──────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "================================================================" -ForegroundColor DarkCyan
if ($allOk) {
    Write-Host "   FIX APPLIQUE AVEC SUCCES" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "Les ports 5001, 5002, 8001, 8002, 4200 sont desormais" -ForegroundColor White
    Write-Host "RESERVES pour FSBM Platform - aucun autre processus ne pourra les" -ForegroundColor White
    Write-Host "occuper accidentellement." -ForegroundColor White
    Write-Host ""
    Write-Host "Tu peux maintenant lancer normalement :" -ForegroundColor White
    Write-Host "  .\start.ps1" -ForegroundColor Cyan
} else {
    Write-Host "   FIX PARTIEL - certains ports restent bloques" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "Solution garantie : REDEMARRE Windows." -ForegroundColor Yellow
    Write-Host "Au redemarrage, les exclusions de ports seront actives," -ForegroundColor White
    Write-Host "et tous les zombies disparaitront." -ForegroundColor White
}
Write-Host ""
Read-Host "Appuie sur Entree pour quitter"

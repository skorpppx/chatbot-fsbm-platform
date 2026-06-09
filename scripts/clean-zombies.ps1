# ============================================================================
#  FSBM Platform - Nettoyage des processus zombies sur les ports
#  USAGE : powershell -ExecutionPolicy Bypass -File .\clean-zombies.ps1
#
#  Tue tous les processus uvicorn/python/node qui occupent les ports FSBM,
#  reset les adapters reseau si besoin.
# ============================================================================

# Note : pas de $ErrorActionPreference="Stop" — on tolere les warnings

$FSBM_PORTS = @(5001, 5002, 4200, 8001, 8002)

function Write-Step { param($msg) Write-Host "`n[*] $msg" -ForegroundColor Cyan }
function Write-Ok   { param($msg) Write-Host "    OK  $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "    !!  $msg" -ForegroundColor Yellow }
function Write-Err  { param($msg) Write-Host "    XX  $msg" -ForegroundColor Red }

Write-Host ""
Write-Host "================================================================" -ForegroundColor DarkCyan
Write-Host "   FSBM Platform - Nettoyage anti-zombies" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor DarkCyan
Write-Host ""

# ─── Etat initial ────────────────────────────────────────────────────────────
Write-Step "Etat initial des ports FSBM"
$zombiePids = @()
foreach ($p in $FSBM_PORTS) {
    $conn = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        foreach ($c in $conn) {
            $proc = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
            $procName = if ($proc) { $proc.ProcessName } else { "<dead>" }
            Write-Warn "Port $p occupe par PID $($c.OwningProcess) ($procName) - $($c.State)"
            $zombiePids += $c.OwningProcess
        }
    } else {
        Write-Ok "Port $p LIBRE"
    }
}

if ($zombiePids.Count -eq 0) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "   Tous les ports sont libres - rien a faire" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Read-Host "Appuie sur Entree pour quitter"
    exit 0
}

# ─── Methode 1 : Stop-Process (gracieux) ─────────────────────────────────────
Write-Step "Tentative 1 : Stop-Process -Force"
foreach ($pid in ($zombiePids | Sort-Object -Unique)) {
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# ─── Methode 2 : taskkill /F /T (force + arbre) ─────────────────────────────
Write-Step "Tentative 2 : taskkill /F /T sur les survivants"
foreach ($p in $FSBM_PORTS) {
    $conn = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        foreach ($c in $conn) {
            $pid = $c.OwningProcess
            $null = cmd /c "taskkill /F /T /PID $pid 2>nul"
        }
    }
}
Start-Sleep -Seconds 2

# ─── Methode 3 : tuer tous les python.exe et node.exe lies a uvicorn/npm ────
Write-Step "Tentative 3 : tuer python.exe / node.exe lies a FSBM"
Get-Process python, node -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine
        if ($cmd -and ($cmd -match "uvicorn|chatbot-fsbm|app\.main|ng serve|angular")) {
            Write-Warn "Killing $($_.ProcessName) PID $($_.Id) : $($cmd.Substring(0,[math]::Min(80,$cmd.Length)))..."
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    } catch {}
}
Start-Sleep -Seconds 2

# ─── Methode 4 : reset WSL si presence ──────────────────────────────────────
$wslAvailable = (Get-Command wsl -ErrorAction SilentlyContinue) -ne $null
if ($wslAvailable) {
    Write-Step "Tentative 4 : reset WSL (cause frequente de zombies)"
    & wsl --shutdown 2>$null
    Write-Ok "WSL arrete"
    Start-Sleep -Seconds 3
} else {
    Write-Warn "WSL non installe - skip"
}

# ─── Methode 5 : restart Host Network Service ───────────────────────────────
# (necessite admin - on tente)
$hnsRunning = (Get-Service hns -ErrorAction SilentlyContinue).Status -eq "Running"
if ($hnsRunning) {
    Write-Step "Tentative 5 : restart du Host Network Service"
    try {
        Restart-Service -Name hns -Force -ErrorAction Stop
        Write-Ok "hns redemarre"
    } catch {
        Write-Warn "hns : besoin d'etre admin - skip"
    }
}

# ─── Verification finale ─────────────────────────────────────────────────────
Write-Step "Verification finale"
Start-Sleep -Seconds 2
$stillBlocked = @()
foreach ($p in $FSBM_PORTS) {
    $conn = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Err "Port $p TOUJOURS occupe (PID $($conn.OwningProcess))"
        $stillBlocked += $p
    } else {
        Write-Ok "Port $p libre"
    }
}

# ─── Resume ──────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "================================================================" -ForegroundColor DarkCyan
if ($stillBlocked.Count -eq 0) {
    Write-Host "   Tous les ports sont desormais LIBRES" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "Tu peux maintenant relancer les services :" -ForegroundColor White
    Write-Host "  scripts\start-all.ps1" -ForegroundColor Cyan
} else {
    Write-Host "   Ports encore bloques : $($stillBlocked -join ', ')" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "Solutions restantes :" -ForegroundColor White
    Write-Host "  1. Lance scripts\fix-windows-ports.ps1 EN ADMINISTRATEUR" -ForegroundColor Cyan
    Write-Host "     (reserve les ports et restart les services reseau)" -ForegroundColor Gray
    Write-Host "  2. Sinon, redemarre Windows (solution garantie)" -ForegroundColor Cyan
    Write-Host "  3. Ou utilise les ports alternatifs 8001/8002 (configures)" -ForegroundColor Cyan
}
Write-Host ""
Read-Host "Appuie sur Entree pour quitter"

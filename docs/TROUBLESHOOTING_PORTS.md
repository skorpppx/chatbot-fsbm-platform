# 🛠️ Dépannage — Processus zombies sur les ports

## 🐛 Le problème

Sous Windows, quand on lance des serveurs locaux (uvicorn, npm, node…), il arrive que les processus restent **« en zombie »** après leur arrêt :
- `taskkill /F /PID xxx` répond « processus introuvable »
- Mais `netstat` ou `Get-NetTCPConnection` montre toujours qu'un PID écoute sur le port
- Résultat : `WinError 10013` ou « address already in use » au redémarrage

## 🎯 Causes principales

| Cause | Détail | Solution |
|---|---|---|
| **WSL2 leak** | Lancer un serveur depuis WSL/bash crée un proxy de port Windows qui survit au processus | `wsl --shutdown` + restart hns |
| **Hyper-V dynamic ports** | Hyper-V/Docker réserve dynamiquement des plages → tes ports peuvent y atterrir | Réserver les ports explicitement |
| **TIME_WAIT** | Socket en attente après fermeture (4 min) | Attendre ou changer de port |
| **Service planté** | Process tué mais socket non libéré par kernel | Restart `hns` ou Windows |

## ✅ Solution rapide (90 % des cas)

Lance le script de nettoyage automatique :

```powershell
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform
powershell -ExecutionPolicy Bypass -File .\scripts\clean-zombies.ps1
```

Ce script essaie 5 méthodes en cascade :
1. `Stop-Process -Force` sur les PID identifiés
2. `taskkill /F /T` (force + arbre de processus)
3. Recherche de tous les `python.exe` / `node.exe` liés à uvicorn/npm
4. `wsl --shutdown` (libère les ports proxy WSL)
5. Restart du Host Network Service (`hns`)

## 🛡️ Solution permanente (à faire une seule fois)

Pour **réserver définitivement** nos ports auprès de Windows et empêcher Hyper-V/WSL de les voler :

### Étape 1 — Ouvrir PowerShell EN ADMINISTRATEUR

- Touche `Windows` → tape `PowerShell`
- Clic droit sur « Windows PowerShell » → **« Exécuter en tant qu'administrateur »**

### Étape 2 — Lancer le script de fix

```powershell
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform
powershell -ExecutionPolicy Bypass -File .\scripts\fix-windows-ports.ps1
```

Ce script (admin requis) :
1. ✅ Vérifie qu'il a les droits administrateur
2. ✅ Tue tous les processus actuels sur les ports FSBM
3. ✅ Arrête temporairement `WinNat`, `hns`, `vmcompute`
4. ✅ Ajoute des **exclusions de port** via `netsh int ipv4 add excludedportrange` pour 5001, 5002, 8001, 8002, 4200
5. ✅ Redémarre les services réseau
6. ✅ Arrête WSL pour libérer ses proxies

Après ce script, ces ports sont **réservés pour ton usage exclusif** — aucun autre processus (Docker, WSL, Hyper-V) ne pourra les voler accidentellement.

### Étape 3 — Vérifier

```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

Tu dois voir tes ports (5001, 5002, 8001, 8002, 4200) listés.

## 🔄 Solution radicale (toujours efficace)

**Redémarrer Windows.** Tous les zombies disparaissent, tous les sockets en TIME_WAIT sont libérés.

Si le problème revient régulièrement, lance d'abord `fix-windows-ports.ps1` en admin (étape 2 ci-dessus) — c'est généralement définitif.

## 📋 Diagnostic manuel

Pour voir qui occupe un port :

```powershell
# PowerShell natif
Get-NetTCPConnection -LocalPort 5001 | Format-List

# CMD classique
netstat -ano | findstr :5001
```

Voir les plages réservées par Hyper-V :

```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

Voir tous les processus écoutant sur 127.0.0.1 :

```powershell
Get-NetTCPConnection -State Listen |
    Where-Object { $_.LocalAddress -eq "127.0.0.1" } |
    Select-Object LocalPort, OwningProcess,
        @{N="Process";E={(Get-Process -Id $_.OwningProcess -EA SilentlyContinue).ProcessName}} |
    Sort-Object LocalPort
```

## 💡 Bonnes pratiques pour éviter les zombies

1. **Lance toujours les services depuis cmd/PowerShell** Windows natif, **jamais depuis WSL/bash** si tu n'es pas obligé(e).
2. **Arrête proprement** avec `Ctrl+C` dans la fenêtre où tourne uvicorn — pas en fermant la fenêtre.
3. **Pour les tests rapides**, utilise des ports élevés (8001-8999) qui sont moins susceptibles d'être dans les plages dynamiques de Hyper-V.
4. **Après un crash**, lance `scripts\clean-zombies.ps1` avant de relancer les services.

## 🎓 Pour aller plus loin

Le problème détaillé : les exclusions de port Windows existent parce que la plage **49152-65535** est dynamique (ports éphémères). Hyper-V/Docker s'attribue dynamiquement des sous-plages dans cette zone. Mais sur Windows 10/11 récents, **les exclusions peuvent grimper jusqu'à 5000** voire plus bas selon la configuration, ce qui explique pourquoi 5001/5002 peuvent être affectés.

La commande qui sauve la mise :
```powershell
netsh int ipv4 add excludedportrange protocol=tcp startport=PORT numberofports=1
```
…force Windows à **ne jamais** allouer ce port dynamiquement.

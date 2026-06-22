<#
.SYNOPSIS
  Lance QuestBoard en local SANS Docker, avec les toolchains portables de .tools.

.DESCRIPTION
  Cette machine n'a ni Docker, ni Python/Node installés au niveau système.
  Une V0 a donc été câblée sur des toolchains portables, locaux et sans droits
  admin, rangés dans .tools\ (Python312 + node). Ce script démarre :
    - le backend FastAPI (uvicorn) sur http://127.0.0.1:8000
    - le frontend SvelteKit (vite) sur http://127.0.0.1:5173

  Astuce proxy : un proxy d'entreprise intercepte localhost. Le backend écoute
  sur 127.0.0.1 ; si le navigateur n'atteint pas l'API, ajouter 127.0.0.1 et
  localhost aux exceptions de proxy (NO_PROXY).

.EXAMPLE
  pwsh -File scripts\dev-local.ps1
#>

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".tools\Python312\python.exe"
$nodeDir = Join-Path $root ".tools\node"

if (-not (Test-Path $py)) { throw "Python portable introuvable : $py" }
if (-not (Test-Path $nodeDir)) { throw "Node portable introuvable : $nodeDir" }

$env:Path = "$nodeDir;$env:Path"
$env:QUESTBOARD_DATABASE_URL = "sqlite:///$root\data\questboard.db"
$env:PUBLIC_API_BASE_URL = "http://127.0.0.1:8000"

Write-Host "Backend  -> http://127.0.0.1:8000  (docs: /docs)" -ForegroundColor Cyan
Start-Process -FilePath $py -WorkingDirectory (Join-Path $root "backend") `
  -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"

Write-Host "Frontend -> http://127.0.0.1:5173" -ForegroundColor Cyan
Start-Process -FilePath (Join-Path $nodeDir "npm.cmd") -WorkingDirectory (Join-Path $root "frontend") `
  -ArgumentList "run", "dev", "--", "--host", "127.0.0.1"

Write-Host "Les deux serveurs tournent dans des fenetres separees. Ctrl+C dans chacune pour arreter." -ForegroundColor Green

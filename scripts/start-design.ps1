$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.local/venv/Scripts/python.exe'
if (-not (Test-Path $python)) { throw 'Run ./scripts/setup-design.ps1 first.' }

# Persist the local encryption key without printing it or committing it.
$keyPath = Join-Path $root '.local/user-secrets.key'
if (-not (Test-Path $keyPath)) {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    [System.IO.File]::WriteAllText($keyPath, [Convert]::ToBase64String($bytes))
}
$env:FORMA_USER_SECRETS_KEY = [System.IO.File]::ReadAllText($keyPath).Trim()
$env:FORMA_DEPLOYMENT_MODE = 'local'
$env:FORMA_AUTH_MODE = 'local'
$env:FORMA_DEVELOPMENT_MODE = 'true'
$env:DATABASE_BACKEND = 'sqlite'
$env:SQLITE_DATABASE_URL = 'sqlite:///./forma.db'
$env:IMAGE_OUTPUT_ENABLED = 'false'

Push-Location (Join-Path $root '.local/OpenForma')
try {
    & $python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
    if ($LASTEXITCODE -ne 0) { throw "OpenForma exited with code $LASTEXITCODE" }
} finally {
    Pop-Location
}

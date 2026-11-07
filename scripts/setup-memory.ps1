$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path '.local/cognee-venv/Scripts/python.exe')) {
    & uv venv --python 3.12 .local/cognee-venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the Cognee environment.' }
}
& uv pip install --python .local/cognee-venv/Scripts/python.exe -r requirements-cognee.txt
if ($LASTEXITCODE -ne 0) { throw 'Cognee installation failed.' }
Write-Host 'Cognee installed. Run ./scripts/start-memory.ps1 -Check for model readiness.'

param([switch]$Check)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$python = '.local/cognee-venv/Scripts/python.exe'
if (-not (Test-Path $python)) { throw 'Run ./scripts/setup-memory.ps1 first.' }
$arguments = @('scripts/cognee_runtime.py')
if ($Check) { $arguments += '--check' }
& $python @arguments
if ($LASTEXITCODE -ne 0) { throw 'Cognee exited unsuccessfully; see the diagnostic above.' }

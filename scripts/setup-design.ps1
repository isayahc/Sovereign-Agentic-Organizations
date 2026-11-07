$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$revision = '718d955c42bb31fd30b512c3a9f08c68f25c02e5'

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program failed with exit code $LASTEXITCODE" }
}

if (-not (Test-Path '.local/OpenForma')) {
    Invoke-Checked git @('clone', 'https://github.com/Mapped-Assembly/OpenForma.git', '.local/OpenForma')
    Invoke-Checked git @('-C', '.local/OpenForma', 'checkout', '--detach', $revision)
}
$actual = & git -C .local/OpenForma rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actual -ne $revision) {
    throw "Expected OpenForma revision $revision; inspect the existing checkout before changing it."
}
if (-not (Test-Path '.local/venv/Scripts/python.exe')) {
    Invoke-Checked uv @('venv', '--python', '3.12', '--seed', '.local/venv')
}
Invoke-Checked uv @('pip', 'install', '--python', '.local/venv/Scripts/python.exe', '-r', '.local/OpenForma/apps/api/requirements.txt', '-e', '.local/OpenForma')
Invoke-Checked '.local/venv/Scripts/python.exe' @('.local/OpenForma/.agents/skills/forma-hardware/scripts/cad.py', 'setup')
Write-Host 'Design dependencies ready. Run ./scripts/start-design.ps1, then opencode mcp list.'

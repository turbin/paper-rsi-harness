param([Parameter(Mandatory=$true)][string]$Target)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Install Git for Windows first.'
}
$paperPython = Get-Command py -ErrorAction SilentlyContinue
if ($paperPython) {
    & $paperPython.Source -3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.10+ required.' }
    & $paperPython.Source -3 (Join-Path $PSScriptRoot 'paper.py') init --root $Target
} else {
    $paperPython = Get-Command python -ErrorAction SilentlyContinue
    if (-not $paperPython) { throw 'Install Python 3.10+ first.' }
    & $paperPython.Source -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.10+ required.' }
    & $paperPython.Source (Join-Path $PSScriptRoot 'paper.py') init --root $Target
}
if ($LASTEXITCODE -ne 0) { throw 'Workspace initialization failed.' }

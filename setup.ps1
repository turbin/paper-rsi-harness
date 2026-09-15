# 一体化安装：初始化论文工作区 + 安装 paper-spec-socratic skill 到本机检测到的 agent。
# 用法：
#   .\setup.ps1 -Target "$env:USERPROFILE\Documents\paper-rsi-harness"
#   .\setup.ps1 -List                              # 只显示检测到的 agent，不安装
#   .\setup.ps1 -Agent kimi -Target "..."          # skill 只装到指定 agent
#   .\setup.ps1 -NoSkill -Target "..."             # 只建工作区，不装 skill
#   .\setup.ps1 -Force -Target "..."               # skill 已存在时覆盖
param(
    [Parameter(Mandatory=$false)][string]$Target,
    [switch]$List,
    [string]$Agent,
    [switch]$NoSkill,
    [switch]$Force
)
$ErrorActionPreference = 'Stop'

$skillName = 'paper-spec-socratic'
$skillSrc = Join-Path $PSScriptRoot "skills/$skillName/SKILL.md"
if (-not (Test-Path $skillSrc)) { throw "缺少 $skillSrc" }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git for Windows first.' }
$paperPython = Get-Command py -ErrorAction SilentlyContinue
if (-not $paperPython) { $paperPython = Get-Command python -ErrorAction SilentlyContinue }
if (-not $paperPython) { throw 'Install Python 3.10+ first.' }

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
if (-not $homeDir) { throw '找不到用户主目录。' }

$map = [ordered]@{
    'kimi'   = @{ Cmd = 'kimi';   Dir = Join-Path $homeDir '.kimi-code\skills' }
    'claude' = @{ Cmd = 'claude'; Dir = Join-Path $homeDir '.claude\skills' }
    'codex'  = @{ Cmd = 'codex';  Dir = Join-Path $homeDir '.agents\skills' }
    'gemini' = @{ Cmd = 'gemini'; Dir = Join-Path $homeDir '.gemini\skills' }
}
$detected = @()
foreach ($name in $map.Keys) {
    if ((Get-Command $map[$name].Cmd -ErrorAction SilentlyContinue) -or (Test-Path $map[$name].Dir)) { $detected += $name }
}

if ($List) {
    if ($detected.Count -eq 0) { '未检测到任何已知 agent。' } else { "检测到: $($detected -join ', ')" }
    exit 0
}
if (-not $Target) { throw '请用 -Target 指定工作区目录。' }

Write-Host "==> 初始化工作区: $Target"
if ($paperPython.Name -eq 'py') {
    & $paperPython.Source -3 (Join-Path $PSScriptRoot 'paper.py') init --root $Target
} else {
    & $paperPython.Source (Join-Path $PSScriptRoot 'paper.py') init --root $Target
}
if ($LASTEXITCODE -ne 0) { throw 'Workspace initialization failed.' }

if (-not $NoSkill) {
    if ($Agent) {
        if (-not $map.Contains($Agent)) { throw "未知 agent: $Agent（可选: kimi|claude|codex|gemini）" }
        $targets = @($Agent)
    } elseif ($detected.Count -gt 0) {
        $targets = $detected
    } else {
        Write-Host '未检测到任何已知 agent，跳过 skill 安装（用 -Agent 显式指定）。'
        $targets = @()
    }
    foreach ($name in $targets) {
        $dest = Join-Path $map[$name].Dir $skillName
        if ((Test-Path (Join-Path $dest 'SKILL.md')) -and -not $Force) {
            Write-Host "跳过 $name：$dest 已存在（用 -Force 覆盖）"
            continue
        }
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
        Copy-Item $skillSrc (Join-Path $dest 'SKILL.md') -Force
        Write-Host "==> skill 已安装到 ${name}: $dest"
    }
}
Write-Host '完成。'

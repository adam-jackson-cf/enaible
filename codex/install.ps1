# Codex Installer (AI‑Assisted Workflows) for Windows PowerShell

param(
  [Parameter(Position=0)] [string]$TargetPath = "",
  [ValidateSet('Fresh','Merge','Update','Cancel')]
  [string]$Mode = '',
  [switch]$Verbose,
  [switch]$DryRun,
  [switch]$SkipPython
)

$ErrorActionPreference = 'Stop'
$VERSION = '1.0.0'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $env:TEMP 'codex-install.log'

function Write-Log([string]$Message,[string]$Level='INFO') {
  $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  $line = "[$ts] [$Level] $Message"
  Add-Content -Path $LogFile -Value $line
  if ($PSBoundParameters.ContainsKey('Verbose')) { Write-Host $line -ForegroundColor Cyan }
}

function Show-Usage {
  @"
Codex Installer (AI‑Assisted Workflows) v$VERSION

USAGE:
  .\install.ps1 [TARGET_PATH] [OPTIONS]

ARGUMENTS:
  TARGET_PATH   Directory where .codex\ will be created (optional)

OPTIONS:
  -Verbose      Verbose output
  -DryRun       Show actions without making changes
  -SkipPython   Skip Python dependency installation
  -Mode         Fresh|Merge|Update|Cancel (existing installs)
"@
}

if ($args -contains '--help' -or $args -contains '-h') { Show-Usage; exit 0 }

Write-Log "Starting Codex installer v$VERSION"

# Resolve CODEX_HOME interactively
$CODEX_HOME = ''
if ($TargetPath) {
  if ($TargetPath -eq '~') { $TargetPath = $env:USERPROFILE }
  if (-not [System.IO.Path]::IsPathRooted($TargetPath)) { $TargetPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $TargetPath)) }
  if ($TargetPath.ToLower().EndsWith('\u002Ecodex')) { $CODEX_HOME = $TargetPath } else { $CODEX_HOME = Join-Path $TargetPath '.codex' }
} else {
  if (-not [Console]::KeyAvailable) {
    $CODEX_HOME = Join-Path $env:USERPROFILE '.codex'
    Write-Log "Non-TTY: default CODEX_HOME=$CODEX_HOME"
  } else {
    Write-Host "Choose install scope for Codex home:" -ForegroundColor Yellow
    Write-Host "  1) User (~/.codex) [default]"
    Write-Host "  2) Project (./.codex)"
    Write-Host "  3) Custom path"
    $choice = Read-Host 'Enter choice [1-3]'
    if (-not $choice) { $choice = '1' }
    switch ($choice) {
      '1' { $CODEX_HOME = Join-Path $env:USERPROFILE '.codex' }
      '2' { $CODEX_HOME = Join-Path (Get-Location) '.codex' }
      '3' {
        $tp = Read-Host 'Enter absolute path (we will create <path>\.codex if needed)'
        if (-not [System.IO.Path]::IsPathRooted($tp)) { $tp = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $tp)) }
        if ($tp.ToLower().EndsWith('\u002Ecodex')) { $CODEX_HOME = $tp } else { $CODEX_HOME = Join-Path $tp '.codex' }
      }
      default { $CODEX_HOME = Join-Path $env:USERPROFILE '.codex' }
    }
  }
}

# Choose scripts root
$SCRIPTS_ROOT = ''
if (-not [Console]::KeyAvailable) {
  $SCRIPTS_ROOT = Join-Path $CODEX_HOME 'scripts'
} else {
  Write-Host "Where should Python scripts live?" -ForegroundColor Yellow
  Write-Host "  1) Inside Codex home ($CODEX_HOME/scripts) [default]"
  Write-Host "  2) User (~/.codex/scripts)"
  Write-Host "  3) Custom path"
  $choice = Read-Host 'Enter choice [1-3]'
  if (-not $choice) { $choice = '1' }
  switch ($choice) {
    '1' { $SCRIPTS_ROOT = Join-Path $CODEX_HOME 'scripts' }
    '2' { $SCRIPTS_ROOT = Join-Path $env:USERPROFILE '.codex\scripts' }
    '3' {
      $sp = Read-Host 'Enter absolute path to scripts root'
      if (-not [System.IO.Path]::IsPathRooted($sp)) { $sp = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $sp)) }
      $SCRIPTS_ROOT = $sp
    }
    default { $SCRIPTS_ROOT = Join-Path $CODEX_HOME 'scripts' }
  }
}

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $CODEX_HOME | Out-Null
  New-Item -ItemType Directory -Force -Path $SCRIPTS_ROOT | Out-Null
}

# Backup and mode handling
if (Test-Path $CODEX_HOME) {
  $backup = "$CODEX_HOME.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
  if (-not $DryRun) { Copy-Item -Recurse -Force -Path $CODEX_HOME -Destination $backup }
  Write-Log "Backup created: $backup"
  if (-not $Mode) {
    if ([Console]::KeyAvailable) {
      Write-Host "Existing $CODEX_HOME found" -ForegroundColor Yellow
      Write-Host "  1) Fresh (replace)\n  2) Merge\n  3) Update\n  4) Cancel"
      $c = Read-Host 'Enter choice [1-4]'
      switch ($c) { '1' { $Mode='Fresh' } '2' { $Mode='Merge' } '3' { $Mode='Update' } '4' { $Mode='Cancel' } default { $Mode='Update' } }
    } else { $Mode='Update' }
  }
  switch ($Mode) {
    'Fresh' { if (-not $DryRun) { Remove-Item -Recurse -Force -Path $CODEX_HOME; New-Item -ItemType Directory -Force -Path $CODEX_HOME | Out-Null } }
    'Cancel' { Write-Log 'Cancelled by user'; exit 0 }
    default { }
  }
}

# Copy prompts and rules
$srcPrompts = Join-Path $ScriptDir 'prompts'
$srcRules   = Join-Path $ScriptDir 'rules'
if (-not (Test-Path $srcPrompts)) { throw "Missing prompts dir: $srcPrompts" }
if (-not (Test-Path $srcRules)) { throw "Missing rules dir: $srcRules" }
if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path (Join-Path $CODEX_HOME 'prompts') | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $CODEX_HOME 'rules')   | Out-Null
  Copy-Item -Recurse -Force -Path (Join-Path $srcPrompts '*') -Destination (Join-Path $CODEX_HOME 'prompts')
  Copy-Item -Recurse -Force -Path (Join-Path $srcRules   '*') -Destination (Join-Path $CODEX_HOME 'rules')
}
Write-Log "Copied prompts and rules"

# Copy Python framework
$sharedRoot = Join-Path (Split-Path $ScriptDir -Parent) 'shared'
$subdirs = @('core','analyzers','setup','config','utils','generators','context')
foreach ($d in $subdirs) { if (-not (Test-Path (Join-Path $sharedRoot $d))) { throw "Missing shared subtree: $d" } }
if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $SCRIPTS_ROOT | Out-Null
  foreach ($d in $subdirs) {
    $src = Join-Path $sharedRoot $d
    $dst = Join-Path $SCRIPTS_ROOT $d
    if (Test-Path $dst) { Remove-Item -Recurse -Force -Path $dst }
    Copy-Item -Recurse -Force -Path $src -Destination $dst
  }
}
Write-Log "Copied Python framework to $SCRIPTS_ROOT"

function Get-PythonExe {
  $candidates = @('python','python3')
  foreach ($c in $candidates) {
    try {
      $v = & $c --version 2>&1
      if ($LASTEXITCODE -eq 0 -and $v -match 'Python (\d+)\.(\d+)\.(\d+)') {
        $maj=[int]$matches[1]; $min=[int]$matches[2]
        if ($maj -gt 3 -or ($maj -eq 3 -and $min -ge 11)) { return $c }
      }
    } catch { }
  }
  throw "Python 3.11+ not found as 'python' or 'python3'"
}

$PythonExe = $null
try { $PythonExe = Get-PythonExe; Write-Log "Selected interpreter: $PythonExe" } catch { }

# Install Python dependencies
if (-not $SkipPython) {
  if (-not $PythonExe) { throw "Python 3.11+ is required" }
  $req = Join-Path $SCRIPTS_ROOT 'setup/requirements.txt'
  if (-not (Test-Path $req)) { throw "Missing requirements: $req" }
  if (-not $DryRun) {
    $installer = Join-Path $SCRIPTS_ROOT 'setup/install_dependencies.py'
    $env:PYTHONPATH = $SCRIPTS_ROOT
    & $PythonExe $installer 2>$null 3>$null < <(echo y) | Out-Null
  }
  Write-Log "Python dependencies installed"
} else {
  Write-Log "Skipping Python dependency installation"
}

# Ensure config and trust entries
$cfg = Join-Path $CODEX_HOME 'config.toml'
if (-not $DryRun) {
  if (-not (Test-Path $cfg)) { Copy-Item -Path (Join-Path $ScriptDir 'config.toml') -Destination $cfg }
  $text = Get-Content -Raw -Path $cfg
  if ($text -notmatch "\[mcp_servers\.chrome-devtools\]") {
    Add-Content -Path $cfg -Value @"

[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--headless", "--isolated"]
"@
  }
  function Add-Trust($path) {
    # Normalize trailing separators
    if ($path.EndsWith('\') -or $path.EndsWith('/')) { $path = $path.TrimEnd('\','/') }
    $raw = Get-Content -Raw -Path $cfg
    $sectionAbs = "[projects.`"$path`"]"
    $sectionTilde = $null
    if ($path -like "$env:USERPROFILE*") {
      $tilde = "~" + $path.Substring($env:USERPROFILE.Length)
      $sectionTilde = "[projects.`"$tilde`"]"
    }
    $exists = $false
    if ($raw -match [regex]::Escape($sectionAbs)) { $exists = $true }
    if (-not $exists -and $sectionTilde -and ($raw -match [regex]::Escape($sectionTilde))) { $exists = $true }
    if (-not $exists) {
      Add-Content -Path $cfg -Value "`n$sectionAbs`ntrust_level = `"trusted`"`n"
      Write-Log "Added trust for $path"
    } else {
      Write-Log "Trust exists for $path (abs/tilde)"
    }
  }
  Add-Trust $CODEX_HOME
  if (-not ($SCRIPTS_ROOT -like "$CODEX_HOME*")) { Add-Trust $SCRIPTS_ROOT }
}

# Update AGENTS.md (Codex global rules only)
$globalRules = Join-Path $ScriptDir 'rules\global.codex.rules.md'
if (Test-Path $globalRules) {
  $targetAgents = Join-Path $CODEX_HOME 'AGENTS.md'
  if (-not $DryRun) { if (-not (Test-Path $targetAgents)) { New-Item -ItemType File -Force -Path $targetAgents | Out-Null } }
  $header = "# AI-Assisted Workflows (Codex Global Rules) v$VERSION - Auto-generated, do not edit"
  if (-not $DryRun) {
    $raw = Get-Content -Raw -Path $targetAgents
    if ($raw -notmatch [regex]::Escape($header)) {
      Add-Content -Path $targetAgents -Value "`n$header`n"
      Add-Content -Path $targetAgents -Value (Get-Content -Raw -Path $globalRules)
      Write-Log "Updated AGENTS.md with Codex global rules"
    }
  }
}

# Offer to inject shell helpers (PowerShell profile)
if ([Console]::KeyAvailable) {
  $ans = Read-Host 'Append Codex helpers to your PowerShell profile? [Y/n]'
  if (-not $ans -or $ans -match '^[Yy]$') {
    $profilePath = $PROFILE
    if (-not $DryRun) {
      if (-not (Test-Path (Split-Path $profilePath -Parent))) { New-Item -ItemType Directory -Force -Path (Split-Path $profilePath -Parent) | Out-Null }
      if (-not (Test-Path $profilePath)) { New-Item -ItemType File -Force -Path $profilePath | Out-Null }
      $block = Select-String -Path (Join-Path $ScriptDir 'codex-init-helpers.md') -Pattern '^```bash$','^```$' -Context 0,0 | ForEach-Object { $_ }
      # Fallback: just append the whole helpers file (PowerShell can run 'codex' commands via cmd)
      Add-Content -Path $profilePath -Value "`n# Codex helpers`n"
      Add-Content -Path $profilePath -Value (Get-Content -Raw -Path (Join-Path $ScriptDir 'codex-init-helpers.md'))
    }
    Write-Log "Appended helpers to $PROFILE"
  }
}

# Verify
if (-not $DryRun) {
  $ok = $true
  if (-not (Test-Path (Join-Path $CODEX_HOME 'prompts'))) { Write-Host "Missing prompts" -ForegroundColor Red; $ok=$false }
  if (-not (Test-Path (Join-Path $CODEX_HOME 'rules')))   { Write-Host "Missing rules" -ForegroundColor Red; $ok=$false }
  try {
    if (-not $PythonExe) { $PythonExe = Get-PythonExe }
    $env:PYTHONPATH = $SCRIPTS_ROOT
    & $PythonExe - << 'PY'
import sys
try:
  import core.base  # noqa
except Exception as e:
  sys.exit(1)
PY
    if ($LASTEXITCODE -ne 0) { throw 'import failed' }
  } catch { Write-Host "Python import failed; programmatic prompts may not work" -ForegroundColor Yellow; $ok=$false }
  if (-not $ok) { Write-Host "Verification had warnings/errors. See $LogFile" -ForegroundColor Yellow } else { Write-Host "Verification successful" -ForegroundColor Green }
}

Write-Host "`n✅ Codex installation complete" -ForegroundColor Green
Write-Host "  CODEX_HOME:   $CODEX_HOME"
Write-Host "  SCRIPTS_ROOT: $SCRIPTS_ROOT"
Write-Host "  Config:       $CODEX_HOME\config.toml (trust entries added)"

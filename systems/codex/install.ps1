# Codex Installer (AI‑Assisted Workflows) for Windows PowerShell

param(
  [Parameter(Position=0)] [string]$TargetPath = "",
  [ValidateSet('Fresh','Merge','Update','Cancel')]
  [string]$Mode = '',
  [string]$ScriptsRoot = '',
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

function Show-Header {
  Write-Host ""
  Write-Host "┌─────────────────────────────────────┐"
  Write-Host "│        Codex CLI Installer          │"
  Write-Host ("│        Version {0}            │" -f $VERSION)
  Write-Host "└─────────────────────────────────────┘"
}

$script:TotalPhases = 11
$script:CurrentPhase = 0
function Next-Phase([string]$Description) {
  $script:CurrentPhase++
  Write-Host ""
  Write-Host ([string]::Format("[{0}/{1}] {2}", $script:CurrentPhase, $script:TotalPhases, $Description))
  Write-Host "----------------------------------------"
}

function Resolve-NormalizedPath([string]$Path) {
  if (-not $Path) { return '' }
  if ($Path -eq '~') { $Path = $env:USERPROFILE }
  if (-not [System.IO.Path]::IsPathRooted($Path)) {
    $Path = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
  }
  return $Path
}

if ($args -contains '--help' -or $args -contains '-h') { Show-Usage; exit 0 }

Write-Log "Starting Codex installer v$VERSION"
Show-Header
Next-Phase "Resolve installation paths"

# Resolve CODEX_HOME interactively
$CODEX_HOME = ''
if ($TargetPath) {
  $normalizedTarget = Resolve-NormalizedPath $TargetPath
  if ($normalizedTarget.ToLower().EndsWith('\u002Ecodex')) { $CODEX_HOME = $normalizedTarget } else { $CODEX_HOME = Join-Path $normalizedTarget '.codex' }
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
        $tp = Resolve-NormalizedPath $tp
        if ($tp.ToLower().EndsWith('\u002Ecodex')) { $CODEX_HOME = $tp } else { $CODEX_HOME = Join-Path $tp '.codex' }
      }
      default { $CODEX_HOME = Join-Path $env:USERPROFILE '.codex' }
    }
  }
}
if (-not $CODEX_HOME) { $CODEX_HOME = Join-Path $env:USERPROFILE '.codex' }

if ($ScriptsRoot) {
  $SCRIPTS_ROOT = Resolve-NormalizedPath $ScriptsRoot
} else {
  $SCRIPTS_ROOT = Join-Path $CODEX_HOME 'scripts'
}

Write-Log "Resolved CODEX_HOME=$CODEX_HOME"
Write-Log "Resolved SCRIPTS_ROOT=$SCRIPTS_ROOT"

Next-Phase "Prepare target directories"
if ($DryRun) {
  Write-Log "Would create $CODEX_HOME"
  Write-Log "Would create $SCRIPTS_ROOT"
} else {
  New-Item -ItemType Directory -Force -Path $CODEX_HOME | Out-Null
  New-Item -ItemType Directory -Force -Path $SCRIPTS_ROOT | Out-Null
}

Next-Phase "Backup existing installation (if present)"
if (Test-Path $CODEX_HOME) {
  $backup = "$CODEX_HOME.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
  if ($DryRun) {
    Write-Log "Would back up $CODEX_HOME to $backup"
  } else {
    Copy-Item -Recurse -Force -Path $CODEX_HOME -Destination $backup
    Write-Log "Backup created: $backup"
  }
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
} else {
  Write-Log "No existing installation detected"
}

Next-Phase "Copy Codex prompts and rules"
$srcPrompts = Join-Path $ScriptDir 'prompts'
$srcRules   = Join-Path $ScriptDir 'rules'
if (-not (Test-Path $srcPrompts)) { throw "Missing prompts dir: $srcPrompts" }
if (-not (Test-Path $srcRules)) { throw "Missing rules dir: $srcRules" }
if ($DryRun) {
  Write-Log "Would copy prompts to $(Join-Path $CODEX_HOME 'prompts')"
  Write-Log "Would copy rules to $(Join-Path $CODEX_HOME 'rules')"
} else {
  New-Item -ItemType Directory -Force -Path (Join-Path $CODEX_HOME 'prompts') | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $CODEX_HOME 'rules')   | Out-Null
  Copy-Item -Recurse -Force -Path (Join-Path $srcPrompts '*') -Destination (Join-Path $CODEX_HOME 'prompts')
  Copy-Item -Recurse -Force -Path (Join-Path $srcRules   '*') -Destination (Join-Path $CODEX_HOME 'rules')
  Write-Log "Copied prompts and rules"
}

Next-Phase "Copy Python framework"
# Repo layout: `shared/` sits at the repository root (sibling to `systems/`).
# This script lives in `systems/codex/`, so resolve two levels up.
$repoRoot = Split-Path (Split-Path $ScriptDir -Parent) -Parent
$sharedRoot = Join-Path $repoRoot 'shared'
$subdirs = @('core','analyzers','setup','config','utils','generators','context')
foreach ($d in $subdirs) { if (-not (Test-Path (Join-Path $sharedRoot $d))) { throw "Missing shared subtree: $(Join-Path $sharedRoot $d)" } }
if ($DryRun) {
  Write-Log "Would copy Python framework to $SCRIPTS_ROOT"
} else {
  New-Item -ItemType Directory -Force -Path $SCRIPTS_ROOT | Out-Null
  foreach ($d in $subdirs) {
    $src = Join-Path $sharedRoot $d
    $dst = Join-Path $SCRIPTS_ROOT $d
    if (Test-Path $dst) { Remove-Item -Recurse -Force -Path $dst }
    Copy-Item -Recurse -Force -Path $src -Destination $dst
  }
  Write-Log "Copied Python framework to $SCRIPTS_ROOT"
}

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

function Install-NodeTools {
  param([bool]$DryRunFlag)

  if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js is required for frontend analysis" }
  if (-not (Get-Command npm  -ErrorAction SilentlyContinue)) { throw "npm is required for frontend analysis" }

  $toolsDir = Join-Path $CODEX_HOME 'eslint'
  if ($DryRunFlag) {
    Write-Log "Would install Node tools into $toolsDir"
    return
  }

  New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
  $packageJson = Join-Path $toolsDir 'package.json'
  if (-not (Test-Path $packageJson)) {
    Set-Content -Path $packageJson -Value @'
{
  "name": "codex-node-tools",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "eslint": "^8.0.0",
    "@typescript-eslint/parser": "^5.0.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "eslint-plugin-react": "^7.32.0",
    "eslint-plugin-import": "^2.27.0",
    "eslint-plugin-vue": "^9.0.0",
    "jscpd": "^3.5.0"
  }
}
'@
  } else {
    $raw = Get-Content -Raw -Path $packageJson
    if ($raw -notmatch '"jscpd"') {
      $updated = $raw -replace '("dependencies"\s*:\s*\{)', "$1`n    \"jscpd\": \"^3.5.0\","
      Set-Content -Path $packageJson -Value $updated
    }
  }

  Push-Location $toolsDir
  try {
    Write-Log "Installing Node tools (ESLint + jscpd)..."
    npm install --no-fund --no-audit --silent | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "npm install failed" }
    Write-Log "Installed Node tools (ESLint + jscpd)"
  } finally {
    Pop-Location
  }
}

$PythonExe = $null
try { $PythonExe = Get-PythonExe; Write-Log "Selected interpreter: $PythonExe" } catch { }

Next-Phase "Install Python dependencies"
if (-not $SkipPython) {
  if (-not $PythonExe) { throw "Python 3.11+ is required" }
  $req = Join-Path $SCRIPTS_ROOT 'setup/requirements.txt'
  if (-not (Test-Path $req)) { throw "Missing requirements: $req" }
  if ($DryRun) {
    Write-Log "Would install Python dependencies from $req"
  } else {
    $installer = Join-Path $SCRIPTS_ROOT 'setup/install_dependencies.py'
    $env:PYTHONPATH = $SCRIPTS_ROOT
    & $PythonExe $installer 2>$null 3>$null < <(echo y) | Out-Null
    Write-Log "Python dependencies installed"
  }
} else {
  Write-Log "Skipping Python dependency installation"
}

Next-Phase "Install Node-based tooling"
Install-NodeTools -DryRunFlag $DryRun

Next-Phase "Configure codex config.toml"
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
  Write-Log "Updated $cfg with Codex defaults and trust entries"
}

if ($DryRun) {
  Write-Log "Would ensure config at $cfg"
}

Next-Phase "Update AGENTS.md"
$globalRules = Join-Path $ScriptDir 'rules\global.codex.rules.md'
if (Test-Path $globalRules) {
  $targetAgents = Join-Path $CODEX_HOME 'AGENTS.md'
  $header = "# AI-Assisted Workflows (Codex Global Rules) v$VERSION - Auto-generated, do not edit"
  $marker = "AI-Assisted Workflows (Codex Global Rules)"
  $startMarker = "<!-- CODEx_GLOBAL_RULES_START -->"
  $endMarker = "<!-- CODEx_GLOBAL_RULES_END -->"
  if ($DryRun) {
    if (Test-Path $targetAgents -and ((Get-Content -Raw -Path $targetAgents) -match $marker)) {
      Write-Log "Would refresh Codex global rules section in $targetAgents"
    } else {
      Write-Log "Would append Codex global rules section to $targetAgents"
    }
  } else {
    if (-not (Test-Path $targetAgents)) { New-Item -ItemType File -Force -Path $targetAgents | Out-Null }
    $raw = [string]::Empty
    if (Test-Path $targetAgents) { $raw = Get-Content -Raw -Path $targetAgents }
    $normalized = $raw -replace "`r`n", "`n"
    $rulesBody = (Get-Content -Raw -Path $globalRules).Trim()
    $block = "{0}`n{1}`n`n{2}`n{3}" -f $startMarker, $header, $rulesBody, $endMarker

    function Join-Sections([string]$prefix, [string]$suffix) {
      $sections = @()
      if ($prefix.Trim()) { $sections += $prefix.TrimEnd() }
      $sections += $block
      if ($suffix.Trim()) { $sections += $suffix.TrimStart() }
      $joined = ($sections -join "`n`n").TrimEnd() + "`n"
      return $joined
    }

    $updated = $null

    if ($normalized.Contains($startMarker) -and $normalized.Contains($endMarker)) {
      $parts = $normalized.Split($startMarker, 2)
      if ($parts.Length -eq 2) {
        $afterStart = $parts[1].Split($endMarker, 2)
        if ($afterStart.Length -eq 2) {
          $prefixPart = $parts[0]
          $suffixPart = $afterStart[1]
          $updated = Join-Sections $prefixPart $suffixPart
        }
      }
    }

    if (-not $updated -and $normalized.Contains($marker)) {
      $index = $normalized.IndexOf($header)
      if ($index -lt 0) { $index = $normalized.IndexOf($marker) }
      if ($index -ge 0) {
        $prefixPart = $normalized.Substring(0, $index).TrimEnd()
        $remainder = $normalized.Substring($index + $header.Length).TrimStart("`n".ToCharArray())
        $rulesTrim = $rulesBody.Trim()
        $suffixPart = ""
        if ($remainder.StartsWith($rulesTrim)) {
          $suffixPart = $remainder.Substring($rulesTrim.Length).TrimStart("`n".ToCharArray())
        } else {
          $pos = $remainder.IndexOf($rulesTrim)
          if ($pos -ge 0) {
            $suffixPart = ($remainder.Remove($pos, $rulesTrim.Length)).TrimStart("`n".ToCharArray())
          } else {
            $updated = $normalized
          }
        }
        if (-not $updated) {
          $updated = Join-Sections $prefixPart $suffixPart
        }
      }
    }

    if (-not $updated) {
      $updated = Join-Sections $normalized.TrimEnd() ""
    }

    $final = $updated -replace "`n", "`r`n"
    Set-Content -Path $targetAgents -Value $final
    Write-Log "Updated AGENTS.md with Codex global rules"
  }
}

# Also place the ExecPlan template alongside AGENTS.md
$srcExecplan = Join-Path $ScriptDir 'execplan.md'
if (Test-Path $srcExecplan) {
  $dstExecplan = Join-Path $CODEX_HOME 'execplan.md'
  if ($DryRun) {
    Write-Log "Would copy ExecPlan template to $dstExecplan"
  } else {
    if (Test-Path $dstExecplan) {
      try {
        $srcHash = (Get-FileHash -Algorithm SHA256 $srcExecplan).Hash
        $dstHash = (Get-FileHash -Algorithm SHA256 $dstExecplan).Hash
        if ($srcHash -ne $dstHash) {
          Copy-Item -Force -Path $srcExecplan -Destination $dstExecplan
          Write-Log "Refreshed ExecPlan template at $dstExecplan"
        } else {
          Write-Log "ExecPlan template already up to date at $dstExecplan"
        }
      } catch {
        Copy-Item -Force -Path $srcExecplan -Destination $dstExecplan
        Write-Log "Copied ExecPlan template to $dstExecplan"
      }
    } else {
      Copy-Item -Force -Path $srcExecplan -Destination $dstExecplan
      Write-Log "Copied ExecPlan template to $dstExecplan"
    }
  }
}

Next-Phase "Offer shell helpers"
if ([Console]::KeyAvailable) {
  $ans = Read-Host 'Append Codex helpers to your PowerShell profile? [Y/n]'
  if (-not $ans -or $ans -match '^[Yy]$') {
    $profilePath = $PROFILE
    if ($DryRun) {
      Write-Log "Would append Codex helpers to $profilePath"
    } else {
      if (-not (Test-Path (Split-Path $profilePath -Parent))) { New-Item -ItemType Directory -Force -Path (Split-Path $profilePath -Parent) | Out-Null }
      if (-not (Test-Path $profilePath)) { New-Item -ItemType File -Force -Path $profilePath | Out-Null }
      $block = Select-String -Path (Join-Path $ScriptDir 'codex-init-helpers.md') -Pattern '^```bash$','^```$' -Context 0,0 | ForEach-Object { $_ }
      # Fallback: just append the whole helpers file (PowerShell can run 'codex' commands via cmd)
      Add-Content -Path $profilePath -Value "`n# Codex helpers`n"
      Add-Content -Path $profilePath -Value (Get-Content -Raw -Path (Join-Path $ScriptDir 'codex-init-helpers.md'))
      Write-Log "Appended helpers to $PROFILE"
    }
  }
}

Next-Phase "Verify installation"
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
} else {
  Write-Log "Dry-run: skipping verification"
}

Write-Host "`n✅ Codex installation complete" -ForegroundColor Green
Write-Host "  CODEX_HOME:   $CODEX_HOME"
Write-Host "  SCRIPTS_ROOT: $SCRIPTS_ROOT"
Write-Host "  Config:       $CODEX_HOME\config.toml (trust entries added)"

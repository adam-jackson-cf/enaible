#!/usr/bin/env pwsh
<#!
.SYNOPSIS
    Enaible bootstrap installer for Windows (PowerShell 7+).
#>

[CmdletBinding()]
param(
    [string]$RepoUrl = "https://github.com/adam-jackson-cf/enaible",
    [string]$CloneDir = (Join-Path $env:USERPROFILE ".enaible/sources/enaible"),
    [string[]]$Systems = @("codex", "claude-code"),
    [ValidateSet("user", "project")] [string]$Scope = "user",
    [string]$Project,
    [string]$Ref = "main",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$sessionDir = Join-Path $env:USERPROFILE ".enaible/install-sessions"
$script:PromptReader = $null
$script:PromptInputMode = 'ReadHost'
$script:PromptAvailable = $true
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$defaultRef = "main"

function Write-Log {
    param([string]$Message)
    $timestamp = (Get-Date -AsUTC).ToString("yyyy-MM-ddTHH:mm:ssZ")
    Write-Host "[$timestamp] $Message"
}

function Initialize-PromptInput {
    $script:PromptInputMode = 'ReadHost'
    $script:PromptAvailable = $true

    if (-not [System.Environment]::UserInteractive) {
        $script:PromptAvailable = $false
        $script:PromptInputMode = 'None'
        return
    }

    if (-not [System.Console]::IsInputRedirected) {
        return
    }

    $path = if ($IsWindows) { 'CONIN$' } else { '/dev/tty' }
    try {
        $stream = [System.IO.FileStream]::new(
            $path,
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::Read,
            [System.IO.FileShare]::ReadWrite
        )
        $script:PromptReader = [System.IO.StreamReader]::new($stream)
        $script:PromptInputMode = 'Stream'
    }
    catch {
        $script:PromptAvailable = $false
        $script:PromptInputMode = 'None'
    }
}

function Read-InteractiveInput {
    param(
        [string]$PromptText,
        [string]$DefaultValue
    )

    if (-not $script:PromptAvailable) {
        throw "Interactive input unavailable; provide -Systems and -Scope parameters when running non-interactively."
    }

    $value = $null
    switch ($script:PromptInputMode) {
        'ReadHost' {
            $value = Read-Host -Prompt $PromptText
        }
        'Stream' {
            $label = if ($PromptText.TrimEnd().EndsWith(':')) { $PromptText } else { "${PromptText}:" }
            Write-Host -NoNewline "$label "
            $value = $script:PromptReader.ReadLine()
            if ($null -eq $value) {
                throw "Failed to read interactive input; rerun with -Systems and -Scope."
            }
        }
        default {
            throw "Interactive input unavailable; provide -Systems and -Scope parameters."
        }
    }

    if ([string]::IsNullOrWhiteSpace($value)) {
        return $DefaultValue
    }

    return $value
}

function Invoke-CommandSafe {
    param(
        [string]$Executable,
        [string[]]$Arguments
    )
    if ($DryRun) {
        Write-Log ("DRY-RUN: {0} {1}" -f $Executable, ($Arguments -join ' '))
        return
    }
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command '$Executable' failed with exit code $LASTEXITCODE"
    }
}

function Invoke-WithRepoEnv {
    param([string[]]$Command)
    if ($DryRun) {
        Write-Log ("DRY-RUN: ENAIBLE_REPO_ROOT={0} {1}" -f $CloneDir, ($Command -join ' '))
        return
    }
    $previous = $env:ENAIBLE_REPO_ROOT
    try {
        $env:ENAIBLE_REPO_ROOT = $CloneDir
        $exe = $Command[0]
        $args = @()
        if ($Command.Length -gt 1) {
            $args = $Command[1..($Command.Length - 1)]
        }
        & $exe @args
        if ($LASTEXITCODE -ne 0) {
            throw "Command '$exe' failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        if ($null -ne $previous) {
            $env:ENAIBLE_REPO_ROOT = $previous
        }
        else {
            Remove-Item Env:ENAIBLE_REPO_ROOT -ErrorAction SilentlyContinue
        }
    }
}

function Ensure-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command: $Name"
    }
}

function Update-Clone {
    $parent = Split-Path -Parent $CloneDir
    if (-not (Test-Path $parent)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    }
    $gitDir = Join-Path $CloneDir ".git"
    if (Test-Path $gitDir) {
        Write-Log "Updating existing clone at $CloneDir"
        Invoke-CommandSafe git @('-C', $CloneDir, 'fetch', '--all', '--prune')
        Invoke-CommandSafe git @('-C', $CloneDir, 'checkout', $Ref)
        Invoke-CommandSafe git @('-C', $CloneDir, 'pull', '--rebase', '--autostash', 'origin', $Ref)
    }
    else {
        Write-Log "Cloning $RepoUrl to $CloneDir"
        # Enable long paths to handle deeply nested test fixtures on Windows
        Invoke-CommandSafe git @('config', '--global', 'core.longpaths', 'true')
        Invoke-CommandSafe git @('clone', '--branch', $Ref, $RepoUrl, $CloneDir)
    }
}

function Auto-DetectRef {
    if ($Ref -ne $defaultRef) {
        return
    }

    if ($env:ENAIBLE_INSTALL_REF) {
        $script:Ref = $env:ENAIBLE_INSTALL_REF
        Write-Log "Using ref from ENAIBLE_INSTALL_REF: $Ref"
        return
    }

    try {
        $localRef = git -C (Join-Path $scriptDir "..") rev-parse --abbrev-ref HEAD 2>$null
    }
    catch {
        $localRef = $null
    }
    if ($localRef) {
        $localRef = $localRef.Trim()
        if ($localRef -and $localRef -ne $defaultRef) {
            $script:Ref = $localRef
            Write-Log "Detected ref from local script checkout: $Ref"
        }
    }
}

function Install-Cli {
    Write-Log "Installing Enaible CLI via uv tool install"
    $path = Join-Path $CloneDir 'tools/enaible'
    Invoke-WithRepoEnv @('uv', 'tool', 'install', '--from', $path, 'enaible')
}

function Install-Scope {
    param(
        [string]$ScopeName,
        [string]$Target
    )
    if ($ScopeName -eq 'project' -and -not (Test-Path $Target)) {
        throw "Project scope requested but target '$Target' was not found"
    }
    foreach ($system in $Systems) {
        Write-Log "Installing system '$system' (scope=$ScopeName)"
        $args = @('uv', 'run', '--project', (Join-Path $CloneDir 'tools/enaible'), 'enaible', 'install', $system, '--mode', 'sync', '--scope', $ScopeName, '--no-install-cli')
        if ($ScopeName -eq 'project') {
            $args += @('--target', $Target)
        }
        Invoke-WithRepoEnv $args
    }
}

function Resolve-ProjectPath {
    if ($Project) {
        if (-not (Test-Path $Project)) {
            throw "Provided project path '$Project' does not exist"
        }
        return
    }
    try {
        $root = git rev-parse --show-toplevel 2>$null
    }
    catch {
        $root = $null
    }
    if (-not $root) {
        throw "Project scope requested but --Project was not provided and no git repository detected"
    }
    $script:Project = $root.Trim()
    Write-Log "Detected project at $Project"
}

function Write-SessionLog {
    if ($DryRun) { return }
    if (-not (Test-Path $sessionDir)) {
        New-Item -ItemType Directory -Force -Path $sessionDir | Out-Null
    }
    $file = Join-Path $sessionDir ("session-{0}.md" -f (Get-Date -AsUTC).ToString('yyyyMMddTHHmmssZ'))
    $systemsJoined = $Systems -join ', '
    $content = @(
        "# Enaible bootstrap session",
        "- Repo URL: $RepoUrl",
        "- Clone dir: $CloneDir",
        "- Systems: $systemsJoined",
        "- Scope: $Scope"
    )
    if ($Project) { $content += "- Project: $Project" }
    Set-Content -Path $file -Value $content -Encoding UTF8
    Write-Log "Session log saved to $file"
}

function Prompt-ForSystems {
    if (-not $script:PromptAvailable) {
        throw "Interactive input unavailable; provide -Systems to proceed."
    }
    Write-Log "Select systems to install (space-separated numbers, e.g., '1 2' for codex and claude-code):"
    Write-Host "  1) codex"
    Write-Host "  2) claude-code"
    Write-Host "  3) copilot"
    Write-Host "  4) cursor"
    Write-Host "  5) gemini"
    Write-Host "  6) antigravity"
    Write-Host "  7) pi"

    $selectedSystems = @()
    while ($selectedSystems.Length -eq 0) {
        $selection = Read-InteractiveInput -PromptText "Enter selection (required)"

        $systems = @()
        foreach ($num in $selection -split '\s+') {
            switch ($num.Trim()) {
                "1" { $systems += "codex" }
                "2" { $systems += "claude-code" }
                "3" { $systems += "copilot" }
                "4" { $systems += "cursor" }
                "5" { $systems += "gemini" }
                "6" { $systems += "antigravity" }
                "7" { $systems += "pi" }
                default {
                    if ($num.Trim()) {
                        Write-Log "Invalid selection: $num"
                    }
                }
            }
        }

        if ($systems.Length -gt 0) {
            $selectedSystems = $systems
        } else {
            Write-Log "ERROR: You must select at least one system"
        }
    }

    $script:Systems = $selectedSystems
    Write-Log "Selected systems: $($selectedSystems -join ', ')"
}

function Prompt-ForScope {
    if (-not $script:PromptAvailable) {
        throw "Interactive input unavailable; provide -Scope to proceed."
    }
    Write-Log "Select installation scope:"
    Write-Host "  1) user    - Install to user profile only"
    Write-Host "  2) project - Install to current/specified project only"

    $selection = Read-InteractiveInput -PromptText "Enter selection [1]" -DefaultValue "1"

    switch ($selection.Trim()) {
        "1" { $script:Scope = "user" }
        "2" { $script:Scope = "project" }
        default {
            Write-Log "Invalid selection, defaulting to 'user'"
            $script:Scope = "user"
        }
    }

    Write-Log "Selected scope: $Scope"
}

function Validate-Systems {
    $current = @()
    if ($null -ne $Systems) {
        if ($Systems -is [System.Collections.IEnumerable] -and $Systems -isnot [string]) {
            foreach ($item in $Systems) {
                $current += ,$item
            }
        }
        else {
            $current += ,$Systems
        }
    }
    if ($current.Length -eq 0) {
        throw "No systems specified"
    }
    $expanded = @()
    foreach ($item in $current) {
        $expanded += ($item -split ',', [System.StringSplitOptions]::RemoveEmptyEntries)
    }
    $clean = @()
    foreach ($entry in $expanded) {
        $trimmed = $entry.Trim()
        if ($trimmed) {
            $clean += $trimmed
        }
    }
    if ($clean.Length -eq 0) {
        throw "No systems specified"
    }
    $script:Systems = $clean
}

Initialize-PromptInput

if (-not $PSBoundParameters.ContainsKey('Systems')) {
    Prompt-ForSystems
}

if (-not $PSBoundParameters.ContainsKey('Scope')) {
    Prompt-ForScope
}

Validate-Systems
Ensure-Command git
Ensure-Command python
Ensure-Command uv

Auto-DetectRef

Update-Clone
Install-Cli

switch ($Scope) {
    'user' { Install-Scope -ScopeName 'user' -Target '' }
    'project' {
        Resolve-ProjectPath
        Install-Scope -ScopeName 'project' -Target $Project
    }
}

Write-SessionLog
Write-Log "Bootstrap complete. Add %USERPROFILE%\.local\bin (or uv tools path) to PATH for future shells."

if ($null -ne $script:PromptReader) {
    $script:PromptReader.Dispose()
}

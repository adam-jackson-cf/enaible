#!/usr/bin/env pwsh
<#!
.SYNOPSIS
    Enaible bootstrap installer for Windows (PowerShell 7+).
#>

[CmdletBinding()]
param(
    [string]$RepoUrl = "https://github.com/adam-versed/ai-assisted-workflows.git",
    [string]$CloneDir = (Join-Path $env:USERPROFILE ".enaible/sources/ai-assisted-workflows"),
    [string[]]$Systems = @("codex", "claude-code"),
    [ValidateSet("user", "project", "both")] [string]$Scope = "user",
    [string]$Project,
    [string]$Ref = "main",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$sessionDir = Join-Path $env:USERPROFILE ".enaible/install-sessions"

function Write-Log {
    param([string]$Message)
    $timestamp = (Get-Date -AsUTC).ToString("yyyy-MM-ddTHH:mm:ssZ")
    Write-Host "[$timestamp] $Message"
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
        Invoke-CommandSafe git @('clone', '--branch', $Ref, $RepoUrl, $CloneDir)
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

function Validate-Systems {
    $current = @($Systems)
    if ($current.Count -eq 0) {
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
    if ($clean.Count -eq 0) {
        throw "No systems specified"
    }
    $script:Systems = $clean
}

Validate-Systems
Ensure-Command git
Ensure-Command python
Ensure-Command uv

Update-Clone
Install-Cli

switch ($Scope) {
    'user' { Install-Scope -ScopeName 'user' -Target '' }
    'project' {
        Resolve-ProjectPath
        Install-Scope -ScopeName 'project' -Target $Project
    }
    'both' {
        Resolve-ProjectPath
        Install-Scope -ScopeName 'user' -Target ''
        Install-Scope -ScopeName 'project' -Target $Project
    }
}

Write-SessionLog
Write-Log "Bootstrap complete. Add %USERPROFILE%\.local\bin (or uv tools path) to PATH for future shells."

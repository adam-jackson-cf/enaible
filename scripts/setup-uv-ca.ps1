#!/usr/bin/env pwsh
<#!
.SYNOPSIS
    Merge system + corporate CA bundles for uv/PowerShell environments.
#>

[CmdletBinding()]
param(
    [string]$CorpCA,
    [string]$Output,
    [switch]$PrintExports,
    [switch]$ExportsOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    Write-Host "[setup-uv-ca] $Message"
}

function Resolve-PathSafe {
    param([string]$PathValue)
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return "" }
    $expanded = [Environment]::ExpandEnvironmentVariables($PathValue)
    if ($expanded.StartsWith("~")) {
        $expanded = $expanded -replace '^~', [Environment]::GetFolderPath("UserProfile")
    }
    return [System.IO.Path]::GetFullPath($expanded)
}

function Emit-Exports {
    param([string]$BundlePath)
    Write-Host "Set-Item Env:SSL_CERT_FILE -Value '$BundlePath'"
}

if (-not $Output) {
    if ($env:UV_CA_BUNDLE_PATH) {
        $Output = $env:UV_CA_BUNDLE_PATH
    }
    else {
        $Output = Join-Path $env:USERPROFILE ".config/claude/corp-ca-bundle.pem"
    }
}
$Output = Resolve-PathSafe $Output

if ($ExportsOnly) {
    if (-not (Test-Path $Output)) {
        throw "Bundle not found at $Output. Run without --ExportsOnly first."
    }
    Write-Log "Emitting commands for existing bundle: $Output"
    Emit-Exports $Output
    return
}

if (-not $CorpCA) {
    if ($env:SSL_CERT_FILE -and (Test-Path $env:SSL_CERT_FILE)) {
        $CorpCA = $env:SSL_CERT_FILE
    }
    else {
        throw "Provide -CorpCA /path/to/cert.pem or set SSL_CERT_FILE before running."
    }
}
$CorpCA = Resolve-PathSafe $CorpCA
if (-not (Test-Path $CorpCA)) {
    throw "Corporate CA file not found: $CorpCA"
}

$pythonScript = @"
import os, ssl
paths = ssl.get_default_verify_paths()
for attr in ("cafile", "openssl_cafile"):
    candidate = getattr(paths, attr, None)
    if candidate and os.path.exists(candidate):
        print(candidate)
        raise SystemExit(0)
raise SystemExit(1)
"@

$systemCA = ""
try {
    $systemCA = (& python "-c" $pythonScript).Trim()
} catch {
    $systemCA = ""
}

if (-not $systemCA) {
    if (Test-Path "C:\\Program Files\\Git\\mingw64\\ssl\\cert.pem") {
        $systemCA = "C:\\Program Files\\Git\\mingw64\\ssl\\cert.pem"
    }
    else {
        throw "Unable to locate the system CA bundle automatically. Pass -CorpCA explicitly from the bash helper."
    }
}
$systemCA = Resolve-PathSafe $systemCA
if (-not (Test-Path $systemCA)) {
    throw "System CA file not found: $systemCA"
}
if ($systemCA -eq $CorpCA) {
    throw "System CA path resolved to the same file as the corporate CA. Specify a different --CorpCA path so both bundles can merge."
}

$destDir = Split-Path -Parent $Output
if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
}

$temp = [System.IO.Path]::GetTempFileName()
Get-Content -Path $systemCA -Encoding utf8 | Set-Content -Path $temp -Encoding utf8
Add-Content -Path $temp -Value ""
Get-Content -Path $CorpCA -Encoding utf8 | Add-Content -Path $temp -Encoding utf8
Move-Item -Force -Path $temp -Destination $Output

Write-Log "Merged CA bundle written to $Output"
Write-Host
Write-Host "Add the following to your PowerShell profile (e.g. `$PROFILE):"
Write-Host "  Set-Item Env:SSL_CERT_FILE -Value '$Output'"
Write-Host
Write-Host "Then restart your shell before rerunning enaible install."
Write-Host
Write-Host "Optional (uv only):"
Write-Host "  uv config set http.cabundle '$Output'"
Write-Host
Write-Host "To update the current shell immediately run:"
Emit-Exports $Output

if ($PrintExports) {
    Write-Host
    Write-Host "# Commands for current shell:"
    Emit-Exports $Output
}

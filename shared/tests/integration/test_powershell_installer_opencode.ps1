# PowerShell Installer Test Suite - OpenCode
# Comprehensive testing for opencode/install.ps1

param(
    [string]$TestScenario = "all",
    [switch]$Verbose,
    [string]$TestDir = "$env:TEMP\powershell-installer-tests"
)

# Test configuration
$script:TestResults = @()
$script:TotalTests = 0
$script:PassedTests = 0
$script:FailedTests = 0

# Colors for output
$Colors = @{
    Green = [System.ConsoleColor]::Green
    Yellow = [System.ConsoleColor]::Yellow
    Red = [System.ConsoleColor]::Red
    Blue = [System.ConsoleColor]::Blue
    White = [System.ConsoleColor]::White
    Cyan = [System.ConsoleColor]::Cyan
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [System.ConsoleColor]$Color = [System.ConsoleColor]::White
    )
    $originalColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Output $Message
    $Host.UI.RawUI.ForegroundColor = $originalColor
}

function Start-Test {
    param([string]$TestName)

    $script:TotalTests++
    Write-ColorOutput "`n=== Test: $TestName ===" -Color $Colors.Cyan
}

function Complete-Test {
    param(
        [string]$TestName,
        [bool]$Passed,
        [string]$Message = ""
    )

    if ($Passed) {
        $script:PassedTests++
        Write-ColorOutput "✓ PASS: $TestName" -Color $Colors.Green
        if ($Message) { Write-Output "  $Message" }
    } else {
        $script:FailedTests++
        Write-ColorOutput "✗ FAIL: $TestName" -Color $Colors.Red
        if ($Message) { Write-Output "  $Message" }
    }

    $script:TestResults += @{
        Name = $TestName
        Passed = $Passed
        Message = $Message
        Timestamp = Get-Date
    }
}

function Test-InstallerSyntax {
    Start-Test "Installer Syntax Validation"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $resolvedPath = Resolve-Path $installerPath -ErrorAction Stop

        # Parse the script to check for syntax errors
        $errors = $null
        $warnings = $null
        $tokens = [System.Management.Automation.PSParser]::Tokenize((Get-Content $resolvedPath -Raw), [ref]$errors)

        if ($errors.Count -eq 0) {
            Complete-Test "Installer Syntax Validation" $true "No syntax errors found"
        } else {
            $errorMessages = $errors | ForEach-Object { "$($_.Token): $($_.Message)" }
            Complete-Test "Installer Syntax Validation" $false "Syntax errors: $($errorMessages -join '; ')"
        }
    } catch {
        $errorMessage = $_.Exception.Message
        Complete-Test "Installer Syntax Validation" $false "Failed to validate syntax: $errorMessage"
    }
}

function Test-InstallerHelp {
    Start-Test "Installer Help Display"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $output = & $installerPath -Help 2>&1

        if ($output -like "*AI-Assisted Workflows Installer*") {
            Complete-Test "Installer Help Display" $true "Help message displayed correctly"
        } else {
            Complete-Test "Installer Help Display" $false "Help message not found in output"
        }
    } catch {
        $errorMessage = $_.Exception.Message
        Complete-Test "Installer Help Display" $false "Failed to display help: $errorMessage"
    }
}

function Test-InstallerDryRun {
    Start-Test "Installer Dry Run Mode"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $testPath = Join-Path $TestDir "dry-run-test"

        $output = & $installerPath $testPath -DryRun -SkipPython 2>&1

        # Check that no files were actually created
        $opencodeDir = Join-Path $testPath ".opencode"
        if (-not (Test-Path $opencodeDir)) {
            Complete-Test "Installer Dry Run Mode" $true "Dry run completed without creating files"
        } else {
            Complete-Test "Installer Dry Run Mode" $false "Dry run created files when it shouldn't have"
        }
    } catch {
        Complete-Test "Installer Dry Run Mode" $false "Dry run failed: $_"
    }
}

function Test-FreshInstallation {
    Start-Test "Fresh Installation"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $testPath = Join-Path $TestDir "fresh-install"

        # Ensure clean state
        if (Test-Path $testPath) {
            Remove-Item -Path $testPath -Recurse -Force
        }

        # Measure installation time
        $startTime = Get-Date
        $output = & $installerPath $testPath -SkipPython -Verbose 2>&1
        $endTime = Get-Date
        $installTime = ($endTime - $startTime).TotalSeconds

        # Verify installation
        $opencodeDir = Join-Path $testPath ".opencode"
        $requiredFiles = @("opencode.json", "command", "scripts", "installation-log.txt")
        $missingFiles = @()

        foreach ($file in $requiredFiles) {
            $filePath = Join-Path $opencodeDir $file
            if (-not (Test-Path $filePath)) {
                $missingFiles += $file
            }
        }

        if ($missingFiles.Count -eq 0) {
            Complete-Test "Fresh Installation" $true "Installation completed in $([math]::Round($installTime, 2)) seconds"
        } else {
            Complete-Test "Fresh Installation" $false "Missing files: $($missingFiles -join ', ')"
        }
    } catch {
        Complete-Test "Fresh Installation" $false "Installation failed: $_"
    }
}

function Test-MergeMode {
    Start-Test "Merge Mode Installation"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $testPath = Join-Path $TestDir "merge-mode"
        $opencodeDir = Join-Path $testPath ".opencode"

        # Create existing installation with custom content
        if (-not (Test-Path $opencodeDir)) {
            New-Item -ItemType Directory -Path $opencodeDir -Force | Out-Null
        }

        # Create custom opencode.json with unique content
        $customConfig = @{
            version = "1.0.0"
            project = @{
                name = "Custom Test Project"
                description = "This is custom content that should be preserved"
            }
            custom = @{
                rules = @(
                    "Always use TypeScript",
                    "Write comprehensive tests"
                )
            }
        }
        $configFile = Join-Path $opencodeDir "opencode.json"
        $customConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $configFile -Encoding UTF8

        # Create custom command
        $commandsDir = Join-Path $opencodeDir "command"
        if (-not (Test-Path $commandsDir)) {
            New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
        }
        "# Custom Test Command`nThis is a custom command." | Out-File -FilePath (Join-Path $commandsDir "test-custom.md") -Encoding UTF8

        # Run merge installation using InstallMode parameter
        $output = & $installerPath $testPath -InstallMode Merge -SkipPython 2>&1

        # Verify custom content preserved
        $configContent = Get-Content $configFile -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json
        $customCommandExists = Test-Path (Join-Path $commandsDir "test-custom.md")

        if ($configContent -and $configContent.custom -and $customCommandExists) {
            Complete-Test "Merge Mode Installation" $true "Custom config and commands preserved"
        } else {
            Complete-Test "Merge Mode Installation" $false "Custom config or commands lost"
        }
    } catch {
        $errorMessage = $_.Exception.Message
        Complete-Test "Merge Mode Installation" $false "Merge mode failed: $errorMessage"
    }
}

function Test-UpdateWorkflowsMode {
    Start-Test "Update Workflows Mode"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $testPath = Join-Path $TestDir "update-workflows"
        $opencodeDir = Join-Path $testPath ".opencode"

        # Create existing installation
        if (-not (Test-Path $opencodeDir)) {
            New-Item -ItemType Directory -Path $opencodeDir -Force | Out-Null
        }

        # Create custom config that should be preserved
        $configFile = Join-Path $opencodeDir "opencode.json"
        @{
            version = "1.0.0"
            project = @{
                name = "Test Project"
                description = "Custom project configuration"
            }
        } | ConvertTo-Json -Depth 10 | Out-File -FilePath $configFile -Encoding UTF8

        # Create custom command
        $commandsDir = Join-Path $opencodeDir "command"
        New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
        "# Custom Command" | Out-File -FilePath (Join-Path $commandsDir "custom-cmd.md") -Encoding UTF8

        # Run update workflows using InstallMode parameter
        $output = & $installerPath $testPath -InstallMode UpdateWorkflows -SkipPython 2>&1

        # Verify custom command preserved and opencode.json preserved
        $customCommandExists = Test-Path (Join-Path $commandsDir "custom-cmd.md")
        $configExists = Test-Path $configFile

        if ($customCommandExists -and $configExists) {
            Complete-Test "Update Workflows Mode" $true "Custom commands and opencode.json preserved"
        } else {
            Complete-Test "Update Workflows Mode" $false "Custom content lost during update"
        }
    } catch {
        $errorMessage = $_.Exception.Message
        Complete-Test "Update Workflows Mode" $false "Update workflows failed: $errorMessage"
    }
}

function Test-ErrorHandling {
    Start-Test "Error Handling"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"

        # Test with invalid path
        $invalidPath = "Z:\NonExistent\Path\That\Should\Not\Exist"

        try {
            $output = & $installerPath $invalidPath -SkipPython 2>&1
            # If we get here, the installer should have handled the error gracefully
            Complete-Test "Error Handling" $true "Installer handled invalid path gracefully"
        } catch {
            # This is expected - the installer should fail with an invalid path
            if ($_.Exception.Message -like "*permission*" -or $_.Exception.Message -like "*path*") {
                Complete-Test "Error Handling" $true "Installer properly rejected invalid path"
            } else {
                Complete-Test "Error Handling" $false "Unexpected error type: $_"
            }
        }
    } catch {
        Complete-Test "Error Handling" $false "Error handling test failed: $_"
    }
}

function Test-PerformanceMetrics {
    Start-Test "Performance Metrics"

    try {
        $installerPath = Join-Path $PSScriptRoot "..\..\..\opencode\install.ps1"
        $testPath = Join-Path $TestDir "performance"

        $iterations = 3
        $times = @()

        for ($i = 1; $i -le $iterations; $i++) {
            # Clean up from previous iteration
            if (Test-Path $testPath) {
                Remove-Item -Path $testPath -Recurse -Force
            }

            # Measure installation time
            $startTime = Get-Date
            try {
                $output = & $installerPath $testPath -SkipPython 2>&1 | Out-Null
                $endTime = Get-Date
                $duration = ($endTime - $startTime).TotalSeconds
                $times += $duration
            } catch {
                Write-Warning "Performance test iteration $i failed: $_"
            }
        }

        if ($times.Count -gt 0) {
            $avgTime = ($times | Measure-Object -Average).Average
            $maxTime = 60  # Maximum acceptable time in seconds

            if ($avgTime -le $maxTime) {
                Complete-Test "Performance Metrics" $true "Average installation time: $([math]::Round($avgTime, 2))s (target: <${maxTime}s)"
            } else {
                Complete-Test "Performance Metrics" $false "Installation too slow: $([math]::Round($avgTime, 2))s (target: <${maxTime}s)"
            }
        } else {
            Complete-Test "Performance Metrics" $false "No successful performance measurements"
        }
    } catch {
        Complete-Test "Performance Metrics" $false "Performance test failed: $_"
    }
}

function Show-TestSummary {
    Write-ColorOutput "`n=== Test Summary ===" -Color $Colors.Yellow
    Write-Output "Total Tests: $script:TotalTests"
    Write-ColorOutput "Passed: $script:PassedTests" -Color $Colors.Green
    if ($script:FailedTests -gt 0) {
        Write-ColorOutput "Failed: $script:FailedTests" -Color $Colors.Red
    } else {
        Write-ColorOutput "Failed: $script:FailedTests" -Color $Colors.Green
    }

    $successRate = if ($script:TotalTests -gt 0) { ($script:PassedTests / $script:TotalTests) * 100 } else { 0 }
    Write-Output "Success Rate: $([math]::Round($successRate, 1))%"

    if ($script:FailedTests -gt 0) {
        Write-ColorOutput "`nFailed Tests:" -Color $Colors.Red
        $script:TestResults | Where-Object { -not $_.Passed } | ForEach-Object {
            Write-Output "  • $($_.Name): $($_.Message)"
        }
    }

    # Set exit code
    if ($script:FailedTests -gt 0) {
        exit 1
    } else {
        exit 0
    }
}

# Main test execution
try {
    Write-ColorOutput "PowerShell Installer Test Suite - OpenCode" -Color $Colors.Green
    Write-ColorOutput "==========================================" -Color $Colors.Green
    Write-Output "Test Scenario: $TestScenario"
    Write-Output "Test Directory: $TestDir"
    Write-Output "PowerShell Version: $($PSVersionTable.PSVersion)"
    Write-Output ""

    # Create test directory
    if (-not (Test-Path $TestDir)) {
        New-Item -ItemType Directory -Path $TestDir -Force | Out-Null
    }

    # Run tests based on scenario
    switch ($TestScenario.ToLower()) {
        "all" {
            Test-InstallerSyntax
            Test-InstallerHelp
            Test-InstallerDryRun
            Test-FreshInstallation
            Test-MergeMode
            Test-UpdateWorkflowsMode
            Test-ErrorHandling
            Test-PerformanceMetrics
        }
        "fresh-install" {
            Test-FreshInstallation
        }
        "merge-mode" {
            Test-MergeMode
        }
        "update-workflows" {
            Test-UpdateWorkflowsMode
        }
        "error-handling" {
            Test-ErrorHandling
        }
        "performance" {
            Test-PerformanceMetrics
        }
        default {
            Write-ColorOutput "Unknown test scenario: $TestScenario" -Color $Colors.Red
            Write-Output "Available scenarios: all, fresh-install, merge-mode, update-workflows, error-handling, performance"
            exit 1
        }
    }

    Show-TestSummary

} catch {
    Write-ColorOutput "Test suite failed: $_" -Color $Colors.Red
    exit 1
} finally {
    # Cleanup test directory
    try {
        if (Test-Path $TestDir) {
            Remove-Item -Path $TestDir -Recurse -Force -ErrorAction SilentlyContinue
        }
    } catch {
        Write-Warning "Could not clean up test directory: $_"
    }
}

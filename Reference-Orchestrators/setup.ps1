# FITPAC Reference-Orchestrators setup script (Windows).
# Run from your project root. Copies the correct rule/orchestrator files for your IDE.
# Usage: .\setup.ps1 [path-to-Reference-Orchestrators]
#   If no path is given, uses the directory containing this script as the source.
#   Use -Force to skip overwrite confirmations (e.g. for CI).
# Requires: PowerShell 5.1 or PowerShell Core (Windows / macOS / Linux).

param(
    [Parameter(Position = 0)]
    [string]$PathToReferenceOrchestrators = $null,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = $PSScriptRoot
$SOURCE = if ($PathToReferenceOrchestrators) { $PathToReferenceOrchestrators } else { $SCRIPT_DIR }
$TARGET = (Get-Location).Path

if (-not (Test-Path -LiteralPath $SOURCE -PathType Container)) {
    Write-Error "Source directory not found: $SOURCE"
    Write-Host "Usage: .\setup.ps1 [-Force] [path-to-Reference-Orchestrators]"
    exit 1
}

function Confirm-Overwrite {
    param([string]$Path)
    if ($Force) { return $true }
    if (Test-Path -LiteralPath $Path) {
        $ans = Read-Host "Overwrite $Path? [y/N]"
        return ($ans -eq "y" -or $ans -eq "Y")
    }
    return $true
}

function Copy-Safe {
    param([string]$Src, [string]$Dst)
    if (-not (Test-Path -LiteralPath $Src)) {
        Write-Error "Missing source $Src"
        exit 1
    }
    $parent = Split-Path -Parent $Dst
    if ($parent -and -not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    if (Confirm-Overwrite -Path $Dst) {
        if (Test-Path -LiteralPath $Dst) {
            Remove-Item -LiteralPath $Dst -Recurse -Force
        }
        Copy-Item -LiteralPath $Src -Destination $Dst -Recurse -Force
        Write-Host "  Copied: $Dst"
    }
}

Write-Host "FITPAC orchestrator setup"
Write-Host "  Source: $SOURCE"
Write-Host "  Target (project root): $TARGET"
Write-Host ""

if ($SOURCE -eq $TARGET) {
    Write-Host "Warning: Source and target are the same. Run this script from your project root with the path to Reference-Orchestrators, or run it from inside Reference-Orchestrators with target as parent."
    Write-Host ""
}

Write-Host "Which IDE are you using?"
Write-Host "  1) Cursor"
Write-Host "  2) Windsurf"
Write-Host "  3) VS Code (Continue / Claude)"
Write-Host "  4) GitHub Copilot"
Write-Host "  5) Roo Code"
Write-Host "  6) Universal (show instructions only; no copy)"
$choice = Read-Host "Choice [1-6]"

$cursorRules = Join-Path $SOURCE "Cursor" ".cursorrules"
$cursorOrch = Join-Path $SOURCE "Cursor" "orchestrator"
$cursorSkills = Join-Path $SOURCE "Cursor" ".cursor" "skills"
$windsurfRules = Join-Path $SOURCE "Windsurf" ".windsurfrules"
$windsurfOrch = Join-Path $SOURCE "Windsurf" "orchestrator"
$vscodeContinue = Join-Path $SOURCE "VSCode" ".continue"
$vscodeClaude = Join-Path $SOURCE "VSCode" "claude" "CLAUDE.md"
$vscodeOrch = Join-Path $SOURCE "VSCode" "orchestrator"
$copilotInst = Join-Path $SOURCE "GitHub-Copilot" "github" "copilot-instructions.md"
$copilotOrch = Join-Path $SOURCE "GitHub-Copilot" "orchestrator"
$rooRules = Join-Path $SOURCE "Roo-Code" ".clinerules"
$rooOrch = Join-Path $SOURCE "Roo-Code" "orchestrator"
$universalInstr = Join-Path $SOURCE "Universal" "FITPAC_INSTRUCTIONS.md"

switch ($choice) {
    "1" {
        Write-Host "Installing Cursor orchestrator..."
        Copy-Safe -Src $cursorRules -Dst (Join-Path $TARGET ".cursorrules")
        Copy-Safe -Src $cursorOrch -Dst (Join-Path $TARGET "orchestrator")
        if (-not $Force) {
            $skill = Read-Host "Install Cursor skill (optional)? [y/N]"
            if ($skill -eq "y" -or $skill -eq "Y") {
                $skillsDst = Join-Path $TARGET ".cursor" "skills"
                New-Item -ItemType Directory -Path $skillsDst -Force | Out-Null
                if (Test-Path -LiteralPath $cursorSkills -PathType Container) {
                    Get-ChildItem -LiteralPath $cursorSkills | Copy-Item -Destination $skillsDst -Recurse -Force
                    Write-Host "  Copied: .cursor/skills/"
                }
            }
        }
        Write-Host "Done. Open the project in Cursor."
    }
    "2" {
        Write-Host "Installing Windsurf orchestrator..."
        Copy-Safe -Src $windsurfRules -Dst (Join-Path $TARGET ".windsurfrules")
        Copy-Safe -Src $windsurfOrch -Dst (Join-Path $TARGET "orchestrator")
        Write-Host "Done. Open the project in Windsurf."
    }
    "3" {
        Write-Host "Installing VS Code orchestrator (Continue + Claude)..."
        Copy-Safe -Src $vscodeContinue -Dst (Join-Path $TARGET ".continue")
        Copy-Safe -Src $vscodeClaude -Dst (Join-Path $TARGET "CLAUDE.md")
        Copy-Safe -Src $vscodeOrch -Dst (Join-Path $TARGET "orchestrator")
        Write-Host "Done. Open the project in VS Code with Continue and/or Claude Code."
    }
    "4" {
        Write-Host "Installing GitHub Copilot orchestrator..."
        $githubDir = Join-Path $TARGET ".github"
        New-Item -ItemType Directory -Path $githubDir -Force | Out-Null
        Copy-Safe -Src $copilotInst -Dst (Join-Path $githubDir "copilot-instructions.md")
        Copy-Safe -Src $copilotOrch -Dst (Join-Path $TARGET "orchestrator")
        Write-Host "Done. Use the project in a Copilot-enabled environment."
    }
    "5" {
        Write-Host "Installing Roo Code orchestrator..."
        Copy-Safe -Src $rooRules -Dst (Join-Path $TARGET ".clinerules")
        Copy-Safe -Src $rooOrch -Dst (Join-Path $TARGET "orchestrator")
        Write-Host "Done. Open the project in VS Code with Roo Code."
    }
    "6" {
        Write-Host ""
        Write-Host "Universal: no files are copied. Copy the contents of this file into your AI's System Prompt or Custom Instructions:"
        Write-Host "  $universalInstr"
        Write-Host ""
        if (Test-Path -LiteralPath $universalInstr -PathType Leaf) {
            $absPath = (Resolve-Path -LiteralPath $universalInstr).Path
            Write-Host "Path (absolute): $absPath"
        }
    }
    default {
        Write-Host "Invalid choice. Exiting."
        exit 1
    }
}

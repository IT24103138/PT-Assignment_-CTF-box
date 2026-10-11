$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

Write-Host "Step 1: Downloading Moodle..."
& "$PSScriptRoot\download-moodle.ps1"

Write-Host "Step 2: Downloading Moodle Docker..."
& "$PSScriptRoot\download-moodle-docker.ps1"

Write-Host "Step 3: Configuring Moodle Docker..."
& "$PSScriptRoot\configure-moodle.ps1"

Write-Host "Moodle source and Docker configuration prepared."

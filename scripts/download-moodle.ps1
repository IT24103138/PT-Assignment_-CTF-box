$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $projectRoot "moodle-source"

if (Test-Path $sourceDir) {
    Write-Host "Moodle source folder already exists. Skipping download."
    exit 0
}

Write-Host "Downloading Moodle v4.5.15..."

git clone https://github.com/moodle/moodle.git $sourceDir

if ($LASTEXITCODE -ne 0) {
    throw "Moodle download failed."
}

git -C $sourceDir checkout 215f44380bdc3ccf852a3a22e34f8423ff64033a

if ($LASTEXITCODE -ne 0) {
    throw "Moodle checkout failed."
}

Write-Host "Moodle source downloaded successfully."

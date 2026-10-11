$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$targetDir = Join-Path $projectRoot "moodle-docker-source"

if (Test-Path $targetDir) {
    Write-Host "Moodle Docker folder already exists. Skipping."
    exit 0
}

git clone https://github.com/moodlehq/moodle-docker.git $targetDir

if ($LASTEXITCODE -ne 0) {
    throw "Moodle Docker download failed."
}

git -C $targetDir checkout f4c2324d32fb74d7753264381f0a9b418b6034b2

if ($LASTEXITCODE -ne 0) {
    throw "Moodle Docker checkout failed."
}

Write-Host "Moodle Docker downloaded successfully."

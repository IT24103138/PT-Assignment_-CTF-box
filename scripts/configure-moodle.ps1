$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$target = Join-Path $root "moodle-docker-source"
$config = Join-Path $root "moodle"

if (-not (Test-Path $target)) {
    throw "Moodle Docker source not found. Run download-moodle-docker.ps1 first."
}

$files = @(
    "base.yml",
    "db.mariadb.yml",
    "localhost.override.yml"
)

foreach ($file in $files) {
    Copy-Item (Join-Path $config $file) (Join-Path $target $file) -Force
}

Write-Host "Moodle Docker configuration files copied successfully."

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$destination = Join-Path $root "ctfd-source"

if (Test-Path $destination) {
    Write-Host "CTFd source folder already exists."
    exit 0
}

git clone https://github.com/CTFd/CTFd.git $destination
git -C $destination checkout 6b01b531e8445c781a8bdcdc9409400e19207037

Write-Host "CTFd source downloaded successfully."


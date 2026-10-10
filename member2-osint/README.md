# Member 2 - OSINT Challenges (IE3132 CTF Play Box, Group 64)

Author: Kapilan V (IT24103425)

## Stages
OSINT-01 The New Hire - flag in the image EXIF Comment - port 8081
OSINT-02 Breadcrumbs in the Git Repository - flag in a deleted file in Git history - port 3000

## Requirements
Kali Linux VM on an isolated (host-only) network, Docker, git, exiftool, imagemagick,
Python 3 with the requests library.

## Run
OSINT-01: cd osint01 and run: sudo docker compose up -d   (open http://localhost:8081)
OSINT-02: cd osint02 and run: sudo docker compose up -d, wait 30 seconds, then run ./reset.sh
          (open http://localhost:3000)

## Solvers
python3 solvers/osint01_solver.py
python3 solvers/osint02_solver.py

## Hints
OSINT-01: 1) Staff emails follow a predictable pattern. 2) Inspect the image metadata.
OSINT-02: 1) Deleted content can remain in Git history. 2) Check earlier commits.

## Reset
OSINT-01: sudo docker compose down && sudo docker compose up -d
OSINT-02: ./reset.sh

## Safety
All names, emails, credentials and flags are fictional. The VM has no internet or
university network access.

## Tools used
Docker, nginx, Gitea, Git, ExifTool, ImageMagick, Python (requests), Kali Linux

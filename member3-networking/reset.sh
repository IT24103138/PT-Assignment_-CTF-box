#!/usr/bin/env bash
# Reset / recovery for the Networking CTF stages.
#
#   ./reset.sh            -> restart all stages back to their initial state
#   ./reset.sh net01      -> reset only NET-01 (grading-system)
#   ./reset.sh net02      -> reset only NET-02 (library-ftp)
#   ./reset.sh full       -> tear down everything and rebuild from images
#
# Because every challenge container is built from a fixed image and holds no
# persistent player-writable state, a restart restores it instantly. "full"
# additionally removes and recreates the containers from scratch.
set -euo pipefail

case "${1:-all}" in
  net01) svc=grading-system ;;
  net02) svc=library-ftp ;;
  all)   svc="" ;;
  full)
    echo "[*] Full rebuild: down + up --build"
    docker compose down
    docker compose up -d --build
    exit 0 ;;
  *) echo "usage: $0 [all|net01|net02|full]"; exit 1 ;;
esac

if [[ -z "$svc" ]]; then
  echo "[*] Restarting ALL stages to initial state..."
  docker compose restart
else
  echo "[*] Restarting $svc to initial state..."
  docker compose restart "$svc"
fi
echo "[+] Done."

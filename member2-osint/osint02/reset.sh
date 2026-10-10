#!/bin/bash
cd ~/ctf-osint/osint02
sudo docker-compose down
sudo rm -rf gitea-data
sudo docker-compose up -d
sleep 30
sudo docker exec -u git ctf-gitea gitea admin user create --username ctfadmin --password CtfAdmin2026 --email admin@ctf.local --admin --must-change-password=false
curl -s -u ctfadmin:CtfAdmin2026 -X POST http://localhost:3000/api/v1/user/repos -H "Content-Type: application/json" -d '{"name":"it-club-portal","private":false}'
rm -rf /tmp/restore
git clone ~/ctf-osint/osint02/seed.bundle /tmp/restore
cd /tmp/restore
git remote add gitea http://ctfadmin:CtfAdmin2026@localhost:3000/ctfadmin/it-club-portal.git
git push gitea --all -f
echo "Reset complete"

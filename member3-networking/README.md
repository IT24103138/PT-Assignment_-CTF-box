# University Campus Network CTF — Networking Domain (Member 3)

**Module:** IE3132 Penetration Testing — Assignment 02 (Working Box Demonstration)
**Member 3 — Challenge Design B (Networking)** — NET-01 and NET-02 (as approved in Assignment 01)

Isolated Docker Compose lab on the `10.10.20.0/24` subnet.

| Stage  | Title                 | Domain     | Difficulty      | Core skill                              |
|--------|-----------------------|------------|-----------------|------------------------------------------|
| NET-01 | Shadow Service        | Networking | Easy            | Host discovery + full-range port scan + banner grab |
| NET-02 | Intercepted Transcript| Networking | Moderate–Hard   | Packet analysis + cleartext creds + FTP + Base64 |

**Flag format:** `SLIIT{...}`

## Topology

```
                 CTF subnet 10.10.20.0/24  (isolated Docker bridge)
   +-------------------------------------------------------------------+
   |  attacker       10.10.20.100   <- you solve from here             |
   |  decoy-ssh      10.10.20.21    (SSH red herring)        [NET-01]  |
   |  decoy-web      10.10.20.22    (HTTP red herring)       [NET-01]  |
   |  grading-system 10.10.20.30    hidden banner :40123     [NET-01]  |
   |  library-ftp    10.10.20.50    cleartext FTP :21        [NET-02]  |
   +-------------------------------------------------------------------+
```

No challenge port is published to the host — the lab can't be reached from
outside the Docker network. You scan/solve from the `attacker` container on the
same subnet. (This is the isolation control.)

## Build & run

```bash
docker compose up -d --build
docker compose ps                 # all 5 containers "running"
docker compose exec attacker bash # your workstation on the CTF subnet
```

## Solve — NET-01 Shadow Service
```bash
nmap -sn 10.10.20.0/24            # discover live hosts
nmap -p- 10.10.20.30              # full port scan -> finds 40123/tcp
nc 10.10.20.30 40123             # read the flag from the banner
```
A default nmap scan checks only the top 1000 ports and deliberately misses
40123; `-p-` scans all 65,535.

## Solve — NET-02 Intercepted Transcript
1. Open `net02-intercepted-transcript/challenge.pcap` in **Wireshark** →
   filter `ftp` → right-click → **Follow → TCP Stream** → read the cleartext
   `USER` / `PASS`. (CLI alternative in the container: `tshark -r /opt/challenge.pcap -Y ftp`)
2. Log in to the live server and get the file:
   ```bash
   ftp 10.10.20.50       # user: libadmin   pass: (from the pcap)
   get db_recovery.txt
   bye
   ```
3. Decode: `base64 -d db_recovery.txt`   → `SLIIT{...}`

## Solver scripts (LO3 — self-developed automation)
Inside the attacker container (`/opt/solvers/`):
```bash
python3 /opt/solvers/solve_net01.py --target 10.10.20.30
python3 /opt/solvers/solve_net02.py --pcap /opt/challenge.pcap --host 10.10.20.50
```

## Reset / recovery
```bash
docker compose restart                 # reset both stages to initial state
docker compose restart grading-system  # reset only NET-01
docker compose restart library-ftp     # reset only NET-02
docker compose down && docker compose up -d --build   # full rebuild
```
Containers hold no persistent player-writable state; FTP is read-only
(`perm="elr"`), so players can't alter the box.

## Customising (flags / creds)
| What          | Where |
|---------------|-------|
| NET-01 flag   | `net01-shadow-service/Dockerfile` (`FLAG=`) |
| NET-02 flag   | regenerate `net02-intercepted-transcript/ftproot/db_recovery.txt` = base64 of new flag |
| FTP user/pass | `net02-intercepted-transcript/Dockerfile` **and** regenerate the pcap (see `pcapgen/`) |

After any edit: `docker compose up -d --build`.

## Tools used (acknowledgement)
nmap, Wireshark/tshark, ftp, netcat, base64; pyftpdlib (FTP server); Scapy
(used offline to craft `challenge.pcap`). Base images: `python:3.12-slim`,
`debian:12-slim`, `nginx:alpine`. All services are intentionally vulnerable,
created for this CTF only, and isolated from institutional/public systems.

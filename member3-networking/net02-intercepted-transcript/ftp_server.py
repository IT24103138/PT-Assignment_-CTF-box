#!/usr/bin/env python3
"""
NET-02  "Intercepted Transcript"  -  the Library Database FTP server.

A deliberately INSECURE, cleartext FTP service. The CTF-only account
`libadmin` can log in and read one file, db_recovery.txt, whose contents
are the Base64-encoded flag.

The credentials for this account were captured earlier in a packet trace
(challenge.pcap) because FTP sends USER/PASS in plain text. Players recover
the credentials from the pcap, log in here, download db_recovery.txt, and
Base64-decode it to reveal the flag.

Creds and flag file are provided via environment / the mounted ftproot so
they can be changed without editing code.
"""
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_USER = os.environ.get("FTP_USER", "libadmin")
FTP_PASS = os.environ.get("FTP_PASS", "L1br@ry_2026")
FTP_ROOT = os.environ.get("FTP_ROOT", "/srv/ftp")
# Address other hosts use to reach this server (for PASV replies).
MASQUERADE = os.environ.get("MASQUERADE_ADDRESS", "10.10.20.50")


def main():
    authorizer = DummyAuthorizer()
    # 'elr' = read-only: list dirs (l), change dir (e), retrieve files (r).
    # No write/delete/upload perms -> players cannot tamper with the box.
    authorizer.add_user(FTP_USER, FTP_PASS, FTP_ROOT, perm="elr")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "220 Library Database FTP (vsFTPd 3.0.5 compatible)"
    # Passive-mode settings so transfers work across the Docker network.
    handler.masquerade_address = MASQUERADE
    handler.passive_ports = range(60000, 60011)

    server = FTPServer(("0.0.0.0", 21), handler)
    server.max_cons = 64
    print(f"[NET-02] Library FTP listening on 0.0.0.0:21 "
          f"(user={FTP_USER}, root={FTP_ROOT})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
NET-01  "Shadow Service"  -  the hidden Grading System banner server.

During the (fictional) campus IT migration, the Grading System was left
running on a high, non-standard TCP port and dropped from the service
directory. When any TCP client connects, the server immediately prints a
static banner that contains the CTF flag, then closes the connection.

Intended solve:
    nmap -sn 10.10.20.0/24            # find live hosts
    nmap -p- 10.10.20.30              # full port scan finds :40123
    nc 10.10.20.30 40123             # read the flag from the banner

The flag is read from the FLAG environment variable so it can be changed
without touching code (see docker-compose / Dockerfile).
"""
import os
import socket
import threading

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "40123"))
FLAG = os.environ.get("FLAG", "SLIIT{sh4d0w_s3rv1c3_0n_p0rt_40123}")

BANNER = (
    "=====================================================\n"
    "  CAMPUS GRADING SYSTEM  --  LEGACY NODE (DO NOT USE)\n"
    "=====================================================\n"
    "  Status : DECOMMISSIONED during IT services migration\n"
    "  Notice : This endpoint was removed from the public\n"
    "           campus service directory. If you are reading\n"
    "           this, you found what migration left behind.\n"
    "-----------------------------------------------------\n"
    f"  flag: {FLAG}\n"
    "=====================================================\n"
)


def handle(conn, addr):
    try:
        conn.sendall(BANNER.encode())
    except OSError:
        pass
    finally:
        conn.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(16)
    print(f"[NET-01] Shadow Service listening on {HOST}:{PORT}", flush=True)
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()

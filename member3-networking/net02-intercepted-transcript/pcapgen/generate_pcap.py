#!/usr/bin/env python3
"""
Generate challenge.pcap for NET-02 "Intercepted Transcript".

This fabricates a realistic, fully valid FTP *control-channel* conversation
between a staff workstation and the Library Database server, with correct TCP
handshake, sequence/ack numbers and teardown, so that opening it in Wireshark
and using "Follow TCP Stream" cleanly shows the cleartext USER/PASS.

IMPORTANT (challenge design): the capture contains ONLY the control channel
(login). It does NOT contain the flag file transfer - players must use the
recovered credentials to log into the LIVE server and download the file.
The username/password below MUST match the live FTP server's credentials.

Run:  python3 generate_pcap.py   ->   writes ../challenge.pcap
"""
import os
from scapy.all import Ether, IP, TCP, Raw, wrpcap

# ---- actors ---------------------------------------------------------------
STAFF_IP   = "10.10.20.77"      # staff workstation that was being monitored
STAFF_PORT = 49722
FTP_IP     = "10.10.20.50"      # Library Database FTP server
FTP_PORT   = 21

# ---- credentials (MUST match the live FTP server) -------------------------
FTP_USER = os.environ.get("FTP_USER", "libadmin")
FTP_PASS = os.environ.get("FTP_PASS", "L1br@ry_2026")

# The ordered FTP control dialogue. ("S", text) = server->client line,
# ("C", text) = client->server command. CRLF added automatically.
DIALOG = [
    ("S", "220 Library Database FTP (vsFTPd 3.0.5 compatible)"),
    ("C", f"USER {FTP_USER}"),
    ("S", "331 Please specify the password."),
    ("C", f"PASS {FTP_PASS}"),
    ("S", "230 Login successful."),
    ("C", "SYST"),
    ("S", "215 UNIX Type: L8"),
    ("C", "PWD"),
    ("S", '257 "/" is the current directory'),
    ("C", "TYPE I"),
    ("S", "200 Switching to Binary mode."),
    ("C", "QUIT"),
    ("S", "221 Goodbye."),
]

ETH_C = Ether(src="02:42:0a:0a:14:4d", dst="02:42:0a:0a:14:32")  # staff -> ftp
ETH_S = Ether(src="02:42:0a:0a:14:32", dst="02:42:0a:0a:14:4d")  # ftp -> staff


def main():
    pkts = []
    t = 1760100000.0            # arbitrary base capture time (epoch seconds)

    # relative-looking but valid absolute ISNs
    cseq = 1000                 # client initial seq
    sseq = 5000                 # server initial seq

    def add(pkt):
        nonlocal t
        pkt.time = t
        t += 0.012
        pkts.append(pkt)

    # ---- TCP 3-way handshake ----------------------------------------------
    add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
        TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="S", seq=cseq))
    cseq += 1
    add(ETH_S / IP(src=FTP_IP, dst=STAFF_IP) /
        TCP(sport=FTP_PORT, dport=STAFF_PORT, flags="SA", seq=sseq, ack=cseq))
    sseq += 1
    add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
        TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="A", seq=cseq, ack=sseq))

    # ---- control dialogue --------------------------------------------------
    for who, line in DIALOG:
        payload = (line + "\r\n").encode()
        if who == "S":
            add(ETH_S / IP(src=FTP_IP, dst=STAFF_IP) /
                TCP(sport=FTP_PORT, dport=STAFF_PORT, flags="PA",
                    seq=sseq, ack=cseq) / Raw(load=payload))
            sseq += len(payload)
            # client acknowledges
            add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
                TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="A",
                    seq=cseq, ack=sseq))
        else:
            add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
                TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="PA",
                    seq=cseq, ack=sseq) / Raw(load=payload))
            cseq += len(payload)
            # server acknowledges
            add(ETH_S / IP(src=FTP_IP, dst=STAFF_IP) /
                TCP(sport=FTP_PORT, dport=STAFF_PORT, flags="A",
                    seq=sseq, ack=cseq))

    # ---- graceful teardown (FIN from client, then server) -----------------
    add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
        TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="FA", seq=cseq, ack=sseq))
    cseq += 1
    add(ETH_S / IP(src=FTP_IP, dst=STAFF_IP) /
        TCP(sport=FTP_PORT, dport=STAFF_PORT, flags="FA", seq=sseq, ack=cseq))
    sseq += 1
    add(ETH_C / IP(src=STAFF_IP, dst=FTP_IP) /
        TCP(sport=STAFF_PORT, dport=FTP_PORT, flags="A", seq=cseq, ack=sseq))

    out = os.path.join(os.path.dirname(__file__), "..", "challenge.pcap")
    out = os.path.abspath(out)
    wrpcap(out, pkts)
    print(f"Wrote {out}  ({len(pkts)} packets)")


if __name__ == "__main__":
    main()

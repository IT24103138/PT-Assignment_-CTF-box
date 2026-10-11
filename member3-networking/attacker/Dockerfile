# Attacker workstation for the Networking CTF stages.
# A lightweight stand-in for Kali: has the tools you need to solve NET-01/02/03.
# (You can also attach your own Kali VM to the 10.10.20.0/24 network instead.)
FROM debian:12-slim

# tshark asks an interactive question at install time; preseed it.
RUN echo "wireshark-common wireshark-common/install-setuid boolean true" \
      | debconf-set-selections
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      nmap \
      ftp \
      netcat-openbsd \
      tshark \
      python3 \
      iputils-ping iproute2 \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# bundle the solver scripts and the challenge pcap into the workstation
# (build context is the project root - see docker-compose.yml)
COPY solvers/ /opt/solvers/
COPY net02-intercepted-transcript/challenge.pcap /opt/challenge.pcap

WORKDIR /opt

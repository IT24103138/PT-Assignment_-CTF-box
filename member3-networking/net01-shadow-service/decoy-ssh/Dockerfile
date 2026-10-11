# Decoy host for NET-01: an ordinary-looking SSH server (red herring).
# It holds no flag. Its only job is to make host-discovery and a default
# top-1000 nmap scan return "normal" results, so the hidden :40123 service
# on the grading-system host stands out only when players scan the FULL
# port range (nmap -p-).
FROM debian:12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /run/sshd \
 && ssh-keygen -A \
 && useradd -m -s /bin/bash student \
 && echo 'student:CampusGuest123' | chpasswd

# A believable login banner - no secrets here.
RUN printf '%s\n' \
    '*** Campus Lab Workstation ***' \
    'Authorised access only. Activity is logged.' \
    > /etc/ssh/banner \
 && sed -i 's@#Banner none@Banner /etc/ssh/banner@' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]

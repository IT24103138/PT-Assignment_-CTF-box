# NET-02 "Intercepted Transcript" - cleartext FTP server (Library Database).
FROM python:3.12-slim

RUN pip install --no-cache-dir "pyftpdlib==1.5.10"

ENV FTP_USER=libadmin
ENV FTP_PASS=L1br@ry_2026
ENV FTP_ROOT=/srv/ftp
ENV MASQUERADE_ADDRESS=10.10.20.50

WORKDIR /app
COPY ftp_server.py /app/ftp_server.py
COPY ftproot/ /srv/ftp/

# control channel + passive data port range
EXPOSE 21
EXPOSE 60000-60010

CMD ["python3", "/app/ftp_server.py"]

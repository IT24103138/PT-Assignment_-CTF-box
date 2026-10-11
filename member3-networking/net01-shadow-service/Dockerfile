# NET-01 "Shadow Service" - minimal Python banner listener on a hidden port.
FROM python:3.12-slim

# The non-standard, undocumented port the Grading System was left on.
ENV PORT=40123
ENV FLAG="SLIIT{sh4d0w_s3rv1c3_0n_p0rt_40123}"

WORKDIR /app
COPY banner_server.py /app/banner_server.py

EXPOSE 40123
CMD ["python3", "/app/banner_server.py"]

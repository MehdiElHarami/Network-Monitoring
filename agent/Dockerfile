FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir scapy requests

COPY . .

CMD ["python", "packet_sniffer.py"]

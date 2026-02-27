from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from datetime import datetime
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/packets")

def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]

        protocol = "OTHER"
        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"

        packet_data = {
            "timestamp": datetime.now().isoformat(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "protocol": protocol,
            "packet_size": len(packet)
        }

        try:
            response = requests.post(API_URL, json=packet_data)
            print(response.status_code)
        except Exception as e:
            print("Error sending packet:", e)

if __name__ == "__main__":
    print("Starting packet capture...")
    sniff(prn=process_packet, store=False)

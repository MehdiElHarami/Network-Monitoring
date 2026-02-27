from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from datetime import datetime

def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]

        protocol = None
        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        else:
            protocol = "OTHER"

        packet_data = {
            "timestamp": datetime.now().isoformat(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "protocol": protocol,
            "packet_size": len(packet)
        }

        print(packet_data)

if __name__ == "__main__":
    print("Starting packet capture...")
    sniff(prn=process_packet, store=False)

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from models import Packet

THRESHOLD = 50
TIME_WINDOW_SECONDS = 10

def detect_port_scanning(db: Session):
    """
    Detect if any IP has sent more than THRESHOLD packets
    in the last TIME_WINDOW_SECONDS.
    """

    time_limit = datetime.now(timezone.utc) - timedelta(seconds=TIME_WINDOW_SECONDS)

    results = (
        db.query(Packet.src_ip)
        .filter(Packet.timestamp >= time_limit)
        .all()
    )

    ip_count = {}

    for row in results:
        ip = row[0]
        ip_count[ip] = ip_count.get(ip, 0) + 1

    alerts = []

    for ip, count in ip_count.items():
        if count > THRESHOLD:
            alerts.append({
                "src_ip": ip,
                "packet_count": count,
                "alert": "Possible port scanning detected"
            })

    return alerts

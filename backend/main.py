from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import Packet
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from database import engine
from models import Base
from detector import detect_port_scanning

Base.metadata.create_all(bind=engine)

app = FastAPI()

class PacketSchema(BaseModel):
    timestamp: datetime
    src_ip: str
    dst_ip: str
    protocol: str
    packet_size: int

@app.post("/packets")
def receive_packet(packet: PacketSchema):
    db: Session = SessionLocal()
    db_packet = Packet(**packet.dict())
    db.add(db_packet)
    db.commit()
    db.close()
    return {"status": "stored"}

@app.get("/alerts")
def get_alerts():
    db: Session = SessionLocal()
    alerts = detect_port_scanning(db)
    db.close()
    return alerts


@app.get("/stats/top-talkers")
def top_talkers():
    db = SessionLocal()

    results = (
        db.query(Packet.src_ip, func.count(Packet.id).label("count"))
        .group_by(Packet.src_ip)
        .order_by(func.count(Packet.id).desc())
        .limit(5)
        .all()
    )

    db.close()

    return [{"src_ip": r[0], "count": r[1]} for r in results]


@app.get("/stats/summary")
def get_summary():
    db = SessionLocal()
    total_packets = db.query(func.count(Packet.id)).scalar() or 0
    unique_sources = db.query(func.count(func.distinct(Packet.src_ip))).scalar() or 0
    unique_destinations = db.query(func.count(func.distinct(Packet.dst_ip))).scalar() or 0
    total_bytes = db.query(func.sum(Packet.packet_size)).scalar() or 0
    db.close()
    return {
        "total_packets": total_packets,
        "unique_sources": unique_sources,
        "unique_destinations": unique_destinations,
        "total_bytes": total_bytes,
    }


@app.get("/stats/protocol-distribution")
def protocol_distribution():
    db = SessionLocal()
    results = (
        db.query(Packet.protocol, func.count(Packet.id).label("count"))
        .group_by(Packet.protocol)
        .order_by(func.count(Packet.id).desc())
        .all()
    )
    db.close()
    return [{"protocol": r[0], "count": r[1]} for r in results]


@app.get("/stats/traffic-over-time")
def traffic_over_time():
    db = SessionLocal()
    time_limit = datetime.now(timezone.utc) - timedelta(minutes=30)
    results = (
        db.query(Packet.timestamp, Packet.packet_size)
        .filter(Packet.timestamp >= time_limit)
        .order_by(Packet.timestamp)
        .all()
    )
    db.close()
    return [{"timestamp": r[0].isoformat(), "packet_size": r[1]} for r in results]


@app.get("/packets/recent")
def recent_packets(limit: int = 20):
    db = SessionLocal()
    results = (
        db.query(Packet)
        .order_by(Packet.timestamp.desc())
        .limit(limit)
        .all()
    )
    db.close()
    return [
        {
            "timestamp": p.timestamp.isoformat() if p.timestamp else "",
            "src_ip": p.src_ip,
            "dst_ip": p.dst_ip,
            "protocol": p.protocol,
            "packet_size": p.packet_size,
        }
        for p in results
    ]
from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import Packet
from sqlalchemy.orm import Session
from datetime import datetime
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
    results = db.execute("""
        SELECT src_ip, COUNT(*) as count
        FROM packets
        GROUP BY src_ip
        ORDER BY count DESC
        LIMIT 5
    """).fetchall()
    db.close()
    return results

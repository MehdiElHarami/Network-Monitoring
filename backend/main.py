from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import Packet
from sqlalchemy.orm import Session
from datetime import datetime
from database import engine
from models import Base

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

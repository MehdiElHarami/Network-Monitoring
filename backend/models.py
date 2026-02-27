from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    src_ip = Column(String)
    dst_ip = Column(String)
    protocol = Column(String)
    packet_size = Column(Integer)


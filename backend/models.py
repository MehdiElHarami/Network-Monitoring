from sqlalchemy import Column, Integer, String
from database import Base

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String)
    src_ip = Column(String)
    dst_ip = Column(String)
    protocol = Column(String)
    packet_size = Column(Integer)

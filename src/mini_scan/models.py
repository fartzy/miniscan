from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    BigInteger,
    ForeignKey,
    Text,
    LargeBinary,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ScanData(Base):
    __tablename__ = "scan_data"

    id = Column(Integer, primary_key=True)
    response_bytes_utf8 = Column(LargeBinary, nullable=True)
    response_str = Column(Text, nullable=True)


class Scans(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    service = Column(String(50), nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    data_version = Column(Integer, nullable=False)
    data_id = Column(Integer, ForeignKey("scan_data.id"))

    data = relationship("ScanData")

from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class EscrowStatus(enum.Enum):
    PENDING = "Pending"
    RELEASED = "Released"
    DISPUTED = "Disputed"

class EscrowTransaction(Base):
    __tablename__ = "escrow_transactions"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(Enum(EscrowStatus), default=EscrowStatus.PENDING)
    delivery_code = Column(String, nullable=True)
    release_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

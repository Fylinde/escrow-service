from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class EscrowStatus(enum.Enum):
    PENDING = "Pending"
    RELEASED = "Released"
    DISPUTED = "Disputed"

class EscrowBase(BaseModel):
    buyer_id: int
    seller_id: int
    amount: float
    currency: str
    status: Optional[EscrowStatus] = EscrowStatus.PENDING
    delivery_code: Optional[str]
    release_time: Optional[datetime]

class EscrowCreate(EscrowBase):
    pass

class EscrowUpdate(BaseModel):
    status: Optional[EscrowStatus]
    delivery_code: Optional[str]
    release_time: Optional[datetime]

class EscrowOut(EscrowBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

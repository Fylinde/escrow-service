from sqlalchemy.orm import Session
from app.models.escrow_model import EscrowTransaction, EscrowStatus
from app.schemas.escrow_schema import EscrowCreate, EscrowUpdate

def create_escrow(db: Session, escrow: EscrowCreate):
    db_escrow = EscrowTransaction(**escrow.dict())
    db.add(db_escrow)
    db.commit()
    db.refresh(db_escrow)
    return db_escrow

def get_escrow(db: Session, escrow_id: int):
    return db.query(EscrowTransaction).filter(EscrowTransaction.id == escrow_id).first()

def update_escrow(db: Session, escrow_id: int, escrow_update: EscrowUpdate):
    db_escrow = db.query(EscrowTransaction).filter(EscrowTransaction.id == escrow_id).first()
    if not db_escrow:
        return None
    for key, value in escrow_update.dict(exclude_unset=True).items():
        setattr(db_escrow, key, value)
    db.commit()
    db.refresh(db_escrow)
    return db_escrow

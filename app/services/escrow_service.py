from app.crud.escrow_crud import create_escrow, get_escrow, update_escrow
from app.schemas.escrow_schema import EscrowCreate, EscrowUpdate
from sqlalchemy.orm import Session
import app.utils.notification_utils as notifications

def initiate_escrow(db: Session, escrow_data: EscrowCreate):
    escrow = create_escrow(db, escrow_data)
    notifications.send_notification(escrow.buyer_id, "Escrow transaction created.")
    return escrow

def release_funds(db: Session, escrow_id: int):
    escrow = get_escrow(db, escrow_id)
    if not escrow or escrow.status != "Pending":
        raise ValueError("Invalid transaction or status.")
    escrow_update = EscrowUpdate(status="Released")
    updated_escrow = update_escrow(db, escrow_id, escrow_update)
    notifications.send_notification(updated_escrow.seller_id, "Funds released to your account.")
    return updated_escrow

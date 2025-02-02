from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.escrow_schema import EscrowCreate, EscrowUpdate
from app.services.escrow_service import initiate_escrow, release_funds
from app.services.blockchain_service import lock_funds, release_funds, raise_dispute
from app.models.escrow_model import EscrowTransaction

router = APIRouter()

@router.post("/escrow")
def create_escrow(escrow: EscrowCreate, db: Session = Depends(get_db)):
    return initiate_escrow(db, escrow)

@router.put("/escrow/{escrow_id}/release")
def release_escrow_funds(escrow_id: int, db: Session = Depends(get_db)):
    try:
        return release_funds(db, escrow_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/escrow/lock")
def lock_escrow(buyer_private_key: str, seller_address: str, amount: float, release_time: int):
    try:
        txn_hash = lock_funds(buyer_private_key, seller_address, amount, release_time)
        return {"transactionHash": txn_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/escrow/{transaction_id}/release")
def release_escrow(buyer_private_key: str, transaction_id: int):
    try:
        txn_hash = release_funds(buyer_private_key, transaction_id)
        return {"transactionHash": txn_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/escrow/{transaction_id}/dispute")
def dispute_escrow(buyer_private_key: str, transaction_id: int):
    try:
        txn_hash = raise_dispute(buyer_private_key, transaction_id)
        return {"transactionHash": txn_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/analytics")
def fetch_escrow_analytics(db: Session = Depends(get_db)):
    # Fetch data grouped by status
    status_counts = (
        db.query(EscrowTransaction.status, func.count(EscrowTransaction.id))
        .group_by(EscrowTransaction.status)
        .all()
    )
    
    # Calculate average release time for completed transactions
    completed_transactions = (
        db.query(EscrowTransaction)
        .filter(EscrowTransaction.status == EscrowStatus.RELEASED)
        .all()
    )
    avg_release_time = (
        sum(
            (txn.release_time - txn.created_at).total_seconds()
            for txn in completed_transactions
        )
        / len(completed_transactions)
        if completed_transactions
        else 0
    )

    # Count total disputes
    dispute_count = (
        db.query(EscrowTransaction)
        .filter(EscrowTransaction.status == EscrowStatus.DISPUTED)
        .count()
    )

    return {
        "status_counts": {status: count for status, count in status_counts},
        "average_release_time": avg_release_time,
        "dispute_count": dispute_count,
    }
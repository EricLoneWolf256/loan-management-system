# payments API endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCreate, RepaymentScheduleResponse
from app.services.payment_service import PaymentService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/loan/{loan_id}/schedule", response_model=list[RepaymentScheduleResponse])
def get_repayment_schedule(
    loan_id: int, 
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get repayment schedule for a loan"""
    return PaymentService.get_loan_repayment_schedule(db=db, loan_id=loan_id, skip=skip, limit=limit)


@router.get("/schedule/{schedule_id}", response_model=RepaymentScheduleResponse)
def get_repayment_detail(schedule_id: int, db: Session = Depends(get_db)):
    """Get a specific repayment schedule detail"""
    return PaymentService.get_repayment_schedule_by_id(db=db, schedule_id=schedule_id)


@router.post("/schedule/{schedule_id}/pay")
def make_payment(
    schedule_id: int,
    amount: float,
    payment_method: str,
    transaction_reference: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Record a payment for a repayment schedule"""
    return PaymentService.make_payment(
        db=db,
        schedule_id=schedule_id,
        amount=amount,
        payment_method=payment_method,
        transaction_reference=transaction_reference
    )


@router.get("/loan/{loan_id}/history")
def get_payment_history(loan_id: int, db: Session = Depends(get_db)):
    """Get payment history for a loan"""
    return PaymentService.get_payment_history(db=db, loan_id=loan_id)


@router.get("/loan/{loan_id}/balance")
def get_loan_balance(loan_id: int, db: Session = Depends(get_db)):
    """Get outstanding balance for a loan"""
    return PaymentService.get_loan_balance(db=db, loan_id=loan_id)

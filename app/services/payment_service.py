# payment service - handles payment business logic
from sqlalchemy.orm import Session
from app.models.payment import RepaymentSchedule, PaymentStatus
from app.schemas.payment import PaymentCreate
from fastapi import HTTPException, status
from datetime import datetime


class PaymentService:
    """Service class for payment operations"""
    
    @staticmethod
    def get_loan_repayment_schedule(db: Session, loan_id: int, skip: int = 0, limit: int = 10):
        """Get repayment schedule for a loan"""
        schedules = db.query(RepaymentSchedule).filter(
            RepaymentSchedule.loan_id == loan_id
        ).offset(skip).limit(limit).all()
        
        if not schedules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No repayment schedule found for this loan"
            )
        
        return schedules
    
    @staticmethod
    def get_repayment_schedule_by_id(db: Session, schedule_id: int) -> RepaymentSchedule:
        """Get a specific repayment schedule"""
        schedule = db.query(RepaymentSchedule).filter(
            RepaymentSchedule.id == schedule_id
        ).first()
        
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repayment schedule not found"
            )
        
        return schedule
    
    @staticmethod
    def make_payment(db: Session, schedule_id: int, amount: float, payment_method: str, transaction_reference: str):
        """Record a payment against a repayment schedule"""
        schedule = PaymentService.get_repayment_schedule_by_id(db, schedule_id)
        
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount must be positive"
            )
        
        remaining_amount = schedule.amount_due - schedule.amount_paid
        
        if amount > remaining_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment amount exceeds remaining balance ({remaining_amount})"
            )
        
        schedule.amount_paid += amount
        schedule.payment_date = datetime.utcnow()
        
        # Update status based on payment
        if schedule.amount_paid >= schedule.amount_due:
            schedule.status = PaymentStatus.PAID
        elif schedule.payment_date > schedule.due_date:
            schedule.status = PaymentStatus.LATE
        else:
            schedule.status = PaymentStatus.PAID
        
        schedule.updated_at = datetime.utcnow()
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        
        return {
            "schedule_id": schedule.id,
            "amount_paid": amount,
            "total_paid": schedule.amount_paid,
            "remaining": remaining_amount - amount,
            "status": schedule.status,
            "transaction_reference": transaction_reference
        }
    
    @staticmethod
    def get_payment_history(db: Session, loan_id: int):
        """Get payment history for a loan"""
        schedules = db.query(RepaymentSchedule).filter(
            RepaymentSchedule.loan_id == loan_id
        ).all()
        
        return [
            {
                "installment": s.installment_number,
                "due_date": s.due_date,
                "amount_due": s.amount_due,
                "amount_paid": s.amount_paid,
                "status": s.status,
                "payment_date": s.payment_date
            }
            for s in schedules
        ]
    
    @staticmethod
    def get_loan_balance(db: Session, loan_id: int) -> dict:
        """Get outstanding balance for a loan"""
        schedules = db.query(RepaymentSchedule).filter(
            RepaymentSchedule.loan_id == loan_id
        ).all()
        
        if not schedules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No repayment schedule found for this loan"
            )
        
        total_due = sum(s.amount_due for s in schedules)
        total_paid = sum(s.amount_paid for s in schedules)
        
        return {
            "loan_id": loan_id,
            "total_due": total_due,
            "total_paid": total_paid,
            "outstanding_balance": total_due - total_paid,
            "paid_percentage": (total_paid / total_due * 100) if total_due > 0 else 0
        }

# loan service - handles loan business logic
from sqlalchemy.orm import Session
from app.models.loan import LoanApplication, LoanStatus
from app.models.payment import RepaymentSchedule
from app.schemas.loan import LoanApplicationCreate, LoanApplicationUpdate
from app.utils.loan_calculator import calculate_monthly_payment, generate_repayment_schedule
from fastapi import HTTPException, status
from datetime import datetime


class LoanService:
    """Service class for loan operations"""
    
    @staticmethod
    def create_loan_application(db: Session, loan: LoanApplicationCreate) -> LoanApplication:
        """Create a new loan application"""
        # Calculate interest rate based on loan type (basic implementation)
        interest_rate = LoanService.calculate_interest_rate(loan.loan_type, loan.requested_amount)
        
        db_loan = LoanApplication(
            applicant_id=loan.applicant_id,
            loan_type=loan.loan_type,
            loan_amount=loan.requested_amount,
            loan_term_months=loan.loan_term_months,
            interest_rate=interest_rate,
            purpose=loan.purpose,
            status=LoanStatus.PENDING
        )
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    
    @staticmethod
    def get_loan_application_by_id(db: Session, loan_id: int) -> LoanApplication:
        """Get loan application by ID"""
        loan = db.query(LoanApplication).filter(LoanApplication.id == loan_id).first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan application not found"
            )
        return loan
    
    @staticmethod
    def get_user_loans(db: Session, user_id: int, skip: int = 0, limit: int = 10):
        """Get all loans for a specific user"""
        return db.query(LoanApplication).filter(
            LoanApplication.applicant_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_loans(db: Session, skip: int = 0, limit: int = 10):
        """Get all loan applications with pagination"""
        return db.query(LoanApplication).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_loan_application(db: Session, loan_id: int, loan_update: LoanApplicationUpdate) -> LoanApplication:
        """Update loan application"""
        db_loan = LoanService.get_loan_application_by_id(db, loan_id)
        
        update_data = loan_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_loan, field, value)
        
        db_loan.updated_at = datetime.utcnow()
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    
    @staticmethod
    def approve_loan(db: Session, loan_id: int) -> LoanApplication:
        """Approve a loan application and generate repayment schedule"""
        db_loan = LoanService.get_loan_application_by_id(db, loan_id)
        
        if db_loan.status != LoanStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending loans can be approved"
            )
        
        db_loan.status = LoanStatus.APPROVED
        db_loan.updated_at = datetime.utcnow()
        
        # Generate repayment schedule
        repayment_schedule = generate_repayment_schedule(
            loan_amount=db_loan.loan_amount,
            interest_rate=db_loan.interest_rate,
            term_months=db_loan.loan_term_months,
            loan_id=loan_id
        )
        
        for schedule in repayment_schedule:
            db.add(schedule)
        
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    
    @staticmethod
    def reject_loan(db: Session, loan_id: int, reason: str = None) -> LoanApplication:
        """Reject a loan application"""
        db_loan = LoanService.get_loan_application_by_id(db, loan_id)
        
        if db_loan.status != LoanStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending loans can be rejected"
            )
        
        db_loan.status = LoanStatus.REJECTED
        db_loan.review_comments = reason
        db_loan.updated_at = datetime.utcnow()
        
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    
    @staticmethod
    def calculate_interest_rate(loan_type: str, amount: float) -> float:
        """Calculate interest rate based on loan type and amount"""
        # Simple interest rate logic - can be enhanced
        base_rates = {
            "personal": 8.5,
            "mortgage": 4.5,
            "auto": 5.5,
            "student": 3.5,
            "business": 7.5,
            "education": 3.0
        }
        
        base_rate = base_rates.get(loan_type, 7.0)
        
        # Adjust based on amount
        if amount < 50000:
            base_rate += 1.0
        elif amount > 500000:
            base_rate -= 0.5
        
        return round(base_rate, 2)

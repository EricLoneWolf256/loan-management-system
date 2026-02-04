# loans API endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.loan import LoanApplicationCreate, LoanApplicationResponse, LoanApplicationUpdate
from app.services.loan_service import LoanService
from app.utils.auth import get_current_user
from app.models.user import UserRole

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_loan_application(
    loan: LoanApplicationCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new loan application"""
    # Users can only create loans for themselves, unless they're admin
    if current_user.id != loan.applicant_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create loan for this user"
        )
    return LoanService.create_loan_application(db=db, loan=loan)


@router.get("/{loan_id}", response_model=LoanApplicationResponse)
def get_loan_application(loan_id: int, db: Session = Depends(get_db)):
    """Get loan application by ID"""
    return LoanService.get_loan_application_by_id(db=db, loan_id=loan_id)


@router.get("/user/{user_id}", response_model=list[LoanApplicationResponse])
def get_user_loans(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all loans for a specific user"""
    return LoanService.get_user_loans(db=db, user_id=user_id, skip=skip, limit=limit)


@router.get("", response_model=list[LoanApplicationResponse])
def get_all_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all loan applications"""
    return LoanService.get_all_loans(db=db, skip=skip, limit=limit)


@router.put("/{loan_id}", response_model=LoanApplicationResponse)
def update_loan_application(
    loan_id: int, 
    loan_update: LoanApplicationUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update loan application status"""
    # Only loan officers and admins can update loan status
    if current_user.role not in [UserRole.LOAN_OFFICER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update loan status"
        )
    return LoanService.update_loan_application(db=db, loan_id=loan_id, loan_update=loan_update)


@router.post("/{loan_id}/approve", response_model=LoanApplicationResponse)
def approve_loan(
    loan_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Approve a loan application"""
    # Only loan officers and admins can approve loans
    if current_user.role not in [UserRole.LOAN_OFFICER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to approve loans"
        )
    return LoanService.approve_loan(db=db, loan_id=loan_id)


@router.post("/{loan_id}/reject", response_model=LoanApplicationResponse)
def reject_loan(
    loan_id: int,
    reason: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Reject a loan application"""
    # Only loan officers and admins can reject loans
    if current_user.role not in [UserRole.LOAN_OFFICER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reject loans"
        )
    return LoanService.reject_loan(db=db, loan_id=loan_id, reason=reason)

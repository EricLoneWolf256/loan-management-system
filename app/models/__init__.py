# database moels 
# import all models here for easy access
from app.models.loan import Loan, LoanApplication, LoanApplication,LoanStatus, LoanType
from app.models.payment import Payment, RepaymentSchedule, PaymentStatus    
from app.models.user import User

__all__ = [
    "User",
    "Loan",
    "LoanApplication",  
    "LoanStatus",
    "LoanType",
    "Payment",
    "RepaymentSchedule",
    "PaymentStatus",
]
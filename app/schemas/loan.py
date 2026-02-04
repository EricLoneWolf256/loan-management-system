# loan schemas - API contracts for loan operations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.loan import LoanType, LoanStatus    


# loan application schemas
class LoanApplicationBase(BaseModel):
    # shared properties for loan application
    applicant_id: int
    loan_type: LoanType
    requested_amount: float = Field(..., gt=0, description="Amount must be positive")
    
    loan_term_months: int = Field(..., gt=0, description="Term in months (maximum duration of the loan) must be greater than zero")
    purpose: Optional[str] = Field(None, max_length=500)
    
class LoanApplicationCreate(LoanApplicationBase):
    # properties required for creating a loan application
    # Interest rate will be determined by the system based on loan type and amount.
    pass    
  
class LoanApplicationUpdate(BaseModel):
    # properties for updating a loan application
    status: Optional[LoanStatus] = None
    review_comments: Optional[str] = Field(None, max_length=1000)  
    
class LoanApplicationResponse(LoanApplicationBase):
    # properties to return to client
    id: int
    applicant_id: int
    interest_rate: float
    status: LoanStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    review_comments: Optional[str] = Field(None, max_length=1000)
    reviewed_by_id: Optional[int] 
    
    class Config:
        from_attributes = True
        
        
# loan schemas
class LoanBase(BaseModel):
    # shared properties for loan
    borrower_id: int
    loan_type: LoanType
    principal_amount: float = Field(..., gt=0, description="Principal amount must be positive")
    interest_rate: float = Field(..., gt=0, description="Interest rate must be positive")
    loan_term_months: int = Field(..., gt=0, description="Term in months must be greater than zero")
    monthly_payment: float = Field(..., gt=0, description="Monthly payment must be positive")
    
class LoanCreate(LoanBase):
    # properties required for creating a loan
    application_id: int  # link to the approved loan application
    disbursement_date: datetime = Field(default_factory=datetime.now)
    
class LoanResponse(LoanBase):
    # properties to return to client
    id: int
    application_id: int
    borrower_id: int
    status: LoanStatus
    outstanding_balance: float
    disbursement_date: datetime
    start_date: Optional[datetime] 
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime] 
    
    class Config:
        from_attributes = True
        
class LoanSummary(BaseModel):
    # summary information about a loan
    id: int
    borrower_id: int
    loan_type: LoanType
    principal_amount: float
    interest_rate: float
    loan_term_months: int
    monthly_payment: float
    status: LoanStatus
    outstanding_balance: float
    next_payment_due: Optional[datetime]
    
    class Config:
        from_attributes = True
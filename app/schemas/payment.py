# payment schemas API contracts for payment operations
from pydantics import BaseModel, Field
from typing import Optional 
from datetime import datetime, date
from.app.models.payment import PaymentStatus

# repayment schedule schemas
class RepaymentScheduleBase(BaseModel):
    # shared properties for repayment schedule

    installment_number: int
    due_date: datetime
    amount_due: float
    principal_component: float
    interest_component: float
    
    
class RepaymentScheduleResponse(RepaymentScheduleBase):
    # properties to return to client
    id: int
    loan_id: int
    status: PaymentStatus = PaymentStatus.PENDING
    amount_paid: float = 0.0
    payment_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
        
        
# payment schemas
class PaymentBase(BaseModel):
    # shared properties for payment
    loan_id: int
    amount: float = Field(..., gt=0, description="Payment amount must be positive")
    payment_method: str = Field(..., max_length=50)
    notes: Optional[str] = Field(None, max_length=500)
    
    
    
class PaymentCreate(PaymentBase):
    # properties required for creating a new payment.used when a borrower makes a payment
    loan_id: int
    amount: float = Field(..., gt=0, description="Payment amount must be positive")
    payment_date: Optional[datetime] = None  # if not provided, will be set to current time
    transaction_reference: str = Field(..., max_length=100)
    
    
    
class PaymentResponse(PaymentBase):
    # complete payment to return to client
    id: int
    loan_id: int
    payment_date: datetime
    transaction_reference: str
    processed_by_id: Optional[int] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
        
        
class PaymentSummary(BaseModel):
    # summary of payments for a loan
    total_paid: float
    total_pending: float
    last_payment_date: Optional[datetime] = None
    next_payment_due: Optional[datetime] = None
    payments_remaining: int
    
    class Config:
        from_attributes = True
    
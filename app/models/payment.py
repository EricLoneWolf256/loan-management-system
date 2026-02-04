# payment models to track money flow
# when payments are due and actual payments made
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    """Status of the payment"""
    PENDING = "pending"
    DUE = "due"
    PAID = "paid"
    LATE = "late"
    MISSED = "missed"


class RepaymentSchedule(Base):
    """Schedule of repayments for a loan"""
    __tablename__ = "repayment_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    # which loan this repayment is for
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    
    installment_number = Column(Integer, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    amount_due = Column(Float, nullable=False)
    
    # how much of this goes to principal vs interest
    principal_component = Column(Float, nullable=False)
    interest_component = Column(Float, nullable=False)
    
    # payment tracking
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    amount_paid = Column(Float, default=0.0)
    payment_date = Column(DateTime(timezone=True), nullable=True)
    
    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # relationships
    loan = relationship("Loan", back_populates="repayments")
    
    def __repr__(self):
        return f"<RepaymentSchedule id={self.id} loan_id={self.loan_id} installment={self.installment_number} due_date={self.due_date} amount_due={self.amount_due} status={self.status}>"


class Payment(Base):
    """Actual payment made towards a loan"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    # which loan this payment is for
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    
    # payment detail
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_method = Column(String)  # e.g., credit card, bank transfer
    
    # transaction tracking
    transaction_reference = Column(String, unique=True, nullable=False)
    notes = Column(String, nullable=True)
    
    # processing details
    processed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # relationships
    loan = relationship("Loan", back_populates="payments")
    processed_by = relationship("User")
    
    def __repr__(self):
        return f"<Payment id={self.id} loan_id={self.loan_id} amount={self.amount} payment_date={self.payment_date} processed_by_id={self.processed_by_id} processed_at={self.processed_at}>"
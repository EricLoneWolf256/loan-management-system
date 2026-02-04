import enum
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from app.database import Base


class LoanType(str, enum.Enum):
    """Types of loans we offer"""
    PERSONAL = "personal"
    MORTGAGE = "mortgage"
    AUTO = "auto"
    STUDENT = "student"
    BUSINESS = "business"
    EDUCATION = "education"

    
class LoanStatus(str, enum.Enum):
    """Status of the loan application"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    CLOSED = "closed"
    UNDER_REVIEW = "under_review"
    DEFAULTED = "defaulted"  
    PAID_OFF = "paid_off" 
    ACTIVE = "active"

    
class LoanApplication(Base):
    """Customer request for a loan"""
    __tablename__ = "loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Who's applying for the loan
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # What are they asking for
    loan_type = Column(Enum(LoanType), nullable=False)
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    loan_term_months = Column(Integer, nullable=False)
    # Why they need the loan
    purpose = Column(Text, nullable=True)
    
    # Application status
    status = Column(Enum(LoanStatus), default=LoanStatus.PENDING)
    
    # Review details
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # If approved, link to the actual loan
    loan = relationship("Loan", back_populates="application", uselist=False)
    applicant = relationship("User", foreign_keys=[applicant_id], back_populates="loan_applications")
    reviewer = relationship("User", foreign_keys=[reviewed_by_id])
    
    def __repr__(self):
        return f"<LoanApplication id={self.id} applicant_id={self.applicant_id} loan_type={self.loan_type} amount={self.loan_amount} status={self.status}>"

    
class Loan(Base):
    """Actual loan record once approved and disbursed"""
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link back to application
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False, unique=True)
    
    # Who borrowed the loan
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Loan details
    loan_type = Column(Enum(LoanType), nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    loan_term_months = Column(Integer, nullable=False)  
    monthly_payment = Column(Float, nullable=False)
    
    # Current status
    status = Column(Enum(LoanStatus), default=LoanStatus.DISBURSED)
    outstanding_balance = Column(Float, nullable=False)
    
    disbursement_date = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="loan")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="loans")
    repayments = relationship("RepaymentSchedule", back_populates="loan", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="loan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Loan id={self.id} borrower_id={self.borrower_id} principal={self.principal_amount} status={self.status}>"

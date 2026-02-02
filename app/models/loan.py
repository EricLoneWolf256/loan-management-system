from calendar import month
import enum
from os import times
from sqlite3 import Date
from tkinter import ACTIVE
from tracemalloc import start
from xmlrpc.client import DateTime
from app.models import payment
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from app.database import Base   

class LoanType(str,enum.Enum):
    # types of loan we offer
    
    PERSONAL = "personal"
    MORTGAGE = "mortgage"
    AUTO = "auto"
    STUDENT = "student"
    BUSINESS = "business"
    EDUCATION = "education"
    
class LoanStatus(str,enum.Enum):
    # status of the loan application
    # Application stages
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
    
    # customer request for a loan
    __tablename__ = "loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # who's applying for the loan
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable =False)
    
    # what are they asking for
    loan_type = Column(Enum(LoanType), nullable = False)
    loan_amount = Column(Float,nullable = False)
    interest_rate = Column(Float,nullable = False)
    loan_term_months = Column(Integer,nullable = False)
    # why they need the loan
    purpose = Column(Text, nullable=True)
    
    # application status
    status = Column(Enum(LoanStatus), default=LoanStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # reiview details
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # if approved , link to the actual loan
    loan = relationship("Loan", back_populates="application", uselist=False)
    
    def __repr__(self):
            return f"<LoanApplication id={self.id} applicant_id={self.applicant_id} loan_type={self.loan_type} amount={self.loan_amount} status={self.status}>"
    
    
    class Loan(Base):
        # actual loan record once approved and disbursed
        __tablename__ = "loans"
        id = Column(Integer, primary_key=True, index=True)
        
        # link back to application
        application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False, unique=True)
        
        # who borrowed the loan
        borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        
        # loan details
        Loan_Type = Column(Enum(LoanType), nullable=False)
        principal_amount = Column(Float, nullable=False)
        
        interest_rate = Column(Float, nullable=False)
        loan_term_months = Column(Integer, nullable=False)  
        monthly_payment = Column(Float, nullable=False)
        
        # current status
        
        status = Column(Enum(LoanStatus), default=LoanStatus.DISBURSED)
        outstanding_balance = Column(Float, nullable=False)
        
        disbursement_date = Column(DateTime(timezone=True), server_default=func.now())
        start_date = Column(DateTime(timezone=True), nullable=True)
        end_date = Column(DateTime(timezone=True), nullable=True)
        
        # timestamps
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        updated_at = Column(DateTime(timezone=True), onupdate=func.now())
        
        # relationships
        application = relationship("LoanApplication", back_populates="loan")
        borrower = relationship("User", back_populates="loans")
        repayments = relationship("RepaymentSchedule", back_populates="loan", cascade="all, delete-orphan")
        payments = relationship("Payment", back_populates="loan", cascade="all, delete-orphan")
        
        def __repr__(self):
            return f"<Loan id={self.id} borrower_id={self.borrower_id} principal={self.principal_amount} status={self.status}>"

# user model
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, DateTime,  Boolean, Enum
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from app.database import Base
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    # different roles a user can have in the system
    
    CUSTOMER = "customer"
    ADMIN = "admin"
    LOAN_OFFICER = "loan_officer"
    
class User(Base):
    # user model representing system users. sotres information about everyone using the system
    __tablename__ = "users"
    
# primary identification fields
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # personal details
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    
    # roles and status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    
    # timestamps   
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # relationships - connections to other tables, a customer can have multiple loans and loan applications
    loans = relationship("Loan", back_populates="borrower", cascade="all, delete-orphan", foreign_keys="[Loan.borrower_id]")
    loan_applications = relationship("LoanApplication", back_populates="applicant", cascade="all, delete-orphan", foreign_keys="[LoanApplication.applicant_id]")
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email} role={self.role}>"
    
# what fields are required, what's optional, what format.
import email
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from.app.models.user import UserRole

class UserBase(BaseModel):
    # shared properties for user
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER
 
 
class UserCreate(UserBase):
    # properties required for creating a user
    password: str = Field(..., min_length=8, max_length=128)  
    role: Optional[UserRole] = UserRole.CUSTOMER
    
    
class UserUpdate(BaseModel):
    # properties for updating a user
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    
class UserInDBBase(UserBase):
    # properties stored in the database
    id: int
    role: UserRole
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        

class UserResponse(UserBase):
    # properties to return to client
    id: int
    role: UserRole
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
        
        
class Token(BaseModel):
    # Authentication token response model
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    # data stored inside the JWT token
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None



    

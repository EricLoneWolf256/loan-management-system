# authentication and authorization utilities e.g password hashing, token generation
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status 
from sqlalchemy.orm import Session

from  app.database import get_db
from app.config import settings
from.app.models.user import User
from.app.schemas.user import TokenData

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/Login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # verify a plain password against its hashed version
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # hash a plain password
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # set expiration time and create a JWT access token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # creates the JWT token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    # decode and validate a JWT access token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            return None
        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        return None
    
    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        # retrieve the current user based on the provided JWT token
        token_data = decode_access_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # get the user from the database
        user = db.query(User).filter(  User.id == token_data.user_id).first()
        if user is none:
            raise credentials_exception
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="inactive user"
                )
        
        return user
    
    async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
        # ensure the current user is active. another layer of security
        if not current_user.is_active:
            raise HTTPException(
                status_code=400,detail="Inactive user"
            )
        return current_user
# users API endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return UserService.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    return UserService.get_user_by_id(db=db, user_id=user_id)


@router.get("", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    return UserService.get_all_users(db=db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Update user information"""
    # Check authorization - users can only update their own profile or admins can update any
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    return UserService.update_user(db=db, user_id=user_id, user_update=user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Delete user"""
    # Only admins can delete users
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete users"
        )
    UserService.delete_user(db=db, user_id=user_id)
    return None

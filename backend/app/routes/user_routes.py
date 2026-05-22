from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# Create a new account
@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password  # plain text for beginner level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# POST 
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Wrong password")

    # Return user id and name
    return {
        "message": "Login successful",
        "user_id": user.id,
        "user_name": user.name
    }



@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

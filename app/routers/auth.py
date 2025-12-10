from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.schemas.login import LoginRequest
from app.crud.user import get_user_by_username, create_user
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.deps.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, data.username)
    if existing:
        raise HTTPException(400, "Username already used")
    return create_user(db, data.username, data.password)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token(user.username)
    return {"access_token": access_token}

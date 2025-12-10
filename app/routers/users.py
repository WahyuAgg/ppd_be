from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.deps.db import get_db
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    """Mendapatkan daftar semua user"""
    users = db.query(User).all()
    return users

@router.get("/count")
def get_users_count(db: Session = Depends(get_db)):
    """Mendapatkan jumlah total user"""
    count = db.query(User).count()
    return {"total_users": count}

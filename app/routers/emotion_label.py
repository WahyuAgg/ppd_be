from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.emotion_label import EmotionLabelCreate, EmotionLabelUpdate, EmotionLabelOut
from app.crud import emotion_label as emotion_label_crud

router = APIRouter(prefix="/emotion-labels", tags=["Emotion Labels"])

@router.post("/", response_model=EmotionLabelOut)
def create_emotion_label(
    data: EmotionLabelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buat emotion label baru"""
    # Cek apakah sudah ada
    existing = emotion_label_crud.get_emotion_label_by_name(db, data.name)
    if existing:
        raise HTTPException(400, f"Emotion label '{data.name}' sudah ada")
    
    return emotion_label_crud.create_emotion_label(db, data.name)

@router.get("/", response_model=List[EmotionLabelOut])
def get_all_emotion_labels(db: Session = Depends(get_db)):
    """Ambil semua emotion labels"""
    return emotion_label_crud.get_all_emotion_labels(db)

@router.get("/{label_id}", response_model=EmotionLabelOut)
def get_emotion_label(label_id: int, db: Session = Depends(get_db)):
    """Ambil detail emotion label berdasarkan ID"""
    label = emotion_label_crud.get_emotion_label_by_id(db, label_id)
    if not label:
        raise HTTPException(404, "Emotion label tidak ditemukan")
    return label

@router.put("/{label_id}", response_model=EmotionLabelOut)
def update_emotion_label(
    label_id: int,
    data: EmotionLabelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update emotion label"""
    label = emotion_label_crud.get_emotion_label_by_id(db, label_id)
    if not label:
        raise HTTPException(404, "Emotion label tidak ditemukan")
    
    if data.name:
        # Cek duplikat nama
        existing = emotion_label_crud.get_emotion_label_by_name(db, data.name)
        if existing and existing.id != label_id:
            raise HTTPException(400, f"Emotion label '{data.name}' sudah ada")
        
        label = emotion_label_crud.update_emotion_label(db, label_id, data.name)
    return label

@router.delete("/{label_id}")
def delete_emotion_label(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hapus emotion label"""
    label = emotion_label_crud.get_emotion_label_by_id(db, label_id)
    if not label:
        raise HTTPException(404, "Emotion label tidak ditemukan")
    
    emotion_label_crud.delete_emotion_label(db, label_id)
    return {"message": "Emotion label berhasil dihapus"}

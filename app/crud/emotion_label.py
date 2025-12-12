from sqlalchemy.orm import Session
from app.models.emotion_label import EmotionLabel
from typing import Optional, List

def create_emotion_label(db: Session, name: str) -> EmotionLabel:
    """Buat emotion label baru"""
    emotion_label = EmotionLabel(name=name)
    db.add(emotion_label)
    db.commit()
    db.refresh(emotion_label)
    return emotion_label

def get_emotion_label_by_id(db: Session, label_id: int) -> Optional[EmotionLabel]:
    """Ambil emotion label berdasarkan ID"""
    return db.query(EmotionLabel).filter(EmotionLabel.id == label_id).first()

def get_emotion_label_by_name(db: Session, name: str) -> Optional[EmotionLabel]:
    """Ambil emotion label berdasarkan nama"""
    return db.query(EmotionLabel).filter(EmotionLabel.name == name).first()

def get_all_emotion_labels(db: Session) -> List[EmotionLabel]:
    """Ambil semua emotion labels"""
    return db.query(EmotionLabel).all()

def update_emotion_label(db: Session, label_id: int, name: str) -> Optional[EmotionLabel]:
    """Update nama emotion label"""
    label = get_emotion_label_by_id(db, label_id)
    if label:
        label.name = name
        db.commit()
        db.refresh(label)
    return label

def delete_emotion_label(db: Session, label_id: int) -> bool:
    """Hapus emotion label"""
    label = get_emotion_label_by_id(db, label_id)
    if label:
        db.delete(label)
        db.commit()
        return True
    return False

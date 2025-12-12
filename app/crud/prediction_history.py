from sqlalchemy.orm import Session
from app.models.prediction_history import PredictionHistory
from app.models.tag import Tag
from typing import List, Optional
from datetime import date, datetime

def create_prediction_history(
    db: Session, 
    user_id: int, 
    input_text: str, 
    prediction: str,
    tag_ids: Optional[List[int]] = None
) -> PredictionHistory:
    """Simpan hasil prediksi ke history dengan tags"""
    history = PredictionHistory(
        user_id=user_id,
        input_text=input_text,
        prediction=prediction
    )
    
    # Tambahkan tags jika ada
    if tag_ids:
        tags = db.query(Tag).filter(
            Tag.id.in_(tag_ids),
            Tag.user_id == user_id  # Pastikan tag milik user
        ).all()
        history.tags = tags
    
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_history_by_user(
    db: Session, 
    user_id: int, 
    date_start: Optional[date] = None, 
    date_end: Optional[date] = None,
    tag_ids: Optional[List[int]] = None
) -> List[PredictionHistory]:
    """
    Ambil history prediksi berdasarkan user_id, rentang tanggal, dan tags.
    """
    query = db.query(PredictionHistory).filter(PredictionHistory.user_id == user_id)
    
    if date_start:
        start_datetime = datetime.combine(date_start, datetime.min.time())
        query = query.filter(PredictionHistory.created_at >= start_datetime)
    
    if date_end:
        end_datetime = datetime.combine(date_end, datetime.max.time())
        query = query.filter(PredictionHistory.created_at <= end_datetime)
    
    # Filter by tags (jika ada salah satu tag yang cocok)
    if tag_ids:
        query = query.filter(PredictionHistory.tags.any(Tag.id.in_(tag_ids)))
    
    return query.order_by(PredictionHistory.created_at.desc()).all()

def delete_history(db: Session, history_id: int, user_id: int) -> bool:
    """Hapus history (hanya jika milik user)"""
    history = db.query(PredictionHistory).filter(
        PredictionHistory.id == history_id,
        PredictionHistory.user_id == user_id
    ).first()
    
    if history:
        db.delete(history)
        db.commit()
        return True
    return False

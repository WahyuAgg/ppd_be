from sqlalchemy.orm import Session
from app.models.music import Music
from app.models.emotion_label import EmotionLabel
from typing import Optional, List

def create_music(
    db: Session, 
    title: str, 
    artist: str, 
    genre: str, 
    file_path: str, 
    file_name: str, 
    uploaded_by: int,
    emotion_label_ids: Optional[List[int]] = None
) -> Music:
    """Create music with optional emotion labels"""
    music = Music(
        title=title,
        artist=artist,
        genre=genre,
        file_path=file_path,
        file_name=file_name,
        uploaded_by=uploaded_by
    )
    
    # Add emotion labels if provided
    if emotion_label_ids:
        emotion_labels = db.query(EmotionLabel).filter(
            EmotionLabel.id.in_(emotion_label_ids)
        ).all()
        music.emotion_labels = emotion_labels
    
    db.add(music)
    db.commit()
    db.refresh(music)
    return music

def get_music_by_id(db: Session, music_id: int) -> Optional[Music]:
    return db.query(Music).filter(Music.id == music_id).first()

def get_all_music(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    emotion_label_ids: Optional[List[int]] = None
) -> List[Music]:
    """Get all music with optional filtering by emotion labels"""
    query = db.query(Music)
    
    # Filter by emotion labels if provided
    if emotion_label_ids:
        query = query.filter(Music.emotion_labels.any(EmotionLabel.id.in_(emotion_label_ids)))
    
    return query.offset(skip).limit(limit).all()

def update_music(
    db: Session, 
    music_id: int, 
    emotion_label_ids: Optional[List[int]] = None,
    **kwargs
) -> Optional[Music]:
    """Update music including emotion labels"""
    music = get_music_by_id(db, music_id)
    if music:
        # Update basic fields
        for key, value in kwargs.items():
            if value is not None and key != 'emotion_label_ids':
                setattr(music, key, value)
        
        # Update emotion labels if provided
        if emotion_label_ids is not None:
            emotion_labels = db.query(EmotionLabel).filter(
                EmotionLabel.id.in_(emotion_label_ids)
            ).all()
            music.emotion_labels = emotion_labels
        
        db.commit()
        db.refresh(music)
    return music

def delete_music(db: Session, music_id: int) -> bool:
    music = get_music_by_id(db, music_id)
    if music:
        db.delete(music)
        db.commit()
        return True
    return False
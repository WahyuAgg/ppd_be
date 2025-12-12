from sqlalchemy.orm import Session
from app.models.music import Music
from typing import Optional, List

def create_music(db: Session, title: str, artist: str, genre: str, 
                 file_path: str, file_name: str, uploaded_by: int) -> Music:
    music = Music(
        title=title,
        artist=artist,
        genre=genre,
        file_path=file_path,
        file_name=file_name,
        uploaded_by=uploaded_by
    )
    db.add(music)
    db.commit()
    db.refresh(music)
    return music

def get_music_by_id(db: Session, music_id: int) -> Optional[Music]:
    return db.query(Music).filter(Music.id == music_id).first()

def get_all_music(db: Session, skip: int = 0, limit: int = 100) -> List[Music]:
    return db.query(Music).offset(skip).limit(limit).all()

def update_music(db: Session, music_id: int, **kwargs) -> Optional[Music]:
    music = get_music_by_id(db, music_id)
    if music:
        for key, value in kwargs.items():
            if value is not None:
                setattr(music, key, value)
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
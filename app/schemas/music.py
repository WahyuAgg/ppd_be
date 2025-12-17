from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.emotion_label import EmotionLabelOut

class MusicBase(BaseModel):
    title: str
    artist: Optional[str] = None
    genre: Optional[str] = None

class MusicCreate(MusicBase):
    emotion_label_ids: Optional[List[int]] = None

class MusicUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    genre: Optional[str] = None
    emotion_label_ids: Optional[List[int]] = None

class MusicOut(MusicBase):
    id: int
    file_path: str
    file_name: str
    uploaded_by: Optional[int] = None
    created_at: datetime
    emotion_labels: List[EmotionLabelOut] = []

    class Config:
        from_attributes = True
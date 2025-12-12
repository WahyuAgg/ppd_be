from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MusicBase(BaseModel):
    title: str
    artist: Optional[str] = None
    genre: Optional[str] = None

class MusicCreate(MusicBase):
    pass

class MusicUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    genre: Optional[str] = None

class MusicOut(MusicBase):
    id: int
    file_path: str
    file_name: str
    uploaded_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
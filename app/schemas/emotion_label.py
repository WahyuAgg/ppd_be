from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmotionLabelCreate(BaseModel):
    name: str

class EmotionLabelUpdate(BaseModel):
    name: Optional[str] = None

class EmotionLabelOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

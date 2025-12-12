from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class TagBasic(BaseModel):
    """Schema minimal untuk tag dalam response history"""
    id: int
    tag_name: str

    class Config:
        from_attributes = True

class PredictionHistoryOut(BaseModel):
    id: int
    user_id: int
    input_text: str
    prediction: str
    created_at: datetime
    tags: List[TagBasic] = []

    class Config:
        from_attributes = True

class HistoryQueryParams(BaseModel):
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    tag_ids: Optional[List[int]] = None

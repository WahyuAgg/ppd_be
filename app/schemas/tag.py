from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TagCreate(BaseModel):
    tag_name: str

class TagUpdate(BaseModel):
    tag_name: Optional[str] = None

class TagOut(BaseModel):
    id: int
    tag_name: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

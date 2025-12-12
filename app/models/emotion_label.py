from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base_class import Base

class EmotionLabel(Base):
    __tablename__ = "emotion_labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

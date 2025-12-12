from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base_class import Base

# Association table untuk many-to-many relationship
prediction_history_tags = Table(
    'prediction_history_tags',
    Base.metadata,
    Column('prediction_history_id', Integer, ForeignKey('prediction_histories.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class PredictionHistory(Base):
    __tablename__ = "prediction_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    prediction = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Many-to-many relationship dengan Tag
    tags = relationship("Tag", secondary=prediction_history_tags, backref="prediction_histories")

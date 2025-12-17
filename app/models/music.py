from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base_class import Base

# Association table untuk many-to-many relationship
music_emotion_labels = Table(
    'music_emotion_labels',
    Base.metadata,
    Column('music_id', Integer, ForeignKey('musics.id', ondelete='CASCADE'), primary_key=True),
    Column('emotion_label_id', Integer, ForeignKey('emotion_labels.id', ondelete='CASCADE'), primary_key=True)
)

class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255))
    genre = Column(String(100))
    file_path = Column(String(500), nullable=False)  # Path file musik
    file_name = Column(String(255), nullable=False)  # Nama file original
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    
    # Many-to-many relationship dengan EmotionLabel
    emotion_labels = relationship("EmotionLabel", secondary=music_emotion_labels, backref="musics")
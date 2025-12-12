from app.database.base_class import Base

# Import semua model di sini agar terdaftar dalam metadata
from app.models.user import User
from app.models.music import Music
from app.models.tag import Tag
from app.models.emotion_label import EmotionLabel
from app.models.prediction_history import PredictionHistory

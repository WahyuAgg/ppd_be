# reset_db.py
import os
from app.database.session import engine
from app.database.base import Base

# Drop semua tabel
Base.metadata.drop_all(bind=engine)
print("[OK] Semua tabel dihapus")

# Buat ulang semua tabel
Base.metadata.create_all(bind=engine)
print("[OK] Semua tabel dibuat ulang")

# Jalankan seeder
from seeders.seed_emotion_labels import seed_emotion_labels
seed_emotion_labels()
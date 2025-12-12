"""
Seeder untuk EmotionLabel
Jalankan dengan: python -m seeders.seed_emotion_labels
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database.session import SessionLocal
from app.models.emotion_label import EmotionLabel

# Daftar emotion labels yang akan di-seed
EMOTION_LABELS = ['anger', 'happy', 'sadness', 'love', 'fear']

def seed_emotion_labels():
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        
        for label_name in EMOTION_LABELS:
            # Cek apakah sudah ada
            existing = db.query(EmotionLabel).filter(EmotionLabel.name == label_name).first()
            if existing:
                print(f"  [SKIP] '{label_name}' sudah ada")
                skipped += 1
            else:
                emotion_label = EmotionLabel(name=label_name)
                db.add(emotion_label)
                print(f"  [ADD]  '{label_name}'")
                added += 1
        
        db.commit()
        print(f"\n[OK] Seeding selesai! Ditambahkan: {added}, Dilewati: {skipped}")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n[SEED] Seeding Emotion Labels...")
    print("-" * 40)
    seed_emotion_labels()

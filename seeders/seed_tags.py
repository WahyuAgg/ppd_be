"""
Seeder untuk Tag
Jalankan dengan: python -m seeders.seed_tags
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database.session import SessionLocal
from app.models.tag import Tag
from app.models.user import User

# Daftar tag yang akan di-seed untuk setiap user
DEFAULT_TAGS = ['diary', 'work', 'social', 'health', 'personal']

def seed_tags():
    db = SessionLocal()
    try:
        # Ambil semua user
        users = db.query(User).all()
        
        if not users:
            print("[WARNING] Tidak ada user ditemukan. Buat user terlebih dahulu.")
            return
        
        total_added = 0
        total_skipped = 0
        
        for user in users:
            print(f"\nUser: {user.username} (ID: {user.id})")
            print("-" * 30)
            
            for tag_name in DEFAULT_TAGS:
                # Cek apakah tag sudah ada untuk user ini
                existing = db.query(Tag).filter(
                    Tag.tag_name == tag_name,
                    Tag.user_id == user.id
                ).first()
                
                if existing:
                    print(f"  [SKIP] '{tag_name}' sudah ada")
                    total_skipped += 1
                else:
                    tag = Tag(tag_name=tag_name, user_id=user.id)
                    db.add(tag)
                    print(f"  [ADD]  '{tag_name}'")
                    total_added += 1
        
        db.commit()
        print(f"\n[OK] Seeding selesai!")
        print(f"     Total user: {len(users)}")
        print(f"     Ditambahkan: {total_added}")
        print(f"     Dilewati: {total_skipped}")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n[SEED] Seeding Tags...")
    print("=" * 40)
    seed_tags()

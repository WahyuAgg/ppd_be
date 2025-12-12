from sqlalchemy.orm import Session
from app.models.tag import Tag
from typing import Optional, List

def create_tag(db: Session, tag_name: str, user_id: int) -> Tag:
    """Buat tag baru untuk user tertentu"""
    tag = Tag(tag_name=tag_name, user_id=user_id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_tag_by_id(db: Session, tag_id: int) -> Optional[Tag]:
    """Ambil tag berdasarkan ID"""
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tags_by_user_id(db: Session, user_id: int) -> List[Tag]:
    """Ambil semua tag milik user tertentu"""
    return db.query(Tag).filter(Tag.user_id == user_id).all()

def get_tag_by_name_and_user(db: Session, tag_name: str, user_id: int) -> Optional[Tag]:
    """Cek apakah tag dengan nama tertentu sudah ada untuk user"""
    return db.query(Tag).filter(Tag.tag_name == tag_name, Tag.user_id == user_id).first()

def update_tag(db: Session, tag_id: int, tag_name: str) -> Optional[Tag]:
    """Update nama tag"""
    tag = get_tag_by_id(db, tag_id)
    if tag:
        tag.tag_name = tag_name
        db.commit()
        db.refresh(tag)
    return tag

def delete_tag(db: Session, tag_id: int) -> bool:
    """Hapus tag"""
    tag = get_tag_by_id(db, tag_id)
    if tag:
        db.delete(tag)
        db.commit()
        return True
    return False

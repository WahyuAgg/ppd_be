from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.tag import TagCreate, TagUpdate, TagOut
from app.crud import tag as tag_crud

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=TagOut)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Buat tag baru untuk user yang sedang login.
    Tag akan otomatis disimpan dengan user_id dari token.
    """
    # Cek apakah tag dengan nama yang sama sudah ada untuk user ini
    existing_tag = tag_crud.get_tag_by_name_and_user(db, tag_data.tag_name, current_user.id)
    if existing_tag:
        raise HTTPException(400, f"Tag '{tag_data.tag_name}' sudah ada")
    
    tag = tag_crud.create_tag(
        db=db,
        tag_name=tag_data.tag_name,
        user_id=current_user.id
    )
    return tag

@router.get("/", response_model=List[TagOut])
def get_my_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ambil semua tag milik user yang sedang login.
    Hanya menampilkan tag yang dimiliki user berdasarkan token.
    """
    return tag_crud.get_tags_by_user_id(db, current_user.id)

@router.get("/{tag_id}", response_model=TagOut)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ambil detail tag berdasarkan ID (hanya jika milik user)"""
    tag = tag_crud.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(404, "Tag tidak ditemukan")
    if tag.user_id != current_user.id:
        raise HTTPException(403, "Tidak memiliki akses ke tag ini")
    return tag

@router.put("/{tag_id}", response_model=TagOut)
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update tag (hanya jika milik user)"""
    tag = tag_crud.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(404, "Tag tidak ditemukan")
    if tag.user_id != current_user.id:
        raise HTTPException(403, "Tidak memiliki akses ke tag ini")
    
    if tag_data.tag_name:
        # Cek duplikat nama
        existing = tag_crud.get_tag_by_name_and_user(db, tag_data.tag_name, current_user.id)
        if existing and existing.id != tag_id:
            raise HTTPException(400, f"Tag '{tag_data.tag_name}' sudah ada")
        
        tag = tag_crud.update_tag(db, tag_id, tag_data.tag_name)
    return tag

@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hapus tag (hanya jika milik user)"""
    tag = tag_crud.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(404, "Tag tidak ditemukan")
    if tag.user_id != current_user.id:
        raise HTTPException(403, "Tidak memiliki akses ke tag ini")
    
    tag_crud.delete_tag(db, tag_id)
    return {"message": "Tag berhasil dihapus"}

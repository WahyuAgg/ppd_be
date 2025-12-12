import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.music import MusicOut, MusicUpdate
from app.crud import music as music_crud

router = APIRouter(prefix="/music", tags=["Music"])

# Folder untuk menyimpan file musik
UPLOAD_DIR = "uploads/music"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".ogg"}

@router.post("/upload", response_model=MusicOut)
async def upload_music(
    title: str = Form(...),
    artist: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload file musik baru"""
    # Validasi extension file
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Format file tidak didukung. Gunakan: {ALLOWED_EXTENSIONS}")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Simpan file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Simpan ke database
    music = music_crud.create_music(
        db=db,
        title=title,
        artist=artist,
        genre=genre,
        file_path=file_path,
        file_name=file.filename,
        uploaded_by=current_user.id
    )
    return music

@router.get("/", response_model=List[MusicOut])
def get_all_music(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Mendapatkan daftar semua musik"""
    return music_crud.get_all_music(db, skip, limit)

@router.get("/{music_id}", response_model=MusicOut)
def get_music(music_id: int, db: Session = Depends(get_db)):
    """Mendapatkan detail musik berdasarkan ID"""
    music = music_crud.get_music_by_id(db, music_id)
    if not music:
        raise HTTPException(404, "Musik tidak ditemukan")
    return music

@router.get("/{music_id}/download")
def download_music(music_id: int, db: Session = Depends(get_db)):
    """Download file musik"""
    music = music_crud.get_music_by_id(db, music_id)
    if not music:
        raise HTTPException(404, "Musik tidak ditemukan")
    
    if not os.path.exists(music.file_path):
        raise HTTPException(404, "File tidak ditemukan")
    
    return FileResponse(music.file_path, filename=music.file_name)

@router.put("/{music_id}", response_model=MusicOut)
def update_music(
    music_id: int,
    music_update: MusicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update data musik"""
    music = music_crud.update_music(db, music_id, **music_update.model_dump(exclude_unset=True))
    if not music:
        raise HTTPException(404, "Musik tidak ditemukan")
    return music

@router.delete("/{music_id}")
def delete_music(
    music_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hapus musik"""
    music = music_crud.get_music_by_id(db, music_id)
    if not music:
        raise HTTPException(404, "Musik tidak ditemukan")
    
    # Hapus file fisik
    if os.path.exists(music.file_path):
        os.remove(music.file_path)
    
    # Hapus dari database
    music_crud.delete_music(db, music_id)
    return {"message": "Musik berhasil dihapus"}
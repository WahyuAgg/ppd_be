from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import pandas as pd
import io
from app.schemas.predict import PredictRequest, BatchPredictRequest, PredictResult
from app.schemas.prediction_history import PredictionHistoryOut
from app.ml.loader import predict_text
from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.models.user import User
from app.crud import prediction_history as history_crud

router = APIRouter(prefix="/predict", tags=["ML"])

@router.post("/")
def predict(
    req: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Prediksi single text dan simpan ke history.
    
    - **text**: Teks yang akan diprediksi
    - **tag_ids**: List ID tag (opsional) untuk menandai prediksi ini
    """
    result = predict_text(req.text)
    
    # Simpan ke history dengan tags
    history = history_crud.create_prediction_history(
        db=db,
        user_id=current_user.id,
        input_text=req.text,
        prediction=result,
        tag_ids=req.tag_ids
    )
    
    return {
        "input": req.text, 
        "prediction": result,
        "tags": [{"id": t.id, "tag_name": t.tag_name} for t in history.tags]
    }

@router.post("/batch", response_model=List[PredictResult])
def predict_batch(
    req: BatchPredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Prediksi batch (multiple texts) - semua disimpan ke history dengan tags yang sama.
    
    - **texts**: List teks yang akan diprediksi
    - **tag_ids**: List ID tag (opsional) untuk menandai semua prediksi dalam batch ini
    """
    results = []
    for text in req.texts:
        prediction = predict_text(text)
        
        # Simpan ke history dengan tags
        history_crud.create_prediction_history(
            db=db,
            user_id=current_user.id,
            input_text=text,
            prediction=prediction,
            tag_ids=req.tag_ids
        )
        
        results.append({"input": text, "prediction": prediction})
    return results

@router.get("/history", response_model=List[PredictionHistoryOut])
def get_prediction_history(
    date_start: Optional[date] = Query(None, description="Tanggal mulai (YYYY-MM-DD)"),
    date_end: Optional[date] = Query(None, description="Tanggal akhir (YYYY-MM-DD)"),
    tag_ids: Optional[str] = Query(None, description="Filter by tag IDs (comma separated, e.g. 1,2,3)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ambil history prediksi milik user yang sedang login.
    
    - **date_start**: Filter dari tanggal (opsional)
    - **date_end**: Filter sampai tanggal (opsional)
    - **tag_ids**: Filter berdasarkan tag IDs (comma separated, opsional)
    
    Jika tidak ada filter, akan menampilkan semua history.
    """
    # Parse tag_ids dari string ke list of int
    parsed_tag_ids = None
    if tag_ids:
        try:
            parsed_tag_ids = [int(x.strip()) for x in tag_ids.split(",")]
        except ValueError:
            raise HTTPException(400, "tag_ids harus berupa angka yang dipisahkan koma (contoh: 1,2,3)")
    
    return history_crud.get_history_by_user(
        db=db,
        user_id=current_user.id,
        date_start=date_start,
        date_end=date_end,
        tag_ids=parsed_tag_ids
    )

@router.delete("/history/{history_id}")
def delete_prediction_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hapus history prediksi (hanya milik user sendiri)"""
    success = history_crud.delete_history(db, history_id, current_user.id)
    if not success:
        raise HTTPException(404, "History tidak ditemukan atau bukan milik Anda")
    return {"message": "History berhasil dihapus"}

@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...), 
    text_column: str = "text",
    tag_ids: Optional[str] = Query(None, description="Tag IDs (comma separated) untuk semua prediksi dalam CSV"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Prediksi batch dari file CSV.
    
    - **file**: File CSV yang berisi kolom teks
    - **text_column**: Nama kolom yang berisi teks (default: "text")
    - **tag_ids**: Tag IDs (comma separated) untuk menandai semua prediksi
    
    Response: CSV file dengan kolom tambahan "prediction"
    """
    # Parse tag_ids
    parsed_tag_ids = None
    if tag_ids:
        try:
            parsed_tag_ids = [int(x.strip()) for x in tag_ids.split(",")]
        except ValueError:
            raise HTTPException(400, "tag_ids harus berupa angka yang dipisahkan koma")
    
    # Validasi file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "File harus berformat CSV")
    
    # Baca CSV
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(400, f"Gagal membaca file CSV: {str(e)}")
    
    # Validasi kolom
    if text_column not in df.columns:
        raise HTTPException(400, f"Kolom '{text_column}' tidak ditemukan. Kolom yang tersedia: {list(df.columns)}")
    
    # Prediksi dan simpan ke history
    predictions = []
    for text in df[text_column].astype(str):
        pred = predict_text(text)
        predictions.append(pred)
        
        # Simpan ke history dengan tags
        history_crud.create_prediction_history(
            db=db,
            user_id=current_user.id,
            input_text=text,
            prediction=pred,
            tag_ids=parsed_tag_ids
        )
    
    df["prediction"] = predictions
    
    # Return CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=predictions_{file.filename}"}
    )

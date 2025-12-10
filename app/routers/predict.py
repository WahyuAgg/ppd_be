from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import pandas as pd
import io
from app.schemas.predict import PredictRequest, BatchPredictRequest, PredictResult
from app.ml.loader import predict_text
from app.deps.auth import get_current_user

router = APIRouter(prefix="/predict", tags=["ML"])

@router.post("/", dependencies=[Depends(get_current_user)])
def predict(req: PredictRequest):
    """Prediksi single text"""
    result = predict_text(req.text)
    return {"input": req.text, "prediction": result}

@router.post("/batch", dependencies=[Depends(get_current_user)], response_model=List[PredictResult])
def predict_batch(req: BatchPredictRequest):
    """Prediksi batch (multiple texts) dari JSON array"""
    results = []
    for text in req.texts:
        prediction = predict_text(text)
        results.append({"input": text, "prediction": prediction})
    return results

@router.post("/csv", dependencies=[Depends(get_current_user)])
async def predict_csv(file: UploadFile = File(...), text_column: str = "text"):
    """
    Prediksi batch dari file CSV.
    
    - **file**: File CSV yang berisi kolom teks
    - **text_column**: Nama kolom yang berisi teks (default: "text")
    
    Response: CSV file dengan kolom tambahan "prediction"
    """
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
    
    # Prediksi
    predictions = []
    for text in df[text_column].astype(str):
        pred = predict_text(text)
        predictions.append(pred)
    
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

from fastapi import APIRouter, Depends
from typing import List
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
    """Prediksi batch (multiple texts)"""
    results = []
    for text in req.texts:
        prediction = predict_text(text)
        results.append({"input": text, "prediction": prediction})
    return results

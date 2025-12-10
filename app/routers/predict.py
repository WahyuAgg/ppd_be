from fastapi import APIRouter, Depends
from app.schemas.predict import PredictRequest
from app.ml.loader import predict_text
from app.deps.auth import get_current_user

router = APIRouter(prefix="/predict", tags=["ML"])

@router.post("/", dependencies=[Depends(get_current_user)])
def predict(req: PredictRequest):
    result = predict_text(req.text)
    return {"input": req.text, "prediction": result}

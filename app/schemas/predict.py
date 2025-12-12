from pydantic import BaseModel
from typing import List, Optional

class PredictRequest(BaseModel):
    text: str
    tag_ids: Optional[List[int]] = None

class BatchPredictRequest(BaseModel):
    texts: List[str]
    tag_ids: Optional[List[int]] = None  # Sama untuk semua texts dalam batch

class PredictResult(BaseModel):
    input: str
    prediction: str


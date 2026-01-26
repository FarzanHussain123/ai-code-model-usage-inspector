from pydantic import BaseModel
from typing import List
from typing import Optional

class DetectedModel(BaseModel):
    model_name: str
    provider: str
    framework: str
    file: str
    confidence: float
    explanation: Optional[str] = None

class DetectedModel(BaseModel):
    model_name: str
    provider: str
    framework: str
    file: str
    confidence: float

class ModelDetectionReport(BaseModel):
    models: List[DetectedModel]

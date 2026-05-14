from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field


class PredictRequest(BaseModel):
    ecg: List[float] = Field(..., description="ECG samples in chronological order")
    sampling_rate_hz: float = Field(..., gt=0, description="Sampling rate of the ECG series")


class PredictionCard(BaseModel):
    title: str
    state: str
    confidence_pct: str
    stress_class: int
    emotion: str
    disease: str
    summary: str
    recommendation: str
    top_features: List[str]
    warnings: List[str] = Field(default_factory=list)
    note: str = Field(
        "This is a machine learning prediction and not a medical diagnosis.",
        description="Disclaimers for user-facing output",
    )


class PredictResponse(BaseModel):
    model_config = ConfigDict(ser_json_by_alias=True)

    prediction: str
    stress_class: int = Field(serialization_alias="class", description="0 non-stress, 1 stress")
    confidence: float
    features: Dict[str, Any]
    card: PredictionCard
    warnings: List[str] = Field(default_factory=list)
    physiological_confidence: str = Field(
        default="acceptable",
        description="Feature quality indicator derived from HRV variability checks.",
    )

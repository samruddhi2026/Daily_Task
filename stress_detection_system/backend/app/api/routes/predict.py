from fastapi import APIRouter, Depends

from app.api.deps import get_inference
from app.schemas.predict import PredictRequest, PredictResponse
from app.services.prediction_service import PredictionService

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictResponse)
def predict(
    body: PredictRequest,
    inference=Depends(get_inference),
) -> PredictResponse:
    service = PredictionService(inference)
    return service.predict_ecg(body.ecg, body.sampling_rate_hz)

from fastapi import APIRouter, Depends

from app.schemas.train import TrainRequest, TrainResponse
from app.services.training_service import TrainingService

router = APIRouter(tags=["train"])


@router.post("/train", response_model=TrainResponse)
def train(body: TrainRequest) -> TrainResponse:
    service = TrainingService()
    return service.run_training(body)

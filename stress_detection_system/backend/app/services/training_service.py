from __future__ import annotations

from app.exceptions.custom_exceptions import ModelTrainingError
from app.ml.trainer import StressModelTrainer
from app.schemas.train import TrainRequest, TrainResponse


class TrainingService:
    def run_training(self, req: TrainRequest) -> TrainResponse:
        trainer = StressModelTrainer()
        try:
            metrics = trainer.train(tune=req.tune, max_windows=req.max_windows)
        except Exception as exc:  # noqa: BLE001
            raise ModelTrainingError(str(exc)) from exc
        return TrainResponse(status="ok", metrics=metrics)

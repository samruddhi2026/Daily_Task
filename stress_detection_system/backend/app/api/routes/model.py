import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_settings_dep
from app.config import Settings
from app.schemas.model import ModelInfoResponse

router = APIRouter(tags=["model"])


@router.get("/model/info", response_model=ModelInfoResponse)
def model_info(settings: Settings = Depends(get_settings_dep)) -> ModelInfoResponse:
    best = settings.best_model_path
    pipe = settings.feature_pipeline_path
    met = settings.metrics_path
    present = best.is_file() and pipe.is_file()
    feature_names = None
    model_name = None
    if met.is_file():
        try:
            with open(met, encoding="utf-8") as f:
                data = json.load(f)
            feature_names = data.get("feature_names")
            model_name = data.get("model_name")
        except Exception:  # noqa: BLE001
            pass
    return ModelInfoResponse(
        best_model_path=str(best.resolve()),
        feature_pipeline_path=str(pipe.resolve()),
        metrics_path=str(met.resolve()),
        artifacts_present=present,
        feature_names=feature_names,
        model_name=model_name,
    )

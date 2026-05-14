import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_settings_dep
from app.config import Settings

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def metrics(settings: Settings = Depends(get_settings_dep)) -> dict:
    path: Path = settings.metrics_path
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Metrics file not found. Run training first.")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data

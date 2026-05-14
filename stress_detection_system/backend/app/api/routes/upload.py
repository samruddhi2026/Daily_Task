from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.deps import get_inference
from app.schemas.predict import PredictResponse
from app.services.prediction_service import PredictionService
from app.utils.csv_ecg import load_ecg_csv

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=PredictResponse)
async def upload_ecg_csv(
    file: UploadFile = File(..., description="CSV with an ECG column"),
    sampling_rate_hz: float | None = Form(
        default=None,
        description="Sampling rate if not present in CSV as sampling_rate_hz column",
    ),
    ecg_column: str | None = Form(default=None),
    inference=Depends(get_inference),
) -> PredictResponse:
    tmp_dir = Path("data/processed/_upload_tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dest = tmp_dir / file.filename.replace("/", "_")
    content = await file.read()
    dest.write_bytes(content)
    ecg, rate_from_csv = load_ecg_csv(dest, ecg_column=ecg_column)
    fs = float(sampling_rate_hz) if sampling_rate_hz is not None else rate_from_csv
    if not (fs > 0) or fs != fs:
        raise HTTPException(
            status_code=400,
            detail="sampling_rate_hz is required when the CSV does not define sampling_rate_hz",
        )
    service = PredictionService(inference)
    return service.predict_ecg(ecg.tolist(), fs)

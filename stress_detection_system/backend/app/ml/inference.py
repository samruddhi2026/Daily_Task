from __future__ import annotations

from typing import Any, Dict, Optional

import joblib
import numpy as np
from loguru import logger

from app.config import Settings, get_settings
from app.exceptions.custom_exceptions import InferenceError
from app.feature_engineering.hrv_pipeline import (
    assess_hrv_feature_quality,
    extract_hrv_feature_row,
    feature_vector_from_dict,
)
from app.preprocessing.ecg_processor import ECGProcessor
from app.preprocessing.peak_detection import detect_r_peaks, rr_from_r_peaks


class StressInference:
    """End-to-end: ECG → HRV features → preprocessing → classifier."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._feature_pipe: Any | None = None
        self._model: Any | None = None
        self._mtime_ns: tuple[int, int] | None = None

    def load_artifacts(self) -> None:
        fp = self.settings.feature_pipeline_path
        mp = self.settings.best_model_path
        if not fp.is_file() or not mp.is_file():
            raise InferenceError(
                f"Missing model artifacts. Train first. Expected {fp} and {mp}."
            )
        mtime = (fp.stat().st_mtime_ns, mp.stat().st_mtime_ns)
        if self._feature_pipe is not None and self._model is not None and getattr(self, "_mtime_ns", None) == mtime:
            return
        self._feature_pipe = joblib.load(fp)
        self._model = joblib.load(mp)
        self._mtime_ns = mtime
        logger.info("Loaded inference artifacts from {} and {}", fp, mp)

    @property
    def ready(self) -> bool:
        return self._feature_pipe is not None and self._model is not None

    def predict_from_ecg(
        self,
        ecg: np.ndarray,
        sampling_rate_hz: float,
    ) -> Dict[str, Any]:
        self.load_artifacts()
        assert self._feature_pipe is not None and self._model is not None

        arr = np.asarray(ecg, dtype=np.float64).ravel()
        fs = float(sampling_rate_hz)
        if fs <= 0.0 or not np.isfinite(fs):
            raise InferenceError("Invalid ECG sampling rate.")
        duration_s = arr.size / fs
        if duration_s < self.settings.min_inference_duration_seconds:
            raise InferenceError("ECG too short for meaningful HRV analysis. Minimum 60 seconds required.")

        proc = ECGProcessor(sampling_rate_hz=sampling_rate_hz)
        try:
            p = proc.preprocess_full(arr)
            peaks = detect_r_peaks(p.signal, sampling_rate_hz)
            rr = rr_from_r_peaks(peaks, sampling_rate_hz)
            feats = extract_hrv_feature_row(rr)
            x = feature_vector_from_dict(feats).reshape(1, -1)
            xt = self._feature_pipe.transform(x)
            proba = self._model.predict_proba(xt)[0, 1]
            cls = int(self._model.predict(xt)[0])
            warnings = assess_hrv_feature_quality(feats)
        except Exception as exc:  # noqa: BLE001
            if isinstance(exc, InferenceError):
                raise
            raise InferenceError(str(exc)) from exc

        label_name = "stress" if cls == 1 else "non-stress"
        return {
            "prediction": label_name,
            "class": cls,
            "confidence": float(max(proba, 1.0 - proba)),
            "features": feats,
            "warnings": warnings,
            "physiological_confidence": "limited" if warnings else "acceptable",
        }

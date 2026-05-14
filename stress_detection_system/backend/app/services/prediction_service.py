from __future__ import annotations

import numpy as np

from app.exceptions.custom_exceptions import InferenceError
from app.ml.inference import StressInference
from app.schemas.predict import PredictionCard, PredictResponse


class PredictionService:
    """Application service for stress inference."""

    def __init__(self, inference: StressInference) -> None:
        self._inference = inference

    def _build_prediction_card(self, raw: dict) -> PredictionCard:
        label = raw["prediction"]
        cls = raw["class"]
        confidence = raw["confidence"]
        features = raw["features"]

        title = "Stress Detected" if cls == 1 else "No Stress Detected"
        state = "stress" if cls == 1 else "non-stress"
        emotion = "stress" if cls == 1 else "relaxed"
        disease = "Disease diagnosis is not available from this model"
        confidence_pct = f"{confidence * 100:.1f}%"

        sorted_features = sorted(
            features.items(), key=lambda item: abs(item[1] if isinstance(item[1], (int, float)) else 0), reverse=True
        )
        top_features = [f"{name}: {value:.3f}" for name, value in sorted_features[:4]]

        summary = (
            "The ECG signal is interpreted as a stress response. "
            if cls == 1
            else "The ECG signal is interpreted as non-stress."
        )
        recommendation = (
            "Consider stress-reduction techniques such as breathing exercises, rest, or talking to a professional. "
            if cls == 1
            else "Continue monitoring and maintain healthy habits to support relaxed state."
        )
        warnings = raw.get("warnings", [])
        if warnings:
            summary = f"{summary} {warnings[0]}"

        return PredictionCard(
            title=title,
            state=state,
            confidence_pct=confidence_pct,
            stress_class=cls,
            emotion=emotion,
            disease=disease,
            summary=summary,
            recommendation=recommendation,
            top_features=top_features,
            warnings=warnings,
        )

    def predict_ecg(self, ecg: list[float], sampling_rate_hz: float) -> PredictResponse:
        arr = np.asarray(ecg, dtype=np.float64).ravel()
        fs = float(sampling_rate_hz)
        if fs <= 0.0 or not np.isfinite(fs):
            raise InferenceError("Invalid ECG sampling rate.")
        min_seconds = float(self._inference.settings.min_inference_duration_seconds)
        min_samples = int(np.ceil(fs * min_seconds))
        if arr.size < min_samples:
            raise InferenceError("ECG too short for meaningful HRV analysis. Minimum 60 seconds required.")
        if not self._inference.ready:
            self._inference.load_artifacts()
        raw = self._inference.predict_from_ecg(arr, sampling_rate_hz)
        return PredictResponse(
            prediction=raw["prediction"],
            stress_class=raw["class"],
            confidence=raw["confidence"],
            features=raw["features"],
            card=self._build_prediction_card(raw),
            warnings=raw.get("warnings", []),
            physiological_confidence=raw.get("physiological_confidence", "acceptable"),
        )

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from app.exceptions.custom_exceptions import FeatureExtractionError

from .frequency_domain import frequency_domain_features
from .nonlinear import nonlinear_features
from .time_domain import time_domain_features

MIN_RR_INTERVALS_FOR_HRV = 30
MIN_RR_DURATION_SECONDS_FOR_HRV = 30.0
LOW_VARIABILITY_WARNING = (
    "Prediction generated with limited physiological confidence due to insufficient HRV variability."
)


def prepare_rr_intervals(rr_ms: np.ndarray) -> np.ndarray:
    """Clean RR intervals before HRV extraction.

    The peak detector already rejects implausible beat intervals, but this second
    pass protects feature extraction from NaNs, zeros, and isolated missed/extra
    detections without flattening real beat-to-beat variability.
    """
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr) & (rr >= 300.0) & (rr <= 2000.0)]
    if rr.size == 0:
        return rr

    median_rr = float(np.median(rr))
    if not np.isfinite(median_rr) or median_rr <= 0.0:
        return np.array([], dtype=np.float64)

    # Broad physiological artifact guard: keep intervals within +/-35% of the
    # local median. This removes obvious missed/double peaks while preserving
    # respiratory sinus arrhythmia and stress-related variability.
    lower = max(300.0, 0.65 * median_rr)
    upper = min(2000.0, 1.35 * median_rr)
    return rr[(rr >= lower) & (rr <= upper)]


def _sanitize_row(row: Dict[str, float]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for k, v in row.items():
        if isinstance(v, (float, np.floating)):
            if not np.isfinite(v):
                out[k] = 0.0
            else:
                out[k] = float(v)
        else:
            out[k] = float(v)
    return out


def extract_hrv_feature_row(rr_ms: np.ndarray) -> Dict[str, Any]:
    """Aggregate time, frequency, and nonlinear HRV features for one window."""
    rr = prepare_rr_intervals(rr_ms)
    if rr.size < MIN_RR_INTERVALS_FOR_HRV:
        raise FeatureExtractionError(
            f"Not enough valid RR intervals for HRV extraction. "
            f"Need at least {MIN_RR_INTERVALS_FOR_HRV}, received {rr.size}."
        )
    duration_s = float(np.sum(rr) / 1000.0)
    if duration_s < MIN_RR_DURATION_SECONDS_FOR_HRV:
        raise FeatureExtractionError(
            f"RR interval series too short for HRV extraction. "
            f"Need at least {MIN_RR_DURATION_SECONDS_FOR_HRV:.0f} seconds, received {duration_s:.1f}."
        )
    try:
        feats: Dict[str, float] = {}
        feats.update(time_domain_features(rr))
        feats.update(frequency_domain_features(rr))
        feats.update(nonlinear_features(rr))
        return _sanitize_row(feats)
    except Exception as exc:  # noqa: BLE001
        raise FeatureExtractionError(str(exc)) from exc


def assess_hrv_feature_quality(row: Dict[str, float]) -> list[str]:
    """Return user-facing warnings for physiologically weak HRV features."""
    sdnn = float(row.get("sdnn", 0.0) or 0.0)
    rmssd = float(row.get("rmssd", 0.0) or 0.0)
    pnn50 = float(row.get("pnn50", 0.0) or 0.0)
    lf = float(row.get("lf", 0.0) or 0.0)
    hf = float(row.get("hf", 0.0) or 0.0)

    low_variability = sdnn < 5.0 or rmssd < 5.0 or pnn50 <= 0.0
    weak_frequency_power = lf <= 0.0 or hf <= 0.0
    if low_variability or weak_frequency_power:
        return [LOW_VARIABILITY_WARNING]
    return []


FEATURE_ORDER: list[str] = [
    "mean_hr",
    "min_hr",
    "max_hr",
    "std_hr",
    "mean_rr",
    "sdnn",
    "rmssd",
    "pnn50",
    "lf",
    "hf",
    "lf_hf_ratio",
    "total_power",
    "vlf",
    "sample_entropy",
    "approximate_entropy",
    "sd1",
    "sd2",
    "stress_index",
]


def feature_vector_from_dict(row: Dict[str, float]) -> np.ndarray:
    x = np.array([float(row.get(k, 0.0)) for k in FEATURE_ORDER], dtype=np.float64)
    return np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)

from __future__ import annotations

from typing import Dict

import numpy as np


def time_domain_features(rr_ms: np.ndarray) -> Dict[str, float]:
    """Compute time-domain HRV metrics from RR intervals in milliseconds."""
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr) & (rr > 0)]
    if rr.size < 2:
        return _nan_time_domain()

    hr = np.divide(60000.0, rr, out=np.full_like(rr, np.nan), where=rr > 0)
    hr = hr[np.isfinite(hr)]
    if hr.size == 0:
        return _nan_time_domain()

    diffs = np.diff(rr)

    sdnn = float(np.std(rr, ddof=1)) if rr.size > 1 else float("nan")
    rmssd = float(np.sqrt(np.mean(diffs**2))) if diffs.size else float("nan")
    pnn50 = float(np.mean(np.abs(diffs) > 50.0) * 100.0) if diffs.size else float("nan")

    return {
        "mean_hr": float(np.mean(hr)),
        "min_hr": float(np.min(hr)),
        "max_hr": float(np.max(hr)),
        "std_hr": float(np.std(hr, ddof=1)) if hr.size > 1 else 0.0,
        "mean_rr": float(np.mean(rr)),
        "sdnn": sdnn,
        "rmssd": rmssd,
        "pnn50": pnn50,
    }


def _nan_time_domain() -> Dict[str, float]:
    keys = [
        "mean_hr",
        "min_hr",
        "max_hr",
        "std_hr",
        "mean_rr",
        "sdnn",
        "rmssd",
        "pnn50",
    ]
    return {k: float("nan") for k in keys}

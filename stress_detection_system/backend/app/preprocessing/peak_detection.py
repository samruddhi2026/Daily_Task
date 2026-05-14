from __future__ import annotations

from typing import Tuple

import numpy as np
from loguru import logger

from app.exceptions.custom_exceptions import PeakDetectionError

try:
    import neurokit2 as nk
except ImportError:  # pragma: no cover
    nk = None  # type: ignore

try:
    import heartpy as hp
except ImportError:  # pragma: no cover
    hp = None  # type: ignore

from scipy import signal as scipy_signal


def _rr_from_peaks(peaks: np.ndarray, fs: float) -> np.ndarray:
    if peaks.size < 2:
        return np.array([], dtype=np.float64)
    rr = np.diff(peaks.astype(np.float64)) / fs * 1000.0
    return rr


def _reject_rr(rr_ms: np.ndarray, min_ms: float = 300.0, max_ms: float = 2000.0) -> np.ndarray:
    if rr_ms.size == 0:
        return rr_ms
    m = (rr_ms >= min_ms) & (rr_ms <= max_ms)
    return rr_ms[m]


def _fallback_peaks(ecg: np.ndarray, fs: float) -> np.ndarray:
    """Derivative + squared + moving integration + peak picking (Pan-Tompkins-like)."""
    x = np.asarray(ecg, dtype=np.float64).ravel()
    dx = np.diff(x, prepend=x[0])
    y = dx**2
    win = int(max(round(0.15 * fs), 1))
    kernel = np.ones(win) / float(win)
    zi = scipy_signal.convolve(y, kernel, mode="same")
    distance = int(max(round(0.25 * fs), 1))
    height = float(np.percentile(zi, 75))
    peaks, _ = scipy_signal.find_peaks(zi, distance=distance, height=height)
    return peaks.astype(np.int64)


def detect_r_peaks(ecg: np.ndarray, sampling_rate_hz: float) -> np.ndarray:
    """Robust R-peak indices; tries NeuroKit2, then HeartPy, then custom fallback."""
    x = np.asarray(ecg, dtype=np.float64).ravel()
    fs = float(sampling_rate_hz)
    if x.size < fs * 2:
        raise PeakDetectionError("Signal too short for R-peak detection")

    peaks: np.ndarray | None = None
    if nk is not None:
        try:
            _, info = nk.ecg_peaks(x, sampling_rate=fs, method="neurokit", correct_artifacts=True)
            peaks = np.asarray(info["ECG_R_Peaks"], dtype=np.int64)
        except Exception as exc:  # noqa: BLE001
            logger.warning("NeuroKit2 ecg_peaks failed: {}", exc)

    if peaks is None or peaks.size < 2:
        if hp is not None:
            try:
                wd, _ = hp.process(x, sample_rate=fs, bpmmin=40, bpmmax=200)
                peaks = np.asarray(wd.get("peaklist", []), dtype=np.int64)
            except Exception as exc:  # noqa: BLE001
                logger.warning("HeartPy peak detection failed: {}", exc)

    if peaks is None or peaks.size < 2:
        peaks = _fallback_peaks(x, fs)

    peaks = np.unique(peaks[(peaks >= 0) & (peaks < x.size)])
    if peaks.size < 2:
        raise PeakDetectionError("Insufficient R-peaks detected")
    return peaks


def rr_from_r_peaks(r_peaks: np.ndarray, sampling_rate_hz: float) -> np.ndarray:
    rr = _rr_from_peaks(r_peaks, float(sampling_rate_hz))
    rr = _reject_rr(rr)
    if rr.size < 2:
        raise PeakDetectionError("Insufficient valid RR intervals after rejection")
    return rr

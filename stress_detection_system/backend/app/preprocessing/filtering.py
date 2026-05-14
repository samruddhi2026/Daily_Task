from __future__ import annotations

import numpy as np
from scipy import signal as scipy_signal


def bandpass_filter(
    ecg: np.ndarray,
    sampling_rate_hz: float,
    low_hz: float = 5.0,
    high_hz: float = 40.0,
    order: int = 4,
) -> np.ndarray:
    """Butterworth bandpass to emphasize QRS while suppressing noise."""
    x = np.asarray(ecg, dtype=np.float64).ravel()
    nyq = 0.5 * float(sampling_rate_hz)
    lo = max(low_hz / nyq, 1e-6)
    hi = min(high_hz / nyq, 0.999)
    if lo >= hi:
        raise ValueError("Invalid bandpass corners relative to Nyquist")
    b, a = scipy_signal.butter(order, [lo, hi], btype="band")
    return scipy_signal.filtfilt(b, a, x)


def remove_baseline_wander(
    ecg: np.ndarray,
    sampling_rate_hz: float,
    cutoff_hz: float = 0.5,
    order: int = 3,
) -> np.ndarray:
    """High-pass filter to reduce baseline wander."""
    x = np.asarray(ecg, dtype=np.float64).ravel()
    nyq = 0.5 * float(sampling_rate_hz)
    wn = min(max(cutoff_hz / nyq, 1e-6), 0.999)
    b, a = scipy_signal.butter(order, wn, btype="high")
    return scipy_signal.filtfilt(b, a, x)


def moving_average_smooth(x: np.ndarray, kernel: int = 5) -> np.ndarray:
    """Light moving-average denoising (odd kernel)."""
    arr = np.asarray(x, dtype=np.float64).ravel()
    k = int(kernel) if int(kernel) % 2 == 1 else int(kernel) + 1
    if k <= 1:
        return arr
    pad = k // 2
    padded = np.pad(arr, (pad, pad), mode="edge")
    cumsum = np.cumsum(np.insert(padded, 0, 0))
    return (cumsum[k:] - cumsum[:-k]) / float(k)

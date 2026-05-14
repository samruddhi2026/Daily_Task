import numpy as np

from app.preprocessing.peak_detection import detect_r_peaks, rr_from_r_peaks


def _synthetic_ecg_with_qrs(fs: float = 250.0, duration_s: float = 45.0, bpm: float = 72.0) -> np.ndarray:
    n = int(duration_s * fs)
    x = np.zeros(n, dtype=np.float64)
    period = int(round(60.0 / bpm * fs))
    peaks = np.arange(period // 2, n, period, dtype=int)
    width = max(int(0.02 * fs), 3)
    for p in peaks:
        lo = max(0, p - width)
        hi = min(n, p + width)
        x[lo:hi] += np.hanning(hi - lo)
    x += 0.01 * np.random.default_rng(0).standard_normal(n)
    return x


def test_rr_extraction() -> None:
    fs = 250.0
    ecg = _synthetic_ecg_with_qrs(fs=fs, duration_s=45.0, bpm=70.0)
    peaks = detect_r_peaks(ecg, fs)
    rr = rr_from_r_peaks(peaks, fs)
    assert rr.size >= 10

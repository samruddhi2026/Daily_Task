from __future__ import annotations

from typing import Dict

import numpy as np
from scipy import interpolate, signal


VLF_BAND = (0.0033, 0.04)
LF_BAND = (0.04, 0.15)
HF_BAND = (0.15, 0.40)
TOTAL_BAND = (0.0033, 0.40)


def frequency_domain_features(rr_ms: np.ndarray, fs_resample_hz: float = 4.0) -> Dict[str, float]:
    """Welch PSD on uniformly resampled RR tachogram.

    RR intervals are interpolated onto a 4 Hz grid, detrended, and integrated over
    standard HRV bands. Output powers are in ms^2 because the tachogram is kept in
    milliseconds.
    """
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr) & (rr > 0)]
    if rr.size < 8:
        return _nan_freq()

    rr_sec = rr / 1000.0
    t_beats = np.concatenate([[0.0], np.cumsum(rr_sec)])
    t_mid = 0.5 * (t_beats[:-1] + t_beats[1:])
    duration = float(t_mid[-1] - t_mid[0])
    if duration < 30.0:
        return _nan_freq()

    t_uniform = np.arange(t_mid[0], t_mid[-1], 1.0 / fs_resample_hz)
    if t_uniform.size < 64:
        return _nan_freq()

    interp = interpolate.interp1d(
        t_mid,
        rr,
        kind="linear",
        fill_value="extrapolate",
        bounds_error=False,
    )
    tachogram = interp(t_uniform)
    tachogram = signal.detrend(tachogram, type="constant")
    if not np.any(np.isfinite(tachogram)) or float(np.nanstd(tachogram)) <= 1e-12:
        return {
            "lf": 0.0,
            "hf": 0.0,
            "lf_hf_ratio": float("nan"),
            "total_power": 0.0,
            "vlf": 0.0,
        }

    nperseg = min(256, len(tachogram))
    noverlap = min(nperseg // 2, nperseg - 1)
    freqs, psd = signal.welch(
        tachogram,
        fs=fs_resample_hz,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend="constant",
        scaling="density",
    )

    def band_power(f_lo: float, f_hi: float) -> float:
        if freqs.size < 2 or psd.size != freqs.size:
            return float("nan")
        if f_hi <= freqs[0] or f_lo >= freqs[-1]:
            return 0.0
        lo = max(f_lo, float(freqs[0]))
        hi = min(f_hi, float(freqs[-1]))
        if hi <= lo:
            return 0.0
        m = (freqs > lo) & (freqs < hi)
        f_band = np.concatenate(([lo], freqs[m], [hi]))
        p_band = np.interp(f_band, freqs, psd)
        _trapz = getattr(np, "trapezoid", np.trapz)
        power = float(_trapz(p_band, f_band))
        return power if np.isfinite(power) and power >= 0.0 else float("nan")

    vlf = band_power(*VLF_BAND)
    lf = band_power(*LF_BAND)
    hf = band_power(*HF_BAND)
    total = band_power(*TOTAL_BAND)
    lf_hf = lf / hf if np.isfinite(lf) and np.isfinite(hf) and hf > 1e-12 else float("nan")

    return {
        "lf": lf,
        "hf": hf,
        "lf_hf_ratio": lf_hf,
        "total_power": total,
        "vlf": vlf,
    }


def _nan_freq() -> Dict[str, float]:
    return {
        "lf": float("nan"),
        "hf": float("nan"),
        "lf_hf_ratio": float("nan"),
        "total_power": float("nan"),
        "vlf": float("nan"),
    }

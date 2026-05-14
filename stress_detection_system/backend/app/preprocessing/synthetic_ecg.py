from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticECG:
    timestamp: np.ndarray
    ecg: np.ndarray
    r_peaks: np.ndarray
    rr_ms: np.ndarray
    sampling_rate_hz: float

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame({"timestamp": self.timestamp, "ecg": self.ecg})

    def to_csv(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        self.to_frame().to_csv(out, index=False)
        return out


def _gaussian(t: np.ndarray, center: float, width: float, amplitude: float) -> np.ndarray:
    return amplitude * np.exp(-0.5 * ((t - center) / width) ** 2)


def _beat_times(
    duration_seconds: float,
    rng: np.random.Generator,
    base_hr_bpm: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Create beat times with LF modulation, RSA, drift, and random jitter."""
    beat_times: list[float] = []
    rr_values: list[float] = []

    respiratory_rate_hz = float(rng.uniform(0.18, 0.32))
    rsa_amp_bpm = float(rng.uniform(6.0, 10.0))
    lf_amp_bpm = float(rng.uniform(3.0, 6.0))
    drift_amp_bpm = float(rng.uniform(1.0, 3.0))
    lf_phase = float(rng.uniform(0.0, 2.0 * np.pi))
    hf_phase = float(rng.uniform(0.0, 2.0 * np.pi))
    drift_phase = float(rng.uniform(0.0, 2.0 * np.pi))

    t = 0.75
    while t < duration_seconds - 0.5:
        instantaneous_hr = (
            base_hr_bpm
            + lf_amp_bpm * np.sin(2.0 * np.pi * 0.10 * t + lf_phase)
            + rsa_amp_bpm * np.sin(2.0 * np.pi * respiratory_rate_hz * t + hf_phase)
            + drift_amp_bpm * np.sin(2.0 * np.pi * 0.025 * t + drift_phase)
            + rng.normal(0.0, 1.8)
        )
        instantaneous_hr = float(np.clip(instantaneous_hr, 60.0, 110.0))
        rr_sec = 60.0 / instantaneous_hr
        rr_sec += float(rng.normal(0.0, 0.025))
        rr_sec = float(np.clip(rr_sec, 60.0 / 110.0, 60.0 / 60.0))
        t += rr_sec
        if t < duration_seconds - 0.5:
            beat_times.append(t)
            rr_values.append(rr_sec * 1000.0)

    return np.asarray(beat_times, dtype=np.float64), np.asarray(rr_values, dtype=np.float64)


def generate_realistic_synthetic_ecg(
    duration_seconds: float = 90.0,
    sampling_rate_hz: float = 700.0,
    seed: int | None = 42,
    base_hr_bpm: float = 78.0,
    noise_std: float = 0.018,
) -> SyntheticECG:
    """Generate physiologically varied synthetic ECG for HRV pipeline testing.

    The signal includes variable RR intervals, respiratory sinus arrhythmia,
    LF autonomic modulation, morphology variation, baseline wander, measurement
    noise, and small transient artifacts. It is intended for software validation,
    not clinical model training.
    """
    if duration_seconds < 60.0:
        raise ValueError("Synthetic ECG duration must be at least 60 seconds for HRV analysis.")
    if sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be positive.")

    fs = float(sampling_rate_hz)
    rng = np.random.default_rng(seed)
    n_samples = int(round(duration_seconds * fs))
    timestamp = np.arange(n_samples, dtype=np.float64) / fs

    base_hr = float(np.clip(base_hr_bpm + rng.normal(0.0, 4.0), 66.0, 92.0))
    beat_times, rr_ms = _beat_times(duration_seconds, rng, base_hr)
    ecg = np.zeros(n_samples, dtype=np.float64)

    for beat_time in beat_times:
        amp_scale = float(np.clip(rng.normal(1.0, 0.06), 0.85, 1.15))
        width_scale = float(np.clip(rng.normal(1.0, 0.04), 0.90, 1.10))
        local = timestamp - beat_time
        mask = (local >= -0.35) & (local <= 0.55)
        if not np.any(mask):
            continue
        lt = local[mask]
        beat = (
            _gaussian(lt, -0.20, 0.045 * width_scale, 0.12 * amp_scale)
            + _gaussian(lt, -0.035, 0.011 * width_scale, -0.16 * amp_scale)
            + _gaussian(lt, 0.0, 0.013 * width_scale, 1.05 * amp_scale)
            + _gaussian(lt, 0.037, 0.017 * width_scale, -0.28 * amp_scale)
            + _gaussian(lt, 0.28, 0.080 * width_scale, 0.34 * amp_scale)
        )
        ecg[mask] += beat

    baseline = (
        0.045 * np.sin(2.0 * np.pi * 0.28 * timestamp + rng.uniform(0.0, 2.0 * np.pi))
        + 0.020 * np.sin(2.0 * np.pi * 0.05 * timestamp + rng.uniform(0.0, 2.0 * np.pi))
    )
    mains = 0.004 * np.sin(2.0 * np.pi * 50.0 * timestamp + rng.uniform(0.0, 2.0 * np.pi))
    noise = rng.normal(0.0, noise_std, n_samples)
    ecg = ecg + baseline + mains + noise

    n_artifacts = max(1, int(duration_seconds // 30))
    for _ in range(n_artifacts):
        center = float(rng.uniform(5.0, duration_seconds - 5.0))
        width = float(rng.uniform(0.08, 0.25))
        amplitude = float(rng.uniform(-0.05, 0.05))
        ecg += _gaussian(timestamp, center, width, amplitude)

    r_peaks = np.clip(np.rint(beat_times * fs).astype(np.int64), 0, n_samples - 1)
    return SyntheticECG(
        timestamp=timestamp,
        ecg=ecg.astype(np.float64),
        r_peaks=r_peaks,
        rr_ms=rr_ms,
        sampling_rate_hz=fs,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from loguru import logger

from app.exceptions.custom_exceptions import ECGPreprocessingError

from .filtering import bandpass_filter, moving_average_smooth, remove_baseline_wander


@dataclass
class ProcessedECG:
    signal: np.ndarray
    sampling_rate_hz: float
    original_length: int


class ECGProcessor:
    """ECG denoising, baseline correction, bandpass, segmentation helpers."""

    def __init__(
        self,
        sampling_rate_hz: float,
        bandpass_low_hz: float = 5.0,
        bandpass_high_hz: float = 40.0,
        baseline_cutoff_hz: float = 0.5,
        smooth_kernel: int = 5,
    ) -> None:
        self.sampling_rate_hz = float(sampling_rate_hz)
        self.bandpass_low_hz = bandpass_low_hz
        self.bandpass_high_hz = bandpass_high_hz
        self.baseline_cutoff_hz = baseline_cutoff_hz
        self.smooth_kernel = smooth_kernel

    def validate_signal(self, ecg: np.ndarray) -> None:
        arr = np.asarray(ecg, dtype=np.float64).ravel()
        if arr.size < int(self.sampling_rate_hz * 2):
            raise ECGPreprocessingError("ECG segment too short for reliable processing")
        if np.all(np.isnan(arr)) or np.nanstd(arr) < 1e-9:
            raise ECGPreprocessingError("ECG signal is flat or all NaN")

    def preprocess_full(self, ecg: np.ndarray) -> ProcessedECG:
        """Full pipeline on one segment."""
        self.validate_signal(ecg)
        x = np.asarray(ecg, dtype=np.float64).ravel()
        orig_len = x.size
        x = np.nan_to_num(x, nan=np.nanmedian(x))
        try:
            x = remove_baseline_wander(x, self.sampling_rate_hz, self.baseline_cutoff_hz)
            x = bandpass_filter(
                x,
                self.sampling_rate_hz,
                self.bandpass_low_hz,
                self.bandpass_high_hz,
            )
            x = moving_average_smooth(x, self.smooth_kernel)
        except Exception as exc:  # noqa: BLE001
            logger.exception("ECG preprocessing failed")
            raise ECGPreprocessingError(str(exc)) from exc
        return ProcessedECG(
            signal=x,
            sampling_rate_hz=self.sampling_rate_hz,
            original_length=orig_len,
        )

    @staticmethod
    def segment_indices(
        length: int,
        window_samples: int,
        step_samples: int,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if window_samples <= 0 or step_samples <= 0:
            raise ECGPreprocessingError("Invalid segmentation parameters")
        starts = np.arange(0, max(length - window_samples + 1, 1), step_samples, dtype=np.int64)
        ends = starts + window_samples
        return starts, ends

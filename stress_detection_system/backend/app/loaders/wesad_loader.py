from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import numpy as np
from loguru import logger

from app.config import Settings, get_settings
from app.exceptions.custom_exceptions import DatasetLoadError

# WESAD chest ECG and label annotation rate (Hz)
WESAD_ECG_FS: float = 700.0

# Raw WESAD label codes (exclude 0,3,4 per project scope)
WESAD_BASELINE: int = 1
WESAD_STRESS: int = 2


@dataclass(frozen=True)
class WESADSample:
    """One window of ECG with a binary stress label."""

    subject_id: str
    ecg: np.ndarray
    label: int  # 0 non-stress (baseline), 1 stress
    start_idx: int
    end_idx: int


def _map_label(raw: int) -> Optional[int]:
    if raw == WESAD_BASELINE:
        return 0
    if raw == WESAD_STRESS:
        return 1
    return None


def _majority_binary_label(segment_labels: np.ndarray) -> Optional[int]:
    mapped = [_map_label(int(x)) for x in np.asarray(segment_labels).ravel()]
    valid = [m for m in mapped if m is not None]
    if not valid:
        return None
    counts = np.bincount(np.asarray(valid, dtype=np.int64), minlength=2)
    if counts.sum() < len(mapped):
        # Contains excluded labels in window — skip if any excluded present
        if len(valid) != len(mapped):
            return None
    if counts[0] == counts[1] and counts[0] > 0:
        return None
    return int(np.argmax(counts))


class WESADLoader:
    """Load WESAD pickle files: chest ECG only, binary baseline/stress labels."""

    def __init__(self, data_dir: Optional[Path] = None, settings: Optional[Settings] = None) -> None:
        self._settings = settings or get_settings()
        self.data_dir = Path(data_dir or self._settings.wesad_data_dir)

    def validate_root(self) -> None:
        if not self.data_dir.is_dir():
            raise DatasetLoadError(f"WESAD root directory does not exist: {self.data_dir}")

    def list_subject_ids(self) -> List[str]:
        self.validate_root()
        subjects: List[str] = []
        for p in sorted(self.data_dir.iterdir()):
            if p.is_dir() and p.name.startswith("S") and p.name[1:].isdigit():
                subjects.append(p.name)
        if not subjects:
            raise DatasetLoadError(f"No WESAD subject folders found under {self.data_dir}")
        logger.info("Discovered {} WESAD subjects: {}", len(subjects), subjects)
        return subjects

    def _pickle_path(self, subject_id: str) -> Path:
        return self.data_dir / subject_id / f"{subject_id}.pkl"

    def load_subject_pickle(self, subject_id: str) -> Dict:
        path = self._pickle_path(subject_id)
        if not path.is_file():
            raise DatasetLoadError(f"Missing pickle for {subject_id}: {path}")
        try:
            with open(path, "rb") as f:
                data = pickle.load(f, encoding="latin1")
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to unpickle {}: {}", path, exc)
            raise DatasetLoadError(f"Corrupted or unreadable pickle: {path}") from exc
        if not isinstance(data, dict):
            raise DatasetLoadError(f"Unexpected pickle structure for {subject_id}")
        return data

    def extract_ecg_and_labels(
        self, subject_id: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Return ECG (mV or arbitrary units) and per-sample labels at 700 Hz."""
        data = self.load_subject_pickle(subject_id)
        try:
            signal = data["signal"]
            chest = signal["chest"]
            ecg = np.asarray(chest["ECG"], dtype=np.float64).ravel()
            labels = np.asarray(data["label"], dtype=np.int64).ravel()
        except Exception as exc:  # noqa: BLE001
            raise DatasetLoadError(f"ECG/label extraction failed for {subject_id}") from exc
        n = min(len(ecg), len(labels))
        if n < self._settings.ecg_sampling_rate_hz * 10:
            raise DatasetLoadError(f"ECG too short for subject {subject_id}")
        ecg = ecg[:n]
        labels = labels[:n]
        return ecg, labels

    def iter_windowed_samples(
        self,
        subject_id: str,
        window_seconds: Optional[float] = None,
        step_seconds: Optional[float] = None,
        fs: float = WESAD_ECG_FS,
    ) -> Iterator[WESADSample]:
        """Yield labeled windows; skips windows with mixed or excluded labels."""
        ws = float(window_seconds or self._settings.window_seconds)
        st = float(step_seconds or self._settings.window_step_seconds)
        win = int(round(ws * fs))
        step = int(round(st * fs))
        if win <= 0 or step <= 0:
            raise DatasetLoadError("Invalid windowing parameters")

        ecg, labels = self.extract_ecg_and_labels(subject_id)
        for start in range(0, len(ecg) - win + 1, step):
            end = start + win
            seg_lab = labels[start:end]
            maj = _majority_binary_label(seg_lab)
            if maj is None:
                continue
            yield WESADSample(
                subject_id=subject_id,
                ecg=ecg[start:end].copy(),
                label=maj,
                start_idx=start,
                end_idx=end,
            )

    def iter_all_samples(self) -> Iterator[WESADSample]:
        for sid in self.list_subject_ids():
            try:
                yield from self.iter_windowed_samples(sid)
            except DatasetLoadError as exc:
                logger.warning("Skipping subject {}: {}", sid, exc)

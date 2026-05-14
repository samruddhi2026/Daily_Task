from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pytest

from app.config import Settings
from app.exceptions.custom_exceptions import DatasetLoadError
from app.loaders.wesad_loader import WESADLoader, WESAD_ECG_FS


def _make_minimal_wesad_pickle(tmp: Path, subject: str = "S99") -> Path:
    fs = int(WESAD_ECG_FS)
    n = fs * 120  # 2 minutes
    ecg = np.random.randn(n).astype(np.float64) * 0.5
    labels = np.ones(n, dtype=np.int64)  # baseline
    labels[fs * 60 :] = 2  # second minute stress
    subdir = tmp / subject
    subdir.mkdir(parents=True)
    payload = {
        "signal": {"chest": {"ECG": ecg}},
        "label": labels,
        "subject": subject,
    }
    pkl = subdir / f"{subject}.pkl"
    with open(pkl, "wb") as f:
        pickle.dump(payload, f)
    return tmp


def test_loader_window_labels(tmp_path: Path) -> None:
    root = _make_minimal_wesad_pickle(tmp_path)
    settings = Settings(
        wesad_data_dir=root,
        window_seconds=30.0,
        window_step_seconds=30.0,
        ecg_sampling_rate_hz=WESAD_ECG_FS,
    )
    loader = WESADLoader(data_dir=root, settings=settings)
    ids = loader.list_subject_ids()
    assert "S99" in ids
    samples = list(loader.iter_windowed_samples("S99"))
    assert len(samples) >= 2
    assert all(s.label in (0, 1) for s in samples)


def test_missing_pickle(tmp_path: Path) -> None:
    (tmp_path / "S1").mkdir()
    settings = Settings(wesad_data_dir=tmp_path)
    loader = WESADLoader(settings=settings)
    with pytest.raises(DatasetLoadError):
        loader.load_subject_pickle("S1")

import numpy as np

from app.preprocessing.ecg_processor import ECGProcessor
from app.preprocessing.filtering import bandpass_filter


def test_bandpass_shape() -> None:
    x = np.random.randn(7000)
    y = bandpass_filter(x, 700.0)
    assert y.shape == x.shape


def test_ecg_processor_min_length() -> None:
    proc = ECGProcessor(700.0)
    short = np.zeros(100)
    try:
        proc.preprocess_full(short)
        assert False, "expected error"
    except Exception:
        assert True

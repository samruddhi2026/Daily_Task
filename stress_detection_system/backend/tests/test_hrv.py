import numpy as np

from app.feature_engineering.hrv_pipeline import extract_hrv_feature_row, FEATURE_ORDER
from app.preprocessing.synthetic_ecg import generate_realistic_synthetic_ecg


def test_hrv_keys() -> None:
    rr = 800.0 + 20.0 * np.sin(np.linspace(0, 6.28, 80))
    row = extract_hrv_feature_row(rr)
    for k in FEATURE_ORDER:
        assert k in row


def test_realistic_synthetic_ecg_produces_nonzero_hrv() -> None:
    synthetic = generate_realistic_synthetic_ecg(duration_seconds=90.0, sampling_rate_hz=700.0, seed=7)
    row = extract_hrv_feature_row(synthetic.rr_ms)

    assert row["sdnn"] > 0.0
    assert row["rmssd"] > 0.0
    assert row["pnn50"] > 0.0
    assert row["lf"] > 0.0
    assert row["hf"] > 0.0
    assert row["sample_entropy"] >= 0.0
    assert row["approximate_entropy"] >= 0.0
    assert row["stress_index"] > 0.0
    assert synthetic.to_frame().columns.tolist() == ["timestamp", "ecg"]

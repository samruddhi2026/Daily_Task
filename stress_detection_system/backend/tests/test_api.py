from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pytest
from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression

from app.config.settings import get_settings
from app.feature_engineering.hrv_pipeline import FEATURE_ORDER
from app.main import create_app
from app.ml.models import build_feature_pipeline
from app.preprocessing.synthetic_ecg import generate_realistic_synthetic_ecg


@pytest.fixture()
def client_with_models(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    wesad = tmp_path / "wesad"
    wesad.mkdir(parents=True, exist_ok=True)
    logs = tmp_path / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(0)
    X = rng.normal(size=(40, len(FEATURE_ORDER)))
    y = rng.integers(0, 2, size=(40,))
    pipe = build_feature_pipeline()
    Xt = pipe.fit_transform(X)
    clf = LogisticRegression(max_iter=500, random_state=0)
    clf.fit(Xt, y)

    joblib.dump(pipe, models_dir / "feature_pipeline.pkl")
    joblib.dump(clf, models_dir / "best_model.pkl")
    metrics = {"model_name": "logistic_regression", "feature_names": FEATURE_ORDER}
    (models_dir / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")

    get_settings.cache_clear()
    monkeypatch.setenv("MODELS_DIR", str(models_dir))
    monkeypatch.setenv("WESAD_DATA_DIR", str(wesad))
    monkeypatch.setenv("LOGS_DIR", str(logs))
    get_settings.cache_clear()

    app = create_app()
    return TestClient(app)


def test_health(client_with_models: TestClient) -> None:
    r = client_with_models.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_model_info(client_with_models: TestClient) -> None:
    r = client_with_models.get("/api/v1/model/info")
    assert r.status_code == 200
    body = r.json()
    assert body["artifacts_present"] is True


def test_predict_json(client_with_models: TestClient) -> None:
    fs = 700.0
    synthetic = generate_realistic_synthetic_ecg(duration_seconds=65.0, sampling_rate_hz=fs, seed=11)
    ecg = synthetic.ecg.tolist()
    r = client_with_models.post("/api/v1/predict", json={"ecg": ecg, "sampling_rate_hz": fs})
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "warnings" in data


def test_predict_rejects_short_ecg(client_with_models: TestClient) -> None:
    fs = 700.0
    t = np.arange(0, 10.0, 1 / fs)
    ecg = (np.sin(2 * np.pi * 1.2 * t) * 0.5).tolist()
    r = client_with_models.post("/api/v1/predict", json={"ecg": ecg, "sampling_rate_hz": fs})
    assert r.status_code == 422
    assert r.json()["detail"] == "ECG too short for meaningful HRV analysis. Minimum 60 seconds required."

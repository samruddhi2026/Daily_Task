from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from loguru import logger
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.svm import SVC
from xgboost import XGBClassifier

from app.config import Settings, get_settings
from app.exceptions.custom_exceptions import ModelTrainingError
from app.feature_engineering.hrv_pipeline import (
    FEATURE_ORDER,
    extract_hrv_feature_row,
    feature_vector_from_dict,
)
from app.loaders.wesad_loader import WESADLoader, WESADSample
from app.evaluation.metrics import compute_classification_metrics, feature_importance_vector
from app.evaluation.visualization import plot_confusion_matrix, plot_roc_curve
from app.ml.models import build_feature_pipeline
from app.preprocessing.ecg_processor import ECGProcessor
from app.preprocessing.peak_detection import detect_r_peaks, rr_from_r_peaks

from .tuning import tune_estimator


def _sample_to_vector(sample: WESADSample, fs: float) -> Optional[np.ndarray]:
    proc = ECGProcessor(sampling_rate_hz=fs)
    try:
        p = proc.preprocess_full(sample.ecg)
        peaks = detect_r_peaks(p.signal, fs)
        rr = rr_from_r_peaks(peaks, fs)
        row = extract_hrv_feature_row(rr)
        return feature_vector_from_dict(row)
    except Exception as exc:  # noqa: BLE001
        logger.debug("Window skipped for training: {}", exc)
        return None


def collect_xy_from_wesad(
    settings: Optional[Settings] = None,
    max_windows: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Build X (n_samples, n_features) and y from WESAD windows."""
    s = settings or get_settings()
    loader = WESADLoader(settings=s)
    X_list: List[np.ndarray] = []
    y_list: List[int] = []
    count = 0
    for sample in loader.iter_all_samples():
        vec = _sample_to_vector(sample, s.ecg_sampling_rate_hz)
        if vec is None:
            continue
        X_list.append(vec)
        y_list.append(sample.label)
        count += 1
        if max_windows is not None and count >= max_windows:
            break
    if len(X_list) < 20:
        raise ModelTrainingError(
            "Too few valid training windows. Check WESAD path, labels, and preprocessing."
        )
    X = np.vstack(X_list)
    y = np.asarray(y_list, dtype=np.int64)
    logger.info("Collected training matrix X={}, y={}, features={}", X.shape, y.shape, FEATURE_ORDER)
    return X, y


def _build_estimator_catalog(random_state: int) -> Dict[str, Any]:
    return {
        "logistic_regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=random_state,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=None,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "svm": SVC(
            kernel="rbf",
            probability=True,
            class_weight="balanced",
            random_state=random_state,
        ),
        "xgboost": XGBClassifier(
            n_estimators=400,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=-1,
        ),
        "lightgbm": LGBMClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=-1,
            subsample=0.9,
            colsample_bytree=0.9,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
            verbosity=-1,
        ),
        "catboost": CatBoostClassifier(
            depth=6,
            iterations=400,
            learning_rate=0.05,
            loss_function="Logloss",
            verbose=False,
            random_seed=random_state,
            auto_class_weights="Balanced",
        ),
    }


def _train_and_save_artifacts(
    settings: Settings,
    X: np.ndarray,
    y: np.ndarray,
    tune: bool,
    extra_metrics: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Shared training, evaluation, and persistence for any feature matrix X and labels y."""
    rs = settings.random_state
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=settings.train_test_size,
            stratify=y,
            random_state=rs,
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=settings.train_test_size,
            stratify=None,
            random_state=rs,
        )

    feature_pipe = build_feature_pipeline()
    X_train_t = feature_pipe.fit_transform(X_train)
    X_test_t = feature_pipe.transform(X_test)

    catalog = _build_estimator_catalog(rs)
    catalog["stacking"] = _build_stacking(rs)

    scores: Dict[str, float] = {}
    fitted: Dict[str, Any] = {}

    for name, est in catalog.items():
        logger.info("Training model: {}", name)
        try:
            model = est
            if tune and name in {"xgboost", "lightgbm", "random_forest", "svm"}:
                model = tune_estimator(name, model, X_train_t, y_train, rs)
            else:
                model.fit(X_train_t, y_train)

            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_test_t)[:, 1]
                auc = float(roc_auc_score(y_test, proba))
            else:
                auc = 0.0
            scores[name] = auc
            fitted[name] = model
            logger.info("Model {} ROC-AUC (holdout) = {:.4f}", name, auc)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Model {} failed: {}", name, exc)

    if not scores:
        raise ModelTrainingError("No models trained successfully")

    best_name = max(scores, key=lambda k: scores[k])
    best_model = fitted[best_name]
    logger.info("Best model: {} with ROC-AUC={}", best_name, scores[best_name])

    y_hat = best_model.predict(X_test_t)
    y_proba = (
        best_model.predict_proba(X_test_t)[:, 1]
        if hasattr(best_model, "predict_proba")
        else None
    )
    test_metrics = compute_classification_metrics(y_test, y_hat, y_proba)

    n0 = int(np.sum(y_train == 0))
    n1 = int(np.sum(y_train == 1))
    cv_splits = min(settings.cv_folds, max(2, min(n0, n1)))
    try:
        cv_auc = cross_val_score(
            best_model,
            X_train_t,
            y_train,
            cv=StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=rs),
            scoring="roc_auc",
            n_jobs=-1,
        )
        cv_auc_list = [float(x) for x in cv_auc]
    except Exception as exc:  # noqa: BLE001
        logger.warning("Cross-validation skipped: {}", exc)
        cv_auc_list = []

    importance = feature_importance_vector(best_model, FEATURE_ORDER)
    plots_dir = settings.models_dir / "plots"
    cm_path = plot_confusion_matrix(y_test, y_hat, plots_dir / "confusion_matrix.png")
    roc_path = None
    if y_proba is not None:
        roc_path = plot_roc_curve(y_test, y_proba, plots_dir / "roc_curve.png")

    joblib.dump(feature_pipe, settings.feature_pipeline_path)
    joblib.dump(best_model, settings.best_model_path)

    metrics: Dict[str, Any] = {
        "model_name": best_name,
        "holdout_roc_auc_by_model": scores,
        "test_metrics": test_metrics,
        "cv_roc_auc_mean": float(np.mean(cv_auc_list)) if cv_auc_list else None,
        "cv_roc_auc_std": float(np.std(cv_auc_list)) if cv_auc_list else None,
        "cv_roc_auc_folds": cv_auc_list,
        "feature_names": FEATURE_ORDER,
        "feature_importance": importance[:25],
        "plots": {
            "confusion_matrix": str(cm_path),
            "roc_curve": str(roc_path) if roc_path else None,
        },
    }
    if extra_metrics:
        metrics.update(extra_metrics)

    import json

    with open(settings.metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, default=str)

    return metrics


def _build_stacking(random_state: int) -> StackingClassifier:
    base = _build_estimator_catalog(random_state)
    estimators = [
        ("rf", base["random_forest"]),
        ("xgb", base["xgboost"]),
        ("lgbm", base["lightgbm"]),
        ("cat", base["catboost"]),
    ]
    return StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(max_iter=2000, class_weight="balanced", random_state=random_state),
        stack_method="predict_proba",
        cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=random_state),
        n_jobs=-1,
    )


class StressModelTrainer:
    """Train, compare, persist best binary stress classifier + feature pipeline."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self.settings.models_dir.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        tune: bool = False,
        max_windows: Optional[int] = None,
    ) -> Dict[str, Any]:
        X, y = collect_xy_from_wesad(self.settings, max_windows=max_windows)
        return _train_and_save_artifacts(self.settings, X, y, tune)

    def train_demo(
        self,
        tune: bool = False,
        n_samples: int = 1200,
    ) -> Dict[str, Any]:
        """Train on synthetic data with the same feature dimension as HRV (UI / pipeline smoke test only)."""
        rs = self.settings.random_state
        n_feat = len(FEATURE_ORDER)
        n_inf = min(12, max(2, n_feat - 4))
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_feat,
            n_informative=n_inf,
            n_redundant=min(4, n_feat - n_inf - 1),
            n_clusters_per_class=1,
            random_state=rs,
        )
        X = X.astype(np.float64)
        y = y.astype(np.int64)
        logger.warning(
            "DEMO training: synthetic features only — not WESAD / not for research claims. "
            "Use train() with real WESAD pickles for production."
        )
        return _train_and_save_artifacts(
            self.settings,
            X,
            y,
            tune,
            extra_metrics={
                "data_source": "synthetic_demo",
                "disclaimer": "Trained on sklearn synthetic data for artifact smoke test only.",
            },
        )


def load_training_frame(settings: Optional[Settings] = None) -> pd.DataFrame:
    """Optional helper: load X,y as DataFrame for analysis."""
    X, y = collect_xy_from_wesad(settings)
    cols = FEATURE_ORDER
    df = pd.DataFrame(X, columns=cols)
    df["label"] = y
    return df

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def confusion_matrix_dict(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "matrix": cm.tolist(),
        "labels": ["non-stress (0)", "stress (1)"],
    }


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix_dict(y_true, y_pred),
        "classification_report": classification_report(
            y_true,
            y_pred,
            target_names=["non-stress", "stress"],
            zero_division=0,
        ),
    }
    if y_proba is not None and y_proba.size:
        try:
            out["roc_auc"] = float(roc_auc_score(y_true, y_proba))
            fpr, tpr, thr = roc_curve(y_true, y_proba)
            out["roc_curve"] = {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
                "thresholds": thr.tolist(),
            }
        except Exception:  # noqa: BLE001
            out["roc_auc"] = float("nan")
            out["roc_curve"] = {}
    return out


def feature_importance_vector(model: Any, feature_names: List[str]) -> List[Dict[str, float]]:
    """Best-effort feature importance for tree models and linear coef magnitude."""
    names = list(feature_names)
    if hasattr(model, "feature_importances_"):
        imp = np.asarray(model.feature_importances_, dtype=np.float64)
        order = np.argsort(-imp)
        return [{"feature": names[i], "importance": float(imp[i])} for i in order]
    if hasattr(model, "coef_"):
        coef = np.asarray(model.coef_, dtype=np.float64).ravel()
        mag = np.abs(coef)
        order = np.argsort(-mag)
        return [{"feature": names[i], "importance": float(mag[i])} for i in order]
    return []

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler


class IQRClipper(BaseEstimator, TransformerMixin):
    """Clip each feature to [Q1 - k*IQR, Q3 + k*IQR] learned on the training set."""

    def __init__(self, factor: float = 1.5) -> None:
        self.factor = float(factor)
        self.low_: np.ndarray | None = None
        self.high_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> "IQRClipper":
        x = np.asarray(X, dtype=np.float64)
        q1 = np.nanpercentile(x, 25.0, axis=0)
        q3 = np.nanpercentile(x, 75.0, axis=0)
        iqr = q3 - q1
        self.low_ = q1 - self.factor * iqr
        self.high_ = q3 + self.factor * iqr
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.low_ is None or self.high_ is None:
            raise RuntimeError("IQRClipper is not fitted")
        x = np.asarray(X, dtype=np.float64)
        return np.clip(x, self.low_, self.high_)


def build_feature_pipeline() -> Pipeline:
    """Imputation → outlier clipping → robust scaling."""
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("clip", IQRClipper(factor=1.5)),
            ("scaler", RobustScaler(with_centering=True, with_scaling=True)),
        ]
    )

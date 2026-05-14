import numpy as np
from sklearn.datasets import make_classification

from app.ml.models import build_feature_pipeline


def test_feature_pipeline_fit_transform() -> None:
    X, _ = make_classification(n_samples=50, n_features=len(np.arange(18)), random_state=0)
    pipe = build_feature_pipeline()
    Xt = pipe.fit_transform(X)
    assert Xt.shape == X.shape

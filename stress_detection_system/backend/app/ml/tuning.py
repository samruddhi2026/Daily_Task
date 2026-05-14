from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import loguniform, randint, uniform
from sklearn.model_selection import RandomizedSearchCV


def tune_estimator(
    name: str,
    estimator: Any,
    X: np.ndarray,
    y: np.ndarray,
    random_state: int,
    n_iter: int = 12,
) -> Any:
    """Lightweight hyperparameter search for a subset of models."""
    if name == "random_forest":
        param_dist = {
            "n_estimators": randint(200, 800),
            "max_depth": [None, 10, 20, 30],
            "min_samples_leaf": randint(1, 5),
        }
    elif name == "xgboost":
        param_dist = {
            "n_estimators": randint(200, 800),
            "max_depth": randint(3, 9),
            "learning_rate": loguniform(1e-3, 0.3),
            "subsample": uniform(0.65, 0.35),
        }
    elif name == "lightgbm":
        param_dist = {
            "n_estimators": randint(200, 800),
            "num_leaves": randint(16, 128),
            "learning_rate": loguniform(1e-3, 0.3),
            "subsample": uniform(0.65, 0.35),
        }
    elif name == "svm":
        param_dist = {
            "C": loguniform(1e-2, 1e3),
            "gamma": loguniform(1e-4, 1e0),
        }
    else:
        estimator.fit(X, y)
        return estimator

    search = RandomizedSearchCV(
        estimator,
        param_distributions=param_dist,
        n_iter=n_iter,
        scoring="roc_auc",
        cv=3,
        random_state=random_state,
        n_jobs=-1,
        verbose=0,
    )
    search.fit(X, y)
    return search.best_estimator_

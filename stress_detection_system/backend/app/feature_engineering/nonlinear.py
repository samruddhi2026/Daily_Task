from __future__ import annotations

import math
from typing import Dict

import numpy as np


def _sample_entropy(data: np.ndarray, m: int = 2, r: float | None = None) -> float:
    """Sample entropy (Richman & Moorman); O(n^2), suitable for short RR series."""
    x = np.asarray(data, dtype=np.float64).ravel()
    x = x[np.isfinite(x)]
    n = x.size
    if n < m + 2:
        return float("nan")
    sd = float(np.std(x, ddof=1))
    if sd <= 0 or not math.isfinite(sd):
        return float("nan")
    r = 0.2 * sd if r is None else r

    def _count_templates(order: int) -> int:
        cnt = 0
        for i in range(n - order + 1):
            xi = x[i : i + order]
            for j in range(i + 1, n - order + 1):
                xj = x[j : j + order]
                if np.max(np.abs(xi - xj)) <= r:
                    cnt += 1
        return cnt

    b = _count_templates(m)
    a = _count_templates(m + 1)
    if b <= 0:
        return float("nan")
    if a <= 0:
        # Small physiological windows can legitimately have no length m+1
        # matches. Use a Laplace-corrected fallback instead of returning an
        # undefined value that later breaks inference.
        a = 1
        b += 1
    return float(-math.log(a / b))


def _approximate_entropy(data: np.ndarray, m: int = 2, r: float | None = None) -> float:
    x = np.asarray(data, dtype=np.float64).ravel()
    x = x[np.isfinite(x)]
    n = x.size
    if n < m + 1:
        return float("nan")
    sd = float(np.std(x, ddof=1))
    if sd <= 0 or not math.isfinite(sd):
        return float("nan")
    r = 0.2 * sd if r is None else r

    def _phi(order: int) -> float:
        patterns = np.array([x[i : i + order] for i in range(n - order + 1)])
        c = np.zeros(patterns.shape[0])
        for i in range(patterns.shape[0]):
            dist = np.max(np.abs(patterns - patterns[i]), axis=1)
            c[i] = np.sum(dist <= r) / float(n - order + 1)
        c = np.clip(c, 1e-12, None)
        return float(np.mean(np.log(c)))

    return float(_phi(m) - _phi(m + 1))


def _poincare_sd1_sd2(rr_ms: np.ndarray) -> tuple[float, float]:
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr)]
    if rr.size < 3:
        return float("nan"), float("nan")
    x = rr[:-1]
    y = rr[1:]
    sd1 = float(np.std((y - x) / np.sqrt(2.0), ddof=1))
    sd2 = float(np.std((x + y) / np.sqrt(2.0), ddof=1))
    return sd1, sd2


def _baevsky_stress_index(rr_ms: np.ndarray, bin_width_ms: float = 50.0) -> float:
    """Approximate Baevsky stress index from RR histogram."""
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr)]
    if rr.size < 5:
        return float("nan")
    edges = np.arange(rr.min(), rr.max() + bin_width_ms, bin_width_ms)
    hist, _ = np.histogram(rr, bins=edges)
    if hist.size == 0 or np.max(hist) == 0:
        return float("nan")
    mode_idx = int(np.argmax(hist))
    mo = float(0.5 * (edges[mode_idx] + edges[mode_idx + 1]))
    amo = float(hist[mode_idx] / rr.size * 100.0)
    mxdmn = float((rr.max() - rr.min()) / 1000.0)  # seconds
    if mxdmn <= 0 or mo <= 0:
        return float("nan")
    si = amo / (2.0 * mxdmn * (mo / 1000.0) + 1e-9)
    return float(si)


def nonlinear_features(rr_ms: np.ndarray) -> Dict[str, float]:
    rr = np.asarray(rr_ms, dtype=np.float64).ravel()
    rr = rr[np.isfinite(rr)]
    sd1, sd2 = _poincare_sd1_sd2(rr)
    return {
        "sample_entropy": _sample_entropy(rr, m=2),
        "approximate_entropy": _approximate_entropy(rr, m=2),
        "sd1": sd1,
        "sd2": sd2,
        "stress_index": _baevsky_stress_index(rr),
    }

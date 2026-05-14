from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from app.exceptions.custom_exceptions import ValidationError


def load_ecg_csv(
    path: Path | str,
    ecg_column: Optional[str] = None,
) -> Tuple[np.ndarray, float]:
    """Load ECG samples from CSV. Column name optional; auto-detect common names.

    Optional column `sampling_rate_hz` as scalar in first row or dedicated row — if absent,
    caller must pass rate via API.
    """
    p = Path(path)
    if not p.is_file():
        raise ValidationError(f"File not found: {p}")
    df = pd.read_csv(p)
    if df.empty:
        raise ValidationError("CSV is empty")

    rate: Optional[float] = None
    if "sampling_rate_hz" in df.columns:
        rate = float(df["sampling_rate_hz"].iloc[0])

    col = ecg_column
    if col is None:
        for c in df.columns:
            cl = str(c).lower().strip()
            if cl in ("ecg", "signal", "ecg_mv", "voltage"):
                col = c
                break
        if col is None and len(df.columns) == 1:
            col = df.columns[0]
    if col is None or col not in df.columns:
        raise ValidationError(
            "Could not determine ECG column. Provide a column named 'ecg' or pass ecg_column."
        )

    ecg = pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=np.float64)
    if np.all(np.isnan(ecg)):
        raise ValidationError("ECG column contains no numeric values")
    ecg = np.nan_to_num(ecg, nan=np.nanmedian(ecg))
    return ecg, (rate if rate is not None else float("nan"))

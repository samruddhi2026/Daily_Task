import pandas as pd
import numpy as np
from pathlib import Path
from typing import List
from .wesad_loader import WESADLoader


def compute_window_features(df: pd.DataFrame, window_size: int = 64 * 30) -> pd.DataFrame:
    """Compute features for non‑overlapping windows.
    window_size is number of samples at 64 Hz (default 30 s).
    Returns a DataFrame where each row is a window.
    """
    # Ensure numeric columns
    numeric_cols = [c for c in df.columns if c not in ["Subject", "Label"]]
    rows = []
    for start in range(0, len(df), window_size):
        end = start + window_size
        if end > len(df):
            break
        win = df.iloc[start:end]
        feats = {}
        # HR stats (if present)
        if "HR" in win.columns:
            feats["hr_mean"] = win["HR"].mean()
            feats["hr_std"] = win["HR"].std()
        # HRV from IBI if present
        if "IBI" in win.columns:
            ibi = win["IBI"].dropna()
            if len(ibi) > 1:
                diffs = ibi.diff().dropna()
                feats["sdnn"] = ibi.std()
                feats["rmssd"] = np.sqrt((diffs ** 2).mean())
        # EDA stats
        if "EDA" in win.columns:
            feats["eda_mean"] = win["EDA"].mean()
            # simple peak count
            peaks = (win["EDA"] > win["EDA"].mean() + win["EDA"].std()).sum()
            feats["eda_peaks"] = peaks
        # TEMP stats
        if "TEMP" in win.columns:
            feats["temp_mean"] = win["TEMP"].mean()
            feats["temp_trend"] = win["TEMP"].iloc[-1] - win["TEMP"].iloc[0]
        # Accelerometer energy
        if all(col in win.columns for col in ["ACC_X", "ACC_Y", "ACC_Z"]):
            acc_vec = np.sqrt(win["ACC_X"] ** 2 + win["ACC_Y"] ** 2 + win["ACC_Z"] ** 2)
            feats["acc_energy"] = (acc_vec ** 2).sum()
        # Add subject and label (majority label in window)
        feats["Subject"] = win["Subject"].iloc[0]
        # Majority label
        if "Label" in win.columns:
            feats["Label"] = win["Label"].mode()[0]
        rows.append(feats)
    return pd.DataFrame(rows)


def build_dataset(data_dir: str = "D:/WESAD", output_path: str = "processed_features.csv"):
    loader = WESADLoader(data_dir)
    all_frames: List[pd.DataFrame] = []
    for sid in loader.subjects:
        df = loader.extract_features(sid)
        if df is not None:
            all_frames.append(df)
    if not all_frames:
        raise RuntimeError("No subject data loaded")
    full = pd.concat(all_frames, ignore_index=True)
    # Compute windowed features
    feature_df = compute_window_features(full)
    # Merge lifestyle context (already merged inside loader if needed)
    feature_df.to_csv(output_path, index=False)
    print(f"Dataset written to {output_path}, shape={feature_df.shape}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create processed WESAD feature dataset")
    parser.add_argument("--data-dir", default="D:/WESAD", help="Root folder of WESAD dataset")
    parser.add_argument("--out", default="processed_features.csv", help="Output CSV file")
    args = parser.parse_args()
    build_dataset(args.data_dir, args.out)

import pandas as pd
from typing import Tuple


def extract_features_from_csv(csv_path: str) -> Tuple[pd.DataFrame, list]:
    """Read a CSV file containing heart rate data and compute simple features.
    Expected CSV columns: `timestamp` (optional) and `HR` (beats per minute).
    Returns a DataFrame with one row of aggregated features and a list of feature names.
    """
    df = pd.read_csv(csv_path)
    if 'HR' not in df.columns:
        raise ValueError('CSV must contain an HR column')
    # If timestamps are present, compute inter-beat intervals (IBI) assuming HR is instantaneous BPM
    # IBI (ms) = 60,000 / HR
    if 'timestamp' in df.columns:
        df['IBI'] = 60000.0 / df['HR']
    else:
        df['IBI'] = 60000.0 / df['HR']
    # Feature engineering
    features = {}
    # Basic HR stats
    features['hr_mean'] = df['HR'].mean()
    features['hr_std'] = df['HR'].std()
    # HRV stats from IBI
    features['ibi_mean'] = df['IBI'].mean()
    features['ibi_std'] = df['IBI'].std()
    # Simple HRV metrics (SDNN, RMSSD)
    features['sdnn'] = df['IBI'].std()
    ibi_diff = df['IBI'].diff().dropna()
    features['rmssd'] = (ibi_diff ** 2).mean() ** 0.5
    # Return as single‑row DataFrame
    feature_df = pd.DataFrame([features])
    return feature_df, list(features.keys())

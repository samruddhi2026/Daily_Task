from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.preprocessing.synthetic_ecg import generate_realistic_synthetic_ecg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate realistic synthetic ECG CSV for HRV testing.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/synthetic_realistic_ecg_90s_700hz.csv"),
        help="Destination CSV path.",
    )
    parser.add_argument("--duration-seconds", type=float, default=90.0)
    parser.add_argument("--sampling-rate-hz", type=float, default=700.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--base-hr-bpm", type=float, default=78.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    synthetic = generate_realistic_synthetic_ecg(
        duration_seconds=args.duration_seconds,
        sampling_rate_hz=args.sampling_rate_hz,
        seed=args.seed,
        base_hr_bpm=args.base_hr_bpm,
    )
    out = synthetic.to_csv(args.output)
    print(f"Wrote {len(synthetic.ecg)} samples at {synthetic.sampling_rate_hz:g} Hz to {out}")
    print(
        "RR summary: "
        f"n={synthetic.rr_ms.size}, "
        f"mean={synthetic.rr_ms.mean():.1f} ms, "
        f"sd={synthetic.rr_ms.std(ddof=1):.1f} ms"
    )


if __name__ == "__main__":
    main()

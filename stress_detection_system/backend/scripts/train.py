"""CLI entrypoint for offline training."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.logger import configure_logging
from app.ml.trainer import StressModelTrainer


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description="Train stress classifier on WESAD ECG windows")
    parser.add_argument("--tune", action="store_true", help="Enable hyperparameter search")
    parser.add_argument("--max-windows", type=int, default=None, help="Cap number of windows")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Train on synthetic features (same dimension as HRV) when WESAD pickles are unavailable — for UI smoke test only",
    )
    parser.add_argument("--demo-samples", type=int, default=1200, help="Samples for --demo mode")
    args = parser.parse_args()
    trainer = StressModelTrainer()
    if args.demo:
        metrics = trainer.train_demo(tune=args.tune, n_samples=args.demo_samples)
        print("DEMO training complete (not real WESAD). Best:", metrics.get("model_name"))
    else:
        metrics = trainer.train(tune=args.tune, max_windows=args.max_windows)
        print("Training complete. Best:", metrics.get("model_name"))


if __name__ == "__main__":
    main()

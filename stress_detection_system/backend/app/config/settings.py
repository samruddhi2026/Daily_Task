from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = Field(default="Stress Detection System (ECG/HRV)")
    version: str = Field(default="1.0.0")
    api_v1_prefix: str = Field(default="/api/v1")
    debug: bool = Field(default=False)

    wesad_data_dir: Path = Field(
        default=Path("data/raw/WESAD"),
        description="Root directory containing WESAD subject folders (S2, S3, ...).",
    )
    models_dir: Path = Field(default=Path("models"))
    logs_dir: Path = Field(default=Path("logs"))
    processed_data_dir: Path = Field(default=Path("data/processed"))
    features_data_dir: Path = Field(default=Path("data/features"))
    metadata_dir: Path = Field(default=Path("data/metadata"))

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    ecg_sampling_rate_hz: float = Field(
        default=700.0,
        description="WESAD chest ECG sampling rate (Hz).",
    )
    window_seconds: float = Field(
        default=60.0,
        description="Segment length for feature extraction (seconds).",
    )
    window_step_seconds: float = Field(
        default=60.0,
        description="Stride between windows (seconds); non-overlapping if equal to window.",
    )
    min_inference_duration_seconds: float = Field(
        default=60.0,
        description="Minimum ECG duration required for meaningful HRV inference.",
    )

    train_test_size: float = Field(default=0.2, ge=0.05, le=0.5)
    random_state: int = Field(default=42)
    cv_folds: int = Field(default=5, ge=2, le=10)

    cors_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
        ]
    )

    log_json: bool = Field(
        default=False,
        description="Emit structured JSON logs when True (production).",
    )

    best_model_filename: str = Field(default="best_model.pkl")
    feature_pipeline_filename: str = Field(default="feature_pipeline.pkl")
    metrics_filename: str = Field(default="metrics.json")

    @field_validator("debug", mode="before")
    @classmethod
    def _parse_debug(cls, v: object) -> object:
        if isinstance(v, str):
            normalized = v.strip().lower()
            if normalized in {"release", "prod", "production", "false", "0", "no", "off"}:
                return False
            if normalized in {"debug", "dev", "development", "true", "1", "yes", "on"}:
                return True
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v: object) -> object:
        if isinstance(v, str):
            import json

            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:  # noqa: BLE001
                return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @field_validator("wesad_data_dir", "models_dir", "logs_dir", mode="before")
    @classmethod
    def _coerce_path(cls, v: Optional[str | Path]) -> Path:
        return Path(v) if v is not None else Path(".")

    @property
    def best_model_path(self) -> Path:
        return self.models_dir / self.best_model_filename

    @property
    def feature_pipeline_path(self) -> Path:
        return self.models_dir / self.feature_pipeline_filename

    @property
    def metrics_path(self) -> Path:
        return self.models_dir / self.metrics_filename


@lru_cache
def get_settings() -> Settings:
    return Settings()

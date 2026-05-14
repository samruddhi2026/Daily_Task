from app.config import Settings, get_settings
from app.ml.inference import StressInference


def get_settings_dep() -> Settings:
    return get_settings()


def get_inference() -> StressInference:
    return StressInference(get_settings_dep())

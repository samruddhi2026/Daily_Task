"""Domain-specific exceptions for the stress detection backend."""


class DatasetLoadError(Exception):
    """Raised when WESAD data cannot be loaded or is invalid."""


class ECGPreprocessingError(Exception):
    """Raised when ECG preprocessing fails."""


class PeakDetectionError(Exception):
    """Raised when R-peak detection or RR extraction fails."""


class FeatureExtractionError(Exception):
    """Raised when HRV or feature extraction fails."""


class ModelTrainingError(Exception):
    """Raised when model training or persistence fails."""


class InferenceError(Exception):
    """Raised when inference pipeline fails."""


class ValidationError(Exception):
    """Raised when input validation fails (distinct from Pydantic ValidationError)."""

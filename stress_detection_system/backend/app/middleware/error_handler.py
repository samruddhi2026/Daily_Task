from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError as PydanticValidationError

from app.exceptions.custom_exceptions import (
    DatasetLoadError,
    ECGPreprocessingError,
    FeatureExtractionError,
    InferenceError,
    ModelTrainingError,
    PeakDetectionError,
    ValidationError as AppValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DatasetLoadError)
    async def _dataset(_: Request, exc: DatasetLoadError) -> JSONResponse:
        logger.exception("Dataset load error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc), "code": "DATASET_LOAD_ERROR"},
        )

    @app.exception_handler(ECGPreprocessingError)
    async def _ecg(_: Request, exc: ECGPreprocessingError) -> JSONResponse:
        logger.exception("ECG preprocessing error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc), "code": "ECG_PREPROCESSING_ERROR"},
        )

    @app.exception_handler(PeakDetectionError)
    async def _peak(_: Request, exc: PeakDetectionError) -> JSONResponse:
        logger.exception("Peak detection error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc), "code": "PEAK_DETECTION_ERROR"},
        )

    @app.exception_handler(FeatureExtractionError)
    async def _feat(_: Request, exc: FeatureExtractionError) -> JSONResponse:
        logger.exception("Feature extraction error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc), "code": "FEATURE_EXTRACTION_ERROR"},
        )

    @app.exception_handler(ModelTrainingError)
    async def _train(_: Request, exc: ModelTrainingError) -> JSONResponse:
        logger.exception("Model training error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc), "code": "MODEL_TRAINING_ERROR"},
        )

    @app.exception_handler(InferenceError)
    async def _inf(_: Request, exc: InferenceError) -> JSONResponse:
        logger.exception("Inference error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc), "code": "INFERENCE_ERROR"},
        )

    @app.exception_handler(AppValidationError)
    async def _val(_: Request, exc: AppValidationError) -> JSONResponse:
        logger.warning("Validation error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc), "code": "VALIDATION_ERROR"},
        )

    @app.exception_handler(PydanticValidationError)
    async def _pydantic(_: Request, exc: PydanticValidationError) -> JSONResponse:
        logger.warning("Request validation failed: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors(), "code": "REQUEST_VALIDATION_ERROR"},
        )

    @app.exception_handler(Exception)
    async def _generic(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error: {}", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "code": "INTERNAL_ERROR"},
        )

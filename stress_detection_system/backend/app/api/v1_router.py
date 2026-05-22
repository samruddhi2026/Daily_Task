from fastapi import APIRouter

from app.api.routes import health, metrics, model, predict, train, upload, reports

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(metrics.router)
api_v1_router.include_router(predict.router)
api_v1_router.include_router(train.router)
api_v1_router.include_router(upload.router)
api_v1_router.include_router(model.router)
api_v1_router.include_router(reports.router)

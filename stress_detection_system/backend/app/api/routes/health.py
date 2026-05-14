from fastapi import APIRouter, Depends

from app.api.deps import get_settings_dep
from app.config import Settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: Settings = Depends(get_settings_dep)) -> dict:
    return {
        "status": "ok",
        "project": settings.project_name,
        "version": settings.version,
    }

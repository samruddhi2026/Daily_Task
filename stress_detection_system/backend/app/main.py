from __future__ import annotations

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1_router import api_v1_router
from app.config import get_settings
from app.core.logger import configure_logging
from app.middleware.error_handler import register_exception_handlers

configure_logging()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000.0
        logger.bind(path=request.url.path, method=request.method, status=response.status_code).info(
            "request completed in {:.2f} ms", duration_ms
        )
        return response

    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    @app.get("/")
    def root() -> dict:
        return {
            "service": settings.project_name,
            "version": settings.version,
            "docs": "/docs",
            "api": settings.api_v1_prefix,
        }

    return app


app = create_app()

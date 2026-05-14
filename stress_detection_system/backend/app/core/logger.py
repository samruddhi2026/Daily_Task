import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger

from app.config import get_settings


def _json_sink(message: Any) -> None:
    record = message.record
    payload: Dict[str, Any] = {
        "time": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
    }
    if record["extra"]:
        payload["extra"] = dict(record["extra"])
    sys.stdout.write(json.dumps(payload, default=str) + "\n")


def configure_logging(log_json: Optional[bool] = None) -> None:
    """Configure Loguru: console sink, optional JSON, file rotation for errors."""
    settings = get_settings()
    use_json = settings.log_json if log_json is None else log_json

    logger.remove()
    if use_json:
        logger.add(_json_sink, level="INFO", enqueue=True)
    else:
        logger.add(
            sys.stderr,
            level="DEBUG" if settings.debug else "INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            enqueue=True,
        )

    logs_dir: Path = settings.logs_dir
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        str(logs_dir / "app_{time:YYYY-MM-DD}.log"),
        rotation="10 MB",
        retention="14 days",
        level="INFO",
        encoding="utf-8",
        enqueue=True,
    )
    logger.add(
        str(logs_dir / "errors_{time:YYYY-MM-DD}.log"),
        rotation="5 MB",
        retention="30 days",
        level="ERROR",
        encoding="utf-8",
        enqueue=True,
    )


def bind_request(request_id: str) -> Any:
    return logger.bind(request_id=request_id)

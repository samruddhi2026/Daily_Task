from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TrainRequest(BaseModel):
    tune: bool = Field(default=False, description="Enable lightweight hyperparameter search")
    max_windows: Optional[int] = Field(
        default=None,
        description="Optional cap on windows for faster experimentation",
        ge=10,
    )


class TrainResponse(BaseModel):
    status: str
    metrics: Dict[str, Any]

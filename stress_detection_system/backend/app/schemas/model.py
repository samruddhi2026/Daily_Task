from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ModelInfoResponse(BaseModel):
    best_model_path: str
    feature_pipeline_path: str
    metrics_path: str
    artifacts_present: bool
    feature_names: Optional[List[str]] = None
    model_name: Optional[str] = None

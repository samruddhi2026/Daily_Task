from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/generate")
def generate_report(data: List[Dict[str, Any]] = Body(...)) -> dict:
    """
    Generate an AI-driven stress report based on HR data using Gemini.
    """
    try:
        report = gemini_service.generate_stress_report(data)
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Health Check Routes
===================
Simple health monitoring endpoint
"""

from fastapi import APIRouter, status
from typing import Dict

router = APIRouter(tags=["health"])
logger_name = "HealthRoutes"


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint

    Returns:
    - status: Service status (ok)
    - message: Status message
    """
    return {
        "status": "ok",
        "message": "Study Buddy AI - Exam Service is running"
    }

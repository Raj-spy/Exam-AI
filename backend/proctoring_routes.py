from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_session
from .models import ProctoringEvent

router = APIRouter(prefix="/api", tags=["proctoring"])


@router.get("/proctoring-report/{exam_id}", response_model=List[dict])
async def get_report(exam_id: str, session: AsyncSession = Depends(get_session)):
    stmt = select(ProctoringEvent).where(ProctoringEvent.exam_id == exam_id).order_by(ProctoringEvent.timestamp)
    result = await session.execute(stmt)
    records = result.scalars().all()
    # convert to serializable dicts
    return [
        {
            "id": r.id,
            "exam_id": r.exam_id,
            "student_name": r.student_name,
            "event_type": r.event_type,
            "status": r.status,
            "suspicion_level": r.suspicion_level,
            "suspicion_score": r.suspicion_score,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in records
    ]

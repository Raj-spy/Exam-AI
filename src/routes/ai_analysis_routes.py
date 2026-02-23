"""AI analysis routes.

Provides an endpoint that accepts facial landmark data and returns a
classification following the format requested by the user.  This is a
simple wrapper around the logic living in :mod:`src.llm.ai_analysis`.
"""

from typing import List, Tuple

from fastapi import APIRouter
from pydantic import BaseModel

from src.llm.ai_analysis import analyze_face_landmarks

router = APIRouter(prefix="/api", tags=["ai"])


class Landmark(BaseModel):
    left_eye: Tuple[float, float]
    right_eye: Tuple[float, float]
    nose_tip: Tuple[float, float]


class FaceRequest(BaseModel):
    landmarks: List[Landmark]


class FaceResponse(BaseModel):
    status: str
    confidence: float
    suspicion_level: str


@router.post("/face-behavior", response_model=FaceResponse)
async def classify_face(request: FaceRequest) -> FaceResponse:
    """Endpoint for classifying student behaviour from face landmarks.

    Request example::

        {
            "landmarks": [
                {"left_eye": [0,0], "right_eye": [1,0], "nose_tip": [0.5,0]},
                ...
            ]
        }

    Returns JSON with ``status``, ``confidence`` and ``suspicion_level``.
    """
    # convert pydantic models to simple dicts for our analysis function
    landmark_dicts = [lm.dict() for lm in request.landmarks]
    return analyze_face_landmarks(landmark_dicts)

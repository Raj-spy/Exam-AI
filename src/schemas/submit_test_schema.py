"""
Submit Test Schema
==================
Pydantic model for exam submission
"""

from pydantic import BaseModel, Field
from typing import Dict


class SubmitTestSchema(BaseModel):
    """Schema for submitting test answers"""

    student_name: str = Field(..., min_length=1, max_length=100, description="Student's name")
    answers: Dict[int, str] = Field(
        ...,
        description="Dictionary of question_id -> answer mapping"
    )

    class Config:
        example = {
            "student_name": "John Doe",
            "answers": {
                0: "India",
                1: "Ashoka",
                2: "Option B"
            }
        }

"""
Create Test Schema
==================
Pydantic model for exam creation request
"""

from pydantic import BaseModel, Field
from typing import Optional


class CreateTestSchema(BaseModel):
    """Schema for creating a new test"""

    topic: str = Field(..., min_length=1, max_length=200, description="Topic for the exam")
    difficulty: str = Field(
        default="medium",
        description="Difficulty level: easy, medium, or hard"
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of questions (1-10)"
    )
    question_type: Optional[str] = Field(
        default="mcq",
        description="Type of questions: 'mcq' or 'fill_blank'"
    )

    class Config:
        example = {
            "topic": "Indian History",
            "difficulty": "medium",
            "num_questions": 5,
            "question_type": "mcq"
        }

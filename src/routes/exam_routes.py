"""
Exam Routes
===========
FastAPI endpoints for exam management:
- Create test (Teacher)
- Get exam questions (Student)
- Submit exam answers (Student)
- View results (Teacher/Admin)
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from src.schemas.create_test_schema import CreateTestSchema
from src.schemas.submit_test_schema import SubmitTestSchema
from src.exams.exam_service import ExamService
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

router = APIRouter(prefix="/api", tags=["exams"])
exam_service = ExamService()
logger = get_logger(__name__)


@router.post("/create-test", status_code=status.HTTP_201_CREATED)
async def create_test(request: CreateTestSchema) -> Dict[str, Any]:
    """
    Create a new exam with AI-generated questions

    **Teacher Endpoint**

    Request body:
    - topic: Subject topic (required)
    - difficulty: Easy, Medium, or Hard (optional, default: medium)
    - number_of_questions: 1-10 (optional, default: 5)
    - question_type: 'mcq' or 'fill_blank' (optional, default: mcq)

    Returns:
    - testId: Unique test identifier
    - totalQuestions: Number of questions generated
    - testLink: URL for students to access exam
    """
    try:
        logger.info(f"Creating test with topic: {request.topic}")

        result = exam_service.create_exam(
            topic=request.topic,
            difficulty=request.difficulty,
            num_questions=request.number_of_questions,
            question_type=request.question_type or "mcq"
        )

        return result

    except CustomException as e:
        logger.error(f"Custom exception in create_test: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_test: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/exam/{test_id}", status_code=status.HTTP_200_OK)
async def get_exam(test_id: str) -> Dict[str, Any]:
    """
    Retrieve exam questions for a student

    **Student Endpoint**

    Path parameters:
    - test_id: The unique test identifier

    Returns:
    - testId: Test identifier
    - topic: Subject topic
    - difficulty: Difficulty level
    - totalQuestions: Number of questions
    - questions: Array of questions (without correct answers)
    """
    try:
        logger.info(f"Fetching exam: {test_id}")

        result = exam_service.get_exam_questions(test_id)

        return result

    except CustomException as e:
        logger.error(f"Custom exception in get_exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/exam/{test_id}/submit", status_code=status.HTTP_200_OK)
async def submit_exam(test_id: str, request: SubmitTestSchema) -> Dict[str, Any]:
    """
    Submit exam answers and get instant evaluation

    **Student Endpoint**

    Path parameters:
    - test_id: The unique test identifier

    Request body:
    - student_name: Student's name (required)
    - answers: Dictionary of question_id -> answer (required)

    Returns:
    - studentName: Student's name
    - score: Score percentage (0-100)
    - correct: Number of correct answers
    - wrong: Number of wrong answers
    - totalAttempted: Total questions answered
    - status: PASSED or FAILED (>= 50% is PASSED)
    """
    try:
        logger.info(f"Submitting exam: {test_id} by student: {request.student_name}")

        result = exam_service.evaluate_exam(
            test_id=test_id,
            student_name=request.student_name,
            answers=request.answers
        )

        return result

    except CustomException as e:
        logger.error(f"Custom exception in submit_exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found or evaluation failed"
        )
    except Exception as e:
        logger.error(f"Unexpected error in submit_exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/exam/{test_id}/results", status_code=status.HTTP_200_OK)
async def get_results(test_id: str) -> Dict[str, Any]:
    """
    View all submissions and results for a test

    **Teacher/Admin Endpoint**

    Path parameters:
    - test_id: The unique test identifier

    Returns:
    - testId: Test identifier
    - totalSubmissions: Number of submissions
    - submissions: Array of all student submissions with scores
    """
    try:
        logger.info(f"Fetching results for exam: {test_id}")

        result = exam_service.get_exam_results(test_id)

        return result

    except Exception as e:
        logger.error(f"Error in get_results: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

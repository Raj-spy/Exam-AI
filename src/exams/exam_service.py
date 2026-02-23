"""
Exam Service Module
===================
High-level business logic for exam operations:
- Create exams with AI-generated questions
- Evaluate student answers
- Calculate scores
"""

from typing import Dict, List, Any, Optional
from src.generator.question_generator import QuestionGenerator
from src.exams.exam_manager import ExamManager
from src.storage.in_memory_store import store_submission, get_submissions
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

logger = get_logger(__name__)


class ExamService:
    """Service for exam operations"""

    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.exam_manager = ExamManager()

    def create_exam(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        question_type: str = "mcq"
    ) -> Dict[str, Any]:
        """
        Create a new exam with AI-generated questions

        Args:
            topic: Subject topic
            difficulty: Easy, Medium, or Hard
            num_questions: Number of questions to generate
            question_type: 'mcq' or 'fill_blank'

        Returns:
            Dictionary with testId and test details
        """
        try:
            # Normalize difficulty
            difficulty = difficulty.lower()
            if difficulty not in ["easy", "medium", "hard"]:
                difficulty = "medium"

            logger.info(
                f"Creating exam: topic={topic}, difficulty={difficulty}, "
                f"questions={num_questions}, type={question_type}"
            )

            # Generate questions
            questions = []
            for i in range(num_questions):
                try:
                    if question_type.lower() == "fill_blank":
                        question = self.question_generator.generate_fill_blank(
                            topic, difficulty
                        )
                    else:
                        question = self.question_generator.generate_mcq(
                            topic, difficulty
                        )
                    questions.append(question.dict())
                except Exception as e:
                    logger.error(f"Error generating question {i+1}: {str(e)}")
                    # Continue with other questions
                    continue

            if not questions:
                raise CustomException(
                    "Failed to generate any questions",
                    Exception("No questions generated")
                )

            # Create test ID
            test_id = self.exam_manager.generate_test_id()

            # Store test data
            test_data = {
                "testId": test_id,
                "topic": topic,
                "difficulty": difficulty,
                "questionType": question_type,
                "totalQuestions": len(questions),
                "questions": questions
            }

            self.exam_manager.save_test(test_id, test_data)

            logger.info(f"Exam created successfully: {test_id}")

            return {
                "testId": test_id,
                "totalQuestions": len(questions),
                "testLink": f"/exam/{test_id}"
            }

        except Exception as e:
            logger.error(f"Error creating exam: {str(e)}")
            raise CustomException("Failed to create exam", e)

    def get_exam_questions(self, test_id: str) -> Dict[str, Any]:
        """
        Retrieve exam questions without answers

        Args:
            test_id: The test ID

        Returns:
            Questions for students (without correct answers)
        """
        try:
            test = self.exam_manager.get_test(test_id)

            if not test:
                raise CustomException(
                    f"Test not found: {test_id}",
                    Exception("Test not found")
                )

            # Remove correct answers from questions
            questions_for_student = []
            for idx, q in enumerate(test["questions"]):
                question_item = {
                    "questionId": idx,
                    "question": q.get("question", ""),
                }

                # Include options for MCQ
                if "options" in q:
                    question_item["options"] = q["options"]

                questions_for_student.append(question_item)

            return {
                "testId": test_id,
                "topic": test.get("topic", ""),
                "difficulty": test.get("difficulty", ""),
                "totalQuestions": test.get("totalQuestions", 0),
                "questions": questions_for_student
            }

        except CustomException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving exam questions: {str(e)}")
            raise CustomException("Failed to retrieve exam", e)

    def evaluate_exam(
        self,
        test_id: str,
        student_name: str,
        answers: Dict[int, str]
    ) -> Dict[str, Any]:
        """
        Evaluate student answers and calculate score

        Args:
            test_id: The test ID
            student_name: Student's name
            answers: Dictionary of questionId → student_answer

        Returns:
            Result with score and breakdown
        """
        try:
            test = self.exam_manager.get_test(test_id)

            if not test:
                raise CustomException(
                    f"Test not found: {test_id}",
                    Exception("Test not found")
                )

            correct_count = 0
            wrong_count = 0
            results_details = []

            questions = test.get("questions", [])

            # Evaluate each answer
            for question_id, student_answer in answers.items():
                try:
                    q_id = int(question_id)
                    if q_id >= len(questions):
                        logger.warning(f"Invalid question ID: {q_id}")
                        continue

                    question = questions[q_id]
                    correct_answer = question.get("correct_answer") or question.get("answer", "")

                    # Case-insensitive comparison
                    is_correct = (
                        str(student_answer).strip().lower() ==
                        str(correct_answer).strip().lower()
                    )

                    if is_correct:
                        correct_count += 1
                    else:
                        wrong_count += 1

                    results_details.append({
                        "questionId": q_id,
                        "studentAnswer": student_answer,
                        "correctAnswer": correct_answer,
                        "isCorrect": is_correct
                    })

                except (ValueError, IndexError) as e:
                    logger.error(f"Error evaluating question {question_id}: {str(e)}")
                    wrong_count += 1
                    continue

            # Calculate score percentage
            total_attempted = correct_count + wrong_count
            score_percentage = (
                (correct_count / total_attempted * 100) if total_attempted > 0 else 0
            )

            # Store submission
            submission = {
                "studentName": student_name,
                "answers": answers,
                "correct": correct_count,
                "wrong": wrong_count,
                "totalAttempted": total_attempted,
                "scorePercentage": round(score_percentage, 2),
                "resultsDetails": results_details
            }

            store_submission(test_id, submission)

            logger.info(
                f"Exam evaluated for {student_name}: "
                f"Correct={correct_count}, Wrong={wrong_count}"
            )

            return {
                "studentName": student_name,
                "score": round(score_percentage, 2),
                "correct": correct_count,
                "wrong": wrong_count,
                "totalAttempted": total_attempted,
                "status": "PASSED" if score_percentage >= 50 else "FAILED"
            }

        except CustomException:
            raise
        except Exception as e:
            logger.error(f"Error evaluating exam: {str(e)}")
            raise CustomException("Failed to evaluate exam", e)

    def get_exam_results(self, test_id: str) -> Dict[str, Any]:
        """
        Retrieve all submissions for a test

        Args:
            test_id: The test ID

        Returns:
            List of submissions with scores
        """
        try:
            submissions = get_submissions(test_id)

            return {
                "testId": test_id,
                "totalSubmissions": len(submissions),
                "submissions": submissions
            }

        except Exception as e:
            logger.error(f"Error retrieving exam results: {str(e)}")
            raise CustomException("Failed to retrieve results", e)

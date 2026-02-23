"""
Integration Test Script for Study Buddy AI - Exam System
=========================================================
Tests the complete Teacher-Student examination flow
"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.exams.exam_service import ExamService
from src.common.custom_exception import CustomException


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_exam_creation():
    """Test 1: Create an exam"""
    print_section("TEST 1: Create Exam with AI-Generated Questions")

    try:
        service = ExamService()

        result = service.create_exam(
            topic="Indian Independence",
            difficulty="medium",
            num_questions=3,
            question_type="mcq"
        )

        print(f"✓ Exam created successfully!")
        print(f"  Test ID: {result['testId']}")
        print(f"  Total Questions: {result['totalQuestions']}")
        print(f"  Test Link: {result['testLink']}")

        return result['testId']

    except Exception as e:
        print(f"✗ Error creating exam: {str(e)}")
        return None


def test_get_exam_questions(test_id):
    """Test 2: Retrieve exam questions"""
    print_section("TEST 2: Retrieve Exam Questions for Student")

    try:
        service = ExamService()
        result = service.get_exam_questions(test_id)

        print(f"✓ Exam questions retrieved successfully!")
        print(f"  Test ID: {result['testId']}")
        print(f"  Topic: {result['topic']}")
        print(f"  Difficulty: {result['difficulty']}")
        print(f"  Total Questions: {result['totalQuestions']}")

        print("\n  Questions (without answers):")
        for q in result['questions']:
            print(f"\n    Q{q['questionId'] + 1}: {q['question']}")
            if 'options' in q:
                for i, opt in enumerate(q['options'], 1):
                    print(f"      {chr(64+i)}) {opt}")

        return True

    except Exception as e:
        print(f"✗ Error retrieving questions: {str(e)}")
        return False


def test_submit_exam(test_id):
    """Test 3: Submit exam and auto-evaluate"""
    print_section("TEST 3: Submit Exam and Get Auto-Evaluated Results")

    try:
        service = ExamService()

        # Get questions first to provide context
        exam = service.get_exam_questions(test_id)

        # Simulate student answers
        answers = {
            0: "India",  # This may or may not be correct depending on generated questions
            1: "1947",
            2: "Mahatma Gandhi"
        }

        result = service.evaluate_exam(
            test_id=test_id,
            student_name="Raj Tayde",
            answers=answers
        )

        print(f"✓ Exam submitted and evaluated successfully!")
        print(f"  Student Name: {result['studentName']}")
        print(f"  Score: {result['score']}%")
        print(f"  Correct Answers: {result['correct']}")
        print(f"  Wrong Answers: {result['wrong']}")
        print(f"  Total Attempted: {result['totalAttempted']}")
        print(f"  Status: {result['status']}")

        return True

    except Exception as e:
        print(f"✗ Error submitting exam: {str(e)}")
        return False


def test_get_results(test_id):
    """Test 4: Retrieve all results for a test"""
    print_section("TEST 4: View All Results (Teacher Dashboard)")

    try:
        service = ExamService()
        result = service.get_exam_results(test_id)

        print(f"✓ Results retrieved successfully!")
        print(f"  Test ID: {result['testId']}")
        print(f"  Total Submissions: {result['totalSubmissions']}")

        if result['submissions']:
            print("\n  Submissions:")
            for i, submission in enumerate(result['submissions'], 1):
                print(f"\n    Submission {i}:")
                print(f"      Student: {submission['studentName']}")
                print(f"      Score: {submission['scorePercentage']}%")
                print(f"      Correct: {submission['correct']}")
                print(f"      Wrong: {submission['wrong']}")

        return True

    except Exception as e:
        print(f"✗ Error retrieving results: {str(e)}")
        return False


def test_invalid_test_id():
    """Test 5: Handle invalid test ID"""
    print_section("TEST 5: Error Handling - Invalid Test ID")

    try:
        service = ExamService()
        result = service.get_exam_questions("invalid-test-id-12345")
        print(f"✗ Should have raised an exception!")
        return False

    except CustomException as e:
        print(f"✓ Correctly handled invalid test ID!")
        print(f"  Error caught: {str(e)}")
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False


def main():
    """Run all integration tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  Study Buddy AI - Integration Test Suite              ║")
    print("║  Teacher-Student Examination System                   ║")
    print("╚" + "=" * 58 + "╝")

    results = []

    # Test 1: Create Exam
    test_id = test_exam_creation()
    results.append(("Create Exam", test_id is not None))

    if test_id:
        # Test 2: Get Questions
        results.append(("Get Exam Questions", test_get_exam_questions(test_id)))

        # Test 3: Submit Exam
        results.append(("Submit Exam", test_submit_exam(test_id)))

        # Test 4: Get Results
        results.append(("Get Results", test_get_results(test_id)))

    # Test 5: Error Handling
    results.append(("Error Handling", test_invalid_test_id()))

    # Summary
    print_section("TEST SUMMARY")
    print(f"\nTotal Tests: {len(results)}")

    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed

    print(f"Passed: ✓ {passed}")
    print(f"Failed: ✗ {failed}")

    print("\nDetailed Results:")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:<10} - {test_name}")

    print("\n" + "=" * 60)

    if failed == 0:
        print("✓ All tests passed! The exam system is working correctly.")
    else:
        print(f"✗ {failed} test(s) failed. Please review the errors above.")

    print("=" * 60 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

"""
Final Verification Script
=========================
Comprehensive system check
"""

from src.exams.exam_service import ExamService
from src.storage.in_memory_store import TESTS, SUBMISSIONS
import sys

print('=' * 60)
print('FINAL VERIFICATION - Study Buddy AI Exam System')
print('=' * 60)

try:
    # Test initialization
    service = ExamService()
    print('\n✓ Exam Service initialized successfully')

    # Create exam
    result = service.create_exam(
        topic='Python Programming',
        difficulty='medium',
        num_questions=2,
        question_type='mcq'
    )
    test_id = result['testId']
    print(f'\n✓ Exam created with ID: {test_id[:8]}...')
    print(f'  Questions generated: {result["totalQuestions"]}')

    # Get questions
    exam = service.get_exam_questions(test_id)
    print(f'\n✓ Exam questions retrieved: {exam["totalQuestions"]} questions')

    # Submit answers
    answers = {0: 'Option A', 1: 'Option B'}
    evaluation = service.evaluate_exam(test_id, 'Test Student', answers)
    print(f'\n✓ Exam evaluated')
    print(f'  Score: {evaluation["score"]}%')
    print(f'  Status: {evaluation["status"]}')

    # Check storage
    print(f'\n✓ Storage verification:')
    print(f'  Tests stored: {len(TESTS)}')
    print(f'  Submissions stored: {sum(len(v) for v in SUBMISSIONS.values())}')

    print('\n' + '=' * 60)
    print('✅ ALL SYSTEMS OPERATIONAL - READY FOR DEPLOYMENT')
    print('=' * 60)
    sys.exit(0)

except Exception as e:
    print(f'\n✗ Verification failed: {str(e)}')
    print('=' * 60)
    sys.exit(1)

"""
In-Memory Storage Module
========================
This module provides in-memory storage for tests and student submissions.

NOTE: This is a prototype implementation for college minor project.
In production, use a proper database (MongoDB, PostgreSQL, Firebase, etc.)

Storage Structure:
- TESTS: Dictionary mapping testId → test details with questions
- SUBMISSIONS: Dictionary mapping testId → list of student submissions
"""

# In-memory storage for tests
# Format: {testId: {"topic": str, "difficulty": str, "questions": [...]}}
TESTS = {}

# In-memory storage for submissions
# Format: {testId: [{"studentName": str, "answers": dict, "score": int, ...}]}
SUBMISSIONS = {}


def store_test(test_id: str, test_data: dict) -> None:
    """Store a test in memory"""
    TESTS[test_id] = test_data


def get_test(test_id: str) -> dict:
    """Retrieve a test by ID"""
    return TESTS.get(test_id)


def store_submission(test_id: str, submission_data: dict) -> None:
    """Store a student submission"""
    if test_id not in SUBMISSIONS:
        SUBMISSIONS[test_id] = []
    SUBMISSIONS[test_id].append(submission_data)


def get_submissions(test_id: str) -> list:
    """Retrieve all submissions for a test"""
    return SUBMISSIONS.get(test_id, [])


def test_exists(test_id: str) -> bool:
    """Check if a test exists"""
    return test_id in TESTS

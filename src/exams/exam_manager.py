"""
Exam Manager Module
===================
Handles core exam operations: ID generation, test storage, retrieval.
"""

import uuid
from typing import Optional, Dict, Any
from src.storage.in_memory_store import store_test, get_test, test_exists
from src.common.logger import get_logger

logger = get_logger(__name__)


class ExamManager:
    """Manages exam lifecycle and storage"""

    @staticmethod
    def generate_test_id() -> str:
        """Generate a unique test ID using UUID"""
        return str(uuid.uuid4())

    @staticmethod
    def save_test(test_id: str, test_data: Dict[str, Any]) -> None:
        """Save test to in-memory storage"""
        try:
            store_test(test_id, test_data)
            logger.info(f"Test saved with ID: {test_id}")
        except Exception as e:
            logger.error(f"Error saving test: {str(e)}")
            raise

    @staticmethod
    def get_test(test_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve test by ID"""
        test = get_test(test_id)
        if test:
            logger.info(f"Test retrieved: {test_id}")
        else:
            logger.warning(f"Test not found: {test_id}")
        return test

    @staticmethod
    def test_exists(test_id: str) -> bool:
        """Check if test exists"""
        exists = test_exists(test_id)
        logger.info(f"Test exists check for {test_id}: {exists}")
        return exists

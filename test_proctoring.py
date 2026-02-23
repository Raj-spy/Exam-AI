"""Unit tests for the face behaviour classification logic."""

import sys
import os

# ensure project root is importable (same pattern as test_exam_system)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.llm.ai_analysis import analyze_face_landmarks

from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.ai_analysis_routes import router


# set up a minimal app for endpoint testing
_app = FastAPI()
_app.include_router(router)
_client = TestClient(_app)



def test_no_face_detected():
    result = analyze_face_landmarks([])
    assert result["status"] == "No Face Detected"
    assert result["confidence"] == 1.0
    assert result["suspicion_level"] == "medium"


def test_multiple_faces():
    # we don't even need realistic coords here, just more than one entry
    fake = {"left_eye": (0, 0), "right_eye": (1, 0), "nose_tip": (0.5, 0)}
    result = analyze_face_landmarks([fake, fake])
    assert result["status"] == "Multiple Faces Detected"
    assert result["suspicion_level"] == "high"
    assert result["confidence"] == 1.0


def test_focused():
    coords = {"left_eye": (0, 0), "right_eye": (1, 0), "nose_tip": (0.5, 0)}
    result = analyze_face_landmarks([coords])
    assert result["status"] == "Focused"
    assert result["suspicion_level"] == "low"
    assert 0.9 <= result["confidence"] <= 1.0


def test_looking_left():
    coords = {"left_eye": (0, 0), "right_eye": (1, 0), "nose_tip": (0.2, 0)}
    result = analyze_face_landmarks([coords])
    assert "Left" in result["status"]
    assert result["suspicion_level"] == "medium"


def test_looking_right():
    coords = {"left_eye": (0, 0), "right_eye": (1, 0), "nose_tip": (0.8, 0)}
    result = analyze_face_landmarks([coords])
    assert "Right" in result["status"]
    assert result["suspicion_level"] == "medium"


def test_looking_away():
    coords = {"left_eye": (0, 0), "right_eye": (1, 0), "nose_tip": (0.5, 0.5)}
    result = analyze_face_landmarks([coords])
    assert "Away" in result["status"]
    assert result["suspicion_level"] == "medium"


def test_endpoint_focus():
    # ensure the FastAPI route is wired correctly
    payload = {
        "landmarks": [
            {"left_eye": [0, 0], "right_eye": [1, 0], "nose_tip": [0.5, 0]}
        ]
    }
    resp = _client.post("/api/face-behavior", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "Focused"
    assert data["suspicion_level"] == "low"

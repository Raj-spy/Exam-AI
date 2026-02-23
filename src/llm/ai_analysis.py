
"""AI analysis utilities for the Study Buddy project.

Currently this module contains helpers that are used by the proctoring
and analysis features.  It started empty but the new proctoring
classification logic has been added here.
"""

from typing import List, Dict, Tuple


def analyze_face_landmarks(
    landmarks: List[Dict[str, Tuple[float, float]]]
) -> Dict[str, object]:
    """Classify student behaviour based on facial landmark data.

    The input ``landmarks`` is expected to be a list containing one
    dictionary per detected face.  Each dictionary should expose at
    least the keys ``left_eye``, ``right_eye`` and ``nose_tip``; their
    values are ``(x, y)`` tuples in a normalized coordinate space (e.g.
    0..1).  The function returns a JSON-like dictionary with the
    requested fields.

    Behaviour classification is intentionally simple so that it can be
    unit tested without depending on any external ML library.  A real
    implementation would obviously use a proper gaze estimator.

    Results
    -------
    A dictionary with the following keys:

    ``status``
        One of the labels the user specified in their request.
    ``confidence``
        A number between 0.0 and 1.0 expressing how confident the
        classifier is in the ``status``.
    ``suspicion_level``
        ``"low"`` for focused behaviour, ``"medium"`` for the three
        "looking" variants, and ``"high"`` when there are either no
        faces or more than one face detected.
    """

    # quick helpers --------------------------------------------------
    def _make(status: str, confidence: float, suspicion: str) -> Dict[str, object]:
        return {"status": status, "confidence": round(confidence, 2), "suspicion_level": suspicion}

    # no faces -------------------------------------------------------
    if not landmarks:
        return _make("No Face Detected", 1.0, "medium")

    # multiple faces -------------------------------------------------
    if len(landmarks) > 1:
        return _make("Multiple Faces Detected", 1.0, "high")

    face = landmarks[0]
    try:
        left_eye = face["left_eye"]
        right_eye = face["right_eye"]
        nose = face["nose_tip"]
    except KeyError:
        # missing data – treat as low confidence focused
        return _make("Focused", 0.4, "low")

    # compute a crude gaze direction using the nose relative to the
    # centre point between the eyes.  The thresholds are completely
    # heuristic; they exist just to make the tests deterministic.
    eye_cx = (left_eye[0] + right_eye[0]) / 2
    eye_cy = (left_eye[1] + right_eye[1]) / 2
    dx = nose[0] - eye_cx
    dy = nose[1] - eye_cy
    eye_dist = abs(right_eye[0] - left_eye[0]) or 1.0
    horiz_thresh = eye_dist * 0.15
    vert_thresh = eye_dist * 0.15

    if abs(dx) <= horiz_thresh and abs(dy) <= vert_thresh:
        return _make("Focused", 0.95, "low")

    # determine which axis dominates
    if abs(dx) >= abs(dy):
        if dx < 0:
            return _make("Looking Left (Suspicious)", 0.75, "medium")
        else:
            return _make("Looking Right (Suspicious)", 0.75, "medium")
    else:
        return _make("Looking Away (Suspicious)", 0.75, "medium")

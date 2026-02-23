from typing import List, Dict, Tuple


def analyze_face_landmarks(
    landmarks: List[Dict[str, Tuple[float, float]]]
) -> Dict[str, object]:
    """Classify student behaviour based on facial landmark data.

    See src/llm/ai_analysis for original description.  Logic is duplicated
    here for the backend proctoring service.
    """

    def _make(status: str, confidence: float, suspicion: str) -> Dict[str, object]:
        return {"status": status, "confidence": round(confidence, 2), "suspicion_level": suspicion}

    if not landmarks:
        return _make("No Face Detected", 1.0, "medium")
    if len(landmarks) > 1:
        return _make("Multiple Faces Detected", 1.0, "high")
    face = landmarks[0]
    try:
        left_eye = face["left_eye"]
        right_eye = face["right_eye"]
        nose = face["nose_tip"]
    except KeyError:
        return _make("Focused", 0.4, "low")
    eye_cx = (left_eye[0] + right_eye[0]) / 2
    eye_cy = (left_eye[1] + right_eye[1]) / 2
    dx = nose[0] - eye_cx
    dy = nose[1] - eye_cy
    eye_dist = abs(right_eye[0] - left_eye[0]) or 1.0
    horiz_thresh = eye_dist * 0.15
    vert_thresh = eye_dist * 0.15
    if abs(dx) <= horiz_thresh and abs(dy) <= vert_thresh:
        return _make("Focused", 0.95, "low")
    if abs(dx) >= abs(dy):
        if dx < 0:
            return _make("Looking Left (Suspicious)", 0.75, "medium")
        else:
            return _make("Looking Right (Suspicious)", 0.75, "medium")
    else:
        return _make("Looking Away (Suspicious)", 0.75, "medium")

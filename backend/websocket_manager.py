import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # mapping exam_id -> student_name -> websocket
        self.active_students_per_exam: Dict[str, Dict[str, WebSocket]] = {}
        # mapping exam_id -> list of teacher websockets
        self.active_teachers_per_exam: Dict[str, List[WebSocket]] = {}
        # per-student suspicion state
        self._scores: Dict[str, Dict[str, Any]] = {}  # exam_id -> student_name -> state
        self._lock = asyncio.Lock()

    async def connect_student(self, exam_id: str, student_name: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_students_per_exam.setdefault(exam_id, {})[student_name] = websocket
            self._scores.setdefault(exam_id, {}).setdefault(student_name, {
                "score": 0,
                "last_status": None,
                "last_status_change": datetime.utcnow(),
            })

    async def disconnect_student(self, exam_id: str, student_name: str):
        async with self._lock:
            self.active_students_per_exam.get(exam_id, {}).pop(student_name, None)
            # optionally remove scores
            self._scores.get(exam_id, {}).pop(student_name, None)

    async def connect_teacher(self, exam_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_teachers_per_exam.setdefault(exam_id, []).append(websocket)

    async def disconnect_teacher(self, exam_id: str, websocket: WebSocket):
        async with self._lock:
            sockets = self.active_teachers_per_exam.get(exam_id, [])
            if websocket in sockets:
                sockets.remove(websocket)

    async def broadcast_to_teachers(self, exam_id: str, message: Dict[str, Any]):
        # send to all connected teachers for this exam
        async with self._lock:
            socks = list(self.active_teachers_per_exam.get(exam_id, []))
        for ws in socks:
            try:
                await ws.send_json(message)
            except Exception:
                # ignore send failures
                pass

    # scoring helpers --------------------------------------------------
    async def update_score(self, exam_id: str, student_name: str, status: str) -> int:
        """Update stored score based on new status; return updated score."""
        async with self._lock:
            student_state = self._scores.setdefault(exam_id, {}).setdefault(student_name, {
                "score": 0,
                "last_status": None,
                "last_status_change": datetime.utcnow(),
            })
            score = student_state["score"]
            now = datetime.utcnow()

            # apply decay if continuous focus
            if status == "Focused":
                if student_state["last_status"] == "Focused":
                    elapsed = (now - student_state["last_status_change"]).total_seconds()
                    if elapsed >= 30:
                        score = max(score - 1, 0)
                        student_state["last_status_change"] = now
                else:
                    student_state["last_status_change"] = now
            else:
                student_state["last_status_change"] = now

            # scoring rules for events
            if status == "Focused":
                delta = 0
            elif status in ("Looking Left (Suspicious)", "Looking Right (Suspicious)", "Looking Away (Suspicious)"):
                delta = 3
            elif status == "No Face Detected":
                delta = 5
            elif status == "Multiple Faces Detected":
                delta = 8
            else:
                # for tab/blur events we'll call separate method
                delta = 0

            student_state["score"] = score + delta
            student_state["last_status"] = status
            return student_state["score"]

    async def add_penalty(self, exam_id: str, student_name: str, points: int) -> int:
        async with self._lock:
            student_state = self._scores.setdefault(exam_id, {}).setdefault(student_name, {
                "score": 0,
                "last_status": None,
                "last_status_change": datetime.utcnow(),
            })
            student_state["score"] += points
            return student_state["score"]

    async def get_score(self, exam_id: str, student_name: str) -> int:
        async with self._lock:
            return self._scores.get(exam_id, {}).get(student_name, {}).get("score", 0)


manager = ConnectionManager()
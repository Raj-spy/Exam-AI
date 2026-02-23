import asyncio
from datetime import datetime
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base, get_session
from .models import ProctoringEvent
from . import websocket_manager as manager_module
from .ai_analysis import analyze_face_landmarks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .proctoring_routes import router as proctoring_router
app.include_router(proctoring_router)


@app.on_event("startup")
async def startup_event():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.websocket("/ws/proctor/{exam_id}/{student_name}")
async def proctor_socket(websocket: WebSocket, exam_id: str, student_name: str):
    await manager_module.manager.connect_student(exam_id, student_name, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                continue

            event_type = payload.get("event_type")
            landmarks = payload.get("landmarks", [])
            # default values
            status = "Focused"
            confidence = 1.0
            suspicion_level = "low"

            if event_type == "face":
                result = analyze_face_landmarks(landmarks)
                status = result["status"]
                confidence = result.get("confidence", 1.0)
                suspicion_level = result.get("suspicion_level", "low")
                score = await manager_module.manager.update_score(exam_id, student_name, status)
            elif event_type == "tab_switch":
                score = await manager_module.manager.add_penalty(exam_id, student_name, 2)
            elif event_type == "window_blur":
                score = await manager_module.manager.add_penalty(exam_id, student_name, 2)
            else:
                # ignore unknown event types
                continue

            # determine suspicion_category based on score
            if score <= 5:
                suspicion_cat = "low"
            elif score <= 12:
                suspicion_cat = "medium"
            else:
                suspicion_cat = "high"

            ts = datetime.utcnow().isoformat()
            broadcast_payload = {
                "exam_id": exam_id,
                "student": student_name,
                "status": status,
                "confidence": confidence,
                "suspicion_level": suspicion_level,
                "suspicion_score": score,
                "timestamp": ts,
            }

            # send update to teachers
            await manager_module.manager.broadcast_to_teachers(exam_id, broadcast_payload)

            # log event except focused
            if status != "Focused" or event_type in ("tab_switch", "window_blur"):
                async with get_session() as session:
                    event = ProctoringEvent(
                        exam_id=exam_id,
                        student_name=student_name,
                        event_type=event_type,
                        status=status,
                        suspicion_level=suspicion_level,
                        suspicion_score=score,
                    )
                    session.add(event)
                    await session.commit()

    except WebSocketDisconnect:
        await manager_module.manager.disconnect_student(exam_id, student_name)


@app.websocket("/ws/teacher/{exam_id}")
async def teacher_socket(websocket: WebSocket, exam_id: str):
    await manager_module.manager.connect_teacher(exam_id, websocket)
    try:
        while True:
            # teacher doesn't send messages; just keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager_module.manager.disconnect_teacher(exam_id, websocket)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class ProctoringEvent(Base):
    __tablename__ = "proctoring_events"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(String, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # face/tab_switch/window_blur
    status = Column(String, nullable=False)
    suspicion_level = Column(String, nullable=False)
    suspicion_score = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

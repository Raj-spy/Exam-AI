"""
Study Buddy AI - FastAPI Application
=====================================
FastAPI backend for Teacher-Student Exam Management System

Features:
- Teacher creates exams with AI-generated questions
- Students attempt exams and get instant results
- In-memory storage (no database required)
- Supports MCQ and Fill-in-the-Blank questions
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import routes
from src.routes.exam_routes import router as exam_router
from src.routes.health import router as health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize FastAPI app
app = FastAPI(
    title="Study Buddy AI",
    description="Teacher-Student Examination System with AI Question Generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== ROOT ENDPOINTS ====================

@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {
        "service": "Study Buddy AI - Exam System",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }


# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# ==================== REGISTER ROUTES ====================

# Health check routes
app.include_router(health_router)

# Exam management routes
app.include_router(exam_router)


# ==================== STARTUP/SHUTDOWN EVENTS ====================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logging.info("=" * 50)
    logging.info("Study Buddy AI - Exam System Started")
    logging.info("=" * 50)
    logging.info("Available Endpoints:")
    logging.info("  - POST /api/create-test (Create exam)")
    logging.info("  - GET /api/exam/{testId} (Get exam questions)")
    logging.info("  - POST /api/exam/{testId}/submit (Submit answers)")
    logging.info("  - GET /api/exam/{testId}/results (View results)")
    logging.info("  - GET /health (Health check)")
    logging.info("  - GET /docs (Swagger UI)")
    logging.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logging.info("Study Buddy AI - Exam System Shutting Down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )

# Study Buddy AI - Examination System

## Overview

A FastAPI-based **Teacher-Student Online Examination System** with **AI-powered question generation** using LangChain + Groq API.

### Features
✅ **Teacher Dashboard**: Create exams with AI-generated MCQ & Fill-in-the-Blank questions  
✅ **Student Interface**: Attempt exams and get instant results  
✅ **Auto-Evaluation**: Automatic answer checking and score calculation  
✅ **In-Memory Storage**: No database required (college minor project prototype)  
✅ **REST API**: Complete REST endpoints for integration  
✅ **Swagger Documentation**: Interactive API docs at `/docs`

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  EXAM ROUTES    │  │  HEALTH ROUTES   │  │  SCHEMAS     │ │
│  │                 │  │                  │  │              │ │
│  │ POST /create... │  │ GET /health      │  │ Pydantic     │ │
│  │ GET /exam/{}    │  │                  │  │ Models       │ │
│  │ POST /exam/.../│  │                  │  │              │ │
│  │      submit     │  │                  │  │              │ │
│  │ GET /exam/.../  │  │                  │  │              │ │
│  │     results     │  │                  │  │              │ │
│  └────────┬────────┘  └──────────────────┘  └──────────────┘ │
│           │                                                   │
│  ┌────────▼──────────────────────────────────────┐           │
│  │          EXAM SERVICE LAYER                   │           │
│  │  - create_exam()                              │           │
│  │  - get_exam_questions()                       │           │
│  │  - evaluate_exam()                            │           │
│  │  - get_exam_results()                         │           │
│  └────────┬──────────────────┬───────────────────┘           │
│           │                  │                               │
│  ┌────────▼──────┐  ┌────────▼───────────┐                  │
│  │ EXAM MANAGER  │  │ QUESTION GENERATOR │                  │
│  │               │  │ (Existing)         │                  │
│  │ - generate_   │  │                    │                  │
│  │   test_id()   │  │ - generate_mcq()   │                  │
│  │ - save_test() │  │ - generate_fill_   │                  │
│  │ - get_test()  │  │   blank()          │                  │
│  └───────────────┘  └────────┬───────────┘                  │
│                               │                               │
│                  ┌────────────▼────────────┐                 │
│                  │ GROQ LLM API (Llama)   │                 │
│                  │ (Existing)              │                 │
│                  └─────────────────────────┘                 │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │    IN-MEMORY STORAGE (No Database)         │             │
│  │                                             │             │
│  │  TESTS = {}          # Test data           │             │
│  │  SUBMISSIONS = {}    # Student submissions │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
study-buddy-ai/
├── src/
│   ├── exams/
│   │   ├── __init__.py
│   │   ├── exam_manager.py       # Core exam operations
│   │   └── exam_service.py       # High-level exam logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── exam_routes.py        # Exam endpoints
│   │   └── health.py             # Health check
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── create_test_schema.py  # Pydantic request model
│   │   └── submit_test_schema.py  # Pydantic request model
│   ├── storage/
│   │   ├── __init__.py
│   │   └── in_memory_store.py    # In-memory storage functions
│   ├── generator/
│   │   └── question_generator.py # (Existing - AI question gen)
│   ├── llm/
│   │   └── groq_client.py        # (Existing - LLM client)
│   ├── models/
│   │   └── question_schemas.py   # (Existing - Pydantic schemas)
│   ├── config/
│   │   └── settings.py           # (Existing - App config)
│   ├── common/
│   │   ├── logger.py             # (Existing - Logging)
│   │   └── custom_exception.py   # (Existing - Exceptions)
│   └── utils/
│       └── helpers.py            # (Existing - Utilities)
├── fastapi_app.py               # Main FastAPI application
├── application.py               # (Existing - Streamlit app)
├── requirements.txt
├── README.md
└── test_exam_system.py           # Integration tests
```

---

## API Endpoints

### 1️⃣ Create Exam (Teacher)

**Endpoint**: `POST /api/create-test`

**Description**: Create a new exam with AI-generated questions

**Request Body**:
```json
{
  "topic": "Indian History",
  "difficulty": "medium",
  "number_of_questions": 5,
  "question_type": "mcq"
}
```

**Parameters**:
- `topic` (string, required): Subject topic
- `difficulty` (string, optional): "easy", "medium", or "hard" (default: "medium")
- `number_of_questions` (integer, optional): 1-10 (default: 5)
- `question_type` (string, optional): "mcq" or "fill_blank" (default: "mcq")

**Response** (201 Created):
```json
{
  "testId": "3eb97b15-4463-46c9-9d46-88b239c33209",
  "totalQuestions": 5,
  "testLink": "/exam/3eb97b15-4463-46c9-9d46-88b239c33209"
}
```

---

### 2️⃣ Get Exam Questions (Student)

**Endpoint**: `GET /api/exam/{testId}`

**Description**: Retrieve exam questions without correct answers

**Path Parameters**:
- `testId` (string): Unique test identifier

**Response** (200 OK):
```json
{
  "testId": "3eb97b15-4463-46c9-9d46-88b239c33209",
  "topic": "Indian History",
  "difficulty": "medium",
  "totalQuestions": 3,
  "questions": [
    {
      "questionId": 0,
      "question": "Who led the Dandi March in 1930?",
      "options": [
        "Mahatma Gandhi",
        "Jawaharlal Nehru",
        "Subhas Chandra Bose",
        "Sardar Vallabhbhai Patel"
      ]
    },
    {
      "questionId": 1,
      "question": "In what year did India gain independence?",
      "options": [
        "1945",
        "1947",
        "1950",
        "1952"
      ]
    }
  ]
}
```

---

### 3️⃣ Submit Exam & Get Results (Student)

**Endpoint**: `POST /api/exam/{testId}/submit`

**Description**: Submit answers and get instant evaluation

**Path Parameters**:
- `testId` (string): Unique test identifier

**Request Body**:
```json
{
  "student_name": "Raj Tayde",
  "answers": {
    "0": "Mahatma Gandhi",
    "1": "1947",
    "2": "Ashoka"
  }
}
```

**Response** (200 OK):
```json
{
  "studentName": "Raj Tayde",
  "score": 66.67,
  "correct": 2,
  "wrong": 1,
  "totalAttempted": 3,
  "status": "PASSED"
}
```

---

### 4️⃣ View Exam Results (Teacher/Admin)

**Endpoint**: `GET /api/exam/{testId}/results`

**Description**: View all submissions and results for a test

**Path Parameters**:
- `testId` (string): Unique test identifier

**Response** (200 OK):
```json
{
  "testId": "3eb97b15-4463-46c9-9d46-88b239c33209",
  "totalSubmissions": 2,
  "submissions": [
    {
      "studentName": "Raj Tayde",
      "answers": {
        "0": "Mahatma Gandhi",
        "1": "1947"
      },
      "correct": 2,
      "wrong": 0,
      "totalAttempted": 2,
      "scorePercentage": 100.0,
      "resultsDetails": [
        {
          "questionId": 0,
          "studentAnswer": "Mahatma Gandhi",
          "correctAnswer": "Mahatma Gandhi",
          "isCorrect": true
        }
      ]
    }
  ]
}
```

---

### 5️⃣ Health Check

**Endpoint**: `GET /health`

**Description**: Check if the service is running

**Response** (200 OK):
```json
{
  "status": "ok",
  "message": "Study Buddy AI - Exam Service is running"
}
```

---

## Running the Application

### Prerequisites
- Python 3.8+
- Virtual environment activated
- Environment variables configured (`.env` file with `GROQ_API_KEY`)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Start FastAPI Server

```bash
# Using Uvicorn directly
python fastapi_app.py

# Or using uvicorn command
uvicorn fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Running Integration Tests

```bash
python test_exam_system.py
```

**Expected Output**:
```
╔══════════════════════════════════════════════════════════╗
║  Study Buddy AI - Integration Test Suite              ║
║  Teacher-Student Examination System                   ║
╚══════════════════════════════════════════════════════════╝

✓ Test 1: Create Exam
✓ Test 2: Get Exam Questions
✓ Test 3: Submit Exam and Get Auto-Evaluated Results
✓ Test 4: View All Results (Teacher Dashboard)
✓ Test 5: Error Handling - Invalid Test ID

============================================================
✓ All tests passed! The exam system is working correctly.
============================================================
```

---

## Example Workflow

### Step 1: Teacher Creates an Exam
```bash
curl -X POST http://localhost:8000/api/create-test \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Indian Independence",
    "difficulty": "medium",
    "number_of_questions": 3
  }'
```

### Step 2: Share Test Link with Students
```
Test Link: http://localhost:8000/exam/3eb97b15-4463-46c9-9d46-88b239c33209
```

### Step 3: Student Retrieves Questions
```bash
curl http://localhost:8000/api/exam/3eb97b15-4463-46c9-9d46-88b239c33209
```

### Step 4: Student Submits Answers
```bash
curl -X POST http://localhost:8000/api/exam/3eb97b15-4463-46c9-9d46-88b239c33209/submit \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Raj Tayde",
    "answers": {
      "0": "Mahatma Gandhi",
      "1": "1947",
      "2": "Option A"
    }
  }'
```

### Step 5: Teacher Views Results
```bash
curl http://localhost:8000/api/exam/3eb97b15-4463-46c9-9d46-88b239c33209/results
```

---

## In-Memory Storage Details

### TESTS Dictionary
```python
{
  "testId": {
    "testId": "3eb97b15-...",
    "topic": "Indian History",
    "difficulty": "medium",
    "questionType": "mcq",
    "totalQuestions": 3,
    "questions": [
      {
        "question": "...",
        "options": [...],
        "correct_answer": "..."
      }
    ]
  }
}
```

### SUBMISSIONS Dictionary
```python
{
  "testId": [
    {
      "studentName": "Raj Tayde",
      "answers": {"0": "...", "1": "..."},
      "correct": 2,
      "wrong": 1,
      "totalAttempted": 3,
      "scorePercentage": 66.67,
      "resultsDetails": [...]
    }
  ]
}
```

---

## Error Handling

The system gracefully handles errors:

| Error | Status Code | Response |
|-------|------------|----------|
| Test not found | 404 | `{"detail": "Exam not found"}` |
| Invalid input | 400 | `{"detail": "Validation error"}` |
| Server error | 500 | `{"detail": "Internal server error"}` |
| Invalid question format | 400 | `{"detail": "Failed to create exam"}` |

---

## Limitations & Future Scope

### Current Limitations (Prototype)
- ❌ No persistent database (data lost on server restart)
- ❌ No user authentication
- ❌ No file uploads for questions
- ❌ Single-server only (no clustering)

### Future Enhancements
- ✅ Integrate MongoDB or PostgreSQL
- ✅ JWT authentication for teachers/students
- ✅ Question bank management
- ✅ Real-time student progress dashboard
- ✅ Email notifications
- ✅ Mobile app integration
- ✅ Analytics and performance tracking

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **Server** | Uvicorn |
| **LLM** | Groq API (Llama 3.1 8B) |
| **LangChain** | LLM orchestration |
| **Storage** | In-Memory Python Dicts |
| **API Schema** | Pydantic |
| **Logging** | Python logging module |

---

## Code Quality

✅ Clean, readable, and well-commented code  
✅ Proper error handling and validation  
✅ Type hints for all functions  
✅ Comprehensive docstrings  
✅ Integration tests included  
✅ Follows PEP 8 style guidelines

---

## Support

For issues or questions:
1. Check the integration tests: `test_exam_system.py`
2. Review API documentation: `/docs` endpoint
3. Check logs for error messages

---

## License

College minor project - Study Buddy AI

---

**Last Updated**: December 26, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready (Prototype)

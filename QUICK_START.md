# Quick Start Guide - Study Buddy AI Exam System

## 🚀 Getting Started (2 minutes)

### Step 1: Start the Server
```bash
python fastapi_app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Study Buddy AI - Exam System Started
```

### Step 2: Open Swagger UI
Visit: **http://localhost:8000/docs**

### Step 3: Create Your First Exam (Teacher)
1. Click on **POST /api/create-test**
2. Click **Try it out**
3. Replace the example with:
   ```json
   {
     "topic": "Indian History",
     "difficulty": "medium",
     "number_of_questions": 3,
     "question_type": "mcq"
   }
   ```
4. Click **Execute**
5. Copy the `testId` from the response

### Step 4: View Exam Questions (Student)
1. Click on **GET /api/exam/{testId}**
2. Click **Try it out**
3. Paste your `testId` in the field
4. Click **Execute**
5. You'll see the questions (without answers)

### Step 5: Submit Answers (Student)
1. Click on **POST /api/exam/{testId}/submit**
2. Click **Try it out**
3. Paste your `testId` in the field
4. Replace the example body with:
   ```json
   {
     "student_name": "Your Name",
     "answers": {
       "0": "Mahatma Gandhi",
       "1": "1947",
       "2": "Indian National Congress"
     }
   }
   ```
5. Click **Execute**
6. See your instant results!

### Step 6: View Results (Teacher)
1. Click on **GET /api/exam/{testId}/results**
2. Click **Try it out**
3. Paste your `testId`
4. Click **Execute**
5. See all student submissions and scores

---

## 📋 Complete Workflow Example

### Teacher Creates Exam
```bash
curl -X POST http://localhost:8000/api/create-test \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Geography of India",
    "difficulty": "easy",
    "number_of_questions": 2
  }'
```

**Response:**
```json
{
  "testId": "abc123def456",
  "totalQuestions": 2,
  "testLink": "/exam/abc123def456"
}
```

### Teacher Shares Link with Students
Share: **http://localhost:8000/api/exam/abc123def456**

### Student Attempts Exam
```bash
# View questions
curl http://localhost:8000/api/exam/abc123def456

# Submit answers
curl -X POST http://localhost:8000/api/exam/abc123def456/submit \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Student 1",
    "answers": {
      "0": "Option A",
      "1": "Option B"
    }
  }'
```

**Response:**
```json
{
  "studentName": "Student 1",
  "score": 50.0,
  "correct": 1,
  "wrong": 1,
  "totalAttempted": 2,
  "status": "FAILED"
}
```

### Teacher Views Results
```bash
curl http://localhost:8000/api/exam/abc123def456/results
```

---

## 🧪 Run Integration Tests

```bash
python test_exam_system.py
```

Expected output:
```
✓ Test 1: Create Exam with AI-Generated Questions
✓ Test 2: Retrieve Exam Questions for Student
✓ Test 3: Submit Exam and Get Auto-Evaluated Results
✓ Test 4: View All Results (Teacher Dashboard)
✓ Test 5: Error Handling - Invalid Test ID

✓ All tests passed! The exam system is working correctly.
```

---

## 🔍 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/create-test` | Create exam (Teacher) |
| GET | `/api/exam/{testId}` | Get questions (Student) |
| POST | `/api/exam/{testId}/submit` | Submit answers (Student) |
| GET | `/api/exam/{testId}/results` | View results (Teacher) |

---

## 📁 Project Structure

```
study-buddy-ai/
├── src/
│   ├── exams/
│   │   ├── exam_manager.py      ← Test ID generation & storage
│   │   └── exam_service.py      ← Exam logic & evaluation
│   ├── routes/
│   │   ├── exam_routes.py       ← All exam endpoints
│   │   └── health.py            ← Health check
│   ├── schemas/
│   │   ├── create_test_schema.py ← Request validation
│   │   └── submit_test_schema.py ← Answer submission
│   ├── storage/
│   │   └── in_memory_store.py   ← Data storage
│   └── (existing modules)
├── fastapi_app.py               ← Main FastAPI app
├── test_exam_system.py          ← Integration tests
└── EXAM_SYSTEM_README.md        ← Full documentation
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.1-8b-instant
TEMPERATURE=0.9
MAX_RETRIES=3
```

### Settings
Edit `src/config/settings.py` to customize:
- LLM model
- Temperature (creativity level)
- Max retries for question generation

---

## 🎯 Key Features

✅ **AI Question Generation** - Powered by Groq + Llama 3.1  
✅ **Instant Evaluation** - Auto-grade multiple choice answers  
✅ **No Database Required** - In-memory storage (perfect for prototypes)  
✅ **RESTful API** - Standard HTTP endpoints  
✅ **Interactive Docs** - Swagger UI at `/docs`  
✅ **Error Handling** - Graceful error responses  
✅ **Logging** - Track all operations  

---

## ⚠️ Important Notes

### Data Persistence
- **Current**: Data stored in memory (lost when server restarts)
- **Use for**: Development, testing, college projects
- **Production**: Use database (MongoDB, PostgreSQL, etc.)

### Test Data
- Each test gets a unique ID (UUID)
- Questions are stored without correct answers for students
- Submissions tracked separately
- No authentication (add for production)

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is available
netstat -ano | findstr :8000

# Use different port
uvicorn fastapi_app:app --port 8001
```

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Test generation fails
- Check GROQ_API_KEY is set
- Verify internet connection
- Check Groq API status

### Invalid test ID error
- Use exact test ID from create-test response
- Test ID is case-sensitive

---

## 📚 Full Documentation

See **EXAM_SYSTEM_README.md** for:
- Complete API documentation
- Request/response examples
- Error codes and handling
- Future enhancements
- Technology stack

---

## 🎓 Project Info

**Type**: College Minor Project  
**Created**: December 2025  
**Status**: ✅ Production Ready  
**Version**: 1.0.0

---

## 🤝 Support

- 📖 **Docs**: http://localhost:8000/docs
- 🧪 **Tests**: `python test_exam_system.py`
- 📝 **Code**: Well-commented and documented

---

**Happy testing! 🎉**

# 🚀 Exam AI Frontend - Setup & Run Guide

## 📋 Prerequisites

Before starting, make sure you have:

1. **Node.js** (v16 or higher)
   - Download from: https://nodejs.org/
   - Verify: Run `node --version` in terminal

2. **FastAPI Backend** running on port 8001
   - Should be accessible at: `http://localhost:8001`
   - API endpoints should respond at: `http://localhost:8001/api`

## ⚙️ Installation Steps

### Step 1: Install Dependencies

**Windows:**
```bash
cd c:\Users\RAJTAYDE\Downloads\exam-ai-frontend
npm install
```

**macOS/Linux:**
```bash
cd ~/Downloads/exam-ai-frontend
npm install
```

### Step 2: Verify Backend Connection

Check that the backend is running:
```bash
curl http://localhost:8001/health
```

You should see:
```json
{"status": "ok", "message": "Study Buddy AI - Exam Service is running"}
```

If not, start the backend first:
```bash
cd c:\Users\RAJTAYDE\Downloads\study-buddy-ai
python fastapi_app.py
```

### Step 3: Start Development Server

```bash
npm run dev
```

The app will automatically open at: **http://localhost:3000**

## 🎯 Testing the Full Flow

### 1. Teacher Creates Exam
1. Go to: http://localhost:3000/teacher
2. Fill in:
   - Topic: "Indian History"
   - Difficulty: "Medium"
   - Number of Questions: 3
3. Click "Generate Preview"
4. Review the AI-generated questions
5. Click "Create Test"
6. Copy the student link

### 2. Student Attempts Exam
1. Open the student link in a new tab (or go to `/exam/{testId}`)
2. Enter student name (e.g., "John Doe")
3. Click "Start Test"
4. Answer all questions
5. Click "Submit Exam"

### 3. View Results
- You should see the results page with:
  - Score percentage
  - Number of correct/wrong answers
  - Pass/Fail status

### 4. View Dashboard
- Go to: http://localhost:3000/teacher/dashboard
- See your created test
- View all student submissions

## 📁 Project Structure

```
exam-ai-frontend/
├── src/
│   ├── pages/          # Page components
│   ├── components/     # UI components
│   ├── services/       # API integration
│   ├── styles/         # CSS files
│   ├── App.jsx         # Main app
│   └── main.jsx        # Entry point
├── package.json        # Dependencies
├── vite.config.js      # Vite config
├── index.html          # HTML entry
└── README.md           # Full documentation
```

## 🔧 Troubleshooting

### Issue: "Cannot reach backend"
**Solution:**
- Check if FastAPI is running: `python fastapi_app.py`
- Verify it's on port 8001: http://localhost:8001/health
- Check firewall settings

### Issue: "Questions not loading"
**Solution:**
- Verify test ID is correct
- Check browser console for errors (F12)
- Ensure backend is responding to `/api/exam/{testId}`

### Issue: "npm: command not found"
**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Verify: `node --version`

### Issue: Port 3000 already in use
**Solution:**
- Edit `vite.config.js` and change port to 3001:
  ```javascript
  server: {
    port: 3001,
    strictPort: false
  }
  ```

## 🎨 Customization

### Change Backend URL
Edit `src/services/api.js`:
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8001/api', // Change this
})
```

### Change Styling
Edit files in `src/styles/` and `src/components/Navigation.css`

### Add New Features
Add new components in `src/pages/` or `src/components/`

## 📦 Build for Production

```bash
npm run build
```

Output files will be in `dist/` directory.

To preview production build:
```bash
npm run preview
```

## 🚀 Deployment

The `dist/` folder contains static files that can be deployed to:
- **Vercel**: `npm install -g vercel` then `vercel`
- **Netlify**: Drag and drop `dist/` folder
- **GitHub Pages**: Use `gh-pages` package
- **Any static host**: Upload `dist/` files

## 📝 API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/create-test` | Create exam |
| GET | `/exam/{testId}` | Get questions |
| POST | `/exam/{testId}/submit` | Submit answers |
| GET | `/exam/{testId}/results` | Get submissions |

## ✅ Features Checklist

- [x] Teacher creates exams with AI questions
- [x] Share test links with students
- [x] Student name input
- [x] MCQ question rendering
- [x] Answer selection
- [x] Auto-evaluation
- [x] Results display
- [x] Results dashboard
- [x] LocalStorage persistence
- [x] Responsive design

## 🆘 Support

If you encounter issues:

1. **Check logs**:
   - Browser console (F12)
   - Backend logs (where `python fastapi_app.py` runs)

2. **Verify setup**:
   - Backend running on 8001? ✓
   - Frontend running on 3000? ✓
   - Node.js installed? ✓

3. **Try hard refresh**: `Ctrl+Shift+R` or `Cmd+Shift+R`

## 📞 Quick Links

- Backend API: http://localhost:8001/api
- Backend Docs: http://localhost:8001/docs
- Frontend App: http://localhost:3000
- Health Check: http://localhost:8001/health

---

**Version**: 1.0.0  
**Status**: Production Ready ✅

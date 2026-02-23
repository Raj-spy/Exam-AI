# Exam AI - React Frontend

A complete React frontend for the Exam AI system that connects to the FastAPI backend.

## 📋 Features

✅ **Teacher Dashboard** - Create exams with AI-generated questions  
✅ **Student Exam Interface** - Attempt exams and submit answers  
✅ **Instant Results** - Auto-evaluated scores  
✅ **Result History** - View submissions and results  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **LocalStorage** - Stores exam data locally

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- FastAPI backend running on `http://localhost:8001`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
exam-ai-frontend/
├── src/
│   ├── pages/
│   │   ├── TeacherCreateTest.jsx     # Create exam page
│   │   ├── StudentExam.jsx           # Take exam page
│   │   ├── ResultPage.jsx            # View results
│   │   └── TeacherDashboard.jsx      # Dashboard
│   ├── components/
│   │   └── Navigation.jsx            # Top navigation
│   ├── services/
│   │   └── api.js                    # Axios API client
│   ├── styles/
│   │   ├── pages.css                 # Page styles
│   │   └── Navigation.css
│   ├── App.jsx                       # Main app
│   ├── App.css
│   ├── index.css                     # Global styles
│   └── main.jsx                      # Entry point
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 🔗 Routes

| Route | Component | Purpose |
|-------|-----------|---------|
| `/teacher` | TeacherCreateTest | Create exams |
| `/exam/:testId` | StudentExam | Take exam |
| `/result` | ResultPage | View results |
| `/teacher/dashboard` | TeacherDashboard | View submissions |

## 🌐 API Integration

The frontend connects to the FastAPI backend at `http://localhost:8001/api`:

- `POST /create-test` - Create exam
- `GET /exam/{testId}` - Get exam questions
- `POST /exam/{testId}/submit` - Submit answers
- `GET /exam/{testId}/results` - Get submissions

## 💾 LocalStorage Usage

The app uses `localStorage` to store:
- `lastCreatedTest` - Recently created test info
- `examResult` - Last exam result

## 🎨 Styling

- Pure CSS (no UI libraries)
- Responsive design with media queries
- Modern gradient backgrounds
- Clean and simple UI

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## 🛠️ Build for Production

```bash
npm run build
```

Output files will be in the `dist/` directory.

## 📝 Key Components

### TeacherCreateTest
- Input exam configuration
- Generate preview questions
- Create test and get shareable link

### StudentExam
- Enter student name
- View exam questions
- Select answers
- Submit exam

### ResultPage
- Display score and statistics
- Show correct/wrong counts
- Display pass/fail status

### TeacherDashboard
- View created tests
- See student submissions
- Monitor statistics

## ⚙️ Configuration

Edit `src/services/api.js` to change the backend URL:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8001/api', // Change this
})
```

## 🐛 Troubleshooting

### "Cannot reach backend"
- Ensure FastAPI server is running on port 8001
- Check CORS settings in backend

### Questions not loading
- Verify test ID is correct
- Check backend logs

### Styles not applying
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)

## 📚 Technology Stack

- **React 18** - UI library
- **React Router 6** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **CSS3** - Styling

## 🤝 Features

✅ Create exams with AI questions  
✅ Share test links with students  
✅ Auto-evaluate answers  
✅ Instant results  
✅ View student submissions  
✅ Responsive design  
✅ LocalStorage data persistence  

## 📄 License

College Minor Project - Exam AI

---

**Version**: 1.0.0  
**Status**: Production Ready ✅

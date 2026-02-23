import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import TeacherCreateTest from './pages/TeacherCreateTest'
import StudentExam from './pages/StudentExam'
import ResultPage from './pages/ResultPage'
import TeacherDashboard from './pages/TeacherDashboard'
import TeacherMonitor from './pages/TeacherMonitor'
import Navigation from './components/Navigation'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>

        {/* Home → Teacher */}
        <Route path="/" element={<Navigate to="/teacher" replace />} />

        {/* TEACHER ROUTES (WITH NAVIGATION) */}
        <Route
          path="/teacher"
          element={
            <>
              <Navigation />
              <TeacherCreateTest />
            </>
          }
        />

        <Route
          path="/teacher/dashboard"
          element={
            <>
              <Navigation />
              <TeacherDashboard />
            </>
          }
        />
        <Route
          path="/teacher/monitor/:testId"
          element={
            <>
              <Navigation />
              <TeacherMonitor />
            </>
          }
        />

        {/* STUDENT ROUTES (NO NAVIGATION) */}
        <Route path="/exam/:testId" element={<StudentExam />} />
        <Route path="/result" element={<ResultPage />} />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />

      </Routes>
    </Router>
  )
}

function NotFound() {
  return (
    <div className="container">
      <div className="error-state">
        <h2>404 - Page Not Found</h2>
        <p>The page you are looking for does not exist.</p>
      </div>
    </div>
  )
}

export default App

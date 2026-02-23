/**
 * Navigation Component
 * ===================
 * Top navigation bar for the application
 */

import { Link, useLocation } from 'react-router-dom'
import './Navigation.css'

export default function Navigation() {
  const location = useLocation()

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/')

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          🎓 Exam AI
        </Link>
        
        <div className="nav-menu">
          <Link
            to="/teacher"
            className={`nav-link ${isActive('/teacher') ? 'active' : ''}`}
          >
            👨‍🏫 Teacher
          </Link>
          <Link
            to="/teacher/dashboard"
            className={`nav-link ${isActive('/teacher/dashboard') ? 'active' : ''}`}
          >
            📊 Dashboard
          </Link>
        </div>
      </div>
    </nav>
  )
}

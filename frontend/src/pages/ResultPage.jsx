/**
 * ResultPage Component
 * ====================
 * Display exam results after student submission
 * 
 * Features:
 * - Show student name
 * - Display score percentage
 * - Show correct and wrong answers count
 * - Display pass/fail status
 * - Option to retake exam or go home
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/pages.css'

export default function ResultPage() {
  const navigate = useNavigate()
  const [result, setResult] = useState(null)

  useEffect(() => {
    const savedResult = localStorage.getItem('examResult')
    if (savedResult) {
      setResult(JSON.parse(savedResult))
    }
  }, [])

  // Student flow is isolated: no navigation to teacher/home allowed from result page.
  // We intentionally do not provide navigation that redirects to teacher or home.

  if (!result) {
    return (
      <div className="container">
        <div className="error-state">
          <h2>❌ No Results Found</h2>
          <p>There are no exam results to display.</p>
        </div>
      </div>
    )
  }

  const isPassed = result.status === 'PASSED'

  return (
    <div className="container">
      {/* Left Sidebar */}
      <div className="sidebar-panel">
        <div className="sidebar-section">
          <h3>Result</h3>
          <div style={{ padding: '1rem', background: '#f9f9f9', border: '1px solid #ddd', borderRadius: '0' }}>
            <p style={{ fontSize: '0.9rem', color: '#666', margin: '0.5rem 0' }}>
              <strong>Status:</strong> {isPassed ? 'Passed' : 'Failed'}
            </p>
            <p style={{ fontSize: '1.5rem', fontWeight: '700', color: isPassed ? '#2e7d32' : '#d32f2f', margin: '1rem 0 0 0' }}>
              {Math.round(result.score)}%
            </p>
          </div>
        </div>

        
      </div>

      {/* Center Content */}
      <div className="content-area">
        
        {/* Student flow: show static confirmation instead of navigation */}

        <div className="content-wrapper">
          <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#e8f5e9', border: '1px solid #c8e6c9', textAlign: 'center' }}>
            <strong>Test completed successfully.</strong>
          </div>
          <div className="result-status">
            <h2 className={`${isPassed ? 'passed' : 'failed'}`} style={{ color: isPassed ? '#2e7d32' : '#d32f2f', textAlign: 'center' }}>
              {isPassed ? 'PASSED' : 'FAILED'}
            </h2>
          </div>

          <div className="score-display">
            <div className="score-box">
              <div className="score-value">{Math.round(result.score)}%</div>
              <div className="score-label">Score</div>
            </div>
          </div>

          <div className="result-details">
            <div className="result-row">
              <span className="result-label">Student</span>
              <span className="result-value">{result.studentName}</span>
            </div>

            <div className="result-row">
              <span className="result-label">Total Questions</span>
              <span className="result-value">{result.totalAttempted}</span>
            </div>

            <div className="result-row">
              <span className="result-label">Correct</span>
              <span className="result-value" style={{ color: '#2e7d32' }}>{result.correct}</span>
            </div>

            <div className="result-row">
              <span className="result-label">Wrong</span>
              <span className="result-value" style={{ color: '#d32f2f' }}>{result.wrong}</span>
            </div>

            <div className="result-row">
              <span className="result-label">Percentage</span>
              <span className="result-value">{result.score.toFixed(1)}%</span>
            </div>
          </div>

          <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#f9f9f9', border: '1px solid #ddd', textAlign: 'center' }}>
            {isPassed ? (
              <p style={{ color: '#2e7d32', fontSize: '1rem' }}>
                <strong>Great job! You passed the exam.</strong>
              </p>
            ) : (
              <p style={{ color: '#d32f2f', fontSize: '1rem' }}>
                <strong>Keep learning! You need 50% to pass.</strong>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

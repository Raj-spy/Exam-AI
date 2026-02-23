/**
 * TeacherDashboard Component
 * =========================
 * (Optional) Teacher dashboard to view test results
 * 
 * Features:
 * - View created tests
 * - View student submissions
 * - Aggregated statistics
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTestResults } from '../services/api'
import '../styles/pages.css'

export default function TeacherDashboard() {
  const navigate = useNavigate()
  const [lastTest, setLastTest] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const saved = localStorage.getItem('lastCreatedTest')
    if (saved) {
      const test = JSON.parse(saved)
      setLastTest(test)
      fetchResults(test.testId)
    }
  }, [])

  const fetchResults = async (testId) => {
    setLoading(true)
    setError('')
    try {
      const data = await getTestResults(testId)
      setResults(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error loading results')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      {/* Left Sidebar */}
      <div className="sidebar-panel">
        <div className="sidebar-section">
          <h3>Actions</h3>
          <div className="sidebar-control-group">
            <button 
              onClick={() => navigate('/teacher')} 
              className="sidebar-button primary"
            >
              Create Test
            </button>
            {lastTest && (
              <button
                onClick={() => fetchResults(lastTest.testId)}
                className="sidebar-button"
                disabled={loading}
              >
                Refresh
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Center Content */}
      <div className="content-area">
        <div className="page-header">
          <h1>Dashboard</h1>
          <p>View your tests and student submissions</p>
        </div>

        <div className="content-wrapper">
          {!lastTest ? (
            <div className="empty-state">
              <p>No tests created yet.</p>
              <button onClick={() => navigate('/teacher')} className="btn btn-primary">
                Create a Test
              </button>
            </div>
          ) : (
            <>
              <h2>Last Created Test</h2>
              
              <div className="dashboard-info-box">
                <p><strong>Test ID:</strong></p>
                <code className="link-box">{lastTest.testId}</code>
                <p style={{ marginTop: '1rem' }}><strong>Share Link:</strong></p>
                <code className="link-box">{lastTest.testLink}</code>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(lastTest.testLink)
                    alert('Link copied!')
                  }}
                  className="btn btn-secondary"
                  style={{ marginTop: '1rem' }}
                >
                  Copy Link
                </button>
              </div>

              {loading ? (
                <div className="loading-state">
                  <p>Loading results...</p>
                </div>
              ) : error ? (
                <div className="error-message">{error}</div>
              ) : results ? (
                <>
                  <h2>Student Submissions</h2>
                  <p style={{ marginBottom: '1rem' }}>Total: {results.totalSubmissions} submission(s)</p>

                  {results.totalSubmissions === 0 ? (
                    <div className="empty-state">
                      <p>No submissions yet. Share the test link with students.</p>
                    </div>
                  ) : (
                    <div className="table-container">
                      <table>
                        <thead>
                          <tr>
                            <th>Student</th>
                            <th>Score</th>
                            <th>Correct</th>
                            <th>Wrong</th>
                            <th>Status</th>
                          </tr>
                        </thead>
                        <tbody>
                          {results.submissions.map((submission, idx) => (
                            <tr key={idx}>
                              <td>{submission.studentName}</td>
                              <td>{submission.scorePercentage.toFixed(1)}%</td>
                              <td>{submission.correct}</td>
                              <td>{submission.wrong}</td>
                              <td>
                                <span className={`status-badge ${submission.scorePercentage >= 50 ? 'status-passed' : 'status-failed'}`}>
                                  {submission.scorePercentage >= 50 ? 'PASSED' : 'FAILED'}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </>
              ) : null}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

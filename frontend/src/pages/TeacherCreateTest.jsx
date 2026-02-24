/**
 * TeacherCreateTest Component
 * ===========================
 * Teacher creates exams with AI-generated questions
 * 
 * Features:
 * - Input topic, difficulty, number of questions
 * - Preview AI-generated questions (read-only)
 * - Create test and get unique shareable link
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createTest } from '../services/api'
import '../styles/pages.css'

export default function TeacherCreateTest() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    topic: '',
    difficulty: 'medium',
    num_questions: 5,
    question_type: 'mcq'
  })
  const [loading, setLoading] = useState(false)
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState('')
  const [testCreated, setTestCreated] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'num_questions' ? parseInt(value) : value
    }))
    setError('')
  }

  const handleGeneratePreview = async (e) => {
    e.preventDefault()
    if (!formData.topic.trim()) {
      setError('Please enter a topic')
      return
    }

    setLoading(true)
    setError('')
    try {
      const result = await createTest(formData)
      
      // Fetch questions for preview
      const { getExamQuestions } = await import('../services/api')
      const examData = await getExamQuestions(result.testId)
      
      setPreview({
        testId: result.testId,
        exam: examData
      })
      setTestCreated(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error generating preview. Check if backend is running.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTest = () => {
    if (!testCreated) {
      setError('Please generate preview first')
      return
    }

    // Store test info for teacher
    localStorage.setItem('lastCreatedTest', JSON.stringify({
      testId: testCreated.testId,
      testLink: `${window.location.origin}/exam/${testCreated.testId}`
    }))

    alert('Test created successfully! Link copied to clipboard.')
  }

  const handleCopyLink = () => {
    if (testCreated) {
      const link = `${window.location.origin}/exam/${testCreated.testId}`
      navigator.clipboard.writeText(link)
      alert('Test link copied to clipboard!')
    }
  }

  return (
    <div className="container">
      {/* Left Sidebar - Control Panel */}
      <div className="sidebar-panel">
        <div className="sidebar-section">
          <h3>Exam Setup</h3>
          
          <div className="form-group">
            <label htmlFor="topic">Topic</label>
            <input
              id="topic"
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="e.g., Indian History"
              className="input-field"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="difficulty">Difficulty</label>
            <select
              id="difficulty"
              name="difficulty"
              value={formData.difficulty}
              onChange={handleInputChange}
              className="input-field"
              disabled={loading}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="num_questions">Questions</label>
            <input
              id="num_questions"
              type="number"
              name="num_questions"
              value={formData.num_questions}
              onChange={handleInputChange}
              min="1"
              max="10"
              className="input-field"
              disabled={loading}
            />
          </div>
        </div>

        <div className="sidebar-section">
          <div className="sidebar-control-group">
            <button
              type="button"
              onClick={handleGeneratePreview}
              disabled={loading}
              className="sidebar-button"
            >
              {loading ? 'Generating...' : 'Generate Preview'}
            </button>
            
            {preview && (
              <>
                <button
                  onClick={handleCopyLink}
                  className="sidebar-button"
                  title="Copy link to share with students"
                >
                  Copy Link
                </button>
                <button
                  onClick={handleCreateTest}
                  className="sidebar-button primary"
                >
                  Create Test
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Center Content Area */}
      <div className="content-area">
        <div className="page-header">
          <h1>Create Exam</h1>
          <p>Generate AI-powered questions and create a test</p>
        </div>

        <div className="content-wrapper">
          {error && <div className="error-message">{error}</div>}

          {preview ? (
            <>
              <h2>Questions Preview</h2>
              
              <div className="test-info">
                <p><strong>Test ID:</strong> <code>{preview.testId}</code></p>
                <p><strong>Topic:</strong> {preview.exam.topic}</p>
                <p><strong>Difficulty:</strong> {preview.exam.difficulty}</p>
                <p><strong>Total:</strong> {preview.exam.totalQuestions} questions</p>
              </div>

              <div className="questions-preview">
                {preview.exam.questions.map((q, idx) => (
                  <div key={idx} className="question-card">
                    <h4>Q{idx + 1}: {q.question}</h4>
                    {q.options && (
                      <ul className="options-list">
                        {q.options.map((opt, oIdx) => (
                          <li key={oIdx}>
                            <span className="option-label">{String.fromCharCode(65 + oIdx)}</span> {opt}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>

              {testCreated && (
                <div className="success-message">
                  <p><strong>Test created successfully!</strong></p>
                  <p>Share this link with students:</p>
                  <code className="link-box">
                    {`${window.location.origin}/exam/${testCreated.testId}`}
                  </code>
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <p>Configure exam settings in the left panel</p>
              <p>Click "Generate Preview" to see questions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}



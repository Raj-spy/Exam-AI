/**
 * StudentExam Component
 * ====================
 * Students attempt exams and submit answers
 * 
 * Features:
 * - Fetch questions for specific test
 * - Enter student name
 * - Render MCQ questions
 * - Select answers
 * - Submit and get instant results
 */

import { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { getExamQuestions, submitExam, getTestResults } from '../services/api'
import '../styles/pages.css'

export default function StudentExam() {
  const { testId } = useParams()
  
  const [exam, setExam] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [studentName, setStudentName] = useState('')
  const [testStarted, setTestStarted] = useState(false)
  const [answers, setAnswers] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [submissionDetails, setSubmissionDetails] = useState([])
  const [resultSummary, setResultSummary] = useState(null)

  // proctoring state
  const [ws, setWs] = useState(null)
  const videoRef = useRef(null)
  const [warning, setWarning] = useState(false)
  const proctorInterval = useRef(null)
  const landmarkSolver = useRef(null)

  useEffect(() => {
    fetchExamQuestions()
  }, [testId])

  const fetchExamQuestions = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getExamQuestions(testId)
      setExam(data)
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Error loading exam. Make sure the test ID is correct.'
      )
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleStartTest = (e) => {
    e.preventDefault()
    if (!studentName.trim()) {
      setError('Please enter your name')
      return
    }
    setTestStarted(true)
    setError('')
  }

  // proctoring lifecycle --------------------------------------------------
  useEffect(() => {
    if (!testStarted) return

    // open websocket
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const host = window.location.hostname + (window.location.port ? ':8000' : '') // assume backend on 8000
    const socket = new WebSocket(`${protocol}://${host}/ws/proctor/${testId}/${encodeURIComponent(studentName)}`)
    socket.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data)
        if (data.suspicion_level === 'high') {
          setWarning(true)
        } else {
          setWarning(false)
        }
      } catch {}
    }
    setWs(socket)

    // webcam setup
    const startWebcam = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      if (videoRef.current) videoRef.current.srcObject = stream
      // once video is playing we can start face mesh
      // load mediapipe
      const mp = await import('@mediapipe/face_mesh')
      const drawingUtils = await import('@mediapipe/drawing_utils')
      const cam = new mp.FaceMesh({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
      })
      cam.setOptions({
        maxNumFaces: 2,
        refineLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      })
      cam.onResults(onResults)
      landmarkSolver.current = cam
      const videoElement = videoRef.current
      const sendFrame = async () => {
        if (videoElement && cam) await cam.send({image: videoElement})
      }
      proctorInterval.current = setInterval(sendFrame, 2000)
    }

    startWebcam().catch(console.error)

    // visibility and blur
    const handleVisibility = () => {
      if (document.visibilityState !== 'visible') {
        wsSend({event_type: 'tab_switch'})
      }
    }
    const handleBlur = () => {
      wsSend({event_type: 'window_blur'})
    }
    document.addEventListener('visibilitychange', handleVisibility)
    window.addEventListener('blur', handleBlur)

    return () => {
      // cleanup
      document.removeEventListener('visibilitychange', handleVisibility)
      window.removeEventListener('blur', handleBlur)
      if (proctorInterval.current) clearInterval(proctorInterval.current)
      if (landmarkSolver.current) landmarkSolver.current.close()
      if (ws) ws.close()
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks()
        tracks.forEach((t) => t.stop())
      }
    }
  }, [testStarted])

  const wsSend = (msg) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg))
    }
  }

  const onResults = (results) => {
    if (!results.multiFaceLandmarks) return
    const landmarks = results.multiFaceLandmarks.map((face) => {
      const left_eye = face[33] || face[1]
      const right_eye = face[263] || face[5]
      const nose_tip = face[1] || face[4]
      return { left_eye: [left_eye.x, left_eye.y], right_eye: [right_eye.x, right_eye.y], nose_tip: [nose_tip.x, nose_tip.y] }
    })
    wsSend({ event_type: 'face', landmarks })
  }

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const handleSubmitExam = async (e) => {
    e.preventDefault()
    
    const answered = Object.keys(answers).length
    const total = exam.totalQuestions
    
    if (answered < total) {
      alert(`You have answered ${answered} out of ${total} questions. Submit anyway?`)
    }

    setSubmitting(true)
    setError('')
    try {
      const result = await submitExam(testId, {
        student_name: studentName,
        answers: answers
      })

      // Store overall result locally
      localStorage.setItem('examResult', JSON.stringify(result))
      setResultSummary(result)

      // Fetch submissions for this test and find the student's submission details
      try {
        const allResults = await getTestResults(testId)
        if (allResults && Array.isArray(allResults.submissions)) {
          // Try to find a matching submission by student name and score
          const found = allResults.submissions.find((s) => {
            return (
              (s.studentName === result.studentName || s.studentName === studentName) &&
              (Math.round(s.scorePercentage) === Math.round(result.score) || s.correct === result.correct)
            )
          })

          if (found && Array.isArray(found.resultsDetails)) {
            setSubmissionDetails(found.resultsDetails)
          }
        }
      } catch (subErr) {
        // Non-fatal: if we can't fetch per-question details, still show overall result
        console.warn('Could not fetch submission details for review', subErr)
      }

      // Keep student on same page and enable review mode
      setSubmitted(true)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error submitting exam')
      console.error('Error:', err)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading-state">
          <h2>Loading Exam</h2>
          <p>Please wait while we fetch the questions.</p>
        </div>
      </div>
    )
  }

  if (error && !exam) {
    return (
      <div className="container">
        <div className="error-state">
          <h2>Error Loading Exam</h2>
          <p>{error}</p>
          <button onClick={fetchExamQuestions} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!exam) {
    return (
      <div className="container">
        <div className="error-state">
          <h2>Exam Not Found</h2>
          <p>The test ID provided is invalid or expired.</p>
        </div>
      </div>
    )
  }

  if (!testStarted) {
    return (
      <div className="container">
        {/* Left Sidebar */}
        <div className="sidebar-panel">
          <div className="sidebar-section">
            <h3>Test Info</h3>
            <div className="form-group">
              <label htmlFor="studentName">Your Name</label>
              <input
                id="studentName"
                type="text"
                value={studentName}
                onChange={(e) => {
                  setStudentName(e.target.value)
                  setError('')
                }}
                placeholder="Enter your name"
                autoFocus
                className="input-field"
              />
            </div>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-control-group">
              <button
                onClick={handleStartTest}
                className="sidebar-button primary"
              >
                Start Test
              </button>
            </div>
          </div>
        </div>

        {/* Center Content */}
          <div className="content-area">

          <div className="content-wrapper">
              {error && <div className="error-message">{error}</div>}

              {/* If submission happened earlier (page revisited), show result summary */}
              {submitted && resultSummary && (
                <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#e8f5e9', border: '1px solid #c8e6c9', textAlign: 'center' }}>
                  <strong>Test completed — Score: {Math.round(resultSummary.score)}% — {resultSummary.status}</strong>
                </div>
              )}

            <div className="exam-info">
              <p><strong>Topic:</strong> {exam.topic}</p>
              <p><strong>Difficulty:</strong> {exam.difficulty}</p>
              <p><strong>Total Questions:</strong> {exam.totalQuestions}</p>
            </div>

            <p style={{ marginTop: '1.5rem', color: '#666' }}>
              Enter your name and click Start Test to begin.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      {/* hidden video for face mesh analysis */}
      <video ref={videoRef} style={{ display: 'none' }} playsInline muted />
      {warning && (
        <div className="warning-popup">
          Suspicious activity detected. Please focus on the exam.
        </div>
      )}
      {/* Left Sidebar */}
      <div className="sidebar-panel">
        <div className="sidebar-section">
          <h3>Student Info</h3>
          <div className="form-group">
            <label htmlFor="studentName">Name</label>
            <input
              id="studentName"
              type="text"
              value={studentName}
              onChange={(e) => {
                setStudentName(e.target.value)
                setError('')
              }}
              placeholder="Enter name"
              className="input-field"
              autoFocus
            />
          </div>
        </div>

        <div className="sidebar-section">
          <p style={{ fontSize: '0.95rem', color: '#666' }}>
            Progress: {Object.keys(answers).length} / {exam.totalQuestions}
          </p>
        </div>
      </div>

      {/* Center Content */}
        <div className="content-area">

        <div className="content-wrapper">
          {submitted && resultSummary && (
            <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#e8f5e9', border: '1px solid #c8e6c9', textAlign: 'center' }}>
              <strong>Test completed — Score: {Math.round(resultSummary.score)}% — {resultSummary.status}</strong>
            </div>
          )}
          <form onSubmit={handleSubmitExam}>
            <div className="questions-container">
              {exam.questions.map((question, idx) => (
                <div key={question.questionId} className="question-section">
                  <h3>Question {idx + 1} of {exam.totalQuestions}</h3>
                  <p className="question-text">{question.question}</p>

                  {question.options && (
                    <div className="options-group">
                      {question.options.map((option, optIdx) => {
                        // Determine option styling based on submissionDetails
                        let optionClass = ''
                        if (submitted && submissionDetails.length) {
                          const detail = submissionDetails.find(d => d.questionId === question.questionId)
                          if (detail) {
                            const correct = String(detail.correctAnswer).trim()
                            const studentAns = String(detail.studentAnswer || '').trim()

                            if (option === correct) {
                              optionClass = 'option-correct'
                            } else if (studentAns && option === studentAns && studentAns !== correct) {
                              optionClass = 'option-wrong'
                            }
                          }
                        }

                        return (
                          <label key={optIdx} className={`option-label-container ${optionClass}`}>
                            <input
                              type="radio"
                              name={`question_${question.questionId}`}
                              value={option}
                              checked={answers[question.questionId] === option}
                              onChange={() => handleAnswerChange(question.questionId, option)}
                              className="option-input"
                              disabled={submitted}
                            />
                            <span className="option-text">{option}</span>
                          </label>
                        )
                      })}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="form-actions">
              <button
                type="submit"
                disabled={submitting}
                className="btn btn-primary btn-block"
              >
                {submitting ? 'Submitting...' : 'Submit Exam'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}



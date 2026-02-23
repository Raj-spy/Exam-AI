import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { BASE_URL } from '../config/backend'
import '../styles/pages.css'

export default function TeacherMonitor() {
  const { testId } = useParams()
  const [ws, setWs] = useState(null)
  const [students, setStudents] = useState({})

  useEffect(() => {
    const wsUrl = `${BASE_URL.replace('https', 'wss')}/ws/teacher/${testId}`
    const socket = new WebSocket(wsUrl)
    socket.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data)
        setStudents(prev => ({
          ...prev,
          [data.student]: {
            status: data.status,
            suspicion_level: data.suspicion_level,
            suspicion_score: data.suspicion_score,
            timestamp: data.timestamp,
          }
        }))
        // play alert if high
        if (data.suspicion_level === 'high') {
          const sound = document.getElementById('alertSound')
          if (sound) sound.play().catch(() => {})
        }
      } catch (e) {
        console.error('invalid message', e)
      }
    }
    setWs(socket)
    return () => {
      if (socket) socket.close()
    }
  }, [testId])

  const renderRow = (name, info) => {
    const level = info.suspicion_level
    let bg = ''
    if (level === 'low') bg = '#e8f5e9'
    if (level === 'medium') bg = '#fff8e1'
    if (level === 'high') bg = '#ffebee'

    return (
      <tr key={name} style={{ background: bg }} className={level === 'high' ? 'flash' : ''}>
        <td>{name}</td>
        <td>{info.status}</td>
        <td>{level}</td>
        <td>{info.suspicion_score}</td>
        <td>{new Date(info.timestamp).toLocaleTimeString()}</td>
      </tr>
    )
  }

  return (
    <div className="container">
      <h2>Proctoring Monitor - Exam {testId}</h2>
      <table className="dashboard-table">
        <thead>
          <tr>
            <th>Student Name</th>
            <th>Status</th>
            <th>Suspicion Level</th>
            <th>Score</th>
            <th>Last Update</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(students).map(([name, info]) => renderRow(name, info))}
        </tbody>
      </table>
      <audio id="alertSound" src="/alert.mp3" />
    </div>
  )
}

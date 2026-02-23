/**
 * API Service Module
 * ==================
 * Centralized Axios instance for all FastAPI backend calls
 * Base URL points to FastAPI backend running on port 8001
 */

import axios from 'axios'

// Create Axios instance with base URL pointing to FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Create a new exam with AI-generated questions
 * @param {Object} data - { topic, difficulty, number_of_questions, question_type }
 * @returns {Promise<Object>} - { testId, totalQuestions, testLink }
 */
export const createTest = async (data) => {
  try {
    const response = await api.post('/create-test', data)
    return response.data
  } catch (error) {
    console.error('Error creating test:', error)
    throw error
  }
}

/**
 * Fetch exam questions by test ID
 * @param {string} testId - The unique test identifier
 * @returns {Promise<Object>} - { testId, topic, difficulty, totalQuestions, questions }
 */
export const getExamQuestions = async (testId) => {
  try {
    const response = await api.get(`/exam/${testId}`)
    return response.data
  } catch (error) {
    console.error('Error fetching exam questions:', error)
    throw error
  }
}

/**
 * Submit exam answers and get evaluation
 * @param {string} testId - The unique test identifier
 * @param {Object} data - { student_name, answers }
 * @returns {Promise<Object>} - { studentName, score, correct, wrong, totalAttempted, status }
 */
export const submitExam = async (testId, data) => {
  try {
    const response = await api.post(`/exam/${testId}/submit`, data)
    return response.data
  } catch (error) {
    console.error('Error submitting exam:', error)
    throw error
  }
}

/**
 * Fetch all results for a test
 * @param {string} testId - The unique test identifier
 * @returns {Promise<Object>} - { testId, totalSubmissions, submissions }
 */
export const getTestResults = async (testId) => {
  try {
    const response = await api.get(`/exam/${testId}/results`)
    return response.data
  } catch (error) {
    console.error('Error fetching test results:', error)
    throw error
  }
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} - { status, message }
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('http://localhost:8001/health')
    return response.data
  } catch (error) {
    console.error('Error in health check:', error)
    throw error
  }
}

export default api

/**
 * API Service Module
 * ==================
 * Centralized Axios instance for all FastAPI backend calls
 * Base URL points to FastAPI backend running on port 8001
 */

import axios from 'axios'
import { BASE_URL } from '../config/backend'

// Create Axios instance with base URL using centralized config
const api = axios.create({
  baseURL: `${BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Create a new exam with AI-generated questions
 * @param {Object} data - { topic, difficulty, num_questions, question_type }
 * @returns {Promise<Object>} - { testId, totalQuestions, testLink }
 */
export const createTest = async (data) => {
  try {
    // build payload matching backend schema exactly
    const {
      topic,
      difficulty,
      num_questions,
      question_type,
    } = data || {}

    const payload = {
      topic,
      difficulty: difficulty ? difficulty.toLowerCase() : undefined,
      num_questions: num_questions !== undefined ? Number(num_questions) : undefined,
      ...(question_type !== undefined && { question_type }),
    }

    // remove undefined keys
    Object.keys(payload).forEach(
      (k) => payload[k] === undefined && delete payload[k]
    )

    const response = await api.post('/create-test', payload)
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
    // Health endpoint is outside /api path so call full BASE_URL
    const response = await axios.get(`${BASE_URL}/health`)
    return response.data
  } catch (error) {
    console.error('Error in health check:', error)
    throw error
  }
}

export default api

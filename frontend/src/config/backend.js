// Centralized backend configuration
// Use Vite environment variable VITE_BACKEND_URL in production
// Fallback to development backend when the env var is not set
export const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8001'

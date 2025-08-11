import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor for adding auth tokens (when implemented)
api.interceptors.request.use(
  (config) => {
    // Add auth token when available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Puzzle endpoints
export const puzzleAPI = {
  getDailyPuzzle: () => api.get('/puzzle/daily/'),
  submitAnswer: (answer) => api.post('/puzzle/submit/', { answer }),
  getPuzzleHistory: () => api.get('/puzzle/history/'),
  generatePuzzle: (puzzleData) => api.post('/puzzle/generate/', puzzleData),
};

// Stats endpoints
export const statsAPI = {
  getPlayerStats: () => api.get('/stats/'),
  getLeaderboard: () => api.get('/leaderboard/'),
  getStumpTally: () => api.get('/stump-tally/'),
};

// Auth endpoints (for future implementation)
export const authAPI = {
  login: (credentials) => api.post('/api-auth/login/', credentials),
  logout: () => api.post('/api-auth/logout/'),
};

export default api;
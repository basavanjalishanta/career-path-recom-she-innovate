/**
 * API Service Layer - Axios Configuration
 * Handles all backend communication with authentication
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

const apiService = {
  // ==================== AUTH ====================
  signup: (data) => api.post('/auth/signup', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  getMe: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),

  // ==================== PROFILE ====================
  getProfile: () => api.get('/profile'),
  updateProfile: (data) => api.post('/profile/update', data),

  // ==================== RECOMMENDATIONS ====================
  getRecommendations: (data) => api.post('/recommendations', data),
  fetchRecommendations: () => api.get('/recommendations'),
  compareRecommendations: (path1, path2) => api.get(`/recommendations/${path1}/compare/${path2}`),

  // ==================== CHATBOT ====================
  sendMessage: (message) => api.post('/chat', { message }),
  getChatHistory: (limit = 50) => api.get(`/chat/history?limit=${limit}`),

  // ==================== INFO ====================
  healthCheck: () => api.get('/health'),
  getCareerPaths: () => api.get('/career-paths'),
  getDomains: () => api.get('/domains'),
  // ==================== SKILL GAP ====================
  skillGap: (data) => api.post('/skillgap', data),
  // ==================== UPLOADS ====================
  uploadResume: (file) => {
    const form = new FormData();
    form.append('resume', file);
    return api.post('/profile/upload_resume', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  downloadResume: () => api.get('/profile/resume', { responseType: 'arraybuffer' }),
};

export default apiService;

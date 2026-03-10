import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';

export const apiClient = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().clearAuth();
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: { email: string; password: string; name: string; role: string }) =>
    apiClient.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    apiClient.post('/auth/login', data),
  getMe: () => apiClient.get('/auth/me'),
};

// Courses API
export const coursesAPI = {
  getAll: (language?: string, level?: string) =>
    apiClient.get('/courses', { params: { language, level } }),
  getOne: (id: string) => apiClient.get(`/courses/${id}`),
  create: (data: any) => apiClient.post('/courses', data),
  getLessons: (courseId: string) => apiClient.get(`/courses/${courseId}/lessons`),
  getQuizzes: (courseId: string) => apiClient.get(`/courses/${courseId}/quizzes`),
};

// Lessons API
export const lessonsAPI = {
  getOne: (id: string) => apiClient.get(`/lessons/${id}`),
  create: (data: any) => apiClient.post('/lessons', data),
  complete: (id: string) => apiClient.post(`/lessons/${id}/complete`),
};

// Flashcards API
export const flashcardsAPI = {
  getAll: (language?: string, level?: string, limit?: number) =>
    apiClient.get('/flashcards', { params: { language, level, limit } }),
  create: (data: any) => apiClient.post('/flashcards', data),
  review: (flashcardId: string, correct: boolean) =>
    apiClient.post('/flashcards/review', { flashcard_id: flashcardId, correct }),
};

// Quiz API
export const quizAPI = {
  getAll: (language?: string, level?: string) =>
    apiClient.get('/quizzes', { params: { language, level } }),
  getOne: (id: string) => apiClient.get(`/quizzes/${id}`),
  create: (data: any) => apiClient.post('/quizzes', data),
  submit: (quizId: string, answers: number[]) =>
    apiClient.post(`/quizzes/${quizId}/submit`, { quiz_id: quizId, answers }),
  seed: () => apiClient.post('/seed-quizzes'),
};

// Progress API
export const progressAPI = {
  get: () => apiClient.get('/progress'),
  byLanguage: () => apiClient.get('/progress/by-language'),
};

// Teacher API
export const teacherAPI = {
  getStudents: () => apiClient.get('/teacher/students'),
  getStats: () => apiClient.get('/teacher/stats'),
};

// AI API
export const aiAPI = {
  generateExercise: (data: { language: string; level: string; topic: string; exercise_type: string }) =>
    apiClient.post('/ai/generate-exercise', data),
  explain: (language: string, level: string, concept: string) =>
    apiClient.post('/ai/explain', null, { params: { language, level, concept } }),
};

// TTS API
export const ttsAPI = {
  generate: (text: string, language: string) =>
    apiClient.post('/tts/generate', { text, language }),
};

// Seed data
export const seedData = () => apiClient.post('/seed-data');

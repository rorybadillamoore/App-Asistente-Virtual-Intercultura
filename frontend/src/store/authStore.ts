import { create } from 'zustand';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'student' | 'teacher';
  created_at: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  initializeAuth: () => void;
}

// Helper to safely access localStorage
const getStoredAuth = () => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      const stored = localStorage.getItem('auth-storage');
      if (stored) {
        return JSON.parse(stored);
      }
    }
  } catch (e) {
    console.log('Error reading auth from storage:', e);
  }
  return null;
};

const saveAuth = (user: User | null, token: string | null, isAuthenticated: boolean) => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('auth-storage', JSON.stringify({ user, token, isAuthenticated }));
    }
  } catch (e) {
    console.log('Error saving auth to storage:', e);
  }
};

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  setAuth: (user, token) => {
    saveAuth(user, token, true);
    set({ user, token, isAuthenticated: true, isLoading: false });
  },
  clearAuth: () => {
    saveAuth(null, null, false);
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },
  initializeAuth: () => {
    const stored = getStoredAuth();
    if (stored?.isAuthenticated && stored?.user && stored?.token) {
      set({ 
        user: stored.user, 
        token: stored.token, 
        isAuthenticated: true, 
        isLoading: false 
      });
    } else {
      set({ isLoading: false });
    }
  },
}));

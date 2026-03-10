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
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
}

// Helper to safely access localStorage - only on client side
const getInitialState = () => {
  if (typeof window === 'undefined') {
    return { user: null, token: null, isAuthenticated: false };
  }
  
  try {
    const stored = localStorage.getItem('auth-storage');
    if (stored) {
      const parsed = JSON.parse(stored);
      if (parsed?.isAuthenticated && parsed?.user && parsed?.token) {
        return {
          user: parsed.user,
          token: parsed.token,
          isAuthenticated: true,
        };
      }
    }
  } catch (e) {
    console.log('Error reading auth from storage:', e);
  }
  
  return { user: null, token: null, isAuthenticated: false };
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

const initialState = getInitialState();

export const useAuthStore = create<AuthState>()((set) => ({
  user: initialState.user,
  token: initialState.token,
  isAuthenticated: initialState.isAuthenticated,
  setAuth: (user, token) => {
    saveAuth(user, token, true);
    set({ user, token, isAuthenticated: true });
  },
  clearAuth: () => {
    saveAuth(null, null, false);
    set({ user: null, token: null, isAuthenticated: false });
  },
}));

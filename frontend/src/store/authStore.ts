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
  _hasHydrated: boolean;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  setHasHydrated: (state: boolean) => void;
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

export const useAuthStore = create<AuthState>()((set) => {
  // Initialize from localStorage if available
  const stored = getStoredAuth();
  
  // Set hydrated after a tick to allow initial render
  setTimeout(() => {
    useAuthStore.setState({ _hasHydrated: true });
  }, 0);
  
  return {
    user: stored?.user || null,
    token: stored?.token || null,
    isAuthenticated: stored?.isAuthenticated || false,
    _hasHydrated: false,
    setAuth: (user, token) => {
      saveAuth(user, token, true);
      set({ user, token, isAuthenticated: true });
    },
    clearAuth: () => {
      saveAuth(null, null, false);
      set({ user: null, token: null, isAuthenticated: false });
    },
    setHasHydrated: (state) => set({ _hasHydrated: state }),
  };
});

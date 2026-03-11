import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

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
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  _hasHydrated: false,
  
  setAuth: async (user, token) => {
    set({ user, token, isAuthenticated: true });
    // Persist to storage
    try {
      await AsyncStorage.setItem('auth-storage', JSON.stringify({ user, token }));
    } catch (e) {
      console.error('Failed to save auth:', e);
    }
  },
  
  clearAuth: async () => {
    set({ user: null, token: null, isAuthenticated: false });
    // Clear from storage
    try {
      await AsyncStorage.removeItem('auth-storage');
    } catch (e) {
      console.error('Failed to clear auth:', e);
    }
  },
  
  hydrate: async () => {
    try {
      const stored = await AsyncStorage.getItem('auth-storage');
      if (stored) {
        const { user, token } = JSON.parse(stored);
        set({ user, token, isAuthenticated: true, _hasHydrated: true });
      } else {
        set({ _hasHydrated: true });
      }
    } catch (e) {
      console.error('Failed to hydrate auth:', e);
      set({ _hasHydrated: true });
    }
  },
}));

// Auto-hydrate on load
if (typeof window !== 'undefined') {
  useAuthStore.getState().hydrate();
}

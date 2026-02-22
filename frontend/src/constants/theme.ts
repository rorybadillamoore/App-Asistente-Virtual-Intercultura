export const COLORS = {
  // Primary colors
  primary: '#4F46E5',
  primaryDark: '#3730A3',
  primaryLight: '#818CF8',
  
  // Secondary colors
  secondary: '#10B981',
  secondaryDark: '#059669',
  secondaryLight: '#34D399',
  
  // Language colors
  spanish: '#EF4444',
  english: '#3B82F6',
  portuguese: '#22C55E',
  
  // Level colors
  a1: '#22C55E',
  a2: '#84CC16',
  b1: '#EAB308',
  b2: '#F97316',
  c1: '#EF4444',
  c2: '#DC2626',
  
  // Neutrals
  white: '#FFFFFF',
  black: '#000000',
  gray50: '#F9FAFB',
  gray100: '#F3F4F6',
  gray200: '#E5E7EB',
  gray300: '#D1D5DB',
  gray400: '#9CA3AF',
  gray500: '#6B7280',
  gray600: '#4B5563',
  gray700: '#374151',
  gray800: '#1F2937',
  gray900: '#111827',
  
  // Status
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',
  
  // Background
  background: '#F9FAFB',
  card: '#FFFFFF',
};

export const FONTS = {
  regular: 'System',
  medium: 'System',
  bold: 'System',
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const BORDER_RADIUS = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 999,
};

export const SHADOWS = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
};

export const LANGUAGES = [
  { id: 'spanish', name: 'Español', flag: '🇪🇸', color: COLORS.spanish },
  { id: 'english', name: 'English', flag: '🇬🇧', color: COLORS.english },
  { id: 'portuguese', name: 'Português', flag: '🇧🇷', color: COLORS.portuguese },
];

export const LEVELS = [
  { id: 'A1', name: 'A1 - Beginner', color: COLORS.a1 },
  { id: 'A2', name: 'A2 - Elementary', color: COLORS.a2 },
  { id: 'B1', name: 'B1 - Intermediate', color: COLORS.b1 },
  { id: 'B2', name: 'B2 - Upper Intermediate', color: COLORS.b2 },
  { id: 'C1', name: 'C1 - Advanced', color: COLORS.c1 },
  { id: 'C2', name: 'C2 - Mastery', color: COLORS.c2 },
];

export const getLanguageColor = (language: string) => {
  switch (language.toLowerCase()) {
    case 'spanish': return COLORS.spanish;
    case 'english': return COLORS.english;
    case 'portuguese': return COLORS.portuguese;
    default: return COLORS.primary;
  }
};

export const getLevelColor = (level: string) => {
  switch (level.toUpperCase()) {
    case 'A1': return COLORS.a1;
    case 'A2': return COLORS.a2;
    case 'B1': return COLORS.b1;
    case 'B2': return COLORS.b2;
    case 'C1': return COLORS.c1;
    case 'C2': return COLORS.c2;
    default: return COLORS.primary;
  }
};

export const COLORS = {
  // Intercultura Brand Colors
  primary: '#22955B',        // Dark green
  primaryLight: '#B6C932',   // Light green
  primaryDark: '#1a7346',    // Darker green
  
  // Accent colors
  accent: '#e34b33',         // Red
  accentOrange: '#fa8a00',   // Orange
  
  // Secondary (keeping for language differentiation)
  secondary: '#B6C932',
  secondaryDark: '#9ab029',
  secondaryLight: '#c8d94d',
  
  // Language colors (using brand palette)
  spanish: '#e34b33',        // Red
  english: '#22955B',        // Dark green  
  portuguese: '#fa8a00',     // Orange
  german: '#1a1a1a',         // Black (German flag)
  french: '#002395',         // Blue (French flag)
  
  // Level colors (gradient from green to red)
  a1: '#B6C932',
  a2: '#8fb82a',
  b1: '#fa8a00',
  b2: '#f07800',
  c1: '#e34b33',
  c2: '#c43d2a',
  
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
  success: '#22955B',
  warning: '#fa8a00',
  error: '#e34b33',
  info: '#22955B',
  
  // Background
  background: '#F9FAFB',
  card: '#FFFFFF',
};

export const FONTS = {
  regular: 'Aller',
  medium: 'Aller',
  bold: 'Aller',
  light: 'Aller_Light',
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
  { id: 'german', name: 'Deutsch', flag: '🇩🇪', color: COLORS.german },
  { id: 'french', name: 'Français', flag: '🇫🇷', color: COLORS.french },
];

export const LEVELS = [
  { id: 'A1', name: 'A1 - Principiante', color: COLORS.a1 },
  { id: 'A2', name: 'A2 - Elemental', color: COLORS.a2 },
  { id: 'B1', name: 'B1 - Intermedio', color: COLORS.b1 },
  { id: 'B2', name: 'B2 - Intermedio Alto', color: COLORS.b2 },
  { id: 'C1', name: 'C1 - Avanzado', color: COLORS.c1 },
  { id: 'C2', name: 'C2 - Maestría', color: COLORS.c2 },
];

export const getLanguageColor = (language: string) => {
  switch (language.toLowerCase()) {
    case 'spanish': return COLORS.spanish;
    case 'english': return COLORS.english;
    case 'portuguese': return COLORS.portuguese;
    case 'german': return COLORS.german;
    case 'french': return COLORS.french;
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

// App Branding
export const APP_NAME = 'Intercultura';
export const APP_TAGLINE = 'Asistente Virtual';
export const APP_FULL_NAME = 'Intercultura Asistente Virtual';

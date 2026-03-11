# PRD: Intercultura Asistente Virtual

## Original Problem Statement
Crear una aplicación móvil (PWA) "Intercultura Asistente Virtual" para una escuela de idiomas costarricense.

## Target Users
- **Estudiantes**: Aprenden idiomas con lecciones, flashcards, quizzes y ejercicios IA
- **Profesores**: Ven el progreso de sus estudiantes en un panel de control

## Core Requirements
- Soporte para 5 idiomas: Español, Inglés, Portugués, Alemán, **Francés** (A1-C2)
- Lecciones, cursos, flashcards con audio TTS, quizzes IA
- Ejercicios IA generativos (gramática, vocabulario, lectura, escritura)
- Autenticación email/contraseña con roles estudiante/profesor
- Branding Intercultura (sin branding Emergent)

## Architecture
- **Frontend**: React Native con Expo, Expo Router, Zustand
- **Backend**: Python FastAPI
- **Database**: MongoDB Atlas (usuario)
- **AI**: OpenAI GPT-4 (ejercicios), ElevenLabs + fallback OpenAI TTS (audio)

## What's Been Implemented

### ✅ Authentication
- Registro y login con email/contraseña
- Roles: estudiante y profesor
- Logout funcional (workaround con window.location.reload para evitar bug de expo-router)
- Sesión persistente con Zustand

### ✅ Content (5 Languages, 6 Levels each)
- **Courses**: 30 cursos (5 idiomas × 6 niveles)
- **Lessons**: 180 lecciones (5 idiomas × 6 niveles × 6 lecciones)
- **Flashcards**: 300 flashcards (5 idiomas × 6 niveles × 10 flashcards)
- **Quizzes**: 30 quizzes (5 idiomas × 6 niveles)
- **Idiomas**: Español, Inglés, Portugués, Alemán, **Francés** (añadido mar 2026)

### ✅ AI Features
- Ejercicios generativos con GPT-4 (gramática, vocabulario, lectura, escritura)
- Soporte para todos los idiomas incluyendo francés
- Resultados con respuestas correctas/incorrectas destacadas

### ✅ TTS Audio
- ElevenLabs con fallback automático a OpenAI TTS
- Nota: ElevenLabs Free Tier bloqueado desde servidores cloud. Usuario necesita plan Starter ($5/mes) para usar ElevenLabs nativo

### ✅ Pantallas Nuevas (mar 2026)
- **Mi Progreso** (`/progress`): Stats por idioma con lecciones, quizzes, flashcards
- **Configuración** (`/settings`): Toggles de notificaciones, sonido, reproducción automática
- **Ayuda** (`/help`): FAQ expandibles, datos de contacto, consejos
- **Acerca de** (`/about`): Info de empresa, características, versión 1.0.0

### ✅ PWA
- Ícono correcto de Intercultura (logo.png)
- manifest.json con name, short_name, theme_color #003189
- apple-touch-icon y favicon correctos
- `+html.tsx` con meta tags PWA completos

### ✅ Teacher Dashboard
- Panel de progreso de estudiantes
- Optimizado para evitar N+1 queries

## Test Credentials
- **Estudiante**: testuser123@test.com / password123
- **Profesor**: profesor@test.com / profesor123

## Preview URL
https://polyglot-lang.preview.emergentagent.com

## Prioritized Backlog

### P0 - Inmediato
- **Despliegue**: Usuario debe hacer clic en el botón "Deploy" en la UI de Emergent para obtener URL permanente

### P1 - Próximo
- **ElevenLabs Paid**: Usuario debe actualizar a plan Starter de ElevenLabs ($5/mes) para audio nativo de calidad superior
- **Fuente "Aller"**: Implementar la fuente corporativa de Intercultura

### P2 - Backlog
- Edición de perfil (nombre, foto)
- Cambio de contraseña
- Notificaciones push reales
- Preparación para tiendas de apps (.apk / .ipa)

## Known Technical Debt
- Logout usa `window.location.reload` (workaround para bug de expo-router en web)
- ElevenLabs requiere plan de pago para funcionar desde servidor cloud (Free Tier bloqueado por IP de servidor)

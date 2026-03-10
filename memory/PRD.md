# Intercultura Asistente Virtual - PRD

## Descripción del Producto
Aplicación móvil para escuela de idiomas que enseña Español, Inglés, Portugués y Alemán siguiendo la metodología Cambridge.

## Stack Tecnológico
- **Frontend**: Expo (React Native) con TypeScript
- **Backend**: FastAPI (Python)
- **Base de Datos**: MongoDB
- **IA**: OpenAI GPT-4o (via Emergent LLM Key)
- **TTS**: OpenAI TTS (via Emergent LLM Key)

## Estado del Contenido Educativo
- **48 cursos** (12 por idioma × 4 idiomas)
- **144 lecciones** (3 por curso)
- **240 flashcards** (10 por idioma/nivel con pronunciación)
- **48 quizzes** (1 por curso con 5 preguntas cada uno)

### Cursos por Idioma
| Idioma | Cursos | Quizzes | Niveles |
|--------|--------|---------|---------|
| Español | 12 | 12 | A1-C2 |
| Inglés | 12 | 12 | A1-C2 |
| Portugués | 12 | 12 | A1-C2 |
| Alemán | 12 | 12 | A1-C2 |

## Funcionalidades Implementadas

### Autenticación
- [x] Registro de usuarios (estudiantes/profesores)
- [x] Login con email/contraseña
- [x] Persistencia de sesión (localStorage)
- [x] Roles diferenciados (estudiante/profesor)

### Estudiantes
- [x] Dashboard con progreso personal
- [x] 4 idiomas disponibles (ES, EN, PT, DE)
- [x] Cursos por idioma y nivel (48 cursos)
- [x] Sistema de flashcards con audio TTS
- [x] **Quizzes con promedios por idioma** ✅ NUEVO
- [x] Ejercicios generados por IA
- [x] Revisión de respuestas (correcto/incorrecto)

### Profesores
- [x] **Panel del Profesor** ✅ NUEVO
- [x] **Ver lista de estudiantes** ✅ NUEVO
- [x] **Estadísticas generales** ✅ NUEVO
- [x] **Progreso individual por estudiante** ✅ NUEVO
- [x] Crear cursos (API lista)
- [x] Crear lecciones (API lista)
- [x] Crear flashcards (API lista)

## API Endpoints

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Usuario actual

### Cursos y Contenido
- `GET /api/courses` - Listar cursos (filtros: language, level)
- `GET /api/flashcards` - Listar flashcards
- `POST /api/tts/generate` - Generar audio de pronunciación

### Quizzes
- `GET /api/quizzes` - Listar todos los quizzes ✅ NUEVO
- `GET /api/quizzes/{id}` - Obtener quiz
- `POST /api/quizzes/{id}/submit` - Enviar respuestas
- `POST /api/seed-quizzes` - Poblar quizzes ✅ NUEVO

### Progreso
- `GET /api/progress` - Progreso del usuario
- `GET /api/progress/by-language` - Progreso por idioma ✅ NUEVO

### Panel Profesor
- `GET /api/teacher/students` - Lista de estudiantes ✅ NUEVO
- `GET /api/teacher/stats` - Estadísticas generales ✅ NUEVO

### IA
- `POST /api/ai/generate-exercise` - Generar ejercicios con IA
- `POST /api/ai/explain` - Explicar conceptos con IA

## Credenciales de Prueba

### Estudiante
- Email: testuser123@test.com
- Password: password123

### Profesor
- Email: profesor@test.com
- Password: profesor123

## Tareas Pendientes
- [ ] Implementar tipografía "Aller" (fuente personalizada)
- [ ] Mejorar ocultamiento del tab "Profesor" para estudiantes

## Próximos pasos sugeridos
1. Agregar más funcionalidades al panel del profesor (crear cursos desde UI)
2. Sistema de notificaciones
3. Estadísticas más detalladas
4. Exportar reportes de progreso

---
*Última actualización: Marzo 2026*

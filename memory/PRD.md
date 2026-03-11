# Intercultura Asistente Virtual - PRD

## Descripción del Producto
Aplicación móvil para escuela de idiomas que enseña Español, Inglés, Portugués y Alemán siguiendo la metodología Cambridge.

## Stack Tecnológico
- **Frontend**: Expo (React Native) con TypeScript
- **Backend**: FastAPI (Python)
- **Base de Datos**: MongoDB Atlas (Cloud) ✅ CONFIGURADO
- **IA**: OpenAI GPT-4o (via Emergent LLM Key)
- **TTS**: OpenAI TTS (via Emergent LLM Key)

## Estado del Contenido Educativo
- **24 cursos** (6 niveles × 4 idiomas)
- **72 lecciones** (3 por curso)
- **4 flashcard decks** (1 por idioma nivel A1)
- **24 quizzes** (1 por curso con 5 preguntas cada uno)

### Cursos por Idioma
| Idioma | Cursos | Quizzes | Niveles |
|--------|--------|---------|---------|
| Español | 6 | 6 | A1-C2 |
| Inglés | 6 | 6 | A1-C2 |
| Portugués | 6 | 6 | A1-C2 |
| Alemán | 6 | 6 | A1-C2 |

## Funcionalidades Implementadas

### Autenticación
- [x] Registro de usuarios (estudiantes/profesores)
- [x] Login con email/contraseña
- [x] Persistencia de sesión (localStorage)
- [x] Roles diferenciados (estudiante/profesor)
- [x] **Logout funcional con redirección** ✅ CORREGIDO

### Perfil de Usuario
- [x] **Menú de perfil funcional** ✅ CORREGIDO
  - Mi Progreso → Dashboard
  - Mis Cursos → Cursos
  - Mis Quizzes → Quizzes
- [x] **Botón Cerrar Sesión funcionando** ✅ CORREGIDO

### Branding PWA
- [x] **Logo de Intercultura en Add to Home Screen** ✅ CORREGIDO
- [x] Favicon, icon, adaptive-icon actualizados

### Estudiantes
- [x] Dashboard con progreso personal
- [x] 4 idiomas disponibles (ES, EN, PT, DE)
- [x] Cursos por idioma y nivel (24 cursos)
- [x] Sistema de flashcards con audio TTS
- [x] Quizzes con promedios por idioma
- [x] Ejercicios generados por IA
- [x] **Revisión de respuestas con colores** ✅ (verde=correcto, rojo=incorrecto)

### Profesores
- [x] Panel del Profesor
- [x] Ver lista de estudiantes
- [x] Estadísticas generales
- [x] Progreso individual por estudiante

## Base de Datos

### MongoDB Atlas (Cloud)
- **Cluster**: cluster0.3ffi81o.mongodb.net
- **Database**: polyglot_academy
- **Estado**: ✅ CONECTADO Y FUNCIONANDO

### Endpoints de Seed
- `POST /api/seed-full` - Poblar base de datos completa
- `POST /api/seed-quizzes` - Poblar solo quizzes

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
- `GET /api/quizzes` - Listar todos los quizzes
- `GET /api/quizzes/{id}` - Obtener quiz
- `POST /api/quizzes/{id}/submit` - Enviar respuestas

### Progreso
- `GET /api/progress` - Progreso del usuario
- `GET /api/progress/by-language` - Progreso por idioma

### Panel Profesor
- `GET /api/teacher/students` - Lista de estudiantes
- `GET /api/teacher/stats` - Estadísticas generales

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
- [ ] Preparar builds móviles (.apk/.ipa) con EAS

## Próximos pasos sugeridos
1. Despliegue a producción (Deploy)
2. Agregar más flashcards para todos los niveles
3. Sistema de notificaciones
4. Exportar reportes de progreso

---
*Última actualización: 11 Marzo 2026*

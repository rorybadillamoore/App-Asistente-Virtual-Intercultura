# Intercultura Asistente Virtual - PRD

## Descripción del Producto
Aplicación móvil para escuela de idiomas que enseña Español, Inglés, Portugués y Alemán siguiendo la metodología Cambridge.

## Stack Tecnológico
- **Frontend**: Expo (React Native) con TypeScript
- **Backend**: FastAPI (Python)
- **Base de Datos**: MongoDB
- **IA**: OpenAI GPT-4o (via Emergent LLM Key)
- **TTS**: OpenAI TTS (via Emergent LLM Key)

## Estado del Contenido Educativo ✅
- **48 cursos** (12 por idioma × 4 idiomas)
- **144 lecciones** (3 por curso)
- **240 flashcards** (10 por idioma/nivel con pronunciación)

### Cursos por Idioma
| Idioma | Cursos | Niveles |
|--------|--------|---------|
| Español | 12 | A1-C2 |
| Inglés | 12 | A1-C2 |
| Portugués | 12 | A1-C2 |
| Alemán | 12 | A1-C2 |

## Funcionalidades Implementadas
- [x] Autenticación (registro/login) ✅ FUNCIONANDO
- [x] Persistencia de sesión (localStorage) ✅ FUNCIONANDO
- [x] Dashboard de estudiante
- [x] Cursos por idioma y nivel (48 cursos)
- [x] Sistema de flashcards con audio TTS
- [x] Selección de 4 idiomas en UI ✅ CORREGIDO
- [x] Ejercicios generados por IA ✅ FUNCIONANDO
- [x] Revisión de respuestas (correcto/incorrecto)
- [x] Branding Intercultura (logo, colores)

## API Endpoints
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login
- `GET /api/courses` - Listar cursos (con filtros language/level)
- `GET /api/flashcards` - Listar flashcards
- `POST /api/tts/generate` - Generar audio de pronunciación
- `POST /api/ai/generate-exercise` - Generar ejercicios con IA
- `POST /api/ai/explain` - Explicar conceptos con IA

## Problemas Resueltos
- [x] IA daba error 403 → Ahora funciona sin autenticación obligatoria
- [x] Contenido C1/C2 incompleto → Ahora tiene contenido completo
- [x] Cursos mezclados por idioma → Ahora cada idioma tiene su contenido correcto
- [x] Alemán no visible en UI → Corregido layout de flashcards (grid 2x2)
- [x] Registro no responde → Botón funciona con Pressable para web
- [x] Sesión no persiste → Implementado localStorage para web

## Tareas Pendientes
- [ ] Implementar tipografía "Aller" (fuente personalizada)
- [ ] Rol de profesor (crear cursos, ver progreso estudiantes)

## Credenciales de Prueba
- Email: testuser123@test.com
- Password: password123

---
*Última actualización: Marzo 2026*

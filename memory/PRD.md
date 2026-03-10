# Intercultura Asistente Virtual - PRD

## Descripción del Producto
Aplicación móvil para escuela de idiomas que enseña Español, Inglés y Portugués siguiendo la metodología Cambridge.

## Stack Tecnológico
- **Frontend**: Expo (React Native) con TypeScript
- **Backend**: FastAPI (Python)
- **Base de Datos**: MongoDB
- **IA**: OpenAI GPT-4o (via Emergent LLM Key)
- **TTS**: OpenAI TTS (via Emergent LLM Key)

## Estado del Contenido Educativo ✅
- **36 cursos** (2 por idioma/nivel × 3 idiomas × 6 niveles)
- **108 lecciones** (3 por curso)
- **180 flashcards** (10 por idioma/nivel con pronunciación)

### Cursos por Idioma
| Idioma | Cursos Básicos | Cursos Prácticos |
|--------|---------------|------------------|
| Español | 6 (A1-C2) | 6 (Práctico, Conversación, Viajeros, Negocios, Académico, Literario) |
| Inglés | 6 (A1-C2) | 6 (Practical, Conversation, Travelers, Business, Academic, Literary) |
| Portugués | 6 (A1-C2) | 6 (Prático, Conversação, Viajantes, Negócios, Acadêmico, Literário) |

## Funcionalidades Implementadas
- [x] Autenticación (registro/login)
- [x] Dashboard de estudiante
- [x] Cursos por idioma y nivel (36 cursos)
- [x] Sistema de flashcards con audio TTS
- [x] **Ejercicios generados por IA** ✅ FUNCIONANDO
- [x] Revisión de respuestas (correcto/incorrecto)
- [x] Branding Intercultura (logo, colores)

## API Endpoints
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login
- `GET /api/courses` - Listar cursos
- `GET /api/flashcards` - Listar flashcards
- `POST /api/tts/generate` - Generar audio de pronunciación
- `POST /api/ai/generate-exercise` - Generar ejercicios con IA (sin auth requerida)
- `POST /api/ai/explain` - Explicar conceptos con IA

## Problemas Resueltos en Esta Sesión
- [x] IA daba error 403 → Ahora funciona sin autenticación obligatoria
- [x] Contenido C1/C2 incompleto → Ahora tiene contenido completo
- [x] Cursos mezclados por idioma → Ahora cada idioma tiene su contenido correcto

## Tareas Pendientes
- [ ] Botón de registro no responde (requiere feedback usuario)
- [ ] Sesión no persiste al recargar página
- [ ] Implementar tipografía "Aller"
- [ ] Rol de profesor

## Credenciales de Prueba
- Email: newtest@test.com
- Password: testpassword

---
*Última actualización: Diciembre 2025*

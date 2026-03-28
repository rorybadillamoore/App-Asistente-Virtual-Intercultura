# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, German, and French across proficiency levels A1-C2.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises), OpenAI TTS tts-1-hd (flashcard audio) via Emergent LLM Key

## Textbook Alignment
- **Spanish**: Instituto Cervantes curriculum
- **English**: Cambridge methodology
- **Portuguese**: Novo Avenida Brasil (Vol 1=A1, Vol 2=A2, Vol 3=B1, Advanced=B2-C2)
- **German**: Menschen (Hueber) A1-B1 + advanced B2-C2
- **French**: Alter Ego+ (Hachette FLE) A1-C2

## Content Stats
- 5 languages x 6 levels = 30 courses
- 6 lessons per course = 180 lessons (ALL with rich educational content 450+ chars)
- Each lesson: vocabulary items + grammar points + rich content
- 300 flashcards, 30 quizzes (randomized answers), AI exercises

## Content Quality Verification (2026-03-28)
| Language | Lessons | Min chars | Avg chars | Status |
|----------|---------|-----------|-----------|--------|
| Spanish | 36 | 643 | 801 | Rich content |
| English | 36 | 719 | 843 | Rich content |
| Portuguese | 36 | 760 | 957 | ENRICHED |
| German | 36 | 925 | 1184 | ENRICHED |
| French | 36 | 1047 | 1324 | ENRICHED |

## What's Been Implemented
- [x] Full authentication (login, register, logout, change password)
- [x] 180 lessons with textbook-aligned RICH content (all languages verified)
- [x] 300 flashcards with TTS audio
- [x] 30 quizzes with randomized answer positions
- [x] AI exercises with GPT-4o
- [x] Student + Teacher dashboards
- [x] Profile: Mi Progreso, Configuracion (change password), Ayuda (contact info), Acerca de
- [x] PWA icons (99% fill, green background) + manifest.json
- [x] Home buttons on all sub-pages
- [x] "Contenido" naming (not "Leccion")
- [x] Quizzes header: "Tu Promedio de Quizzes Completados"
- [x] Portuguese content enrichment (grammar, vocabulary, dialogues, cultural notes)
- [x] German content enrichment (conjugations, vocabulary, cultural notes, dialogues)
- [x] French content enrichment (grammar rules, vocabulary, cultural references, examples)
- [x] DB validation: ALL 180 lessons pass minimum 450 char requirement

## Remaining Tasks
- P2: Custom "Aller" typeface
- P2: Mobile app store builds (.apk/.ipa)

## Deployment
User must click "Deploy" in Emergent platform for production URL.

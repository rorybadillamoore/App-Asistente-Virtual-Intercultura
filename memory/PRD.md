# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, and German across proficiency levels A1-C2. Features courses, flashcards with TTS audio, AI-powered quizzes/exercises, and separate student/teacher roles.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth state
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises via Emergent LLM Key), OpenAI TTS tts-1-hd (flashcard audio via Emergent LLM Key)

## Core Requirements
- 4 languages x 6 levels = 24 courses, each with 6 lessons
- 10 flashcards per language/level (240 total)
- 1 quiz per course with 10 questions each (24 quizzes)
- AI exercise generation (grammar, vocabulary, reading, writing)
- TTS audio pronunciation for flashcards
- Student and Teacher roles with separate dashboards
- Intercultura branding (logo, colors, no Emergent/Polyglot references)

## What's Been Implemented (as of 2026-03-27)
- [x] Authentication (login, register, logout) - fully stable
- [x] Database seeded: 24 courses, 144 lessons, 240 flashcards, 24 quizzes
- [x] All 4 language x 6 level combinations have complete content
- [x] Courses with 6 lessons each, detailed content with vocabulary and grammar
- [x] Flashcards with flip animation and TTS audio playback
- [x] TTS with language-specific voice optimization (nova voice, language context prefixes)
- [x] Quizzes with 10 questions each, submission and scoring
- [x] AI exercise generation with GPT-4o (randomized, unique per request)
- [x] Student dashboard with progress tracking by language
- [x] Teacher dashboard with student list and statistics
- [x] Profile page with user info, stats (4 Idiomas, 6 Niveles), and logout
- [x] Intercultura branding: logo in all assets, PWA config, favicon, title
- [x] Removed all Emergent/Polyglot placeholder text
- [x] Optimized N+1 queries in teacher dashboard
- [x] Fixed infinite loop bug in auth state management
- [x] Favicon link added in +html.tsx for web

## Backend Testing
- 27/27 API tests passing (auth, courses, lessons, flashcards, quizzes, TTS, progress, teacher)

## Known Limitations
- Favicon may not show in Expo dev mode (works in production build)
- French courses exist in DB but not shown in UI (only 4 languages in theme)
- Custom "Aller" font not yet implemented

## Remaining Tasks
### P1
- Custom "Aller" typeface implementation

### P2
- Mobile app store deployment preparation (.apk/.ipa)

## Deployment
- User must click "Deploy" button in Emergent platform UI to get permanent production URL
- The preview URL requires the agent session to be active
- Production deployment gives a fixed URL that works 24/7

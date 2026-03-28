# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, German, and French across proficiency levels A1-C2.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises), OpenAI TTS tts-1-hd (flashcard audio) via Emergent LLM Key

## Core Data
- 5 languages x 6 levels = 30 courses
- 6 lessons per course = 180 lessons (all enriched with real educational content)
- 10 flashcards per language/level = 300 total
- 1 quiz per course with 10 questions = 30 quizzes

## What's Been Implemented

### Authentication
- [x] Login, Register, Logout (stable - Zustand + AsyncStorage)
- [x] Student and Teacher roles
- [x] Change password (POST /api/auth/change-password)

### Content (100% verified - zero placeholders)
- [x] 30 courses across 5 languages x 6 levels
- [x] 180 enriched lessons with vocabulary (6+ items) and grammar points
- [x] 300 flashcards with TTS audio
- [x] 30 quizzes with 10 questions each
- [x] AI exercises via GPT-4o

### Profile Section (Updated 2026-03-28)
- [x] Mi Progreso: real stats from backend
- [x] Configuracion: functional change password form (3 inputs, validation, API call)
- [x] Ayuda: real Intercultura contact info (phone, WhatsApp, email, website, 2 campus locations, FAQ)
- [x] Acerca de: school info (founded 1993, methodology, programs, version)

### Branding
- [x] Intercultura logo on all assets (favicon, PWA icon, splash, adaptive icon)
- [x] PWA manifest.json with Intercultura name, theme color, icon
- [x] apple-touch-icon and meta tags for mobile install
- [x] No Emergent/Polyglot references anywhere

### Navigation
- [x] Home buttons on all sub-pages (course, lesson, quiz, ai-exercise, flashcard-session)
- [x] Tab navigation: Inicio, Cursos, Quizzes, Flashcards, IA, Perfil

## Content Validation (2026-03-28)
- Lessons: 30/30 OK (0 placeholders)
- Flashcards: 30/30 OK
- Quizzes: 30/30 OK

## Testing Results
- iteration_1.json: Initial feature tests (PASS)
- iteration_2.json: Content and navigation tests (PASS)
- iteration_3.json: Profile features + change password + PWA (10/10 backend, 100% frontend PASS)

## Remaining Tasks
### P1
- Custom "Aller" typeface across frontend
### P2
- Mobile app store builds (.apk/.ipa)

## Deployment
User must click "Deploy" in Emergent platform for production URL.

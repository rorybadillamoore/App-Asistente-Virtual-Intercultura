# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, German, and French across proficiency levels A1-C2.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises), OpenAI TTS tts-1-hd (flashcard audio) via Emergent LLM Key

## What's Been Implemented

### Authentication
- [x] Login, Register, Logout (stable - Zustand + AsyncStorage)
- [x] Student and Teacher roles
- [x] Change password (POST /api/auth/change-password)

### Content (100% verified - zero placeholders)
- [x] 30 courses across 5 languages x 6 levels
- [x] 180 enriched lessons ("Contenido" naming) with vocabulary (6+ items) and grammar
- [x] 300 flashcards with TTS audio
- [x] 30 quizzes with 10 questions each, answers randomized across positions A-D
- [x] AI exercises via GPT-4o

### Profile Section
- [x] Mi Progreso: real stats from backend
- [x] Configuracion: functional change password form
- [x] Ayuda: real Intercultura contact info (phone, WhatsApp, email, website, 2 campus locations, FAQ)
- [x] Acerca de: school info (founded 1993, methodology, version)

### Branding & PWA
- [x] Intercultura logo on all assets (favicon, PWA icon, splash, adaptive icon)
- [x] PWA icons with green background, logo filling 99% of space (no white gaps)
- [x] PWA manifest.json with proper icons (192x192, 512x512, maskable)
- [x] apple-touch-icon (180x180) for iOS home screen
- [x] No Emergent/Polyglot references anywhere

### Navigation
- [x] Home buttons on all sub-pages
- [x] Tab navigation: Inicio, Cursos, Quizzes, Flashcards, IA, Perfil

### Quizzes
- [x] Header: "Tu Promedio de Quizzes Completados"
- [x] All 300 questions have randomized answer positions (A=79, B=69, C=77, D=75)
- [x] Lessons renamed to "Contenido/Content/Conteúdo/Inhalt/Contenu" across all languages

## Remaining Tasks
### P1
- Custom "Aller" typeface
### P2
- Mobile app store builds (.apk/.ipa)

## Deployment
User must click "Deploy" in Emergent platform for production URL.

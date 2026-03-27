# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, German, and French across proficiency levels A1-C2.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises), OpenAI TTS tts-1-hd (flashcard audio) via Emergent LLM Key

## Core Data
- 5 languages × 6 levels = 30 courses
- 6 lessons per course = 180 lessons (enriched with Cambridge-style content)
- 10 flashcards per language/level = 300 total
- 1 quiz per course with 10 questions = 30 quizzes
- AI exercise generation with GPT-4o

## What's Been Implemented (as of 2026-03-27)
- [x] Authentication (login, register, logout) - stable
- [x] Database: 30 courses, 180 enriched lessons, 300 flashcards, 30 quizzes
- [x] 5 languages (Spanish, English, Portuguese, German, French) × 6 levels
- [x] All lesson content enriched with detailed educational material, vocabulary (6+ items), grammar points
- [x] Flashcards with TTS audio (language-specific voice + context prefixes)
- [x] Quizzes with scoring
- [x] AI exercises with GPT-4o
- [x] Student + Teacher dashboards
- [x] Profile with Mi Progreso (shows real progress data), 5 Idiomas, logout
- [x] Intercultura branding throughout (logos, favicon, title, no Emergent refs)
- [x] 33/33 backend tests passing, 100% frontend verified

## Remaining Tasks
### P1
- Custom "Aller" typeface
### P2
- Mobile app store deployment (.apk/.ipa)

## Deployment
User must click "Deploy" button in Emergent platform to get production URL (24/7, no agent needed).

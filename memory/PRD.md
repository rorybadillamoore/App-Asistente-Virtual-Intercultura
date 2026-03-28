# Intercultura Asistente Virtual - PRD

## Problem Statement
Mobile/web application for Intercultura Costa Rica language school. Supports Spanish, English, Portuguese, German, and French across proficiency levels A1-C2.

## Architecture
- **Frontend**: React Native (Expo) with Expo Router, Zustand for auth
- **Backend**: FastAPI + PyMongo (Motor async)
- **Database**: MongoDB Atlas
- **Integrations**: OpenAI GPT-4o (AI exercises), OpenAI TTS tts-1-hd (flashcard audio) via Emergent LLM Key

## Textbook Alignment (Updated 2026-03-28)
- **Portuguese**: Novo Avenida Brasil (Vol 1=A1, Vol 2=A2, Vol 3=B1, Advanced=B2-C2)
- **German**: Menschen (Hueber) A1-B1 + advanced B2-C2
- **French**: Alter Ego+ (Hachette FLE) A1-C2

## Content Stats
- 5 languages x 6 levels = 30 courses
- 6 lessons per course = 180 lessons
- Each lesson: 6 vocabulary items + 3 grammar points + rich content
- 300 flashcards, 30 quizzes (randomized answers), AI exercises

## What's Been Implemented
- [x] Full authentication (login, register, logout, change password)
- [x] 180 lessons with textbook-aligned content (PT/DE/FR updated 2026-03-28)
- [x] 300 flashcards with TTS audio
- [x] 30 quizzes with randomized answer positions
- [x] AI exercises with GPT-4o
- [x] Student + Teacher dashboards
- [x] Profile: Mi Progreso, Configuracion (change password), Ayuda (contact info), Acerca de
- [x] PWA icons (99% fill, green background) + manifest.json
- [x] Home buttons on all sub-pages
- [x] "Contenido" naming (not "Leccion")
- [x] Quizzes header: "Tu Promedio de Quizzes Completados"

## Remaining Tasks
- P1: Custom "Aller" typeface
- P2: Mobile app store builds (.apk/.ipa)

## Deployment
User must click "Deploy" in Emergent platform for production URL.

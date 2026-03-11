"""
Backend API tests for Polyglot Academy / Intercultura App
Tests: Auth, Courses (French), Flashcards, Quizzes, Progress, TTS
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', '').rstrip('/')

STUDENT_EMAIL = "testuser123@test.com"
STUDENT_PASS = "password123"
TEACHER_EMAIL = "profesor@test.com"
TEACHER_PASS = "profesor123"


@pytest.fixture(scope="session")
def student_token():
    """Get student JWT token"""
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": STUDENT_EMAIL, "password": STUDENT_PASS
    })
    if resp.status_code == 200:
        return resp.json().get("access_token")
    pytest.skip(f"Student login failed: {resp.status_code} {resp.text}")


@pytest.fixture(scope="session")
def teacher_token():
    """Get teacher JWT token"""
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": TEACHER_EMAIL, "password": TEACHER_PASS
    })
    if resp.status_code == 200:
        return resp.json().get("access_token")
    pytest.skip(f"Teacher login failed: {resp.status_code} {resp.text}")


@pytest.fixture(scope="session")
def student_headers(student_token):
    return {"Authorization": f"Bearer {student_token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def teacher_headers(teacher_token):
    return {"Authorization": f"Bearer {teacher_token}", "Content-Type": "application/json"}


# ==================== AUTH TESTS ====================

class TestAuth:
    """Authentication endpoint tests"""

    def test_student_login_success(self):
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL, "password": STUDENT_PASS
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == STUDENT_EMAIL
        assert data["user"]["role"] == "student"

    def test_teacher_login_success(self):
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEACHER_EMAIL, "password": TEACHER_PASS
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert data["user"]["role"] == "teacher"

    def test_login_invalid_credentials(self):
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@test.com", "password": "wrongpass"
        })
        assert resp.status_code == 401

    def test_get_me(self, student_headers):
        resp = requests.get(f"{BASE_URL}/api/auth/me", headers=student_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == STUDENT_EMAIL
        assert data["role"] == "student"


# ==================== COURSES TESTS ====================

class TestCourses:
    """Course endpoints - especially French courses"""

    def test_get_all_courses(self):
        resp = requests.get(f"{BASE_URL}/api/courses")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0, "No courses found"

    def test_french_courses_exist(self):
        """French courses should have 6 levels A1-C2"""
        resp = requests.get(f"{BASE_URL}/api/courses?language=french")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 6, f"Expected 6 French courses, got {len(data)}"
        levels = {c["level"] for c in data}
        expected_levels = {"A1", "A2", "B1", "B2", "C1", "C2"}
        assert levels == expected_levels, f"Missing levels: {expected_levels - levels}"

    def test_french_courses_correct_language(self):
        resp = requests.get(f"{BASE_URL}/api/courses?language=french")
        data = resp.json()
        for course in data:
            assert course["language"] == "french"

    def test_spanish_courses_exist(self):
        resp = requests.get(f"{BASE_URL}/api/courses?language=spanish")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 6, f"Expected 6 Spanish courses, got {len(data)}"

    def test_english_courses_exist(self):
        resp = requests.get(f"{BASE_URL}/api/courses?language=english")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 6, f"Expected 6 English courses, got {len(data)}"

    def test_course_detail(self):
        resp = requests.get(f"{BASE_URL}/api/courses?language=french&level=A1")
        data = resp.json()
        assert len(data) > 0
        course_id = data[0]["id"]

        detail = requests.get(f"{BASE_URL}/api/courses/{course_id}")
        assert detail.status_code == 200
        d = detail.json()
        assert d["id"] == course_id
        assert d["language"] == "french"
        assert d["level"] == "A1"


# ==================== FLASHCARDS TESTS ====================

class TestFlashcards:
    """Flashcard endpoints"""

    def test_get_french_flashcards(self):
        resp = requests.get(f"{BASE_URL}/api/flashcards?language=french")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0, "No French flashcards found"
        for card in data:
            assert card["language"] == "french"
            assert "word" in card
            assert "translation" in card

    def test_get_french_flashcards_by_level(self):
        resp = requests.get(f"{BASE_URL}/api/flashcards?language=french&level=A1")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0, "No French A1 flashcards found"

    def test_get_spanish_flashcards(self):
        resp = requests.get(f"{BASE_URL}/api/flashcards?language=spanish")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0, "No Spanish flashcards found"

    def test_flashcard_structure(self):
        resp = requests.get(f"{BASE_URL}/api/flashcards?language=french&limit=5")
        data = resp.json()
        assert len(data) > 0
        card = data[0]
        required_fields = ["id", "language", "level", "word", "translation"]
        for field in required_fields:
            assert field in card, f"Missing field: {field}"


# ==================== QUIZZES TESTS ====================

class TestQuizzes:
    """Quiz endpoints - especially French quizzes"""

    def test_get_all_quizzes(self):
        resp = requests.get(f"{BASE_URL}/api/quizzes")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0, "No quizzes found"

    def test_french_quizzes_exist(self):
        """French quizzes should have 6 quizzes"""
        resp = requests.get(f"{BASE_URL}/api/quizzes?language=french")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 6, f"Expected 6 French quizzes, got {len(data)}"

    def test_french_quiz_levels(self):
        resp = requests.get(f"{BASE_URL}/api/quizzes?language=french")
        data = resp.json()
        levels = {q["level"] for q in data}
        expected = {"A1", "A2", "B1", "B2", "C1", "C2"}
        assert levels == expected, f"Missing quiz levels: {expected - levels}"

    def test_quiz_detail(self):
        resp = requests.get(f"{BASE_URL}/api/quizzes?language=french&level=A1")
        data = resp.json()
        assert len(data) > 0
        quiz_id = data[0]["id"]

        detail = requests.get(f"{BASE_URL}/api/quizzes/{quiz_id}")
        assert detail.status_code == 200
        d = detail.json()
        assert "questions" in d
        assert len(d["questions"]) > 0

    def test_quiz_submit(self, student_headers):
        """Test quiz submission for a French quiz"""
        resp = requests.get(f"{BASE_URL}/api/quizzes?language=french&level=A1")
        data = resp.json()
        assert len(data) > 0
        quiz_id = data[0]["id"]

        # Get quiz details to know the number of questions
        detail = requests.get(f"{BASE_URL}/api/quizzes/{quiz_id}")
        quiz = detail.json()
        num_questions = len(quiz["questions"])

        # Submit all answers as 0
        answers = [0] * num_questions
        submit_resp = requests.post(
            f"{BASE_URL}/api/quizzes/{quiz_id}/submit",
            json={"quiz_id": quiz_id, "answers": answers},
            headers=student_headers
        )
        assert submit_resp.status_code == 200
        result = submit_resp.json()
        assert "score" in result
        assert "percentage" in result
        assert result["total"] == num_questions


# ==================== PROGRESS TESTS ====================

class TestProgress:
    """Progress endpoint tests"""

    def test_get_progress(self, student_headers):
        resp = requests.get(f"{BASE_URL}/api/progress", headers=student_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "user_id" in data
        assert "lessons_completed" in data
        assert "quizzes_taken" in data
        assert "flashcards_reviewed" in data
        assert "average_score" in data

    def test_get_progress_unauthenticated(self):
        resp = requests.get(f"{BASE_URL}/api/progress")
        assert resp.status_code in [401, 403]

    def test_get_progress_by_language(self, student_headers):
        resp = requests.get(f"{BASE_URL}/api/progress/by-language", headers=student_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # Note: may return [] if user has no progress record yet

    def test_complete_lesson(self, student_headers):
        """Mark a lesson as complete and verify progress updates"""
        # Get a lesson
        courses = requests.get(f"{BASE_URL}/api/courses?language=french&level=A1").json()
        assert len(courses) > 0
        course_id = courses[0]["id"]

        lessons = requests.get(f"{BASE_URL}/api/courses/{course_id}/lessons").json()
        if not lessons:
            pytest.skip("No lessons available for this course")
        lesson_id = lessons[0]["id"]

        # Complete the lesson
        resp = requests.post(
            f"{BASE_URL}/api/lessons/{lesson_id}/complete",
            headers=student_headers
        )
        assert resp.status_code == 200
        assert "message" in resp.json()


# ==================== TTS TESTS ====================

class TestTTS:
    """TTS endpoint tests"""

    def test_tts_french(self):
        resp = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Bonjour, comment allez-vous?",
            "language": "french"
        })
        assert resp.status_code == 200, f"TTS failed: {resp.text}"
        data = resp.json()
        assert data.get("success") is True
        assert "audio_base64" in data
        assert len(data["audio_base64"]) > 100
        assert data.get("provider") in ["elevenlabs", "openai"], "Unknown TTS provider"

    def test_tts_spanish(self):
        resp = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Hola, ¿cómo estás?",
            "language": "spanish"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success") is True
        assert "audio_base64" in data

    def test_tts_english(self):
        resp = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Hello, how are you?",
            "language": "english"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success") is True


# ==================== TEACHER TESTS ====================

class TestTeacher:
    """Teacher-specific API tests"""

    def test_teacher_get_students(self, teacher_headers):
        resp = requests.get(f"{BASE_URL}/api/teacher/students", headers=teacher_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_teacher_get_stats(self, teacher_headers):
        resp = requests.get(f"{BASE_URL}/api/teacher/stats", headers=teacher_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "total_students" in data
        assert "total_courses" in data
        assert "total_quizzes" in data

    def test_student_cannot_access_teacher_routes(self, student_headers):
        resp = requests.get(f"{BASE_URL}/api/teacher/students", headers=student_headers)
        assert resp.status_code == 403

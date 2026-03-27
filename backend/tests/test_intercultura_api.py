"""
Intercultura API Tests
Tests for language school web app supporting Spanish, English, Portuguese, and German
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://intercultura-dev.preview.emergentagent.com').rstrip('/')

# Test credentials
STUDENT_EMAIL = "testuser123@test.com"
STUDENT_PASSWORD = "password123"
TEACHER_EMAIL = "profesor@test.com"
TEACHER_PASSWORD = "profesor123"


class TestHealthCheck:
    """Health check endpoint tests"""
    
    def test_health_endpoint(self):
        """Test that health endpoint returns healthy status"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✓ Health check passed")


class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_student_login_success(self):
        """Test student login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == STUDENT_EMAIL
        assert data["user"]["role"] == "student"
        assert data["user"]["name"] == "Test User"
        print("✓ Student login successful")
    
    def test_teacher_login_success(self):
        """Test teacher login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEACHER_EMAIL,
            "password": TEACHER_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["role"] == "teacher"
        assert data["user"]["name"] == "Profesor Demo"
        print("✓ Teacher login successful")
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials returns 401"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print("✓ Invalid credentials rejected correctly")
    
    def test_auth_me_with_token(self):
        """Test /auth/me endpoint with valid token"""
        # First login to get token
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        token = login_response.json()["access_token"]
        
        # Test /auth/me
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == STUDENT_EMAIL
        print("✓ Auth me endpoint works with token")


class TestCourses:
    """Course endpoint tests - 4 languages x 6 levels = 24 courses expected"""
    
    def test_get_all_courses(self):
        """Test getting all courses"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        courses = response.json()
        assert isinstance(courses, list)
        # Should have 24 courses (4 languages x 6 levels) - French courses should be in DB but filtered by frontend
        assert len(courses) >= 24, f"Expected at least 24 courses, got {len(courses)}"
        print(f"✓ Got {len(courses)} courses")
    
    def test_get_courses_by_language_spanish(self):
        """Test filtering courses by Spanish language"""
        response = requests.get(f"{BASE_URL}/api/courses?language=spanish")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 6, f"Expected 6 Spanish courses, got {len(courses)}"
        for course in courses:
            assert course["language"] == "spanish"
        print("✓ Spanish courses filter works (6 courses)")
    
    def test_get_courses_by_language_english(self):
        """Test filtering courses by English language"""
        response = requests.get(f"{BASE_URL}/api/courses?language=english")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 6, f"Expected 6 English courses, got {len(courses)}"
        print("✓ English courses filter works (6 courses)")
    
    def test_get_courses_by_language_portuguese(self):
        """Test filtering courses by Portuguese language"""
        response = requests.get(f"{BASE_URL}/api/courses?language=portuguese")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 6, f"Expected 6 Portuguese courses, got {len(courses)}"
        print("✓ Portuguese courses filter works (6 courses)")
    
    def test_get_courses_by_language_german(self):
        """Test filtering courses by German language"""
        response = requests.get(f"{BASE_URL}/api/courses?language=german")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 6, f"Expected 6 German courses, got {len(courses)}"
        print("✓ German courses filter works (6 courses)")
    
    def test_get_courses_by_level(self):
        """Test filtering courses by level A1"""
        response = requests.get(f"{BASE_URL}/api/courses?level=A1")
        assert response.status_code == 200
        courses = response.json()
        # Should have at least 4 A1 courses (one per language)
        assert len(courses) >= 4, f"Expected at least 4 A1 courses, got {len(courses)}"
        for course in courses:
            assert course["level"] == "A1"
        print(f"✓ Level A1 filter works ({len(courses)} courses)")
    
    def test_course_has_lessons(self):
        """Test that courses have lesson_count field"""
        response = requests.get(f"{BASE_URL}/api/courses?language=spanish&level=A1")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) > 0
        course = courses[0]
        assert "lesson_count" in course
        assert course["lesson_count"] == 6, f"Expected 6 lessons, got {course['lesson_count']}"
        print("✓ Course has 6 lessons")


class TestLessons:
    """Lesson endpoint tests"""
    
    def test_get_lessons_for_course(self):
        """Test getting lessons for a specific course"""
        # First get a course
        courses_response = requests.get(f"{BASE_URL}/api/courses?language=spanish&level=A1")
        course_id = courses_response.json()[0]["id"]
        
        # Get lessons
        response = requests.get(f"{BASE_URL}/api/courses/{course_id}/lessons")
        assert response.status_code == 200
        lessons = response.json()
        assert isinstance(lessons, list)
        assert len(lessons) == 6, f"Expected 6 lessons, got {len(lessons)}"
        
        # Verify lesson structure
        lesson = lessons[0]
        assert "id" in lesson
        assert "title" in lesson
        assert "content" in lesson
        assert "vocabulary" in lesson
        print("✓ Got 6 lessons for course with correct structure")


class TestFlashcards:
    """Flashcard endpoint tests"""
    
    def test_get_flashcards_spanish_a1(self):
        """Test getting Spanish A1 flashcards"""
        response = requests.get(f"{BASE_URL}/api/flashcards?language=spanish&level=A1")
        assert response.status_code == 200
        flashcards = response.json()
        assert isinstance(flashcards, list)
        assert len(flashcards) >= 10, f"Expected at least 10 flashcards, got {len(flashcards)}"
        
        # Verify flashcard structure
        card = flashcards[0]
        assert "word" in card
        assert "translation" in card
        assert "example" in card
        print(f"✓ Got {len(flashcards)} Spanish A1 flashcards")
    
    def test_get_flashcards_english(self):
        """Test getting English flashcards"""
        response = requests.get(f"{BASE_URL}/api/flashcards?language=english")
        assert response.status_code == 200
        flashcards = response.json()
        assert len(flashcards) > 0
        print(f"✓ Got {len(flashcards)} English flashcards")
    
    def test_get_flashcards_portuguese(self):
        """Test getting Portuguese flashcards"""
        response = requests.get(f"{BASE_URL}/api/flashcards?language=portuguese")
        assert response.status_code == 200
        flashcards = response.json()
        assert len(flashcards) > 0
        print(f"✓ Got {len(flashcards)} Portuguese flashcards")
    
    def test_get_flashcards_german(self):
        """Test getting German flashcards"""
        response = requests.get(f"{BASE_URL}/api/flashcards?language=german")
        assert response.status_code == 200
        flashcards = response.json()
        assert len(flashcards) > 0
        print(f"✓ Got {len(flashcards)} German flashcards")


class TestQuizzes:
    """Quiz endpoint tests"""
    
    def test_get_quizzes_for_course(self):
        """Test getting quizzes for a course"""
        # Get a Spanish A1 course
        courses_response = requests.get(f"{BASE_URL}/api/courses?language=spanish&level=A1")
        course_id = courses_response.json()[0]["id"]
        
        # Get quizzes
        response = requests.get(f"{BASE_URL}/api/courses/{course_id}/quizzes")
        assert response.status_code == 200
        quizzes = response.json()
        assert isinstance(quizzes, list)
        assert len(quizzes) >= 1, "Expected at least 1 quiz"
        
        # Verify quiz structure
        quiz = quizzes[0]
        assert "id" in quiz
        assert "title" in quiz
        assert "questions" in quiz
        assert len(quiz["questions"]) >= 5, "Expected at least 5 questions"
        print(f"✓ Got quiz with {len(quiz['questions'])} questions")


class TestTTS:
    """Text-to-Speech endpoint tests"""
    
    def test_tts_spanish(self):
        """Test TTS for Spanish"""
        response = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Hola",
            "language": "spanish"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "audio_base64" in data
        assert len(data["audio_base64"]) > 100  # Should have substantial audio data
        print("✓ TTS Spanish works")
    
    def test_tts_english(self):
        """Test TTS for English"""
        response = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Hello",
            "language": "english"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print("✓ TTS English works")
    
    def test_tts_portuguese(self):
        """Test TTS for Portuguese"""
        response = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Olá",
            "language": "portuguese"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print("✓ TTS Portuguese works")
    
    def test_tts_german(self):
        """Test TTS for German"""
        response = requests.post(f"{BASE_URL}/api/tts/generate", json={
            "text": "Hallo",
            "language": "german"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print("✓ TTS German works")


class TestProgress:
    """Progress endpoint tests (requires authentication)"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token for student"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        return response.json()["access_token"]
    
    def test_get_progress(self, auth_token):
        """Test getting user progress"""
        response = requests.get(
            f"{BASE_URL}/api/progress",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "lessons_completed" in data
        assert "flashcards_reviewed" in data
        assert "quizzes_taken" in data
        assert "average_score" in data
        print("✓ Progress endpoint works")
    
    def test_get_progress_by_language(self, auth_token):
        """Test getting progress broken down by language"""
        response = requests.get(
            f"{BASE_URL}/api/progress/by-language",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should have progress for 4 languages
        assert len(data) == 4, f"Expected 4 language progress entries, got {len(data)}"
        languages = [p["language"] for p in data]
        assert "spanish" in languages
        assert "english" in languages
        assert "portuguese" in languages
        assert "german" in languages
        print("✓ Progress by language works (4 languages)")


class TestTeacherEndpoints:
    """Teacher-specific endpoint tests"""
    
    @pytest.fixture
    def teacher_token(self):
        """Get authentication token for teacher"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEACHER_EMAIL,
            "password": TEACHER_PASSWORD
        })
        return response.json()["access_token"]
    
    def test_get_students(self, teacher_token):
        """Test teacher can get student list"""
        response = requests.get(
            f"{BASE_URL}/api/teacher/students",
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        assert response.status_code == 200
        students = response.json()
        assert isinstance(students, list)
        print(f"✓ Teacher can view {len(students)} students")
    
    def test_get_teacher_stats(self, teacher_token):
        """Test teacher can get statistics"""
        response = requests.get(
            f"{BASE_URL}/api/teacher/stats",
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        assert response.status_code == 200
        stats = response.json()
        assert "total_students" in stats
        assert "total_courses" in stats
        assert "total_quizzes" in stats
        print("✓ Teacher stats endpoint works")
    
    def test_student_cannot_access_teacher_endpoints(self):
        """Test that students cannot access teacher endpoints"""
        # Login as student
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        student_token = login_response.json()["access_token"]
        
        # Try to access teacher endpoint
        response = requests.get(
            f"{BASE_URL}/api/teacher/students",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403
        print("✓ Student correctly denied access to teacher endpoints")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

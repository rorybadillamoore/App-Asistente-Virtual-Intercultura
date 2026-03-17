#!/usr/bin/env python3
"""
Backend API Testing Suite for Intercultura Language Learning Platform
Tests all core endpoints including authentication, courses, lessons, flashcards, quizzes, progress, and AI integration.
Specifically designed to test the required features from the review request.
"""

import requests
import json
import sys
from datetime import datetime
import time

# Base URL from frontend environment - Updated for Intercultura
BASE_URL = "https://lingua-hub-56.preview.emergentagent.com/api"

class InterCulturaAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_token = None
        self.user_data = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }
        self.courses_data = []
        self.student_user = None
        self.teacher_user = None
    
    def log_result(self, test_name, success, message):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results["details"].append(f"{status}: {test_name} - {message}")
        if success:
            self.test_results["passed"] += 1
        else:
            self.test_results["failed"] += 1
        print(f"{status}: {test_name} - {message}")
    
    def make_request(self, method, endpoint, data=None, headers=None, params=None):
        """Make HTTP request with proper error handling"""
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        
        if headers:
            default_headers.update(headers)
            
        if self.auth_token:
            default_headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, params=params, timeout=15)
            elif method.upper() == "POST":
                response = requests.post(url, headers=default_headers, json=data, timeout=15)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=default_headers, json=data, timeout=15)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, timeout=15)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
    
    def test_register_test_user(self):
        """Register a test user for authentication testing"""
        print("\n=== Testing User Registration ===")
        timestamp = int(time.time())
        user_data = {
            "email": f"testuser{timestamp}@intercultura.com",
            "password": "TestPass123!",
            "name": "Test User",
            "role": "student"
        }
        
        response = self.make_request("POST", "/auth/register", user_data)
        
        if response is None:
            self.log_result("User Registration", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "access_token" in data and "user" in data:
                    self.auth_token = data["access_token"]
                    self.user_data = data["user"]
                    self.student_user = data["user"]
                    self.log_result("User Registration", True, f"Student {data['user']['name']} registered successfully")
                    return True
                else:
                    self.log_result("User Registration", False, f"Missing required fields in response: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("User Registration", False, "Invalid JSON response")
                return False
        elif response.status_code == 400:
            try:
                error = response.json()
                self.log_result("User Registration", False, f"Registration failed: {error.get('detail', response.text)}")
                return False
            except:
                self.log_result("User Registration", False, f"Registration failed: {response.text}")
                return False
        else:
            self.log_result("User Registration", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_user_login(self):
        """Test user login with the registered user"""
        print("\n=== Testing User Login ===")
        if not self.student_user:
            self.log_result("User Login", False, "No registered user to login with")
            return False
            
        login_data = {
            "email": self.student_user["email"],
            "password": "TestPass123!"
        }
        
        response = self.make_request("POST", "/auth/login", login_data)
        
        if response is None:
            self.log_result("User Login", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "access_token" in data and "user" in data:
                    self.auth_token = data["access_token"]
                    self.user_data = data["user"]
                    self.log_result("User Login", True, f"User {data['user']['name']} logged in successfully")
                    return True
                else:
                    self.log_result("User Login", False, f"Missing required fields in response: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("User Login", False, "Invalid JSON response")
                return False
        else:
            self.log_result("User Login", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_user_profile(self):
        """Test getting current user profile"""
        print("\n=== Testing User Profile (/auth/me) ===")
        if not self.auth_token:
            self.log_result("User Profile", False, "No auth token available")
            return False
        
        response = self.make_request("GET", "/auth/me")
        
        if response is None:
            self.log_result("User Profile", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["id", "email", "name", "role"]
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    self.log_result("User Profile", True, f"Profile retrieved for {data['name']} ({data['role']})")
                    return True
                else:
                    self.log_result("User Profile", False, f"Missing fields: {missing_fields}")
                    return False
            except json.JSONDecodeError:
                self.log_result("User Profile", False, "Invalid JSON response")
                return False
        else:
            self.log_result("User Profile", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_all_courses(self):
        """Test getting all courses - should return 18 courses according to requirements"""
        print("\n=== Testing Get All Courses ===")
        response = self.make_request("GET", "/courses")
        
        if response is None:
            self.log_result("Get All Courses", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.courses_data = data
                    expected_course_count = 18
                    actual_count = len(data)
                    
                    if actual_count >= expected_course_count:
                        self.log_result("Get All Courses", True, f"Retrieved {actual_count} courses (expected {expected_course_count})")
                        
                        # Validate course structure
                        if len(data) > 0:
                            course = data[0]
                            required_fields = ["id", "language", "level", "title", "description", "lesson_count"]
                            missing_fields = [field for field in required_fields if field not in course]
                            if not missing_fields:
                                self.log_result("Course Structure", True, "All required fields present in course data")
                                
                                # Check language distribution
                                languages = {}
                                for course in data:
                                    lang = course.get("language", "unknown")
                                    languages[lang] = languages.get(lang, 0) + 1
                                
                                self.log_result("Language Distribution", True, f"Languages: {dict(languages)}")
                            else:
                                self.log_result("Course Structure", False, f"Missing fields in course: {missing_fields}")
                                
                        return True
                    else:
                        self.log_result("Get All Courses", False, f"Expected {expected_course_count} courses, got {actual_count}")
                        return False
                else:
                    self.log_result("Get All Courses", False, f"Expected list, got: {type(data)}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get All Courses", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get All Courses", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_course_by_id(self):
        """Test getting a specific course by ID"""
        print("\n=== Testing Get Course By ID ===")
        
        if not self.courses_data:
            self.log_result("Get Course By ID", False, "No courses available for testing")
            return False
        
        # Test with the first course
        course_id = self.courses_data[0]["id"]
        response = self.make_request("GET", f"/courses/{course_id}")
        
        if response is None:
            self.log_result("Get Course By ID", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["id", "language", "level", "title", "description", "lesson_count"]
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    self.log_result("Get Course By ID", True, f"Course '{data['title']}' ({data['language']}-{data['level']}) retrieved with {data['lesson_count']} lessons")
                    return True
                else:
                    self.log_result("Get Course By ID", False, f"Missing fields: {missing_fields}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get Course By ID", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get Course By ID", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_lessons_for_course(self):
        """Test getting lessons for a specific course"""
        print("\n=== Testing Get Lessons for Course ===")
        
        if not self.courses_data:
            self.log_result("Get Lessons", False, "No courses available for testing")
            return False
        
        # Test with the first course that has lessons
        course_id = self.courses_data[0]["id"]
        response = self.make_request("GET", f"/courses/{course_id}/lessons")
        
        if response is None:
            self.log_result("Get Lessons", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get Lessons", True, f"Retrieved {len(data)} lessons for course")
                    
                    # Validate lesson structure if lessons exist
                    if len(data) > 0:
                        lesson = data[0]
                        required_fields = ["id", "course_id", "title", "content", "vocabulary", "grammar_points"]
                        missing_fields = [field for field in required_fields if field not in lesson]
                        if not missing_fields:
                            self.log_result("Lesson Structure", True, f"Lesson '{lesson['title']}' has all required fields")
                            
                            # Check if vocabulary has proper structure
                            vocab_count = len(lesson.get("vocabulary", []))
                            grammar_count = len(lesson.get("grammar_points", []))
                            self.log_result("Lesson Content", True, f"Lesson has {vocab_count} vocabulary items, {grammar_count} grammar points")
                        else:
                            self.log_result("Lesson Structure", False, f"Missing fields: {missing_fields}")
                    
                    return True
                else:
                    self.log_result("Get Lessons", False, f"Expected list, got: {type(data)}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get Lessons", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get Lessons", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_flashcards(self):
        """Test getting flashcards - should return 180+ flashcards according to requirements"""
        print("\n=== Testing Get Flashcards ===")
        
        # Test getting flashcards without filters first
        response = self.make_request("GET", "/flashcards", params={"limit": 200})
        
        if response is None:
            self.log_result("Get Flashcards (All)", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    expected_min = 180
                    actual_count = len(data)
                    
                    if actual_count >= expected_min:
                        self.log_result("Get Flashcards (All)", True, f"Retrieved {actual_count} flashcards (expected {expected_min}+)")
                    else:
                        self.log_result("Get Flashcards (All)", False, f"Expected {expected_min}+ flashcards, got {actual_count}")
                        
                    # Test flashcard structure
                    if len(data) > 0:
                        card = data[0]
                        required_fields = ["id", "language", "level", "word", "translation", "example"]
                        missing_fields = [field for field in required_fields if field not in card]
                        if not missing_fields:
                            self.log_result("Flashcard Structure", True, f"Flashcard '{card['word']}' -> '{card['translation']}' has all required fields")
                        else:
                            self.log_result("Flashcard Structure", False, f"Missing fields: {missing_fields}")
                    
                    # Test filtered flashcards for Spanish A1
                    spanish_response = self.make_request("GET", "/flashcards", params={"language": "spanish", "level": "A1", "limit": 50})
                    if spanish_response and spanish_response.status_code == 200:
                        spanish_data = spanish_response.json()
                        self.log_result("Get Spanish A1 Flashcards", True, f"Retrieved {len(spanish_data)} Spanish A1 flashcards")
                        return True
                    else:
                        self.log_result("Get Spanish A1 Flashcards", False, "Failed to get filtered flashcards")
                        
                    return True
                else:
                    self.log_result("Get Flashcards", False, f"Expected list, got: {type(data)}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get Flashcards", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get Flashcards", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_quizzes_for_course(self):
        """Test getting quizzes for a specific course"""
        print("\n=== Testing Get Quizzes for Course ===")
        
        if not self.courses_data:
            self.log_result("Get Quizzes", False, "No courses available for testing")
            return False
        
        # Test with the first course
        course_id = self.courses_data[0]["id"]
        response = self.make_request("GET", f"/courses/{course_id}/quizzes")
        
        if response is None:
            self.log_result("Get Quizzes", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get Quizzes", True, f"Retrieved {len(data)} quizzes for course")
                    
                    # Validate quiz structure if quizzes exist
                    if len(data) > 0:
                        quiz = data[0]
                        required_fields = ["id", "course_id", "title", "questions", "time_limit_minutes"]
                        missing_fields = [field for field in required_fields if field not in quiz]
                        if not missing_fields:
                            questions_count = len(quiz.get("questions", []))
                            self.log_result("Quiz Structure", True, f"Quiz '{quiz['title']}' has {questions_count} questions")
                            
                            # Validate question structure
                            if questions_count > 0:
                                question = quiz["questions"][0]
                                q_required = ["question", "options", "correct_answer"]
                                q_missing = [field for field in q_required if field not in question]
                                if not q_missing:
                                    options_count = len(question.get("options", []))
                                    self.log_result("Question Structure", True, f"Question has {options_count} options")
                                else:
                                    self.log_result("Question Structure", False, f"Missing question fields: {q_missing}")
                        else:
                            self.log_result("Quiz Structure", False, f"Missing fields: {missing_fields}")
                    
                    return True
                else:
                    self.log_result("Get Quizzes", False, f"Expected list, got: {type(data)}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get Quizzes", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get Quizzes", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_progress_tracking(self):
        """Test progress tracking endpoint"""
        print("\n=== Testing Progress Tracking ===")
        if not self.auth_token:
            self.log_result("Progress Tracking", False, "No auth token available")
            return False
        
        response = self.make_request("GET", "/progress")
        
        if response is None:
            self.log_result("Progress Tracking", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["user_id", "courses_started", "lessons_completed", "flashcards_reviewed", "quizzes_taken", "average_score"]
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    self.log_result("Progress Tracking", True, f"Progress: {data['courses_started']} courses, {data['lessons_completed']} lessons, {data['quizzes_taken']} quizzes, {data['average_score']}% avg")
                    
                    # Test progress by language
                    lang_response = self.make_request("GET", "/progress/by-language")
                    if lang_response and lang_response.status_code == 200:
                        lang_data = lang_response.json()
                        if isinstance(lang_data, list):
                            self.log_result("Progress by Language", True, f"Progress data for {len(lang_data)} languages")
                        else:
                            self.log_result("Progress by Language", False, f"Expected list, got: {type(lang_data)}")
                    else:
                        self.log_result("Progress by Language", False, "Failed to get progress by language")
                    
                    return True
                else:
                    self.log_result("Progress Tracking", False, f"Missing fields: {missing_fields}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Progress Tracking", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Progress Tracking", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_ai_exercise_generation(self):
        """Test AI exercise generation with GPT-4"""
        print("\n=== Testing AI Exercise Generation ===")
        
        exercise_request = {
            "language": "spanish",
            "level": "A1", 
            "topic": "greetings",
            "exercise_type": "vocabulary"
        }
        
        response = self.make_request("POST", "/ai/generate-exercise", exercise_request)
        
        if response is None:
            self.log_result("AI Exercise Generation", False, "Request failed - connection error")
            return False
        
        # Allow longer timeout for AI generation
        time.sleep(2)
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "success" in data and data["success"]:
                    if "exercise" in data:
                        exercise = data["exercise"]
                        if "title" in exercise and "questions" in exercise:
                            questions_count = len(exercise.get("questions", []))
                            vocab_count = len(exercise.get("vocabulary", []))
                            self.log_result("AI Exercise Generation", True, f"Generated exercise '{exercise['title']}' with {questions_count} questions, {vocab_count} vocab items")
                            return True
                        elif "raw_content" in exercise:
                            self.log_result("AI Exercise Generation", True, "AI exercise generated (raw format)")
                            return True
                        else:
                            self.log_result("AI Exercise Generation", False, f"Invalid exercise structure: {exercise}")
                            return False
                    else:
                        self.log_result("AI Exercise Generation", False, "Missing exercise data in response")
                        return False
                else:
                    self.log_result("AI Exercise Generation", False, f"AI generation failed: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("AI Exercise Generation", False, "Invalid JSON response")
                return False
        elif response.status_code == 500:
            try:
                error_data = response.json()
                if "AI service not configured" in error_data.get("detail", ""):
                    self.log_result("AI Exercise Generation", False, "AI service not configured (missing EMERGENT_LLM_KEY)")
                    return False
                else:
                    self.log_result("AI Exercise Generation", False, f"Server error: {error_data}")
                    return False
            except:
                self.log_result("AI Exercise Generation", False, f"HTTP 500: {response.text}")
                return False
        else:
            self.log_result("AI Exercise Generation", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_tts_generation(self):
        """Test Text-to-Speech generation"""
        print("\n=== Testing TTS Generation ===")
        
        tts_request = {
            "text": "Hola, ¿cómo estás?",
            "language": "spanish"
        }
        
        response = self.make_request("POST", "/tts/generate", tts_request)
        
        if response is None:
            self.log_result("TTS Generation", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "success" in data and data["success"]:
                    if "audio_base64" in data and "format" in data:
                        provider = data.get("provider", "unknown")
                        self.log_result("TTS Generation", True, f"Audio generated successfully using {provider}")
                        return True
                    else:
                        self.log_result("TTS Generation", False, "Missing audio data in response")
                        return False
                else:
                    self.log_result("TTS Generation", False, f"TTS generation failed: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("TTS Generation", False, "Invalid JSON response")
                return False
        elif response.status_code == 500:
            try:
                error_data = response.json()
                if "TTS service not configured" in error_data.get("detail", ""):
                    self.log_result("TTS Generation", False, "TTS service not configured (missing API keys)")
                    return False
                else:
                    self.log_result("TTS Generation", False, f"Server error: {error_data}")
                    return False
            except:
                self.log_result("TTS Generation", False, f"HTTP 500: {response.text}")
                return False
        else:
            self.log_result("TTS Generation", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests for Intercultura platform"""
        print("🚀 Starting Intercultura Backend API Tests")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Core functionality tests
        tests = [
            self.test_register_test_user,
            self.test_user_login,
            self.test_user_profile,
            self.test_get_all_courses,
            self.test_get_course_by_id,
            self.test_get_lessons_for_course,
            self.test_get_flashcards,
            self.test_get_quizzes_for_course,
            self.test_progress_tracking,
            self.test_ai_exercise_generation,
            self.test_tts_generation
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_result(test.__name__, False, f"Test crashed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 INTERCULTURA BACKEND TEST SUMMARY")
        print("=" * 80)
        
        total_tests = self.test_results["passed"] + self.test_results["failed"]
        pass_rate = (self.test_results["passed"] / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.test_results['passed']} ✅")
        print(f"Failed: {self.test_results['failed']} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.test_results["failed"] > 0:
            print("\n🔍 FAILED TESTS:")
            for detail in self.test_results["details"]:
                if "❌ FAIL" in detail:
                    print(f"  {detail}")
        
        print("\n" + "=" * 80)
        
        return self.test_results["failed"] == 0

if __name__ == "__main__":
    tester = InterCulturaAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All backend tests passed!")
        sys.exit(0)
    else:
        print("💥 Some backend tests failed!")
        sys.exit(1)
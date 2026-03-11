#!/usr/bin/env python3
"""
Backend API Testing Suite for Polyglot Academy Language Learning App
Tests all core endpoints including authentication, courses, lessons, flashcards, quizzes, progress, and AI integration.
"""

import requests
import json
import sys
from datetime import datetime

# Base URL from frontend environment
BASE_URL = "https://costa-rica-lang.preview.emergentagent.com/api"

class PolyglotAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_token = None
        self.user_data = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }
    
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
                response = requests.get(url, headers=default_headers, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=default_headers, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=default_headers, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, timeout=10)
            
            return response
        except requests.exceptions.RequestException as e:
            return None
    
    def test_health_check(self):
        """Test the health endpoint"""
        print("\n=== Testing Health Check ===")
        response = self.make_request("GET", "/health")
        
        if response is None:
            self.log_result("Health Check", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_result("Health Check", True, f"Service healthy, timestamp: {data.get('timestamp', 'N/A')}")
                    return True
                else:
                    self.log_result("Health Check", False, f"Unexpected response format: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Health Check", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("\n=== Testing User Registration ===")
        user_data = {
            "email": "maria.teacher@polyglotacademy.com",
            "password": "SecurePass123!",
            "name": "Maria García",
            "role": "teacher"
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
                    self.log_result("User Registration", True, f"Teacher {data['user']['name']} registered successfully")
                    return True
                else:
                    self.log_result("User Registration", False, f"Missing required fields in response: {data}")
                    return False
            except json.JSONDecodeError:
                self.log_result("User Registration", False, "Invalid JSON response")
                return False
        elif response.status_code == 400:
            # User might already exist, try login instead
            self.log_result("User Registration", False, f"Registration failed (user exists): {response.text}")
            return self.test_user_login()
        else:
            self.log_result("User Registration", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        print("\n=== Testing User Login ===")
        login_data = {
            "email": "maria.teacher@polyglotacademy.com",
            "password": "SecurePass123!"
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
                    self.log_result("User Login", True, f"Teacher {data['user']['name']} logged in successfully")
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
    
    def test_get_courses(self):
        """Test getting all courses"""
        print("\n=== Testing Get Courses ===")
        response = self.make_request("GET", "/courses")
        
        if response is None:
            self.log_result("Get Courses", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get Courses", True, f"Retrieved {len(data)} courses")
                    if len(data) == 0:
                        # Try to seed data first
                        self.seed_sample_data()
                        # Retry getting courses
                        response = self.make_request("GET", "/courses")
                        if response and response.status_code == 200:
                            data = response.json()
                            self.log_result("Get Courses (after seeding)", True, f"Retrieved {len(data)} courses after seeding")
                    return True
                else:
                    self.log_result("Get Courses", False, f"Expected list, got: {type(data)}")
                    return False
            except json.JSONDecodeError:
                self.log_result("Get Courses", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Get Courses", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def test_get_flashcards(self):
        """Test getting flashcards with specific language and level"""
        print("\n=== Testing Get Flashcards ===")
        params = {"language": "spanish", "level": "A1"}
        response = self.make_request("GET", "/flashcards", params=params)
        
        if response is None:
            self.log_result("Get Flashcards", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get Flashcards", True, f"Retrieved {len(data)} Spanish A1 flashcards")
                    # Verify flashcard structure
                    if len(data) > 0:
                        card = data[0]
                        required_fields = ["id", "language", "level", "word", "translation", "example"]
                        missing_fields = [field for field in required_fields if field not in card]
                        if not missing_fields:
                            self.log_result("Flashcard Structure", True, "All required fields present")
                        else:
                            self.log_result("Flashcard Structure", False, f"Missing fields: {missing_fields}")
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
    
    def test_ai_generate_exercise(self):
        """Test AI exercise generation"""
        print("\n=== Testing AI Exercise Generation ===")
        if not self.auth_token:
            self.log_result("AI Exercise Generation", False, "No auth token available")
            return False
        
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
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "success" in data and data["success"]:
                    if "exercise" in data:
                        exercise = data["exercise"]
                        if "title" in exercise or "raw_content" in exercise:
                            self.log_result("AI Exercise Generation", True, "AI exercise generated successfully")
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
                    self.log_result("AI Exercise Generation", False, "AI service not configured (missing API key)")
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
    
    def test_user_profile(self):
        """Test getting current user profile"""
        print("\n=== Testing User Profile ===")
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
                    self.log_result("Progress Tracking", True, f"Progress data: {data['courses_started']} courses, {data['lessons_completed']} lessons, {data['average_score']}% avg score")
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
    
    def seed_sample_data(self):
        """Seed the database with sample data"""
        print("\n=== Seeding Sample Data ===")
        response = self.make_request("POST", "/seed-data")
        
        if response is None:
            self.log_result("Seed Data", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                self.log_result("Seed Data", True, f"Sample data seeded: {data.get('message', 'Success')}")
                return True
            except json.JSONDecodeError:
                self.log_result("Seed Data", False, "Invalid JSON response")
                return False
        else:
            self.log_result("Seed Data", False, f"HTTP {response.status_code}: {response.text}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Polyglot Academy Backend API Tests")
        print(f"Base URL: {self.base_url}")
        print("=" * 60)
        
        # Core functionality tests
        tests = [
            self.test_health_check,
            self.test_user_registration,
            self.test_user_login,
            self.test_user_profile,
            self.test_get_courses,
            self.test_get_flashcards,
            self.test_progress_tracking,
            self.test_ai_generate_exercise
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_result(test.__name__, False, f"Test crashed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
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
        
        print("\n" + "=" * 60)
        
        return self.test_results["failed"] == 0

if __name__ == "__main__":
    tester = PolyglotAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)
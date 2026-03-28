"""
Test suite for verifying lesson content enrichment across all languages and levels.
This test verifies that all 180 lessons (5 languages × 6 levels × 6 lessons) have
content with 450+ characters of real educational material.
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://intercultura-dev.preview.emergentagent.com')

# All languages and levels to test
LANGUAGES = ['spanish', 'english', 'portuguese', 'german', 'french']
LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
MIN_CONTENT_LENGTH = 450
EXPECTED_LESSONS_PER_COURSE = 6


class TestLessonContentEnrichment:
    """Test that all lessons have rich educational content (450+ chars)"""
    
    @pytest.fixture(scope="class")
    def session(self):
        """Create a requests session"""
        return requests.Session()
    
    def test_all_courses_exist(self, session):
        """Verify all 30 courses exist (5 languages × 6 levels)"""
        response = session.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200, f"Failed to get courses: {response.text}"
        
        courses = response.json()
        assert len(courses) >= 30, f"Expected at least 30 courses, got {len(courses)}"
        
        # Verify each language has all 6 levels
        for lang in LANGUAGES:
            lang_courses = [c for c in courses if c['language'] == lang]
            assert len(lang_courses) == 6, f"Expected 6 courses for {lang}, got {len(lang_courses)}"
            
            for level in LEVELS:
                level_courses = [c for c in lang_courses if c['level'] == level]
                assert len(level_courses) == 1, f"Expected 1 course for {lang}-{level}, got {len(level_courses)}"
        
        print(f"✓ All 30 courses exist (5 languages × 6 levels)")
    
    def test_all_courses_have_6_lessons(self, session):
        """Verify each course has exactly 6 lessons"""
        response = session.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        courses = response.json()
        
        courses_with_wrong_count = []
        for course in courses:
            if course['lesson_count'] != EXPECTED_LESSONS_PER_COURSE:
                courses_with_wrong_count.append(
                    f"{course['language']}-{course['level']}: {course['lesson_count']} lessons"
                )
        
        assert len(courses_with_wrong_count) == 0, \
            f"Courses with wrong lesson count: {courses_with_wrong_count}"
        
        print(f"✓ All 30 courses have exactly 6 lessons each (180 total)")
    
    @pytest.mark.parametrize("language", LANGUAGES)
    def test_language_lessons_have_rich_content(self, session, language):
        """Test that all lessons for a language have 450+ character content"""
        # Get courses for this language
        response = session.get(f"{BASE_URL}/api/courses?language={language}")
        assert response.status_code == 200, f"Failed to get {language} courses"
        courses = response.json()
        
        short_content_lessons = []
        total_lessons = 0
        
        for course in courses:
            course_id = course['id']
            level = course['level']
            
            # Get lessons for this course
            lessons_response = session.get(f"{BASE_URL}/api/courses/{course_id}/lessons")
            assert lessons_response.status_code == 200, \
                f"Failed to get lessons for {language}-{level}"
            
            lessons = lessons_response.json()
            
            for lesson in lessons:
                total_lessons += 1
                content_length = len(lesson.get('content', ''))
                
                if content_length < MIN_CONTENT_LENGTH:
                    short_content_lessons.append({
                        'language': language,
                        'level': level,
                        'lesson_title': lesson.get('title', 'Unknown'),
                        'content_length': content_length,
                        'content_preview': lesson.get('content', '')[:100] + '...'
                    })
        
        # Report results
        if short_content_lessons:
            print(f"\n⚠ {language.upper()} - Lessons with content < {MIN_CONTENT_LENGTH} chars:")
            for lesson in short_content_lessons:
                print(f"  - {lesson['level']}: {lesson['lesson_title']} ({lesson['content_length']} chars)")
                print(f"    Preview: {lesson['content_preview']}")
        
        assert len(short_content_lessons) == 0, \
            f"{language.upper()} has {len(short_content_lessons)} lessons with content < {MIN_CONTENT_LENGTH} chars"
        
        print(f"✓ {language.upper()}: All {total_lessons} lessons have {MIN_CONTENT_LENGTH}+ chars")


class TestSpecificLanguageContent:
    """Test specific content quality for Portuguese, German, and French (enriched languages)"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    def _get_sample_lesson(self, session, language, level):
        """Helper to get first lesson of a language/level"""
        response = session.get(f"{BASE_URL}/api/courses?language={language}&level={level}")
        if response.status_code != 200 or not response.json():
            return None
        
        course = response.json()[0]
        lessons_response = session.get(f"{BASE_URL}/api/courses/{course['id']}/lessons")
        if lessons_response.status_code != 200 or not lessons_response.json():
            return None
        
        return lessons_response.json()[0]
    
    def test_german_a1_has_real_content(self, session):
        """Verify German A1 has actual teaching material, not TOC descriptions"""
        lesson = self._get_sample_lesson(session, 'german', 'A1')
        assert lesson is not None, "Could not get German A1 lesson"
        
        content = lesson.get('content', '')
        content_length = len(content)
        
        # Check for educational content markers
        has_grammar = any(word in content.lower() for word in ['verb', 'konjugation', 'sein', 'haben', 'artikel'])
        has_vocabulary = any(word in content.lower() for word in ['vokabular', 'wort', 'wörter', 'bedeutet'])
        has_examples = any(word in content.lower() for word in ['beispiel', 'zum beispiel', "'", '"'])
        
        assert content_length >= MIN_CONTENT_LENGTH, \
            f"German A1 lesson has only {content_length} chars, expected {MIN_CONTENT_LENGTH}+"
        assert has_grammar or has_vocabulary, \
            f"German A1 lesson lacks grammar/vocabulary content"
        
        print(f"✓ German A1: {content_length} chars with grammar/vocabulary content")
        print(f"  Preview: {content[:200]}...")
    
    def test_french_a1_has_real_content(self, session):
        """Verify French A1 has actual teaching material, not TOC descriptions"""
        lesson = self._get_sample_lesson(session, 'french', 'A1')
        assert lesson is not None, "Could not get French A1 lesson"
        
        content = lesson.get('content', '')
        content_length = len(content)
        
        # Check for educational content markers
        has_grammar = any(word in content.lower() for word in ['verbe', 'conjugaison', 'être', 'avoir', 'article'])
        has_vocabulary = any(word in content.lower() for word in ['vocabulaire', 'mot', 'mots', 'signifie'])
        has_examples = any(word in content.lower() for word in ['exemple', 'par exemple', "'", '"'])
        
        assert content_length >= MIN_CONTENT_LENGTH, \
            f"French A1 lesson has only {content_length} chars, expected {MIN_CONTENT_LENGTH}+"
        assert has_grammar or has_vocabulary, \
            f"French A1 lesson lacks grammar/vocabulary content"
        
        print(f"✓ French A1: {content_length} chars with grammar/vocabulary content")
        print(f"  Preview: {content[:200]}...")
    
    def test_portuguese_a1_has_real_content(self, session):
        """Verify Portuguese A1 has actual teaching material, not TOC descriptions"""
        lesson = self._get_sample_lesson(session, 'portuguese', 'A1')
        assert lesson is not None, "Could not get Portuguese A1 lesson"
        
        content = lesson.get('content', '')
        content_length = len(content)
        
        # Check for educational content markers
        has_grammar = any(word in content.lower() for word in ['verbo', 'conjugação', 'ser', 'ter', 'artigo'])
        has_vocabulary = any(word in content.lower() for word in ['vocabulário', 'palavra', 'palavras', 'significa'])
        has_examples = any(word in content.lower() for word in ['exemplo', 'por exemplo', "'", '"'])
        
        assert content_length >= MIN_CONTENT_LENGTH, \
            f"Portuguese A1 lesson has only {content_length} chars, expected {MIN_CONTENT_LENGTH}+"
        assert has_grammar or has_vocabulary, \
            f"Portuguese A1 lesson lacks grammar/vocabulary content"
        
        print(f"✓ Portuguese A1: {content_length} chars with grammar/vocabulary content")
        print(f"  Preview: {content[:200]}...")


class TestLoginAndCoursesAPI:
    """Test login flow and courses API filtering"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    def test_login_with_student_credentials(self, session):
        """Test login with student account"""
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": "testuser123@test.com",
            "password": "password123"
        })
        
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        
        assert 'access_token' in data, "Response missing access_token"
        assert 'user' in data, "Response missing user"
        assert data['user']['email'] == "testuser123@test.com"
        
        print(f"✓ Student login successful: {data['user']['name']}")
        return data['access_token']
    
    def test_login_with_teacher_credentials(self, session):
        """Test login with teacher account"""
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": "profesor@test.com",
            "password": "profesor123"
        })
        
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        
        assert 'access_token' in data, "Response missing access_token"
        assert data['user']['role'] == "teacher"
        
        print(f"✓ Teacher login successful: {data['user']['name']}")
    
    def test_courses_filter_by_language(self, session):
        """Test courses API filtering by language"""
        for language in LANGUAGES:
            response = session.get(f"{BASE_URL}/api/courses?language={language}")
            assert response.status_code == 200
            
            courses = response.json()
            assert len(courses) == 6, f"Expected 6 courses for {language}, got {len(courses)}"
            
            for course in courses:
                assert course['language'] == language, \
                    f"Course language mismatch: expected {language}, got {course['language']}"
        
        print(f"✓ Courses filter by language works for all 5 languages")
    
    def test_courses_filter_by_level(self, session):
        """Test courses API filtering by level"""
        for level in LEVELS:
            response = session.get(f"{BASE_URL}/api/courses?level={level}")
            assert response.status_code == 200
            
            courses = response.json()
            assert len(courses) == 5, f"Expected 5 courses for {level}, got {len(courses)}"
            
            for course in courses:
                assert course['level'] == level, \
                    f"Course level mismatch: expected {level}, got {course['level']}"
        
        print(f"✓ Courses filter by level works for all 6 levels")
    
    def test_courses_filter_by_language_and_level(self, session):
        """Test courses API filtering by both language and level"""
        response = session.get(f"{BASE_URL}/api/courses?language=german&level=A1")
        assert response.status_code == 200
        
        courses = response.json()
        assert len(courses) == 1, f"Expected 1 course for german-A1, got {len(courses)}"
        assert courses[0]['language'] == 'german'
        assert courses[0]['level'] == 'A1'
        
        print(f"✓ Courses filter by language+level works")


class TestLessonDetailAPI:
    """Test lesson detail API returns rich content"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    def test_lesson_detail_returns_content(self, session):
        """Test that lesson detail API returns the content field properly"""
        # Get a German A1 course
        response = session.get(f"{BASE_URL}/api/courses?language=german&level=A1")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) > 0
        
        course_id = courses[0]['id']
        
        # Get lessons
        lessons_response = session.get(f"{BASE_URL}/api/courses/{course_id}/lessons")
        assert lessons_response.status_code == 200
        lessons = lessons_response.json()
        assert len(lessons) > 0
        
        # Get first lesson detail
        lesson_id = lessons[0]['id']
        detail_response = session.get(f"{BASE_URL}/api/lessons/{lesson_id}")
        assert detail_response.status_code == 200
        
        lesson = detail_response.json()
        assert 'content' in lesson, "Lesson detail missing content field"
        assert len(lesson['content']) >= MIN_CONTENT_LENGTH, \
            f"Lesson content too short: {len(lesson['content'])} chars"
        
        print(f"✓ Lesson detail API returns rich content ({len(lesson['content'])} chars)")


class TestContentQualitySampling:
    """Sample content quality across all languages and levels"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    def test_content_length_statistics(self, session):
        """Generate statistics on content length across all lessons"""
        response = session.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        courses = response.json()
        
        stats = {lang: {'total': 0, 'min': float('inf'), 'max': 0, 'sum': 0, 'below_450': 0} 
                 for lang in LANGUAGES}
        
        for course in courses:
            lang = course['language']
            if lang not in LANGUAGES:
                continue
                
            lessons_response = session.get(f"{BASE_URL}/api/courses/{course['id']}/lessons")
            if lessons_response.status_code != 200:
                continue
            
            for lesson in lessons_response.json():
                content_len = len(lesson.get('content', ''))
                stats[lang]['total'] += 1
                stats[lang]['sum'] += content_len
                stats[lang]['min'] = min(stats[lang]['min'], content_len)
                stats[lang]['max'] = max(stats[lang]['max'], content_len)
                if content_len < MIN_CONTENT_LENGTH:
                    stats[lang]['below_450'] += 1
        
        print("\n📊 Content Length Statistics by Language:")
        print("-" * 70)
        all_pass = True
        for lang in LANGUAGES:
            s = stats[lang]
            if s['total'] > 0:
                avg = s['sum'] / s['total']
                status = "✓" if s['below_450'] == 0 else "✗"
                if s['below_450'] > 0:
                    all_pass = False
                print(f"{status} {lang.upper():12} | Lessons: {s['total']:2} | "
                      f"Min: {s['min']:4} | Max: {s['max']:4} | Avg: {avg:6.0f} | "
                      f"Below 450: {s['below_450']}")
        print("-" * 70)
        
        assert all_pass, "Some languages have lessons with content below 450 characters"
        print("✓ All lessons across all languages have 450+ character content")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

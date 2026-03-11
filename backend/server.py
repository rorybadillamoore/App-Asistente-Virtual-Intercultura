from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import bcrypt
import jwt
from bson import ObjectId

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Settings
JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

# Create the main app
app = FastAPI(title="Polyglot Academy API")
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================== MODELS ==================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "student"  # student or teacher

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class CourseCreate(BaseModel):
    language: str  # spanish, english, portuguese
    level: str  # A1, A2, B1, B2, C1, C2
    title: str
    description: str

class CourseResponse(BaseModel):
    id: str
    language: str
    level: str
    title: str
    description: str
    created_by: str
    created_at: datetime
    lesson_count: int = 0

class LessonCreate(BaseModel):
    course_id: str
    title: str
    content: str
    vocabulary: List[dict] = []
    grammar_points: List[str] = []
    order: int = 0

class LessonResponse(BaseModel):
    id: str
    course_id: str
    title: str
    content: str
    vocabulary: List[dict]
    grammar_points: List[str]
    order: int
    created_at: datetime

class FlashcardCreate(BaseModel):
    language: str
    level: str
    word: str
    translation: str
    example: str = ""
    pronunciation: str = ""

class FlashcardResponse(BaseModel):
    id: str
    language: str
    level: str
    word: str
    translation: str
    example: str
    pronunciation: str
    created_by: str
    created_at: datetime

class QuizQuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str = ""

class QuizCreate(BaseModel):
    course_id: str
    title: str
    questions: List[QuizQuestionCreate]
    time_limit_minutes: int = 15

class QuizResponse(BaseModel):
    id: str
    course_id: str
    title: str
    questions: List[dict]
    time_limit_minutes: int
    created_by: str
    created_at: datetime

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[int]

class QuizResult(BaseModel):
    quiz_id: str
    score: int
    total: int
    percentage: float
    results: List[dict]

class ProgressResponse(BaseModel):
    user_id: str
    courses_started: int
    lessons_completed: int
    flashcards_reviewed: int
    quizzes_taken: int
    average_score: float

class AIExerciseRequest(BaseModel):
    language: str
    level: str
    topic: str
    exercise_type: str = "grammar"  # grammar, vocabulary, reading, writing

class FlashcardProgressUpdate(BaseModel):
    flashcard_id: str
    correct: bool

class TTSRequest(BaseModel):
    text: str
    language: str = "spanish"  # spanish, english, portuguese

# ================== AUTH HELPERS ==================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = await db.users.find_one({"_id": ObjectId(payload["user_id"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Optional authentication - allows both authenticated and unauthenticated requests
from fastapi.security import HTTPAuthorizationCredentials as OptionalHTTPAuthorizationCredentials
optional_security = HTTPBearer(auto_error=False)

async def get_current_user_optional(credentials: OptionalHTTPAuthorizationCredentials = Depends(optional_security)):
    """Returns user if authenticated, None otherwise"""
    if not credentials:
        return None
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = await db.users.find_one({"_id": ObjectId(payload["user_id"])})
        return user
    except:
        return None

# ================== AUTH ROUTES ==================

@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = {
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "name": user_data.name,
        "role": user_data.role,
        "created_at": datetime.utcnow()
    }
    result = await db.users.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    # Initialize progress
    await db.progress.insert_one({
        "user_id": user_id,
        "completed_lessons": [],
        "quiz_scores": [],
        "flashcards_reviewed": [],
        "created_at": datetime.utcnow()
    })
    
    token = create_token(user_id, user_data.email, user_data.role)
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            role=user_data.role,
            created_at=user_dict["created_at"]
        )
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(user["_id"])
    token = create_token(user_id, user["email"], user["role"])
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user["email"],
            name=user["name"],
            role=user["role"],
            created_at=user["created_at"]
        )
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        name=current_user["name"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )

# ================== COURSE ROUTES ==================

@api_router.post("/courses", response_model=CourseResponse)
async def create_course(course: CourseCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create courses")
    
    course_dict = {
        "language": course.language.lower(),
        "level": course.level.upper(),
        "title": course.title,
        "description": course.description,
        "created_by": str(current_user["_id"]),
        "created_at": datetime.utcnow()
    }
    result = await db.courses.insert_one(course_dict)
    return CourseResponse(id=str(result.inserted_id), lesson_count=0, **course_dict)

@api_router.get("/courses", response_model=List[CourseResponse])
async def get_courses(language: Optional[str] = None, level: Optional[str] = None):
    query = {}
    if language:
        query["language"] = language.lower()
    if level:
        query["level"] = level.upper()
    
    courses = await db.courses.find(query).to_list(100)
    
    # Optimized: Get all lesson counts in one aggregation query
    lesson_counts = await db.lessons.aggregate([
        {"$group": {"_id": "$course_id", "count": {"$sum": 1}}}
    ]).to_list(None)
    lesson_count_map = {item["_id"]: item["count"] for item in lesson_counts}
    
    result = []
    for course in courses:
        course_id = str(course["_id"])
        result.append(CourseResponse(
            id=course_id,
            language=course["language"],
            level=course["level"],
            title=course["title"],
            description=course["description"],
            created_by=course["created_by"],
            created_at=course["created_at"],
            lesson_count=lesson_count_map.get(course_id, 0)
        ))
    return result

@api_router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    lesson_count = await db.lessons.count_documents({"course_id": course_id})
    return CourseResponse(
        id=str(course["_id"]),
        lesson_count=lesson_count,
        **{k: v for k, v in course.items() if k != "_id"}
    )

# ================== LESSON ROUTES ==================

@api_router.post("/lessons", response_model=LessonResponse)
async def create_lesson(lesson: LessonCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create lessons")
    
    lesson_dict = {
        "course_id": lesson.course_id,
        "title": lesson.title,
        "content": lesson.content,
        "vocabulary": lesson.vocabulary,
        "grammar_points": lesson.grammar_points,
        "order": lesson.order,
        "created_at": datetime.utcnow()
    }
    result = await db.lessons.insert_one(lesson_dict)
    return LessonResponse(id=str(result.inserted_id), **lesson_dict)

@api_router.get("/courses/{course_id}/lessons", response_model=List[LessonResponse])
async def get_lessons(course_id: str):
    lessons = await db.lessons.find({"course_id": course_id}).sort("order", 1).to_list(100)
    return [LessonResponse(id=str(l["_id"]), **{k: v for k, v in l.items() if k != "_id"}) for l in lessons]

@api_router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str):
    lesson = await db.lessons.find_one({"_id": ObjectId(lesson_id)})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonResponse(id=str(lesson["_id"]), **{k: v for k, v in lesson.items() if k != "_id"})

@api_router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(lesson_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    await db.progress.update_one(
        {"user_id": user_id},
        {"$addToSet": {"completed_lessons": lesson_id}},
        upsert=True
    )
    return {"message": "Lesson marked as complete"}

# ================== FLASHCARD ROUTES ==================

@api_router.post("/flashcards", response_model=FlashcardResponse)
async def create_flashcard(card: FlashcardCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create flashcards")
    
    card_dict = {
        "language": card.language.lower(),
        "level": card.level.upper(),
        "word": card.word,
        "translation": card.translation,
        "example": card.example,
        "pronunciation": card.pronunciation,
        "created_by": str(current_user["_id"]),
        "created_at": datetime.utcnow()
    }
    result = await db.flashcards.insert_one(card_dict)
    return FlashcardResponse(id=str(result.inserted_id), **card_dict)

@api_router.get("/flashcards", response_model=List[FlashcardResponse])
async def get_flashcards(language: Optional[str] = None, level: Optional[str] = None, limit: int = 20):
    query = {}
    if language:
        query["language"] = language.lower()
    if level:
        query["level"] = level.upper()
    
    cards = await db.flashcards.find(query).limit(limit).to_list(limit)
    return [FlashcardResponse(id=str(c["_id"]), **{k: v for k, v in c.items() if k != "_id"}) for c in cards]

@api_router.post("/flashcards/review")
async def review_flashcard(update: FlashcardProgressUpdate, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    await db.flashcard_progress.update_one(
        {"user_id": user_id, "flashcard_id": update.flashcard_id},
        {
            "$inc": {"review_count": 1, "correct_count": 1 if update.correct else 0},
            "$set": {"last_reviewed": datetime.utcnow()}
        },
        upsert=True
    )
    await db.progress.update_one(
        {"user_id": user_id},
        {"$addToSet": {"flashcards_reviewed": update.flashcard_id}},
        upsert=True
    )
    return {"message": "Progress updated"}

# ================== QUIZ ROUTES ==================

@api_router.post("/quizzes", response_model=QuizResponse)
async def create_quiz(quiz: QuizCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create quizzes")
    
    quiz_dict = {
        "course_id": quiz.course_id,
        "title": quiz.title,
        "questions": [q.dict() for q in quiz.questions],
        "time_limit_minutes": quiz.time_limit_minutes,
        "created_by": str(current_user["_id"]),
        "created_at": datetime.utcnow()
    }
    result = await db.quizzes.insert_one(quiz_dict)
    return QuizResponse(id=str(result.inserted_id), **quiz_dict)

@api_router.get("/courses/{course_id}/quizzes", response_model=List[QuizResponse])
async def get_quizzes(course_id: str):
    quizzes = await db.quizzes.find({"course_id": course_id}).to_list(100)
    return [QuizResponse(id=str(q["_id"]), **{k: v for k, v in q.items() if k != "_id"}) for q in quizzes]

@api_router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: str):
    quiz = await db.quizzes.find_one({"_id": ObjectId(quiz_id)})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return QuizResponse(id=str(quiz["_id"]), **{k: v for k, v in quiz.items() if k != "_id"})

@api_router.post("/quizzes/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(quiz_id: str, submission: QuizSubmission, current_user: dict = Depends(get_current_user)):
    quiz = await db.quizzes.find_one({"_id": ObjectId(quiz_id)})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    questions = quiz["questions"]
    if len(submission.answers) != len(questions):
        raise HTTPException(status_code=400, detail="Answer count mismatch")
    
    results = []
    correct = 0
    for i, (q, a) in enumerate(zip(questions, submission.answers)):
        is_correct = a == q["correct_answer"]
        if is_correct:
            correct += 1
        results.append({
            "question": q["question"],
            "your_answer": a,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })
    
    score_percentage = (correct / len(questions)) * 100
    
    # Save to progress
    user_id = str(current_user["_id"])
    await db.progress.update_one(
        {"user_id": user_id},
        {"$push": {"quiz_scores": {"quiz_id": quiz_id, "score": score_percentage, "date": datetime.utcnow()}}},
        upsert=True
    )
    
    return QuizResult(
        quiz_id=quiz_id,
        score=correct,
        total=len(questions),
        percentage=score_percentage,
        results=results
    )

# ================== TEACHER ROUTES ==================

class StudentProgress(BaseModel):
    user_id: str
    name: str
    email: str
    lessons_completed: int
    quizzes_taken: int
    average_score: float
    flashcards_reviewed: int

@api_router.get("/teacher/students", response_model=List[StudentProgress])
async def get_students(current_user: dict = Depends(get_current_user)):
    """Get all students and their progress (teacher only)"""
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view students")
    
    students = await db.users.find({"role": "student"}).to_list(100)
    result = []
    
    for student in students:
        student_id = str(student["_id"])
        progress = await db.progress.find_one({"user_id": student_id})
        
        if progress:
            quiz_scores = progress.get("quiz_scores", [])
            avg_score = sum(q["score"] for q in quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
            result.append(StudentProgress(
                user_id=student_id,
                name=student["name"],
                email=student["email"],
                lessons_completed=len(progress.get("completed_lessons", [])),
                quizzes_taken=len(quiz_scores),
                average_score=round(avg_score, 1),
                flashcards_reviewed=len(progress.get("flashcards_reviewed", []))
            ))
        else:
            result.append(StudentProgress(
                user_id=student_id,
                name=student["name"],
                email=student["email"],
                lessons_completed=0,
                quizzes_taken=0,
                average_score=0.0,
                flashcards_reviewed=0
            ))
    
    return result

class LanguageStats(BaseModel):
    language: str
    courses_count: int
    students_active: int
    avg_score: float

@api_router.get("/teacher/stats")
async def get_teacher_stats(current_user: dict = Depends(get_current_user)):
    """Get overall statistics for teachers"""
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view stats")
    
    total_students = await db.users.count_documents({"role": "student"})
    total_courses = await db.courses.count_documents({})
    total_quizzes = await db.quizzes.count_documents({})
    
    # Get average scores from all progress
    all_progress = await db.progress.find({}).to_list(None)
    all_scores = []
    for p in all_progress:
        all_scores.extend([q["score"] for q in p.get("quiz_scores", [])])
    
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0.0
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_quizzes": total_quizzes,
        "average_score": round(avg_score, 1),
        "quizzes_completed": len(all_scores)
    }

# ================== PROGRESS ROUTES ==================

class LanguageProgress(BaseModel):
    language: str
    lessons_completed: int
    quizzes_taken: int
    average_score: float
    flashcards_reviewed: int

@api_router.get("/progress/by-language")
async def get_progress_by_language(current_user: dict = Depends(get_current_user)):
    """Get user progress broken down by language"""
    user_id = str(current_user["_id"])
    progress = await db.progress.find_one({"user_id": user_id})
    
    if not progress:
        return []
    
    # Get completed lessons with their course info
    completed_lessons = progress.get("completed_lessons", [])
    quiz_scores = progress.get("quiz_scores", [])
    
    # Build language stats
    languages = ["spanish", "english", "portuguese", "german"]
    result = []
    
    for lang in languages:
        # Get courses for this language
        courses = await db.courses.find({"language": lang}, {"_id": 1}).to_list(None)
        course_ids = [str(c["_id"]) for c in courses]
        
        # Count lessons completed in this language
        lang_lessons = 0
        for lid in completed_lessons:
            lesson = await db.lessons.find_one({"_id": ObjectId(lid)}, {"course_id": 1})
            if lesson and lesson.get("course_id") in course_ids:
                lang_lessons += 1
        
        # Count quizzes and scores for this language
        lang_quiz_scores = []
        for qs in quiz_scores:
            quiz = await db.quizzes.find_one({"_id": ObjectId(qs["quiz_id"])}, {"course_id": 1})
            if quiz and quiz.get("course_id") in course_ids:
                lang_quiz_scores.append(qs["score"])
        
        avg = sum(lang_quiz_scores) / len(lang_quiz_scores) if lang_quiz_scores else 0.0
        
        # Get flashcards for this language
        flashcards = await db.flashcards.find({"language": lang}, {"_id": 1}).to_list(None)
        flashcard_ids = [str(f["_id"]) for f in flashcards]
        reviewed = len(set(progress.get("flashcards_reviewed", [])) & set(flashcard_ids))
        
        result.append({
            "language": lang,
            "lessons_completed": lang_lessons,
            "quizzes_taken": len(lang_quiz_scores),
            "average_score": round(avg, 1),
            "flashcards_reviewed": reviewed
        })
    
    return result

@api_router.get("/progress", response_model=ProgressResponse)
async def get_progress(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    progress = await db.progress.find_one({"user_id": user_id})
    
    if not progress:
        return ProgressResponse(
            user_id=user_id,
            courses_started=0,
            lessons_completed=0,
            flashcards_reviewed=0,
            quizzes_taken=0,
            average_score=0.0
        )
    
    quiz_scores = progress.get("quiz_scores", [])
    avg_score = sum(q["score"] for q in quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
    
    # Optimized: Batch query all lessons at once
    completed_lessons = progress.get("completed_lessons", [])
    courses_started = set()
    if completed_lessons:
        valid_ids = [ObjectId(lid) for lid in completed_lessons if ObjectId.is_valid(lid)]
        if valid_ids:
            lessons = await db.lessons.find({"_id": {"$in": valid_ids}}, {"course_id": 1}).to_list(None)
            courses_started = set(lesson["course_id"] for lesson in lessons)
    
    return ProgressResponse(
        user_id=user_id,
        courses_started=len(courses_started),
        lessons_completed=len(completed_lessons),
        flashcards_reviewed=len(progress.get("flashcards_reviewed", [])),
        quizzes_taken=len(quiz_scores),
        average_score=round(avg_score, 1)
    )

# ================== AI ROUTES ==================

@api_router.post("/ai/generate-exercise")
async def generate_exercise(request: AIExerciseRequest, current_user: dict = Depends(get_current_user_optional)):
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        # Generate a session ID (use user_id if available, otherwise random)
        user_id = str(current_user['_id']) if current_user else "anonymous"
        
        system_message = f"""You are an expert language teacher specializing in {request.language} following Cambridge methodology.
Generate educational exercises appropriate for {request.level} level students.
Always respond in a structured JSON format."""

        chat = LlmChat(
            api_key=api_key,
            session_id=f"exercise-{user_id}-{datetime.utcnow().timestamp()}",
            system_message=system_message
        ).with_model("openai", "gpt-4o")

        # Build reading passage instruction if needed
        reading_instruction = ""
        if request.exercise_type == "reading":
            reading_instruction = "IMPORTANT: For reading exercises, you MUST include a reading passage (texto de lectura) of 100-150 words that the student needs to read before answering the questions. The questions should be about the content of the passage."
        
        # Build writing instruction if needed
        writing_instruction = ""
        if request.exercise_type == "writing":
            writing_instruction = "IMPORTANT: For writing exercises, provide clear writing prompts that ask the student to write sentences or short paragraphs. Each question should give specific context and guidance for what to write."
        
        # Build reading passage field if needed
        reading_field = ""
        if request.exercise_type == "reading":
            reading_field = f'"reading_passage": "A reading text of 100-150 words in {request.language} appropriate for {request.level} level",'

        prompt = f"""Generate a {request.exercise_type} exercise for {request.language} learners at {request.level} level.
Topic: {request.topic}

{reading_instruction}

{writing_instruction}

Return a JSON object with this structure:
{{
    "title": "Exercise title in {request.language}",
    "description": "Brief description of what this exercise will help the student practice",
    "instructions": "Clear instructions for the student in Spanish",
    {reading_field}
    "questions": [
        {{
            "question": "The question text",
            "options": ["option A", "option B", "option C", "option D"],
            "correct_answer": 0,
            "explanation": "Why this is correct"
        }}
    ],
    "vocabulary": [
        {{"word": "word", "translation": "translation", "example": "example sentence"}}
    ],
    "grammar_tip": "A helpful grammar tip related to the topic"
}}

Generate 5 questions and 5 vocabulary items.
All content should be appropriate for {request.level} level."""

        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        # Try to parse as JSON
        import json
        try:
            # Clean response - remove markdown code blocks if present
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            exercise_data = json.loads(clean_response.strip())
            return {"success": True, "exercise": exercise_data}
        except json.JSONDecodeError:
            return {"success": True, "exercise": {"raw_content": response}}
            
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# ================== TTS ROUTE ==================

@api_router.post("/tts/generate")
async def generate_tts(request: TTSRequest):
    """Generate audio pronunciation for a word or phrase"""
    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="TTS service not configured")
        
        # Select voice based on language
        voice_map = {
            "spanish": "nova",      # Energetic, good for Spanish
            "english": "alloy",     # Neutral, balanced for English
            "portuguese": "shimmer" # Bright, cheerful for Portuguese
        }
        voice = voice_map.get(request.language.lower(), "alloy")
        
        tts = OpenAITextToSpeech(api_key=api_key)
        
        # Generate audio as base64 for easy frontend consumption
        audio_base64 = await tts.generate_speech_base64(
            text=request.text,
            model="tts-1",
            voice=voice,
            response_format="mp3"
        )
        
        return {
            "success": True,
            "audio_base64": audio_base64,
            "format": "mp3"
        }
        
    except Exception as e:
        logger.error(f"TTS generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@api_router.post("/ai/explain")
async def explain_concept(language: str, level: str, concept: str, current_user: dict = Depends(get_current_user_optional)):
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        chat = LlmChat(
            api_key=api_key,
            session_id=f"explain-{str(current_user['_id'])}-{datetime.utcnow().timestamp()}",
            system_message=f"You are an expert {language} teacher using Cambridge methodology. Explain concepts clearly for {level} level students."
        ).with_model("openai", "gpt-4o")

        prompt = f"""Explain the following {language} concept for a {level} level student:

{concept}

Provide:
1. A clear explanation
2. 3 example sentences
3. Common mistakes to avoid
4. A practice tip"""

        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        return {"success": True, "explanation": response}
            
    except Exception as e:
        logger.error(f"AI explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI explanation failed: {str(e)}")

# ================== SEED DATA ROUTE ==================

# ================== QUIZ GENERATION ==================

@api_router.post("/seed-quizzes")
async def seed_quizzes():
    """Seed quizzes for all courses"""
    existing = await db.quizzes.count_documents({})
    if existing > 0:
        return {"message": "Quizzes already exist", "count": existing}
    
    courses = await db.courses.find({}).to_list(None)
    created = 0
    
    quiz_templates = {
        "spanish": {
            "A1": [
                {"q": "¿Cómo se dice 'hello' en español?", "opts": ["Hola", "Adiós", "Gracias", "Por favor"], "ans": 0},
                {"q": "¿Cuál es el plural de 'libro'?", "opts": ["Libros", "Libroes", "Libras", "Libro"], "ans": 0},
                {"q": "Completa: 'Yo ___ estudiante'", "opts": ["soy", "eres", "es", "somos"], "ans": 0},
                {"q": "¿Qué significa 'buenos días'?", "opts": ["Good morning", "Good night", "Goodbye", "Thank you"], "ans": 0},
                {"q": "El artículo para 'casa' es:", "opts": ["la", "el", "los", "las"], "ans": 0},
            ],
            "A2": [
                {"q": "Ayer yo ___ al cine", "opts": ["fui", "voy", "iré", "iba"], "ans": 0},
                {"q": "¿Cuál es el pasado de 'comer'?", "opts": ["comí", "como", "comeré", "comía"], "ans": 0},
                {"q": "El superlativo de 'grande' es:", "opts": ["grandísimo", "más grande", "muy grande", "el grande"], "ans": 0},
                {"q": "¿Qué tiempo verbal es 'hablaré'?", "opts": ["Futuro", "Presente", "Pasado", "Condicional"], "ans": 0},
                {"q": "Completa: 'Me gusta ___ música'", "opts": ["la", "el", "un", "una"], "ans": 0},
            ],
        },
        "english": {
            "A1": [
                {"q": "What is 'hola' in English?", "opts": ["Hello", "Goodbye", "Thanks", "Please"], "ans": 0},
                {"q": "The plural of 'book' is:", "opts": ["Books", "Bookes", "Bookies", "Book"], "ans": 0},
                {"q": "Complete: 'I ___ a student'", "opts": ["am", "is", "are", "be"], "ans": 0},
                {"q": "What does 'good morning' mean?", "opts": ["Buenos días", "Buenas noches", "Adiós", "Gracias"], "ans": 0},
                {"q": "The article for 'apple' is:", "opts": ["an", "a", "the", "none"], "ans": 0},
            ],
            "A2": [
                {"q": "Yesterday I ___ to the cinema", "opts": ["went", "go", "will go", "going"], "ans": 0},
                {"q": "The past of 'eat' is:", "opts": ["ate", "eat", "eaten", "eating"], "ans": 0},
                {"q": "The superlative of 'big' is:", "opts": ["biggest", "bigger", "more big", "most big"], "ans": 0},
                {"q": "What tense is 'will speak'?", "opts": ["Future", "Present", "Past", "Conditional"], "ans": 0},
                {"q": "Complete: 'I like ___ music'", "opts": ["the", "a", "an", "some"], "ans": 0},
            ],
        },
        "portuguese": {
            "A1": [
                {"q": "Como se diz 'hello' em português?", "opts": ["Olá", "Tchau", "Obrigado", "Por favor"], "ans": 0},
                {"q": "O plural de 'livro' é:", "opts": ["Livros", "Livroes", "Livras", "Livro"], "ans": 0},
                {"q": "Complete: 'Eu ___ estudante'", "opts": ["sou", "és", "é", "somos"], "ans": 0},
                {"q": "O que significa 'bom dia'?", "opts": ["Good morning", "Good night", "Goodbye", "Thank you"], "ans": 0},
                {"q": "O artigo para 'casa' é:", "opts": ["a", "o", "os", "as"], "ans": 0},
            ],
            "A2": [
                {"q": "Ontem eu ___ ao cinema", "opts": ["fui", "vou", "irei", "ia"], "ans": 0},
                {"q": "O passado de 'comer' é:", "opts": ["comi", "como", "comerei", "comia"], "ans": 0},
                {"q": "O superlativo de 'grande' é:", "opts": ["grandíssimo", "mais grande", "muito grande", "o grande"], "ans": 0},
                {"q": "Que tempo verbal é 'falarei'?", "opts": ["Futuro", "Presente", "Passado", "Condicional"], "ans": 0},
                {"q": "Complete: 'Eu gosto ___ música'", "opts": ["da", "do", "de um", "de uma"], "ans": 0},
            ],
        },
        "german": {
            "A1": [
                {"q": "Wie sagt man 'hello' auf Deutsch?", "opts": ["Hallo", "Tschüss", "Danke", "Bitte"], "ans": 0},
                {"q": "Der Plural von 'Buch' ist:", "opts": ["Bücher", "Buchs", "Buche", "Buch"], "ans": 0},
                {"q": "Ergänze: 'Ich ___ Student'", "opts": ["bin", "bist", "ist", "sind"], "ans": 0},
                {"q": "Was bedeutet 'Guten Morgen'?", "opts": ["Good morning", "Good night", "Goodbye", "Thank you"], "ans": 0},
                {"q": "Der Artikel für 'Haus' ist:", "opts": ["das", "der", "die", "den"], "ans": 0},
            ],
            "A2": [
                {"q": "Gestern ___ ich ins Kino", "opts": ["ging", "gehe", "werde gehen", "gegangen"], "ans": 0},
                {"q": "Die Vergangenheit von 'essen' ist:", "opts": ["aß", "esse", "werde essen", "gegessen"], "ans": 0},
                {"q": "Der Superlativ von 'groß' ist:", "opts": ["am größten", "größer", "mehr groß", "sehr groß"], "ans": 0},
                {"q": "Welche Zeitform ist 'werde sprechen'?", "opts": ["Futur", "Präsens", "Präteritum", "Konjunktiv"], "ans": 0},
                {"q": "Ergänze: 'Ich mag ___ Musik'", "opts": ["die", "der", "das", "den"], "ans": 0},
            ],
        }
    }
    
    for course in courses:
        course_id = str(course["_id"])
        lang = course["language"]
        level = course["level"]
        
        # Get template or create generic
        if lang in quiz_templates and level in quiz_templates[lang]:
            questions = quiz_templates[lang][level]
        else:
            # Generic quiz for levels without templates
            questions = [
                {"q": f"Question 1 for {lang} {level}", "opts": ["Correct", "Wrong A", "Wrong B", "Wrong C"], "ans": 0},
                {"q": f"Question 2 for {lang} {level}", "opts": ["Correct", "Wrong A", "Wrong B", "Wrong C"], "ans": 0},
                {"q": f"Question 3 for {lang} {level}", "opts": ["Correct", "Wrong A", "Wrong B", "Wrong C"], "ans": 0},
                {"q": f"Question 4 for {lang} {level}", "opts": ["Correct", "Wrong A", "Wrong B", "Wrong C"], "ans": 0},
                {"q": f"Question 5 for {lang} {level}", "opts": ["Correct", "Wrong A", "Wrong B", "Wrong C"], "ans": 0},
            ]
        
        quiz_dict = {
            "course_id": course_id,
            "title": f"Quiz {course['title']}",
            "questions": [
                {
                    "question": q["q"],
                    "options": q["opts"],
                    "correct_answer": q["ans"],
                    "explanation": f"La respuesta correcta es: {q['opts'][q['ans']]}"
                } for q in questions
            ],
            "time_limit_minutes": 10,
            "created_by": "system",
            "created_at": datetime.utcnow()
        }
        await db.quizzes.insert_one(quiz_dict)
        created += 1
    
    return {"message": "Quizzes created", "count": created}

@api_router.get("/quizzes")
async def get_all_quizzes(language: Optional[str] = None, level: Optional[str] = None):
    """Get all quizzes with optional filters"""
    # First get courses matching filters
    course_query = {}
    if language:
        course_query["language"] = language.lower()
    if level:
        course_query["level"] = level.upper()
    
    if course_query:
        courses = await db.courses.find(course_query, {"_id": 1}).to_list(None)
        course_ids = [str(c["_id"]) for c in courses]
        quizzes = await db.quizzes.find({"course_id": {"$in": course_ids}}).to_list(100)
    else:
        quizzes = await db.quizzes.find({}).to_list(100)
    
    # Add course info to each quiz
    result = []
    for q in quizzes:
        course = await db.courses.find_one({"_id": ObjectId(q["course_id"])})
        result.append({
            "id": str(q["_id"]),
            "title": q["title"],
            "course_id": q["course_id"],
            "language": course["language"] if course else "unknown",
            "level": course["level"] if course else "unknown",
            "question_count": len(q["questions"]),
            "time_limit_minutes": q["time_limit_minutes"]
        })
    
    return result

@api_router.post("/seed-data")
async def seed_sample_data():
    """Seed the database with sample courses and content"""
    
    # Check if already seeded
    existing = await db.courses.count_documents({})
    if existing > 0:
        return {"message": "Database already has data", "courses": existing}
    
    # Create sample courses
    languages = ["spanish", "english", "portuguese"]
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    courses_data = [
        {"language": "spanish", "level": "A1", "title": "Spanish Basics", "description": "Start your Spanish journey with fundamental vocabulary and grammar."},
        {"language": "spanish", "level": "A2", "title": "Spanish Elementary", "description": "Build on basics with everyday conversations and simple texts."},
        {"language": "spanish", "level": "B1", "title": "Spanish Intermediate", "description": "Express opinions and handle most travel situations."},
        {"language": "english", "level": "A1", "title": "English Basics", "description": "Begin learning English with essential phrases and grammar."},
        {"language": "english", "level": "A2", "title": "English Elementary", "description": "Develop skills for routine tasks and simple descriptions."},
        {"language": "english", "level": "B1", "title": "English Intermediate", "description": "Communicate confidently in work, school, and travel."},
        {"language": "portuguese", "level": "A1", "title": "Portuguese Basics", "description": "Discover Portuguese with foundational vocabulary and structures."},
        {"language": "portuguese", "level": "A2", "title": "Portuguese Elementary", "description": "Progress to everyday conversations and cultural topics."},
        {"language": "portuguese", "level": "B1", "title": "Portuguese Intermediate", "description": "Navigate daily life and express experiences fluently."},
    ]
    
    created_courses = []
    for course in courses_data:
        course["created_by"] = "system"
        course["created_at"] = datetime.utcnow()
        result = await db.courses.insert_one(course)
        created_courses.append({"id": str(result.inserted_id), **course})
    
    # Add sample flashcards
    flashcards_data = [
        # Spanish A1
        {"language": "spanish", "level": "A1", "word": "Hola", "translation": "Hello", "example": "¡Hola! ¿Cómo estás?", "pronunciation": "OH-lah"},
        {"language": "spanish", "level": "A1", "word": "Gracias", "translation": "Thank you", "example": "Muchas gracias por tu ayuda.", "pronunciation": "GRAH-syahs"},
        {"language": "spanish", "level": "A1", "word": "Por favor", "translation": "Please", "example": "Un café, por favor.", "pronunciation": "por fah-VOR"},
        {"language": "spanish", "level": "A1", "word": "Buenos días", "translation": "Good morning", "example": "Buenos días, ¿cómo está usted?", "pronunciation": "BWEH-nohs DEE-ahs"},
        {"language": "spanish", "level": "A1", "word": "Adiós", "translation": "Goodbye", "example": "Adiós, hasta mañana.", "pronunciation": "ah-DYOHS"},
        # English A1
        {"language": "english", "level": "A1", "word": "Hello", "translation": "Hola", "example": "Hello, how are you?", "pronunciation": "heh-LOH"},
        {"language": "english", "level": "A1", "word": "Thank you", "translation": "Gracias", "example": "Thank you for your help.", "pronunciation": "THANK yoo"},
        {"language": "english", "level": "A1", "word": "Please", "translation": "Por favor", "example": "A coffee, please.", "pronunciation": "pleez"},
        {"language": "english", "level": "A1", "word": "Good morning", "translation": "Buenos días", "example": "Good morning, everyone!", "pronunciation": "good MOR-ning"},
        {"language": "english", "level": "A1", "word": "Goodbye", "translation": "Adiós", "example": "Goodbye, see you tomorrow.", "pronunciation": "good-BYE"},
        # Portuguese A1
        {"language": "portuguese", "level": "A1", "word": "Olá", "translation": "Hello", "example": "Olá! Como vai você?", "pronunciation": "oh-LAH"},
        {"language": "portuguese", "level": "A1", "word": "Obrigado/a", "translation": "Thank you", "example": "Muito obrigado pela ajuda.", "pronunciation": "oh-bree-GAH-doo"},
        {"language": "portuguese", "level": "A1", "word": "Por favor", "translation": "Please", "example": "Um café, por favor.", "pronunciation": "por fah-VOR"},
        {"language": "portuguese", "level": "A1", "word": "Bom dia", "translation": "Good morning", "example": "Bom dia! Tudo bem?", "pronunciation": "bom DEE-ah"},
        {"language": "portuguese", "level": "A1", "word": "Tchau", "translation": "Goodbye", "example": "Tchau, até amanhã!", "pronunciation": "chow"},
    ]
    
    for card in flashcards_data:
        card["created_by"] = "system"
        card["created_at"] = datetime.utcnow()
        await db.flashcards.insert_one(card)
    
    return {"message": "Sample data created", "courses": len(created_courses), "flashcards": len(flashcards_data)}

# ================== ROOT ROUTES ==================

@api_router.get("/")
async def root():
    return {"message": "Polyglot Academy API", "version": "1.0.0"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Include router and middleware
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

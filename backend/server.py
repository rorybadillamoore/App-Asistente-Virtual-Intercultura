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
    
    # Pre-fetch all lessons and quizzes to avoid N+1 queries
    all_lesson_ids = [ObjectId(lid) for lid in completed_lessons if ObjectId.is_valid(lid)]
    all_quiz_ids = [ObjectId(qs["quiz_id"]) for qs in quiz_scores if ObjectId.is_valid(qs.get("quiz_id", ""))]
    
    lessons_map = {}
    if all_lesson_ids:
        lessons_cursor = db.lessons.find({"_id": {"$in": all_lesson_ids}}, {"_id": 1, "course_id": 1})
        async for lesson in lessons_cursor:
            lessons_map[str(lesson["_id"])] = lesson.get("course_id")
    
    quizzes_map = {}
    if all_quiz_ids:
        quizzes_cursor = db.quizzes.find({"_id": {"$in": all_quiz_ids}}, {"_id": 1, "course_id": 1})
        async for quiz in quizzes_cursor:
            quizzes_map[str(quiz["_id"])] = quiz.get("course_id")
    
    for lang in languages:
        # Get courses for this language
        courses = await db.courses.find({"language": lang}, {"_id": 1}).to_list(None)
        course_ids = [str(c["_id"]) for c in courses]
        
        # Count lessons completed in this language (using pre-fetched data)
        lang_lessons = sum(1 for lid in completed_lessons if lessons_map.get(lid) in course_ids)
        
        # Count quizzes and scores for this language (using pre-fetched data)
        lang_quiz_scores = [qs["score"] for qs in quiz_scores if quizzes_map.get(qs.get("quiz_id")) in course_ids]
        
        avg = sum(lang_quiz_scores) / len(lang_quiz_scores) if lang_quiz_scores else 0.0
        
        # Get flashcards for this language (with limit)
        flashcards = await db.flashcards.find({"language": lang}, {"_id": 1}).to_list(500)
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
        import random
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        # Generate a unique session ID for each request to ensure different exercises
        user_id = str(current_user['_id']) if current_user else "anonymous"
        unique_seed = random.randint(10000, 99999)
        
        # Determine the target language name in that language and instruction language
        language_names = {
            "spanish": {"native": "Español", "instruction": "Spanish"},
            "english": {"native": "English", "instruction": "English"},
            "portuguese": {"native": "Português", "instruction": "Portuguese"},
            "german": {"native": "Deutsch", "instruction": "German"}
        }
        lang_info = language_names.get(request.language.lower(), {"native": request.language, "instruction": request.language})
        
        system_message = f"""You are an expert {lang_info['instruction']} language teacher following Cambridge methodology.
You MUST generate ALL content in {lang_info['instruction']} language.
Generate educational exercises appropriate for {request.level} level students.
IMPORTANT: Generate completely NEW and UNIQUE content each time. Do NOT repeat previous exercises.
Always respond in a structured JSON format."""

        chat = LlmChat(
            api_key=api_key,
            session_id=f"exercise-{user_id}-{datetime.utcnow().timestamp()}-{unique_seed}",
            system_message=system_message
        ).with_model("openai", "gpt-4o")

        # Build reading passage instruction if needed
        reading_instruction = ""
        if request.exercise_type == "reading":
            reading_instruction = f"IMPORTANT: For reading exercises, you MUST include a reading passage of 100-150 words IN {lang_info['instruction'].upper()} that the student needs to read before answering the questions. The questions should be about the content of the passage."
        
        # Build writing instruction if needed
        writing_instruction = ""
        if request.exercise_type == "writing":
            writing_instruction = f"IMPORTANT: For writing exercises, provide clear writing prompts IN {lang_info['instruction'].upper()} that ask the student to write sentences or short paragraphs."
        
        # Build reading passage field if needed
        reading_field = ""
        if request.exercise_type == "reading":
            reading_field = f'"reading_passage": "A reading text of 100-150 words written entirely in {lang_info["instruction"]}",'

        prompt = f"""Generate a {request.exercise_type} exercise for {lang_info['instruction']} learners at {request.level} level.
Topic: {request.topic}

UNIQUENESS REQUIREMENT (CRITICAL):
- This is exercise variation #{unique_seed}
- Generate COMPLETELY NEW content that is DIFFERENT from any previous exercise
- Use different contexts, scenarios, and vocabulary than before
- Create original questions - do NOT repeat common examples

CRITICAL LANGUAGE REQUIREMENT:
- ALL questions MUST be written in {lang_info['instruction']}
- ALL answer options MUST be in {lang_info['instruction']}
- ALL instructions MUST be in {lang_info['instruction']}
- ALL explanations MUST be in {lang_info['instruction']}
- The vocabulary words should be in {lang_info['instruction']} with translations to Spanish

{reading_instruction}

{writing_instruction}

Return a JSON object with this structure:
{{
    "title": "Exercise title in {lang_info['instruction']}",
    "description": "Brief description in {lang_info['instruction']}",
    "instructions": "Clear instructions in {lang_info['instruction']}",
    {reading_field}
    "questions": [
        {{
            "question": "Question text in {lang_info['instruction']}",
            "options": ["option A in {lang_info['instruction']}", "option B", "option C", "option D"],
            "correct_answer": 0,
            "explanation": "Explanation in {lang_info['instruction']}"
        }}
    ],
    "vocabulary": [
        {{"word": "word in {lang_info['instruction']}", "translation": "traducción al español", "example": "example sentence in {lang_info['instruction']}"}}
    ],
    "grammar_tip": "Grammar tip in {lang_info['instruction']}"
}}

Generate 5 questions appropriate for {request.level} level and 5 vocabulary items.
Remember: EVERYTHING except vocabulary translations must be in {lang_info['instruction']}.
IMPORTANT: Make this exercise unique and different from previous ones."""

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
        
        # Select voice based on language for native-sounding pronunciation
        # OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
        # - onyx: Deep, warm - works well for Spanish and Portuguese
        # - fable: Expressive, dramatic - good for German
        # - nova: Warm, conversational - good for English
        # - echo: Soft, clear - alternative for Romance languages
        voice_map = {
            "spanish": "onyx",       # Deep warm voice sounds natural for Spanish
            "english": "nova",       # Warm conversational for English  
            "portuguese": "onyx",    # Same deep warmth works well for Portuguese
            "german": "fable"        # Expressive voice suits German pronunciation
        }
        voice = voice_map.get(request.language.lower(), "nova")
        
        tts = OpenAITextToSpeech(api_key=api_key)
        
        # Generate audio as base64 for easy frontend consumption
        # Using tts-1-hd for higher quality pronunciation
        audio_base64 = await tts.generate_speech_base64(
            text=request.text,
            model="tts-1-hd",
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

@api_router.post("/reset-quizzes")
async def reset_quizzes():
    """Delete all quizzes to allow regeneration"""
    result = await db.quizzes.delete_many({})
    return {"message": "Quizzes deleted", "count": result.deleted_count}

@api_router.post("/seed-quizzes")
async def seed_quizzes():
    """Seed quizzes for all courses with complete questions for all levels"""
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
                {"q": "¿Cómo se dice 'thank you'?", "opts": ["Gracias", "Hola", "Adiós", "Por favor"], "ans": 0},
                {"q": "Completa: 'Ella ___ María'", "opts": ["se llama", "me llamo", "te llamas", "nos llamamos"], "ans": 0},
                {"q": "¿Cuál es el número 'cinco'?", "opts": ["5", "4", "6", "3"], "ans": 0},
                {"q": "El color 'rojo' en inglés es:", "opts": ["Red", "Blue", "Green", "Yellow"], "ans": 0},
                {"q": "¿Qué día viene después del lunes?", "opts": ["Martes", "Miércoles", "Domingo", "Viernes"], "ans": 0},
            ],
            "A2": [
                {"q": "Ayer yo ___ al cine", "opts": ["fui", "voy", "iré", "iba"], "ans": 0},
                {"q": "¿Cuál es el pasado de 'comer'?", "opts": ["comí", "como", "comeré", "comía"], "ans": 0},
                {"q": "El superlativo de 'grande' es:", "opts": ["grandísimo", "más grande", "muy grande", "el grande"], "ans": 0},
                {"q": "¿Qué tiempo verbal es 'hablaré'?", "opts": ["Futuro", "Presente", "Pasado", "Condicional"], "ans": 0},
                {"q": "Completa: 'Me gusta ___ música'", "opts": ["la", "el", "un", "una"], "ans": 0},
                {"q": "El opuesto de 'alto' es:", "opts": ["bajo", "grande", "pequeño", "gordo"], "ans": 0},
                {"q": "¿Cómo se dice 'I was eating'?", "opts": ["Estaba comiendo", "Estoy comiendo", "Comeré", "Comí"], "ans": 0},
                {"q": "Completa: 'Nosotros ___ en Madrid'", "opts": ["vivimos", "vivo", "vives", "viven"], "ans": 0},
                {"q": "¿Qué significa 'hace frío'?", "opts": ["It's cold", "It's hot", "It's raining", "It's sunny"], "ans": 0},
                {"q": "El plural de 'ciudad' es:", "opts": ["ciudades", "ciudads", "ciudades", "ciudad"], "ans": 0},
            ],
            "B1": [
                {"q": "Si yo ___ rico, viajaría por el mundo", "opts": ["fuera", "soy", "era", "seré"], "ans": 0},
                {"q": "¿Qué es un 'sinónimo'?", "opts": ["Palabra con significado similar", "Palabra opuesta", "Palabra técnica", "Palabra antigua"], "ans": 0},
                {"q": "El condicional de 'poder' es:", "opts": ["podría", "puedo", "pude", "podré"], "ans": 0},
                {"q": "'Había comido' es un tiempo:", "opts": ["Pluscuamperfecto", "Presente", "Futuro", "Pretérito"], "ans": 0},
                {"q": "Completa: 'Dudo que él ___ la verdad'", "opts": ["diga", "dice", "dirá", "dijo"], "ans": 0},
                {"q": "¿Qué expresa 'ojalá llueva'?", "opts": ["Deseo", "Certeza", "Obligación", "Pasado"], "ans": 0},
                {"q": "'Aunque' introduce una oración:", "opts": ["Concesiva", "Causal", "Final", "Temporal"], "ans": 0},
                {"q": "El gerundio de 'dormir' es:", "opts": ["durmiendo", "dormiendo", "dormido", "dormir"], "ans": 0},
                {"q": "¿Qué significa 'echar de menos'?", "opts": ["To miss", "To throw", "To find", "To lose"], "ans": 0},
                {"q": "Completa: 'Es importante que ___ a tiempo'", "opts": ["llegues", "llegas", "llegarás", "llegaste"], "ans": 0},
            ],
            "B2": [
                {"q": "'Habría ido si hubiera podido' expresa:", "opts": ["Condición irreal pasada", "Certeza", "Obligación", "Deseo presente"], "ans": 0},
                {"q": "¿Qué figura retórica es 'sus ojos son soles'?", "opts": ["Metáfora", "Símil", "Hipérbole", "Personificación"], "ans": 0},
                {"q": "El subjuntivo expresa:", "opts": ["Duda, deseo o irrealidad", "Hechos concretos", "Acciones pasadas", "Órdenes directas"], "ans": 0},
                {"q": "'A pesar de que' indica:", "opts": ["Concesión", "Causa", "Finalidad", "Tiempo"], "ans": 0},
                {"q": "¿Qué es una 'perífrasis verbal'?", "opts": ["Verbo auxiliar + infinitivo/gerundio/participio", "Un solo verbo conjugado", "Dos sustantivos", "Adjetivo + sustantivo"], "ans": 0},
                {"q": "'No bien llegó, empezó a llover' significa:", "opts": ["Tan pronto como llegó", "Aunque llegó", "Porque llegó", "Si llegó"], "ans": 0},
                {"q": "¿Qué es una 'locución adverbial'?", "opts": ["Grupo de palabras que funciona como adverbio", "Un solo adverbio", "Un verbo", "Un sustantivo"], "ans": 0},
                {"q": "El antónimo de 'efímero' es:", "opts": ["Duradero", "Breve", "Rápido", "Lento"], "ans": 0},
                {"q": "'Cuyo' es un pronombre:", "opts": ["Relativo posesivo", "Personal", "Demostrativo", "Indefinido"], "ans": 0},
                {"q": "¿Qué tiempo es 'hubiera cantado'?", "opts": ["Pretérito pluscuamperfecto de subjuntivo", "Condicional", "Futuro", "Presente"], "ans": 0},
            ],
            "C1": [
                {"q": "¿Qué es el 'leísmo'?", "opts": ["Uso de 'le' como objeto directo", "Uso incorrecto de 'la'", "Omisión del artículo", "Uso de doble negación"], "ans": 0},
                {"q": "'Hubiere cantado' pertenece al:", "opts": ["Futuro perfecto de subjuntivo", "Condicional compuesto", "Pretérito anterior", "Presente de subjuntivo"], "ans": 0},
                {"q": "El registro lingüístico 'coloquial' se caracteriza por:", "opts": ["Espontaneidad y expresividad", "Formalidad extrema", "Tecnicismos", "Arcaísmos"], "ans": 0},
                {"q": "Una 'oración subordinada sustantiva' funciona como:", "opts": ["Sustantivo", "Adjetivo", "Adverbio", "Verbo"], "ans": 0},
                {"q": "El 'estilo indirecto libre' combina:", "opts": ["Narración y pensamiento del personaje", "Solo diálogos", "Solo descripción", "Solo narración"], "ans": 0},
                {"q": "¿Qué es una 'analepsis'?", "opts": ["Flashback narrativo", "Anticipación", "Descripción", "Diálogo"], "ans": 0},
                {"q": "'Queísmo' es:", "opts": ["Omisión indebida de 'de' antes de 'que'", "Uso excesivo de 'que'", "Uso de 'qué'", "Repetición de 'que'"], "ans": 0},
                {"q": "La 'elipsis' consiste en:", "opts": ["Omisión de elementos sobreentendidos", "Repetición", "Exageración", "Comparación"], "ans": 0},
                {"q": "¿Qué es un 'cultismo'?", "opts": ["Palabra culta del latín o griego", "Palabra popular", "Neologismo", "Extranjerismo"], "ans": 0},
                {"q": "'Dequeísmo' es:", "opts": ["Uso indebido de 'de que'", "Omisión de 'de'", "Uso de 'que'", "Repetición"], "ans": 0},
            ],
            "C2": [
                {"q": "¿Qué es la 'deixis'?", "opts": ["Referencias contextuales del discurso", "Repetición de sonidos", "Cambio de significado", "Orden de palabras"], "ans": 0},
                {"q": "El 'modo pragmático' estudia:", "opts": ["Uso del lenguaje en contexto", "La estructura gramatical", "Los sonidos", "El origen de palabras"], "ans": 0},
                {"q": "Una 'implicatura conversacional' es:", "opts": ["Significado implícito no literal", "Significado literal", "Error gramatical", "Falta de coherencia"], "ans": 0},
                {"q": "El 'polisíndeton' consiste en:", "opts": ["Repetición de conjunciones", "Omisión de conjunciones", "Uso de metáforas", "Cambio de orden"], "ans": 0},
                {"q": "¿Qué estudia la 'sociolingüística'?", "opts": ["Relación entre lengua y sociedad", "Solo gramática", "Solo fonética", "Solo etimología"], "ans": 0},
                {"q": "La 'cohesión textual' se logra mediante:", "opts": ["Conectores y referencias", "Solo puntuación", "Solo vocabulario", "Solo gramática"], "ans": 0},
                {"q": "¿Qué es un 'acto perlocutivo'?", "opts": ["Efecto del enunciado en el oyente", "Pronunciación", "Estructura", "Significado literal"], "ans": 0},
                {"q": "'Modalización' se refiere a:", "opts": ["Actitud del hablante hacia lo dicho", "Estructura oracional", "Vocabulario", "Fonética"], "ans": 0},
                {"q": "La 'intertextualidad' implica:", "opts": ["Relación entre textos", "Gramática", "Pronunciación", "Vocabulario"], "ans": 0},
                {"q": "¿Qué es la 'diglosia'?", "opts": ["Coexistencia de dos variedades lingüísticas", "Un dialecto", "Un idioma", "Un acento"], "ans": 0},
            ],
        },
        "english": {
            "A1": [
                {"q": "What is 'hola' in English?", "opts": ["Hello", "Goodbye", "Thanks", "Please"], "ans": 0},
                {"q": "The plural of 'book' is:", "opts": ["Books", "Bookes", "Bookies", "Book"], "ans": 0},
                {"q": "Complete: 'I ___ a student'", "opts": ["am", "is", "are", "be"], "ans": 0},
                {"q": "What does 'good morning' mean?", "opts": ["Buenos días", "Buenas noches", "Adiós", "Gracias"], "ans": 0},
                {"q": "The article for 'apple' is:", "opts": ["an", "a", "the", "none"], "ans": 0},
                {"q": "How do you say 'gracias'?", "opts": ["Thank you", "Hello", "Goodbye", "Please"], "ans": 0},
                {"q": "Complete: 'She ___ a teacher'", "opts": ["is", "am", "are", "be"], "ans": 0},
                {"q": "What number is 'seven'?", "opts": ["7", "6", "8", "5"], "ans": 0},
                {"q": "The color 'azul' in English is:", "opts": ["Blue", "Red", "Green", "Yellow"], "ans": 0},
                {"q": "What day comes after Monday?", "opts": ["Tuesday", "Wednesday", "Sunday", "Friday"], "ans": 0},
            ],
            "A2": [
                {"q": "Yesterday I ___ to the cinema", "opts": ["went", "go", "will go", "going"], "ans": 0},
                {"q": "The past of 'eat' is:", "opts": ["ate", "eat", "eaten", "eating"], "ans": 0},
                {"q": "The superlative of 'big' is:", "opts": ["biggest", "bigger", "more big", "most big"], "ans": 0},
                {"q": "What tense is 'will speak'?", "opts": ["Future", "Present", "Past", "Conditional"], "ans": 0},
                {"q": "Complete: 'I like ___ music'", "opts": ["the", "a", "an", "some"], "ans": 0},
                {"q": "The opposite of 'tall' is:", "opts": ["short", "big", "small", "fat"], "ans": 0},
                {"q": "How do you say 'estaba comiendo'?", "opts": ["I was eating", "I am eating", "I will eat", "I ate"], "ans": 0},
                {"q": "Complete: 'They ___ in London'", "opts": ["live", "lives", "living", "lived"], "ans": 0},
                {"q": "What does 'it's raining' mean?", "opts": ["Está lloviendo", "Hace frío", "Hace calor", "Está nevando"], "ans": 0},
                {"q": "The plural of 'child' is:", "opts": ["children", "childs", "childes", "child"], "ans": 0},
            ],
            "B1": [
                {"q": "If I ___ rich, I would travel the world", "opts": ["were", "am", "was", "will be"], "ans": 0},
                {"q": "What is a 'synonym'?", "opts": ["Word with similar meaning", "Opposite word", "Technical word", "Old word"], "ans": 0},
                {"q": "The conditional of 'can' is:", "opts": ["could", "can", "will can", "canned"], "ans": 0},
                {"q": "'Had eaten' is which tense?", "opts": ["Past Perfect", "Present", "Future", "Simple Past"], "ans": 0},
                {"q": "Complete: 'I wish he ___ here'", "opts": ["were", "is", "will be", "was"], "ans": 0},
                {"q": "What does 'although' express?", "opts": ["Contrast", "Cause", "Purpose", "Time"], "ans": 0},
                {"q": "'Unless' means:", "opts": ["If not", "Because", "Although", "When"], "ans": 0},
                {"q": "The gerund of 'swim' is:", "opts": ["swimming", "swiming", "swam", "swim"], "ans": 0},
                {"q": "What does 'to miss' mean?", "opts": ["Echar de menos", "Encontrar", "Perder", "Tirar"], "ans": 0},
                {"q": "Complete: 'It's important that he ___ on time'", "opts": ["arrive", "arrives", "will arrive", "arrived"], "ans": 0},
            ],
            "B2": [
                {"q": "'I would have gone if I had known' expresses:", "opts": ["Unreal past condition", "Certainty", "Obligation", "Present wish"], "ans": 0},
                {"q": "What figure of speech is 'her eyes are diamonds'?", "opts": ["Metaphor", "Simile", "Hyperbole", "Personification"], "ans": 0},
                {"q": "The subjunctive expresses:", "opts": ["Doubt, wish or unreality", "Concrete facts", "Past actions", "Direct orders"], "ans": 0},
                {"q": "'Despite' indicates:", "opts": ["Concession", "Cause", "Purpose", "Time"], "ans": 0},
                {"q": "What is a 'phrasal verb'?", "opts": ["Verb + particle with idiomatic meaning", "Single verb", "Two nouns", "Adjective + noun"], "ans": 0},
                {"q": "'No sooner had he arrived than it started raining' means:", "opts": ["As soon as he arrived", "Although he arrived", "Because he arrived", "If he arrived"], "ans": 0},
                {"q": "What is an 'idiom'?", "opts": ["Expression with non-literal meaning", "Single word", "Grammar rule", "Pronunciation"], "ans": 0},
                {"q": "The antonym of 'ephemeral' is:", "opts": ["Lasting", "Brief", "Quick", "Slow"], "ans": 0},
                {"q": "'Whose' is a ___ pronoun:", "opts": ["Relative possessive", "Personal", "Demonstrative", "Indefinite"], "ans": 0},
                {"q": "What tense is 'had been working'?", "opts": ["Past Perfect Continuous", "Conditional", "Future", "Present"], "ans": 0},
            ],
            "C1": [
                {"q": "What is 'hedging' in academic writing?", "opts": ["Using cautious language", "Being direct", "Using slang", "Repetition"], "ans": 0},
                {"q": "'Were he to arrive' is an example of:", "opts": ["Inversion in conditionals", "Simple past", "Future", "Present"], "ans": 0},
                {"q": "The register 'colloquial' is characterized by:", "opts": ["Informality and spontaneity", "Extreme formality", "Technical terms", "Archaisms"], "ans": 0},
                {"q": "A 'noun clause' functions as:", "opts": ["Noun", "Adjective", "Adverb", "Verb"], "ans": 0},
                {"q": "'Free indirect speech' combines:", "opts": ["Narration and character's thoughts", "Only dialogues", "Only description", "Only narration"], "ans": 0},
                {"q": "What is an 'analepsis'?", "opts": ["Flashback", "Flash forward", "Description", "Dialogue"], "ans": 0},
                {"q": "'Litotes' is:", "opts": ["Understatement using negation", "Exaggeration", "Comparison", "Repetition"], "ans": 0},
                {"q": "An 'ellipsis' consists of:", "opts": ["Omission of understood elements", "Repetition", "Exaggeration", "Comparison"], "ans": 0},
                {"q": "What is a 'cognate'?", "opts": ["Word with same origin in another language", "Slang", "Neologism", "Acronym"], "ans": 0},
                {"q": "'Cataphora' refers to:", "opts": ["Forward reference", "Backward reference", "No reference", "Self reference"], "ans": 0},
            ],
            "C2": [
                {"q": "What is 'deixis'?", "opts": ["Context-dependent references", "Sound repetition", "Meaning change", "Word order"], "ans": 0},
                {"q": "'Pragmatics' studies:", "opts": ["Language use in context", "Grammar structure", "Sounds", "Word origins"], "ans": 0},
                {"q": "A 'conversational implicature' is:", "opts": ["Implicit non-literal meaning", "Literal meaning", "Grammar error", "Incoherence"], "ans": 0},
                {"q": "'Polysyndeton' consists of:", "opts": ["Repetition of conjunctions", "Omission of conjunctions", "Use of metaphors", "Word order change"], "ans": 0},
                {"q": "What does 'sociolinguistics' study?", "opts": ["Relationship between language and society", "Only grammar", "Only phonetics", "Only etymology"], "ans": 0},
                {"q": "'Textual cohesion' is achieved through:", "opts": ["Connectors and references", "Only punctuation", "Only vocabulary", "Only grammar"], "ans": 0},
                {"q": "What is a 'perlocutionary act'?", "opts": ["Effect of utterance on listener", "Pronunciation", "Structure", "Literal meaning"], "ans": 0},
                {"q": "'Modality' refers to:", "opts": ["Speaker's attitude toward what is said", "Sentence structure", "Vocabulary", "Phonetics"], "ans": 0},
                {"q": "'Intertextuality' implies:", "opts": ["Relationship between texts", "Grammar", "Pronunciation", "Vocabulary"], "ans": 0},
                {"q": "What is 'code-switching'?", "opts": ["Alternating between languages", "A dialect", "A language", "An accent"], "ans": 0},
            ],
        },
        "portuguese": {
            "A1": [
                {"q": "Como se diz 'hello' em português?", "opts": ["Olá", "Tchau", "Obrigado", "Por favor"], "ans": 0},
                {"q": "Qual é o plural de 'livro'?", "opts": ["Livros", "Livroes", "Livras", "Livro"], "ans": 0},
                {"q": "Complete: 'Eu ___ estudante'", "opts": ["sou", "és", "é", "somos"], "ans": 0},
                {"q": "O que significa 'bom dia'?", "opts": ["Good morning", "Good night", "Goodbye", "Thank you"], "ans": 0},
                {"q": "O artigo para 'casa' é:", "opts": ["a", "o", "os", "as"], "ans": 0},
                {"q": "Como se diz 'thank you'?", "opts": ["Obrigado", "Olá", "Tchau", "Por favor"], "ans": 0},
                {"q": "Complete: 'Ela ___ Maria'", "opts": ["se chama", "me chamo", "te chamas", "nos chamamos"], "ans": 0},
                {"q": "Qual é o número 'cinco'?", "opts": ["5", "4", "6", "3"], "ans": 0},
                {"q": "A cor 'vermelho' em inglês é:", "opts": ["Red", "Blue", "Green", "Yellow"], "ans": 0},
                {"q": "Que dia vem depois de segunda-feira?", "opts": ["Terça-feira", "Quarta-feira", "Domingo", "Sexta-feira"], "ans": 0},
            ],
            "A2": [
                {"q": "Ontem eu ___ ao cinema", "opts": ["fui", "vou", "irei", "ia"], "ans": 0},
                {"q": "Qual é o passado de 'comer'?", "opts": ["comi", "como", "comerei", "comia"], "ans": 0},
                {"q": "O superlativo de 'grande' é:", "opts": ["grandíssimo", "mais grande", "muito grande", "o grande"], "ans": 0},
                {"q": "Que tempo verbal é 'falarei'?", "opts": ["Futuro", "Presente", "Passado", "Condicional"], "ans": 0},
                {"q": "Complete: 'Eu gosto ___ música'", "opts": ["da", "do", "de um", "de uma"], "ans": 0},
                {"q": "O oposto de 'alto' é:", "opts": ["baixo", "grande", "pequeno", "gordo"], "ans": 0},
                {"q": "Como se diz 'I was eating'?", "opts": ["Eu estava comendo", "Eu estou comendo", "Comerei", "Comi"], "ans": 0},
                {"q": "Complete: 'Nós ___ em Lisboa'", "opts": ["moramos", "moro", "moras", "moram"], "ans": 0},
                {"q": "O que significa 'está frio'?", "opts": ["It's cold", "It's hot", "It's raining", "It's sunny"], "ans": 0},
                {"q": "O plural de 'cidade' é:", "opts": ["cidades", "cidads", "cidadees", "cidade"], "ans": 0},
            ],
            "B1": [
                {"q": "Se eu ___ rico, viajaria pelo mundo", "opts": ["fosse", "sou", "era", "serei"], "ans": 0},
                {"q": "O que é um 'sinônimo'?", "opts": ["Palavra com significado similar", "Palavra oposta", "Palavra técnica", "Palavra antiga"], "ans": 0},
                {"q": "O condicional de 'poder' é:", "opts": ["poderia", "posso", "pude", "poderei"], "ans": 0},
                {"q": "'Tinha comido' é que tempo?", "opts": ["Mais-que-perfeito", "Presente", "Futuro", "Pretérito"], "ans": 0},
                {"q": "Complete: 'Duvido que ele ___ a verdade'", "opts": ["diga", "diz", "dirá", "disse"], "ans": 0},
                {"q": "O que expressa 'oxalá chova'?", "opts": ["Desejo", "Certeza", "Obrigação", "Passado"], "ans": 0},
                {"q": "'Embora' introduz uma oração:", "opts": ["Concessiva", "Causal", "Final", "Temporal"], "ans": 0},
                {"q": "O gerúndio de 'dormir' é:", "opts": ["dormindo", "dormido", "dormir", "dorme"], "ans": 0},
                {"q": "O que significa 'ter saudades'?", "opts": ["To miss", "To throw", "To find", "To lose"], "ans": 0},
                {"q": "Complete: 'É importante que ___ a tempo'", "opts": ["chegues", "chegas", "chegarás", "chegaste"], "ans": 0},
            ],
            "B2": [
                {"q": "'Teria ido se tivesse podido' expressa:", "opts": ["Condição irreal passada", "Certeza", "Obrigação", "Desejo presente"], "ans": 0},
                {"q": "Que figura de linguagem é 'seus olhos são sóis'?", "opts": ["Metáfora", "Símile", "Hipérbole", "Personificação"], "ans": 0},
                {"q": "O subjuntivo expressa:", "opts": ["Dúvida, desejo ou irrealidade", "Fatos concretos", "Ações passadas", "Ordens diretas"], "ans": 0},
                {"q": "'Apesar de que' indica:", "opts": ["Concessão", "Causa", "Finalidade", "Tempo"], "ans": 0},
                {"q": "O que é uma 'perífrase verbal'?", "opts": ["Verbo auxiliar + infinitivo/gerúndio/particípio", "Um só verbo conjugado", "Dois substantivos", "Adjetivo + substantivo"], "ans": 0},
                {"q": "'Mal chegou, começou a chover' significa:", "opts": ["Assim que chegou", "Embora chegou", "Porque chegou", "Se chegou"], "ans": 0},
                {"q": "O que é uma 'locução adverbial'?", "opts": ["Grupo de palavras que funciona como advérbio", "Um só advérbio", "Um verbo", "Um substantivo"], "ans": 0},
                {"q": "O antônimo de 'efêmero' é:", "opts": ["Duradouro", "Breve", "Rápido", "Lento"], "ans": 0},
                {"q": "'Cujo' é um pronome:", "opts": ["Relativo possessivo", "Pessoal", "Demonstrativo", "Indefinido"], "ans": 0},
                {"q": "Que tempo é 'tivesse cantado'?", "opts": ["Pretérito mais-que-perfeito do subjuntivo", "Condicional", "Futuro", "Presente"], "ans": 0},
            ],
            "C1": [
                {"q": "O que é a 'crase'?", "opts": ["Fusão de duas vogais iguais", "Acentuação", "Pontuação", "Concordância"], "ans": 0},
                {"q": "'Houvera cantado' pertence ao:", "opts": ["Pretérito mais-que-perfeito", "Condicional composto", "Futuro", "Presente do subjuntivo"], "ans": 0},
                {"q": "O registro linguístico 'coloquial' caracteriza-se por:", "opts": ["Espontaneidade e expressividade", "Formalidade extrema", "Tecnicismos", "Arcaísmos"], "ans": 0},
                {"q": "Uma 'oração subordinada substantiva' funciona como:", "opts": ["Substantivo", "Adjetivo", "Advérbio", "Verbo"], "ans": 0},
                {"q": "O 'discurso indireto livre' combina:", "opts": ["Narração e pensamento do personagem", "Só diálogos", "Só descrição", "Só narração"], "ans": 0},
                {"q": "O que é uma 'analepse'?", "opts": ["Flashback narrativo", "Antecipação", "Descrição", "Diálogo"], "ans": 0},
                {"q": "'Pleonasmo' é:", "opts": ["Redundância expressiva", "Omissão", "Comparação", "Exagero"], "ans": 0},
                {"q": "A 'elipse' consiste em:", "opts": ["Omissão de elementos subentendidos", "Repetição", "Exagero", "Comparação"], "ans": 0},
                {"q": "O que é um 'neologismo'?", "opts": ["Palavra nova na língua", "Palavra antiga", "Palavra estrangeira", "Gíria"], "ans": 0},
                {"q": "'Regência verbal' refere-se a:", "opts": ["Relação entre verbo e complemento", "Conjugação", "Concordância", "Acentuação"], "ans": 0},
            ],
            "C2": [
                {"q": "O que é a 'dêixis'?", "opts": ["Referências contextuais do discurso", "Repetição de sons", "Mudança de significado", "Ordem das palavras"], "ans": 0},
                {"q": "A 'pragmática' estuda:", "opts": ["Uso da linguagem em contexto", "Estrutura gramatical", "Sons", "Origem das palavras"], "ans": 0},
                {"q": "Uma 'implicatura conversacional' é:", "opts": ["Significado implícito não literal", "Significado literal", "Erro gramatical", "Falta de coerência"], "ans": 0},
                {"q": "O 'polissíndeto' consiste em:", "opts": ["Repetição de conjunções", "Omissão de conjunções", "Uso de metáforas", "Mudança de ordem"], "ans": 0},
                {"q": "O que estuda a 'sociolinguística'?", "opts": ["Relação entre língua e sociedade", "Só gramática", "Só fonética", "Só etimologia"], "ans": 0},
                {"q": "A 'coesão textual' é conseguida mediante:", "opts": ["Conectores e referências", "Só pontuação", "Só vocabulário", "Só gramática"], "ans": 0},
                {"q": "O que é um 'ato perlocutório'?", "opts": ["Efeito do enunciado no ouvinte", "Pronúncia", "Estrutura", "Significado literal"], "ans": 0},
                {"q": "'Modalização' refere-se a:", "opts": ["Atitude do falante em relação ao dito", "Estrutura oracional", "Vocabulário", "Fonética"], "ans": 0},
                {"q": "A 'intertextualidade' implica:", "opts": ["Relação entre textos", "Gramática", "Pronúncia", "Vocabulário"], "ans": 0},
                {"q": "O que é a 'variação linguística'?", "opts": ["Diferentes formas de usar a língua", "Uma regra fixa", "Um erro", "Uma exceção"], "ans": 0},
            ],
        },
        "german": {
            "A1": [
                {"q": "Wie sagt man 'hello' auf Deutsch?", "opts": ["Hallo", "Tschüss", "Danke", "Bitte"], "ans": 0},
                {"q": "Was ist der Plural von 'Buch'?", "opts": ["Bücher", "Buchs", "Buchen", "Buch"], "ans": 0},
                {"q": "Ergänze: 'Ich ___ Student'", "opts": ["bin", "bist", "ist", "sind"], "ans": 0},
                {"q": "Was bedeutet 'guten Morgen'?", "opts": ["Good morning", "Good night", "Goodbye", "Thank you"], "ans": 0},
                {"q": "Der Artikel für 'Haus' ist:", "opts": ["das", "der", "die", "den"], "ans": 0},
                {"q": "Wie sagt man 'thank you'?", "opts": ["Danke", "Hallo", "Tschüss", "Bitte"], "ans": 0},
                {"q": "Ergänze: 'Sie ___ Maria'", "opts": ["heißt", "heiße", "heißt", "heißen"], "ans": 0},
                {"q": "Welche Zahl ist 'fünf'?", "opts": ["5", "4", "6", "3"], "ans": 0},
                {"q": "Die Farbe 'rot' auf Englisch ist:", "opts": ["Red", "Blue", "Green", "Yellow"], "ans": 0},
                {"q": "Welcher Tag kommt nach Montag?", "opts": ["Dienstag", "Mittwoch", "Sonntag", "Freitag"], "ans": 0},
            ],
            "A2": [
                {"q": "Gestern ___ ich ins Kino", "opts": ["ging", "gehe", "werde gehen", "gegangen"], "ans": 0},
                {"q": "Was ist das Präteritum von 'essen'?", "opts": ["aß", "esse", "gegessen", "essend"], "ans": 0},
                {"q": "Der Superlativ von 'groß' ist:", "opts": ["am größten", "größer", "mehr groß", "meist groß"], "ans": 0},
                {"q": "Welche Zeitform ist 'werde sprechen'?", "opts": ["Futur", "Präsens", "Präteritum", "Konjunktiv"], "ans": 0},
                {"q": "Ergänze: 'Ich mag ___ Musik'", "opts": ["die", "der", "ein", "eine"], "ans": 0},
                {"q": "Das Gegenteil von 'groß' ist:", "opts": ["klein", "dick", "dünn", "lang"], "ans": 0},
                {"q": "Wie sagt man 'I was eating'?", "opts": ["Ich aß gerade", "Ich esse", "Ich werde essen", "Ich habe gegessen"], "ans": 0},
                {"q": "Ergänze: 'Wir ___ in Berlin'", "opts": ["wohnen", "wohne", "wohnst", "wohnt"], "ans": 0},
                {"q": "Was bedeutet 'es ist kalt'?", "opts": ["It's cold", "It's hot", "It's raining", "It's sunny"], "ans": 0},
                {"q": "Der Plural von 'Kind' ist:", "opts": ["Kinder", "Kinds", "Kindes", "Kind"], "ans": 0},
            ],
            "B1": [
                {"q": "Wenn ich reich ___, würde ich reisen", "opts": ["wäre", "bin", "war", "werde sein"], "ans": 0},
                {"q": "Was ist ein 'Synonym'?", "opts": ["Wort mit ähnlicher Bedeutung", "Gegenteil", "Fachbegriff", "Altes Wort"], "ans": 0},
                {"q": "Der Konjunktiv II von 'können' ist:", "opts": ["könnte", "kann", "konnte", "werde können"], "ans": 0},
                {"q": "'Hatte gegessen' ist welche Zeitform?", "opts": ["Plusquamperfekt", "Präsens", "Futur", "Präteritum"], "ans": 0},
                {"q": "Ergänze: 'Ich bezweifle, dass er die Wahrheit ___'", "opts": ["sagt", "sagen", "gesagt", "sagte"], "ans": 0},
                {"q": "Was drückt 'obwohl' aus?", "opts": ["Gegensatz", "Grund", "Zweck", "Zeit"], "ans": 0},
                {"q": "'Falls' bedeutet:", "opts": ["If/In case", "Because", "Although", "When"], "ans": 0},
                {"q": "Das Partizip I von 'schlafen' ist:", "opts": ["schlafend", "geschlafen", "schlafen", "schlief"], "ans": 0},
                {"q": "Was bedeutet 'vermissen'?", "opts": ["To miss", "To find", "To lose", "To throw"], "ans": 0},
                {"q": "Ergänze: 'Es ist wichtig, dass er pünktlich ___'", "opts": ["kommt", "kommen", "gekommen", "kam"], "ans": 0},
            ],
            "B2": [
                {"q": "'Ich wäre gegangen, wenn ich gekonnt hätte' drückt aus:", "opts": ["Irreale Bedingung in der Vergangenheit", "Sicherheit", "Pflicht", "Gegenwärtiger Wunsch"], "ans": 0},
                {"q": "Welche Stilfigur ist 'ihre Augen sind Sonnen'?", "opts": ["Metapher", "Vergleich", "Übertreibung", "Personifikation"], "ans": 0},
                {"q": "Der Konjunktiv drückt aus:", "opts": ["Zweifel, Wunsch oder Irrealität", "Konkrete Fakten", "Vergangene Handlungen", "Direkte Befehle"], "ans": 0},
                {"q": "'Trotzdem' zeigt an:", "opts": ["Konzession", "Ursache", "Zweck", "Zeit"], "ans": 0},
                {"q": "Was ist ein 'trennbares Verb'?", "opts": ["Verb mit abtrennbarer Vorsilbe", "Einzelnes Verb", "Zwei Nomen", "Adjektiv + Nomen"], "ans": 0},
                {"q": "'Kaum war er angekommen, fing es an zu regnen' bedeutet:", "opts": ["Sobald er ankam", "Obwohl er ankam", "Weil er ankam", "Falls er ankam"], "ans": 0},
                {"q": "Was ist eine 'Redewendung'?", "opts": ["Feste Wortverbindung mit übertragener Bedeutung", "Einzelnes Wort", "Grammatikregel", "Aussprache"], "ans": 0},
                {"q": "Das Antonym von 'kurzlebig' ist:", "opts": ["langlebig", "kurz", "schnell", "langsam"], "ans": 0},
                {"q": "'Dessen' ist ein ___ Pronomen:", "opts": ["Relativpronomen im Genitiv", "Personalpronomen", "Demonstrativpronomen", "Indefinitpronomen"], "ans": 0},
                {"q": "Welche Zeitform ist 'hätte gearbeitet'?", "opts": ["Konjunktiv II Vergangenheit", "Futur", "Präsens", "Präteritum"], "ans": 0},
            ],
            "C1": [
                {"q": "Was ist 'Nominalisierung'?", "opts": ["Substantivierung von Verben", "Verbkonjugation", "Adjektivdeklination", "Satzstellung"], "ans": 0},
                {"q": "Das 'Passiv' betont:", "opts": ["Die Handlung", "Den Handelnden", "Die Zeit", "Den Ort"], "ans": 0},
                {"q": "Ein 'Partizipialattribut' ist:", "opts": ["Partizip als Adjektiv vor Nomen", "Verb im Satz", "Adverb", "Konjunktion"], "ans": 0},
                {"q": "Der 'gehobene Stil' zeichnet sich aus durch:", "opts": ["Formelle Sprache", "Umgangssprache", "Dialekt", "Jugendsprache"], "ans": 0},
                {"q": "Was ist eine 'Ellipse'?", "opts": ["Auslassung von Wörtern", "Wiederholung", "Übertreibung", "Vergleich"], "ans": 0},
                {"q": "Was ist eine 'Analepse'?", "opts": ["Rückblende", "Vorausschau", "Beschreibung", "Dialog"], "ans": 0},
                {"q": "'Litotes' ist:", "opts": ["Untertreibung durch Verneinung", "Übertreibung", "Vergleich", "Wiederholung"], "ans": 0},
                {"q": "Eine 'Ellipse' besteht aus:", "opts": ["Auslassung verstandener Elemente", "Wiederholung", "Übertreibung", "Vergleich"], "ans": 0},
                {"q": "Was ist ein 'Lehnwort'?", "opts": ["Aus einer anderen Sprache übernommenes Wort", "Slang", "Neologismus", "Akronym"], "ans": 0},
                {"q": "'Kataphorik' bezieht sich auf:", "opts": ["Vorwärtsverweis", "Rückwärtsverweis", "Kein Verweis", "Selbstverweis"], "ans": 0},
            ],
            "C2": [
                {"q": "Was untersucht die 'Pragmatik'?", "opts": ["Sprachverwendung im Kontext", "Grammatikregeln", "Laute", "Wortbildung"], "ans": 0},
                {"q": "Eine 'Implikatur' ist:", "opts": ["Implizite Bedeutung", "Wörtliche Bedeutung", "Grammatikfehler", "Stilmittel"], "ans": 0},
                {"q": "'Register' bezieht sich auf:", "opts": ["Sprachvarietät je nach Situation", "Akzent", "Dialekt", "Nur Slang"], "ans": 0},
                {"q": "Ein 'Sprechakt' ist:", "opts": ["Durch Sprache vollzogene Handlung", "Nur Text", "Grammatikregel", "Wortliste"], "ans": 0},
                {"q": "Was ist 'Deixis'?", "opts": ["Kontextabhängige Verweise", "Feste Bedeutungen", "Grammatikregeln", "Aussprache"], "ans": 0},
                {"q": "'Textkohäsion' wird erreicht durch:", "opts": ["Konnektoren und Verweise", "Nur Interpunktion", "Nur Wortschatz", "Nur Grammatik"], "ans": 0},
                {"q": "Was ist ein 'perlokutionärer Akt'?", "opts": ["Wirkung der Äußerung auf den Hörer", "Aussprache", "Struktur", "Wörtliche Bedeutung"], "ans": 0},
                {"q": "'Modalität' bezieht sich auf:", "opts": ["Einstellung des Sprechers zum Gesagten", "Satzstruktur", "Wortschatz", "Phonetik"], "ans": 0},
                {"q": "'Intertextualität' impliziert:", "opts": ["Beziehung zwischen Texten", "Grammatik", "Aussprache", "Wortschatz"], "ans": 0},
                {"q": "Was ist 'Code-Switching'?", "opts": ["Wechsel zwischen Sprachen", "Ein Dialekt", "Eine Sprache", "Ein Akzent"], "ans": 0},
            ],
        },
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

@api_router.post("/seed-full")
async def seed_full_database():
    """Seed the database with complete courses, flashcards, and quizzes for all 4 languages and 6 levels"""
    
    # Course titles and descriptions for all languages and levels
    course_configs = {
        "spanish": {
            "name": "Español",
            "levels": {
                "A1": {"title": "Español Básico", "desc": "Fundamentos del español: saludos, presentaciones y vocabulario esencial."},
                "A2": {"title": "Español Elemental", "desc": "Conversaciones cotidianas, compras y descripciones básicas."},
                "B1": {"title": "Español Intermedio", "desc": "Expresar opiniones, narrar experiencias y situaciones de viaje."},
                "B2": {"title": "Español Intermedio Alto", "desc": "Debates, textos complejos y expresión fluida de ideas."},
                "C1": {"title": "Español Avanzado", "desc": "Comunicación profesional, textos académicos y matices culturales."},
                "C2": {"title": "Español Maestría", "desc": "Dominio nativo, literatura, dialectos y expresiones idiomáticas."},
            }
        },
        "english": {
            "name": "English",
            "levels": {
                "A1": {"title": "English Basics", "desc": "Foundation English: greetings, introductions and essential vocabulary."},
                "A2": {"title": "English Elementary", "desc": "Daily conversations, shopping and basic descriptions."},
                "B1": {"title": "English Intermediate", "desc": "Express opinions, narrate experiences and travel situations."},
                "B2": {"title": "English Upper-Intermediate", "desc": "Debates, complex texts and fluent expression of ideas."},
                "C1": {"title": "English Advanced", "desc": "Professional communication, academic texts and cultural nuances."},
                "C2": {"title": "English Mastery", "desc": "Native-level proficiency, literature, dialects and idiomatic expressions."},
            }
        },
        "portuguese": {
            "name": "Português",
            "levels": {
                "A1": {"title": "Português Básico", "desc": "Fundamentos do português: saudações, apresentações e vocabulário essencial."},
                "A2": {"title": "Português Elementar", "desc": "Conversas cotidianas, compras e descrições básicas."},
                "B1": {"title": "Português Intermediário", "desc": "Expressar opiniões, narrar experiências e situações de viagem."},
                "B2": {"title": "Português Intermediário Alto", "desc": "Debates, textos complexos e expressão fluente de ideias."},
                "C1": {"title": "Português Avançado", "desc": "Comunicação profissional, textos acadêmicos e nuances culturais."},
                "C2": {"title": "Português Maestria", "desc": "Proficiência nativa, literatura, dialetos e expressões idiomáticas."},
            }
        },
        "german": {
            "name": "Deutsch",
            "levels": {
                "A1": {"title": "Deutsch Grundlagen", "desc": "Deutsche Grundlagen: Begrüßungen, Vorstellungen und grundlegendes Vokabular."},
                "A2": {"title": "Deutsch Elementar", "desc": "Alltägliche Gespräche, Einkaufen und grundlegende Beschreibungen."},
                "B1": {"title": "Deutsch Mittelstufe", "desc": "Meinungen ausdrücken, Erfahrungen erzählen und Reisesituationen."},
                "B2": {"title": "Deutsch Obere Mittelstufe", "desc": "Debatten, komplexe Texte und fließender Ausdruck von Ideen."},
                "C1": {"title": "Deutsch Fortgeschritten", "desc": "Professionelle Kommunikation, akademische Texte und kulturelle Nuancen."},
                "C2": {"title": "Deutsch Meisterschaft", "desc": "Muttersprachliche Kompetenz, Literatur, Dialekte und idiomatische Ausdrücke."},
            }
        }
    }
    
    # Clear existing data
    await db.courses.delete_many({})
    await db.lessons.delete_many({})
    await db.flashcards.delete_many({})
    await db.quizzes.delete_many({})
    
    # Lesson templates per language with full content
    lesson_templates = {
        "spanish": [
            {
                "title": "Lección 1: Introducción y Saludos",
                "content": """Bienvenido al curso de español. En esta lección aprenderás los saludos básicos y presentaciones.

**Saludos formales:**
- Buenos días (Good morning)
- Buenas tardes (Good afternoon)  
- Buenas noches (Good evening)
- ¿Cómo está usted? (How are you? - formal)

**Saludos informales:**
- ¡Hola! (Hello!)
- ¿Qué tal? (How's it going?)
- ¿Cómo estás? (How are you? - informal)

**Presentaciones:**
- Me llamo... (My name is...)
- Mucho gusto (Nice to meet you)
- Encantado/a (Pleased to meet you)""",
                "vocabulary": [
                    {"word": "Hola", "translation": "Hello", "example": "¡Hola! ¿Cómo estás?"},
                    {"word": "Buenos días", "translation": "Good morning", "example": "Buenos días, señor García."},
                    {"word": "Gracias", "translation": "Thank you", "example": "Muchas gracias por tu ayuda."},
                    {"word": "Por favor", "translation": "Please", "example": "Un café, por favor."},
                    {"word": "Adiós", "translation": "Goodbye", "example": "¡Adiós! Hasta mañana."}
                ],
                "grammar_points": ["Pronombres personales: yo, tú, él/ella, usted", "Verbo SER en presente: soy, eres, es", "Artículos: el, la, los, las"]
            },
            {
                "title": "Lección 2: Vocabulario Esencial",
                "content": """En esta lección aprenderás el vocabulario más útil para situaciones cotidianas.

**Números del 1 al 10:**
uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez

**Colores básicos:**
rojo, azul, verde, amarillo, blanco, negro, naranja, rosa

**Días de la semana:**
lunes, martes, miércoles, jueves, viernes, sábado, domingo

**Lugares comunes:**
- la casa (the house)
- la escuela (the school)
- el trabajo (the work/job)
- el restaurante (the restaurant)""",
                "vocabulary": [
                    {"word": "Casa", "translation": "House", "example": "Mi casa es grande."},
                    {"word": "Familia", "translation": "Family", "example": "Mi familia es pequeña."},
                    {"word": "Amigo", "translation": "Friend", "example": "Juan es mi amigo."},
                    {"word": "Trabajo", "translation": "Work", "example": "Voy al trabajo cada día."},
                    {"word": "Comida", "translation": "Food", "example": "La comida está deliciosa."}
                ],
                "grammar_points": ["Género de sustantivos: masculino y femenino", "Plural de sustantivos: -s, -es", "Adjetivos posesivos: mi, tu, su"]
            },
            {
                "title": "Lección 3: Gramática Fundamental",
                "content": """Domina las estructuras gramaticales esenciales del español.

**Verbos regulares en presente (-AR):**
- hablar: hablo, hablas, habla, hablamos, hablan
- trabajar: trabajo, trabajas, trabaja, trabajamos, trabajan

**Verbos regulares en presente (-ER):**
- comer: como, comes, come, comemos, comen
- beber: bebo, bebes, bebe, bebemos, beben

**Verbos regulares en presente (-IR):**
- vivir: vivo, vives, vive, vivimos, viven
- escribir: escribo, escribes, escribe, escribimos, escriben

**Estructura de oraciones:**
Sujeto + Verbo + Complemento
Ejemplo: Yo hablo español.""",
                "vocabulary": [
                    {"word": "Hablar", "translation": "To speak", "example": "Yo hablo español."},
                    {"word": "Comer", "translation": "To eat", "example": "Nosotros comemos pizza."},
                    {"word": "Vivir", "translation": "To live", "example": "Ellos viven en Madrid."},
                    {"word": "Escribir", "translation": "To write", "example": "Tú escribes una carta."},
                    {"word": "Leer", "translation": "To read", "example": "Ella lee un libro."}
                ],
                "grammar_points": ["Conjugación de verbos regulares -AR, -ER, -IR", "Estructura básica de oraciones", "Negación con 'no'"]
            },
            {
                "title": "Lección 4: La Familia y Descripciones",
                "content": """Aprende vocabulario sobre la familia y cómo describir personas.

**Miembros de la familia:**
- padre/madre (father/mother)
- hijo/hija (son/daughter)
- hermano/hermana (brother/sister)
- abuelo/abuela (grandfather/grandmother)
- tío/tía (uncle/aunt)
- primo/prima (cousin)

**Adjetivos para describir personas:**
- alto/bajo (tall/short)
- joven/viejo (young/old)
- guapo/feo (handsome/ugly)
- simpático/antipático (nice/unpleasant)

**Estructura: SER + adjetivo**
- Mi padre es alto.
- Mi hermana es simpática.""",
                "vocabulary": [
                    {"word": "Familia", "translation": "Family", "example": "Mi familia es grande."},
                    {"word": "Padre", "translation": "Father", "example": "Mi padre trabaja mucho."},
                    {"word": "Madre", "translation": "Mother", "example": "Mi madre cocina muy bien."},
                    {"word": "Hermano", "translation": "Brother", "example": "Tengo un hermano mayor."},
                    {"word": "Alto", "translation": "Tall", "example": "Mi abuelo es muy alto."}
                ],
                "grammar_points": ["Adjetivos: concordancia de género y número", "Verbo TENER: tengo, tienes, tiene", "Posesivos: mi, tu, su, nuestro"]
            },
            {
                "title": "Lección 5: Actividades Diarias",
                "content": """Aprende a hablar sobre tu rutina diaria y actividades cotidianas.

**Verbos reflexivos:**
- levantarse (to get up)
- ducharse (to shower)
- vestirse (to get dressed)
- acostarse (to go to bed)

**Expresiones de tiempo:**
- por la mañana (in the morning)
- por la tarde (in the afternoon)
- por la noche (at night)
- todos los días (every day)

**Ejemplo de rutina:**
Me levanto a las 7. Me ducho y me visto. Desayuno a las 8. Voy al trabajo a las 9.""",
                "vocabulary": [
                    {"word": "Levantarse", "translation": "To get up", "example": "Me levanto temprano."},
                    {"word": "Desayunar", "translation": "To have breakfast", "example": "Desayuno café con tostadas."},
                    {"word": "Trabajar", "translation": "To work", "example": "Trabajo en una oficina."},
                    {"word": "Almorzar", "translation": "To have lunch", "example": "Almuerzo a las 2."},
                    {"word": "Cenar", "translation": "To have dinner", "example": "Ceno con mi familia."}
                ],
                "grammar_points": ["Verbos reflexivos y su conjugación", "Expresiones de frecuencia: siempre, nunca, a veces", "La hora: ¿Qué hora es?"]
            },
            {
                "title": "Lección 6: Lugares y Direcciones",
                "content": """Aprende a preguntar y dar direcciones, y vocabulario de lugares.

**Lugares en la ciudad:**
- la estación (the station)
- el supermercado (the supermarket)
- el banco (the bank)
- la farmacia (the pharmacy)
- el hospital (the hospital)

**Preguntar direcciones:**
- ¿Dónde está...? (Where is...?)
- ¿Cómo llego a...? (How do I get to...?)

**Dar direcciones:**
- Sigue recto (Go straight)
- Gira a la derecha/izquierda (Turn right/left)
- Está al lado de... (It's next to...)
- Está enfrente de... (It's in front of...)""",
                "vocabulary": [
                    {"word": "Calle", "translation": "Street", "example": "Vivo en la calle Mayor."},
                    {"word": "Cerca", "translation": "Near", "example": "El banco está cerca."},
                    {"word": "Lejos", "translation": "Far", "example": "El aeropuerto está lejos."},
                    {"word": "Derecha", "translation": "Right", "example": "Gira a la derecha."},
                    {"word": "Izquierda", "translation": "Left", "example": "El parque está a la izquierda."}
                ],
                "grammar_points": ["Preposiciones de lugar: en, sobre, debajo, al lado de", "Verbo ESTAR para ubicación", "Imperativo: sigue, gira, cruza"]
            },
        ],
        "english": [
            {
                "title": "Lesson 1: Introduction and Greetings",
                "content": """Welcome to the English course. In this lesson you will learn basic greetings and introductions.

**Formal greetings:**
- Good morning
- Good afternoon
- Good evening
- How do you do?

**Informal greetings:**
- Hello! / Hi!
- How are you?
- What's up?

**Introductions:**
- My name is...
- Nice to meet you
- Pleased to meet you""",
                "vocabulary": [
                    {"word": "Hello", "translation": "Hola", "example": "Hello! How are you?"},
                    {"word": "Goodbye", "translation": "Adiós", "example": "Goodbye! See you tomorrow."},
                    {"word": "Please", "translation": "Por favor", "example": "A coffee, please."},
                    {"word": "Thank you", "translation": "Gracias", "example": "Thank you very much."},
                    {"word": "Welcome", "translation": "Bienvenido", "example": "Welcome to our class!"}
                ],
                "grammar_points": ["Personal pronouns: I, you, he, she, it, we, they", "Verb TO BE: am, is, are", "Articles: a, an, the"]
            },
            {
                "title": "Lesson 2: Essential Vocabulary",
                "content": """Learn the most useful vocabulary for everyday situations.

**Numbers 1 to 10:**
one, two, three, four, five, six, seven, eight, nine, ten

**Basic colors:**
red, blue, green, yellow, white, black, orange, pink

**Days of the week:**
Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

**Common places:**
- the house
- the school
- the office
- the restaurant""",
                "vocabulary": [
                    {"word": "House", "translation": "Casa", "example": "My house is big."},
                    {"word": "Family", "translation": "Familia", "example": "My family is small."},
                    {"word": "Friend", "translation": "Amigo", "example": "John is my friend."},
                    {"word": "Work", "translation": "Trabajo", "example": "I go to work every day."},
                    {"word": "Food", "translation": "Comida", "example": "The food is delicious."}
                ],
                "grammar_points": ["Singular and plural nouns", "Possessive adjectives: my, your, his, her", "There is / There are"]
            },
            {
                "title": "Lesson 3: Fundamental Grammar",
                "content": """Master the essential grammatical structures of English.

**Present Simple:**
- I work, you work, he/she works, we work, they work
- I eat, you eat, he/she eats, we eat, they eat

**Present Continuous:**
- I am working, you are working, he/she is working
- I am eating, you are eating, he/she is eating

**Question formation:**
- Do you speak English?
- Does he work here?
- Are you studying?

**Sentence structure:**
Subject + Verb + Object
Example: I speak English.""",
                "vocabulary": [
                    {"word": "Speak", "translation": "Hablar", "example": "I speak English."},
                    {"word": "Eat", "translation": "Comer", "example": "We eat pizza."},
                    {"word": "Live", "translation": "Vivir", "example": "They live in London."},
                    {"word": "Write", "translation": "Escribir", "example": "You write a letter."},
                    {"word": "Read", "translation": "Leer", "example": "She reads a book."}
                ],
                "grammar_points": ["Present Simple tense", "Present Continuous tense", "Question formation with do/does"]
            },
            {
                "title": "Lesson 4: Family and Descriptions",
                "content": """Learn vocabulary about family and how to describe people.

**Family members:**
- father/mother
- son/daughter
- brother/sister
- grandfather/grandmother
- uncle/aunt
- cousin

**Adjectives to describe people:**
- tall/short
- young/old
- handsome/ugly
- nice/unpleasant

**Structure: BE + adjective**
- My father is tall.
- My sister is nice.""",
                "vocabulary": [
                    {"word": "Family", "translation": "Familia", "example": "My family is big."},
                    {"word": "Father", "translation": "Padre", "example": "My father works a lot."},
                    {"word": "Mother", "translation": "Madre", "example": "My mother cooks very well."},
                    {"word": "Brother", "translation": "Hermano", "example": "I have an older brother."},
                    {"word": "Tall", "translation": "Alto", "example": "My grandfather is very tall."}
                ],
                "grammar_points": ["Adjectives: order and position", "Verb HAVE: have, has", "Possessives: my, your, his, her, our, their"]
            },
            {
                "title": "Lesson 5: Daily Activities",
                "content": """Learn to talk about your daily routine and everyday activities.

**Daily routine verbs:**
- wake up
- take a shower
- get dressed
- go to bed

**Time expressions:**
- in the morning
- in the afternoon
- at night
- every day

**Example routine:**
I wake up at 7. I take a shower and get dressed. I have breakfast at 8. I go to work at 9.""",
                "vocabulary": [
                    {"word": "Wake up", "translation": "Despertarse", "example": "I wake up early."},
                    {"word": "Breakfast", "translation": "Desayuno", "example": "I have coffee for breakfast."},
                    {"word": "Work", "translation": "Trabajo", "example": "I work in an office."},
                    {"word": "Lunch", "translation": "Almuerzo", "example": "I have lunch at 2."},
                    {"word": "Dinner", "translation": "Cena", "example": "I have dinner with my family."}
                ],
                "grammar_points": ["Adverbs of frequency: always, never, sometimes", "Telling the time: What time is it?", "Prepositions of time: at, in, on"]
            },
            {
                "title": "Lesson 6: Places and Directions",
                "content": """Learn to ask for and give directions, and vocabulary about places.

**Places in the city:**
- the station
- the supermarket
- the bank
- the pharmacy
- the hospital

**Asking for directions:**
- Where is...?
- How do I get to...?

**Giving directions:**
- Go straight
- Turn right/left
- It's next to...
- It's in front of...""",
                "vocabulary": [
                    {"word": "Street", "translation": "Calle", "example": "I live on Main Street."},
                    {"word": "Near", "translation": "Cerca", "example": "The bank is near."},
                    {"word": "Far", "translation": "Lejos", "example": "The airport is far."},
                    {"word": "Right", "translation": "Derecha", "example": "Turn right."},
                    {"word": "Left", "translation": "Izquierda", "example": "The park is on the left."}
                ],
                "grammar_points": ["Prepositions of place: in, on, under, next to", "There is / There are", "Imperative: go, turn, cross"]
            },
        ],
        "portuguese": [
            {
                "title": "Lição 1: Introdução e Saudações",
                "content": """Bem-vindo ao curso de português. Nesta lição você aprenderá saudações básicas.

**Saudações formais:**
- Bom dia (Good morning)
- Boa tarde (Good afternoon)
- Boa noite (Good evening)
- Como vai o senhor/a senhora?

**Saudações informais:**
- Olá! / Oi!
- Tudo bem?
- Como você está?

**Apresentações:**
- Meu nome é... / Eu me chamo...
- Prazer em conhecê-lo
- Muito prazer""",
                "vocabulary": [
                    {"word": "Olá", "translation": "Hello", "example": "Olá! Como vai você?"},
                    {"word": "Tchau", "translation": "Bye", "example": "Tchau! Até amanhã."},
                    {"word": "Obrigado/a", "translation": "Thank you", "example": "Muito obrigado pela ajuda."},
                    {"word": "Por favor", "translation": "Please", "example": "Um café, por favor."},
                    {"word": "Desculpe", "translation": "Sorry", "example": "Desculpe pelo atraso."}
                ],
                "grammar_points": ["Pronomes pessoais: eu, tu/você, ele/ela", "Verbo SER: sou, és, é, somos, são", "Artigos: o, a, os, as"]
            },
            {
                "title": "Lição 2: Vocabulário Essencial",
                "content": """Aprenda o vocabulário mais útil para situações do dia a dia.

**Números de 1 a 10:**
um, dois, três, quatro, cinco, seis, sete, oito, nove, dez

**Cores básicas:**
vermelho, azul, verde, amarelo, branco, preto, laranja, rosa

**Dias da semana:**
segunda-feira, terça-feira, quarta-feira, quinta-feira, sexta-feira, sábado, domingo""",
                "vocabulary": [
                    {"word": "Casa", "translation": "House", "example": "A minha casa é grande."},
                    {"word": "Família", "translation": "Family", "example": "A minha família é pequena."},
                    {"word": "Amigo", "translation": "Friend", "example": "O João é meu amigo."},
                    {"word": "Trabalho", "translation": "Work", "example": "Eu vou ao trabalho."},
                    {"word": "Comida", "translation": "Food", "example": "A comida está deliciosa."}
                ],
                "grammar_points": ["Gênero dos substantivos", "Plural dos substantivos", "Adjetivos possessivos: meu, teu, seu"]
            },
            {
                "title": "Lição 3: Gramática Fundamental",
                "content": """Domine as estruturas gramaticais essenciais do português.

**Verbos regulares em -AR:**
- falar: falo, falas, fala, falamos, falam
- trabalhar: trabalho, trabalhas, trabalha, trabalhamos, trabalham

**Verbos regulares em -ER:**
- comer: como, comes, come, comemos, comem
- beber: bebo, bebes, bebe, bebemos, bebem

**Verbos regulares em -IR:**
- partir: parto, partes, parte, partimos, partem""",
                "vocabulary": [
                    {"word": "Falar", "translation": "To speak", "example": "Eu falo português."},
                    {"word": "Comer", "translation": "To eat", "example": "Nós comemos pizza."},
                    {"word": "Viver", "translation": "To live", "example": "Eles vivem em Lisboa."},
                    {"word": "Escrever", "translation": "To write", "example": "Tu escreves uma carta."},
                    {"word": "Ler", "translation": "To read", "example": "Ela lê um livro."}
                ],
                "grammar_points": ["Conjugação de verbos regulares -AR, -ER, -IR", "Estrutura básica de frases", "Negação com 'não'"]
            },
            {
                "title": "Lição 4: A Família e Descrições",
                "content": """Aprenda vocabulário sobre a família e como descrever pessoas.

**Membros da família:**
- pai/mãe (father/mother)
- filho/filha (son/daughter)
- irmão/irmã (brother/sister)
- avô/avó (grandfather/grandmother)
- tio/tia (uncle/aunt)
- primo/prima (cousin)

**Adjetivos para descrever pessoas:**
- alto/baixo (tall/short)
- jovem/velho (young/old)
- bonito/feio (handsome/ugly)
- simpático/antipático (nice/unpleasant)""",
                "vocabulary": [
                    {"word": "Família", "translation": "Family", "example": "A minha família é grande."},
                    {"word": "Pai", "translation": "Father", "example": "O meu pai trabalha muito."},
                    {"word": "Mãe", "translation": "Mother", "example": "A minha mãe cozinha muito bem."},
                    {"word": "Irmão", "translation": "Brother", "example": "Tenho um irmão mais velho."},
                    {"word": "Alto", "translation": "Tall", "example": "O meu avô é muito alto."}
                ],
                "grammar_points": ["Adjetivos: concordância de gênero e número", "Verbo TER: tenho, tens, tem", "Possessivos: meu, teu, seu, nosso"]
            },
            {
                "title": "Lição 5: Atividades Diárias",
                "content": """Aprenda a falar sobre sua rotina diária.

**Verbos reflexivos:**
- acordar (to wake up)
- tomar banho (to shower)
- vestir-se (to get dressed)
- deitar-se (to go to bed)

**Expressões de tempo:**
- de manhã (in the morning)
- à tarde (in the afternoon)
- à noite (at night)
- todos os dias (every day)""",
                "vocabulary": [
                    {"word": "Acordar", "translation": "To wake up", "example": "Eu acordo cedo."},
                    {"word": "Pequeno-almoço", "translation": "Breakfast", "example": "Tomo o pequeno-almoço às 8."},
                    {"word": "Trabalhar", "translation": "To work", "example": "Trabalho num escritório."},
                    {"word": "Almoçar", "translation": "To have lunch", "example": "Almoço às 13 horas."},
                    {"word": "Jantar", "translation": "To have dinner", "example": "Janto com a família."}
                ],
                "grammar_points": ["Verbos reflexivos e sua conjugação", "Expressões de frequência", "As horas: Que horas são?"]
            },
            {
                "title": "Lição 6: Lugares e Direções",
                "content": """Aprenda a pedir e dar direções.

**Lugares na cidade:**
- a estação (the station)
- o supermercado (the supermarket)
- o banco (the bank)
- a farmácia (the pharmacy)

**Pedir direções:**
- Onde fica...? (Where is...?)
- Como chego a...? (How do I get to...?)

**Dar direções:**
- Siga em frente (Go straight)
- Vire à direita/esquerda (Turn right/left)""",
                "vocabulary": [
                    {"word": "Rua", "translation": "Street", "example": "Moro na Rua Principal."},
                    {"word": "Perto", "translation": "Near", "example": "O banco fica perto."},
                    {"word": "Longe", "translation": "Far", "example": "O aeroporto fica longe."},
                    {"word": "Direita", "translation": "Right", "example": "Vire à direita."},
                    {"word": "Esquerda", "translation": "Left", "example": "O parque fica à esquerda."}
                ],
                "grammar_points": ["Preposições de lugar: em, sobre, debaixo", "Verbo FICAR para localização", "Imperativo: siga, vire, atravesse"]
            },
        ],
        "german": [
            {
                "title": "Lektion 1: Einführung und Begrüßungen",
                "content": """Willkommen zum Deutschkurs. In dieser Lektion lernen Sie grundlegende Begrüßungen.

**Formelle Begrüßungen:**
- Guten Morgen (Good morning)
- Guten Tag (Good day)
- Guten Abend (Good evening)
- Wie geht es Ihnen?

**Informelle Begrüßungen:**
- Hallo!
- Wie geht's?
- Was geht?

**Vorstellungen:**
- Ich heiße... / Mein Name ist...
- Freut mich
- Angenehm""",
                "vocabulary": [
                    {"word": "Hallo", "translation": "Hello", "example": "Hallo! Wie geht es dir?"},
                    {"word": "Tschüss", "translation": "Bye", "example": "Tschüss! Bis morgen."},
                    {"word": "Danke", "translation": "Thank you", "example": "Vielen Dank für Ihre Hilfe."},
                    {"word": "Bitte", "translation": "Please/You're welcome", "example": "Einen Kaffee, bitte."},
                    {"word": "Entschuldigung", "translation": "Sorry/Excuse me", "example": "Entschuldigung, wo ist der Bahnhof?"}
                ],
                "grammar_points": ["Personalpronomen: ich, du, er/sie/es, wir, sie", "Verb SEIN: bin, bist, ist, sind", "Artikel: der, die, das"]
            },
            {
                "title": "Lektion 2: Grundwortschatz",
                "content": """Lernen Sie den wichtigsten Wortschatz für alltägliche Situationen.

**Zahlen von 1 bis 10:**
eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn

**Grundfarben:**
rot, blau, grün, gelb, weiß, schwarz, orange, rosa

**Wochentage:**
Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag, Sonntag""",
                "vocabulary": [
                    {"word": "Haus", "translation": "House", "example": "Mein Haus ist groß."},
                    {"word": "Familie", "translation": "Family", "example": "Meine Familie ist klein."},
                    {"word": "Freund", "translation": "Friend", "example": "Hans ist mein Freund."},
                    {"word": "Arbeit", "translation": "Work", "example": "Ich gehe zur Arbeit."},
                    {"word": "Essen", "translation": "Food", "example": "Das Essen ist lecker."}
                ],
                "grammar_points": ["Genus der Substantive: maskulin, feminin, neutral", "Plural der Substantive", "Possessivartikel: mein, dein, sein"]
            },
            {
                "title": "Lektion 3: Grundgrammatik",
                "content": """Beherrschen Sie die wesentlichen grammatikalischen Strukturen.

**Regelmäßige Verben im Präsens:**
- spielen: ich spiele, du spielst, er spielt, wir spielen
- arbeiten: ich arbeite, du arbeitest, er arbeitet
- lernen: ich lerne, du lernst, er lernt

**Wichtige unregelmäßige Verben:**
- haben: ich habe, du hast, er hat
- sein: ich bin, du bist, er ist

**Satzstruktur:**
Subjekt + Verb + Objekt
Beispiel: Ich spreche Deutsch.""",
                "vocabulary": [
                    {"word": "Sprechen", "translation": "To speak", "example": "Ich spreche Deutsch."},
                    {"word": "Essen", "translation": "To eat", "example": "Wir essen Pizza."},
                    {"word": "Wohnen", "translation": "To live", "example": "Sie wohnen in Berlin."},
                    {"word": "Schreiben", "translation": "To write", "example": "Du schreibst einen Brief."},
                    {"word": "Lesen", "translation": "To read", "example": "Sie liest ein Buch."}
                ],
                "grammar_points": ["Konjugation regelmäßiger Verben", "Verben haben und sein", "Grundlegende Satzstellung"]
            },
            {
                "title": "Lektion 4: Familie und Beschreibungen",
                "content": """Lernen Sie Vokabular über die Familie und wie man Personen beschreibt.

**Familienmitglieder:**
- Vater/Mutter (father/mother)
- Sohn/Tochter (son/daughter)
- Bruder/Schwester (brother/sister)
- Großvater/Großmutter (grandfather/grandmother)
- Onkel/Tante (uncle/aunt)
- Cousin/Cousine (cousin)

**Adjektive zur Personenbeschreibung:**
- groß/klein (tall/short)
- jung/alt (young/old)
- hübsch/hässlich (handsome/ugly)
- nett/unfreundlich (nice/unfriendly)""",
                "vocabulary": [
                    {"word": "Familie", "translation": "Family", "example": "Meine Familie ist groß."},
                    {"word": "Vater", "translation": "Father", "example": "Mein Vater arbeitet viel."},
                    {"word": "Mutter", "translation": "Mother", "example": "Meine Mutter kocht sehr gut."},
                    {"word": "Bruder", "translation": "Brother", "example": "Ich habe einen älteren Bruder."},
                    {"word": "Groß", "translation": "Tall/Big", "example": "Mein Großvater ist sehr groß."}
                ],
                "grammar_points": ["Adjektivdeklination", "Verb HABEN: habe, hast, hat", "Possessivartikel: mein, dein, sein, ihr, unser"]
            },
            {
                "title": "Lektion 5: Tägliche Aktivitäten",
                "content": """Lernen Sie, über Ihren Tagesablauf zu sprechen.

**Reflexive Verben:**
- aufstehen (to get up)
- sich duschen (to shower)
- sich anziehen (to get dressed)
- ins Bett gehen (to go to bed)

**Zeitausdrücke:**
- morgens (in the morning)
- nachmittags (in the afternoon)
- abends (in the evening)
- jeden Tag (every day)""",
                "vocabulary": [
                    {"word": "Aufstehen", "translation": "To get up", "example": "Ich stehe früh auf."},
                    {"word": "Frühstück", "translation": "Breakfast", "example": "Ich esse Frühstück um 8 Uhr."},
                    {"word": "Arbeiten", "translation": "To work", "example": "Ich arbeite in einem Büro."},
                    {"word": "Mittagessen", "translation": "Lunch", "example": "Das Mittagessen ist um 12."},
                    {"word": "Abendessen", "translation": "Dinner", "example": "Wir essen Abendessen zusammen."}
                ],
                "grammar_points": ["Reflexive Verben und ihre Konjugation", "Trennbare Verben: aufstehen, anfangen", "Die Uhrzeit: Wie spät ist es?"]
            },
            {
                "title": "Lektion 6: Orte und Wegbeschreibungen",
                "content": """Lernen Sie, nach dem Weg zu fragen und Wegbeschreibungen zu geben.

**Orte in der Stadt:**
- der Bahnhof (the station)
- der Supermarkt (the supermarket)
- die Bank (the bank)
- die Apotheke (the pharmacy)

**Nach dem Weg fragen:**
- Wo ist...? (Where is...?)
- Wie komme ich zu...? (How do I get to...?)

**Wegbeschreibungen geben:**
- Gehen Sie geradeaus (Go straight)
- Biegen Sie rechts/links ab (Turn right/left)""",
                "vocabulary": [
                    {"word": "Straße", "translation": "Street", "example": "Ich wohne in der Hauptstraße."},
                    {"word": "Nah", "translation": "Near", "example": "Die Bank ist nah."},
                    {"word": "Weit", "translation": "Far", "example": "Der Flughafen ist weit."},
                    {"word": "Rechts", "translation": "Right", "example": "Biegen Sie rechts ab."},
                    {"word": "Links", "translation": "Left", "example": "Der Park ist links."}
                ],
                "grammar_points": ["Präpositionen mit Dativ: in, an, auf, neben", "Imperativ: gehen Sie, biegen Sie ab", "Wechselpräpositionen"]
            },
        ],
    }
    
    # Create courses and lessons
    courses_created = 0
    lessons_created = 0
    
    # Level-specific lesson content for each language
    level_lessons = {
        "spanish": {
            "A1": [
                {"title": "Lección 1: Saludos Básicos", "content": "Aprende los saludos más básicos: Hola, Buenos días, Buenas tardes, Buenas noches, Adiós.", "vocabulary": [{"word": "Hola", "translation": "Hello"}, {"word": "Adiós", "translation": "Goodbye"}, {"word": "Gracias", "translation": "Thank you"}, {"word": "Por favor", "translation": "Please"}, {"word": "Sí/No", "translation": "Yes/No"}], "grammar_points": ["Pronombres: yo, tú, él/ella", "Verbo SER: soy, eres, es"]},
                {"title": "Lección 2: Presentaciones", "content": "Aprende a presentarte: Me llamo..., Soy de..., Tengo... años.", "vocabulary": [{"word": "Nombre", "translation": "Name"}, {"word": "Edad", "translation": "Age"}, {"word": "País", "translation": "Country"}, {"word": "Ciudad", "translation": "City"}, {"word": "Profesión", "translation": "Profession"}], "grammar_points": ["Verbo TENER", "Verbo LLAMARSE"]},
                {"title": "Lección 3: Números 1-20", "content": "Aprende los números del 1 al 20 en español.", "vocabulary": [{"word": "Uno", "translation": "One"}, {"word": "Diez", "translation": "Ten"}, {"word": "Veinte", "translation": "Twenty"}, {"word": "Cero", "translation": "Zero"}, {"word": "Número", "translation": "Number"}], "grammar_points": ["Números cardinales", "¿Cuántos?"]},
                {"title": "Lección 4: Colores Básicos", "content": "Aprende los colores: rojo, azul, verde, amarillo, blanco, negro.", "vocabulary": [{"word": "Rojo", "translation": "Red"}, {"word": "Azul", "translation": "Blue"}, {"word": "Verde", "translation": "Green"}, {"word": "Amarillo", "translation": "Yellow"}, {"word": "Negro", "translation": "Black"}], "grammar_points": ["Concordancia de género", "Adjetivos de color"]},
                {"title": "Lección 5: Familia Inmediata", "content": "Vocabulario de familia: padre, madre, hermano, hermana.", "vocabulary": [{"word": "Padre", "translation": "Father"}, {"word": "Madre", "translation": "Mother"}, {"word": "Hermano", "translation": "Brother"}, {"word": "Hermana", "translation": "Sister"}, {"word": "Familia", "translation": "Family"}], "grammar_points": ["Posesivos: mi, tu, su", "Plural de sustantivos"]},
                {"title": "Lección 6: Objetos del Aula", "content": "Vocabulario escolar: libro, cuaderno, lápiz, mesa, silla.", "vocabulary": [{"word": "Libro", "translation": "Book"}, {"word": "Lápiz", "translation": "Pencil"}, {"word": "Mesa", "translation": "Table"}, {"word": "Silla", "translation": "Chair"}, {"word": "Pizarra", "translation": "Blackboard"}], "grammar_points": ["Artículos: el, la, los, las", "Hay + sustantivo"]},
            ],
            "A2": [
                {"title": "Lección 1: Rutina Diaria", "content": "Describe tu día: Me levanto, desayuno, trabajo, ceno, me acuesto.", "vocabulary": [{"word": "Levantarse", "translation": "To get up"}, {"word": "Desayunar", "translation": "To have breakfast"}, {"word": "Almorzar", "translation": "To have lunch"}, {"word": "Cenar", "translation": "To have dinner"}, {"word": "Acostarse", "translation": "To go to bed"}], "grammar_points": ["Verbos reflexivos", "Expresiones de frecuencia"]},
                {"title": "Lección 2: La Casa", "content": "Partes de la casa: cocina, dormitorio, baño, salón, jardín.", "vocabulary": [{"word": "Cocina", "translation": "Kitchen"}, {"word": "Dormitorio", "translation": "Bedroom"}, {"word": "Baño", "translation": "Bathroom"}, {"word": "Salón", "translation": "Living room"}, {"word": "Jardín", "translation": "Garden"}], "grammar_points": ["Preposiciones de lugar", "Estar + ubicación"]},
                {"title": "Lección 3: Compras y Precios", "content": "En la tienda: ¿Cuánto cuesta? Me llevo este. ¿Tiene...?", "vocabulary": [{"word": "Tienda", "translation": "Shop"}, {"word": "Precio", "translation": "Price"}, {"word": "Barato", "translation": "Cheap"}, {"word": "Caro", "translation": "Expensive"}, {"word": "Dinero", "translation": "Money"}], "grammar_points": ["Números 20-100", "Verbo COSTAR"]},
                {"title": "Lección 4: El Tiempo Atmosférico", "content": "Clima: Hace sol, llueve, nieva, hace frío, hace calor.", "vocabulary": [{"word": "Sol", "translation": "Sun"}, {"word": "Lluvia", "translation": "Rain"}, {"word": "Nieve", "translation": "Snow"}, {"word": "Viento", "translation": "Wind"}, {"word": "Nube", "translation": "Cloud"}], "grammar_points": ["Expresiones con HACER", "Verbos impersonales"]},
                {"title": "Lección 5: Pasado Simple", "content": "Hablar del pasado: Ayer fui, comí, hablé, vi, estuve.", "vocabulary": [{"word": "Ayer", "translation": "Yesterday"}, {"word": "La semana pasada", "translation": "Last week"}, {"word": "El año pasado", "translation": "Last year"}, {"word": "Anoche", "translation": "Last night"}, {"word": "Antes", "translation": "Before"}], "grammar_points": ["Pretérito indefinido regular", "Marcadores temporales"]},
                {"title": "Lección 6: Planes Futuros", "content": "Expresar planes: Voy a viajar, Mañana iré, El próximo año...", "vocabulary": [{"word": "Mañana", "translation": "Tomorrow"}, {"word": "Próximo", "translation": "Next"}, {"word": "Futuro", "translation": "Future"}, {"word": "Plan", "translation": "Plan"}, {"word": "Vacaciones", "translation": "Vacation"}], "grammar_points": ["IR A + infinitivo", "Futuro simple"]},
            ],
            "B1": [
                {"title": "Lección 1: Experiencias de Vida", "content": "Pretérito perfecto: He viajado, he conocido, nunca he...", "vocabulary": [{"word": "Experiencia", "translation": "Experience"}, {"word": "Viaje", "translation": "Trip"}, {"word": "Aventura", "translation": "Adventure"}, {"word": "Recuerdo", "translation": "Memory"}, {"word": "Oportunidad", "translation": "Opportunity"}], "grammar_points": ["Pretérito perfecto", "Participios regulares e irregulares"]},
                {"title": "Lección 2: Dar Consejos", "content": "Expresar consejos: Deberías, te recomiendo, es mejor que...", "vocabulary": [{"word": "Consejo", "translation": "Advice"}, {"word": "Recomendar", "translation": "To recommend"}, {"word": "Sugerir", "translation": "To suggest"}, {"word": "Convenir", "translation": "To be suitable"}, {"word": "Evitar", "translation": "To avoid"}], "grammar_points": ["Condicional simple", "Subjuntivo presente básico"]},
                {"title": "Lección 3: Salud y Bienestar", "content": "En el médico: Me duele, tengo fiebre, necesito una receta.", "vocabulary": [{"word": "Médico", "translation": "Doctor"}, {"word": "Enfermedad", "translation": "Illness"}, {"word": "Síntoma", "translation": "Symptom"}, {"word": "Medicamento", "translation": "Medicine"}, {"word": "Cita", "translation": "Appointment"}], "grammar_points": ["Verbo DOLER", "Expresiones de malestar"]},
                {"title": "Lección 4: Medio Ambiente", "content": "Ecología: reciclar, contaminar, energía renovable, cambio climático.", "vocabulary": [{"word": "Medio ambiente", "translation": "Environment"}, {"word": "Reciclar", "translation": "To recycle"}, {"word": "Contaminación", "translation": "Pollution"}, {"word": "Naturaleza", "translation": "Nature"}, {"word": "Sostenible", "translation": "Sustainable"}], "grammar_points": ["Oraciones impersonales", "Se pasivo"]},
                {"title": "Lección 5: Mundo Laboral", "content": "Trabajo: entrevista, currículum, experiencia, habilidades.", "vocabulary": [{"word": "Empleo", "translation": "Job"}, {"word": "Entrevista", "translation": "Interview"}, {"word": "Sueldo", "translation": "Salary"}, {"word": "Jefe", "translation": "Boss"}, {"word": "Compañero", "translation": "Colleague"}], "grammar_points": ["Oraciones condicionales tipo 1", "Conectores causales"]},
                {"title": "Lección 6: Viajes y Turismo", "content": "Planificar viajes: reservar, alojamiento, itinerario, destino.", "vocabulary": [{"word": "Reserva", "translation": "Reservation"}, {"word": "Alojamiento", "translation": "Accommodation"}, {"word": "Vuelo", "translation": "Flight"}, {"word": "Equipaje", "translation": "Luggage"}, {"word": "Turista", "translation": "Tourist"}], "grammar_points": ["Oraciones temporales con CUANDO", "Futuro en subordinadas"]},
            ],
            "B2": [
                {"title": "Lección 1: Debates y Opiniones", "content": "Argumentar: Desde mi punto de vista, considero que, sin embargo...", "vocabulary": [{"word": "Argumento", "translation": "Argument"}, {"word": "Perspectiva", "translation": "Perspective"}, {"word": "Defender", "translation": "To defend"}, {"word": "Refutar", "translation": "To refute"}, {"word": "Consenso", "translation": "Consensus"}], "grammar_points": ["Conectores argumentativos", "Subjuntivo en expresiones de opinión"]},
                {"title": "Lección 2: Condicionales Complejos", "content": "Si hubiera sabido, habría ido. Si tuviera tiempo, lo haría.", "vocabulary": [{"word": "Hipótesis", "translation": "Hypothesis"}, {"word": "Condición", "translation": "Condition"}, {"word": "Consecuencia", "translation": "Consequence"}, {"word": "Probabilidad", "translation": "Probability"}, {"word": "Suposición", "translation": "Assumption"}], "grammar_points": ["Condicionales tipo 2 y 3", "Pluscuamperfecto de subjuntivo"]},
                {"title": "Lección 3: Cultura y Sociedad", "content": "Temas sociales: inmigración, globalización, tradiciones, identidad.", "vocabulary": [{"word": "Sociedad", "translation": "Society"}, {"word": "Cultura", "translation": "Culture"}, {"word": "Tradición", "translation": "Tradition"}, {"word": "Globalización", "translation": "Globalization"}, {"word": "Identidad", "translation": "Identity"}], "grammar_points": ["Voz pasiva", "Oraciones de relativo"]},
                {"title": "Lección 4: Tecnología y Futuro", "content": "Innovación: inteligencia artificial, redes sociales, privacidad digital.", "vocabulary": [{"word": "Tecnología", "translation": "Technology"}, {"word": "Innovación", "translation": "Innovation"}, {"word": "Digital", "translation": "Digital"}, {"word": "Privacidad", "translation": "Privacy"}, {"word": "Algoritmo", "translation": "Algorithm"}], "grammar_points": ["Futuro perfecto", "Expresiones de probabilidad"]},
                {"title": "Lección 5: Arte y Literatura", "content": "Crítica cultural: analizar, interpretar, simbolismo, metáfora.", "vocabulary": [{"word": "Obra", "translation": "Work"}, {"word": "Autor", "translation": "Author"}, {"word": "Estilo", "translation": "Style"}, {"word": "Crítica", "translation": "Criticism"}, {"word": "Influencia", "translation": "Influence"}], "grammar_points": ["Oraciones concesivas", "Aunque + subjuntivo/indicativo"]},
                {"title": "Lección 6: Economía y Negocios", "content": "Mundo empresarial: inversión, mercado, estrategia, competencia.", "vocabulary": [{"word": "Empresa", "translation": "Company"}, {"word": "Inversión", "translation": "Investment"}, {"word": "Mercado", "translation": "Market"}, {"word": "Beneficio", "translation": "Profit"}, {"word": "Competencia", "translation": "Competition"}], "grammar_points": ["Estilo indirecto", "Verbos de cambio"]},
            ],
            "C1": [
                {"title": "Lección 1: Matices del Subjuntivo", "content": "Uso avanzado: expresiones de duda, deseo, emoción en contextos complejos.", "vocabulary": [{"word": "Matiz", "translation": "Nuance"}, {"word": "Sutileza", "translation": "Subtlety"}, {"word": "Ambigüedad", "translation": "Ambiguity"}, {"word": "Precisión", "translation": "Precision"}, {"word": "Registro", "translation": "Register"}], "grammar_points": ["Subjuntivo en oraciones independientes", "Alternancia indicativo/subjuntivo"]},
                {"title": "Lección 2: Expresiones Idiomáticas", "content": "Modismos: estar en las nubes, meter la pata, ponerse las pilas.", "vocabulary": [{"word": "Modismo", "translation": "Idiom"}, {"word": "Expresión", "translation": "Expression"}, {"word": "Coloquial", "translation": "Colloquial"}, {"word": "Figurado", "translation": "Figurative"}, {"word": "Literal", "translation": "Literal"}], "grammar_points": ["Frases hechas", "Lenguaje figurado"]},
                {"title": "Lección 3: Redacción Académica", "content": "Escribir ensayos: tesis, argumentos, conclusiones, citas.", "vocabulary": [{"word": "Ensayo", "translation": "Essay"}, {"word": "Tesis", "translation": "Thesis"}, {"word": "Hipótesis", "translation": "Hypothesis"}, {"word": "Bibliografía", "translation": "Bibliography"}, {"word": "Citar", "translation": "To cite"}], "grammar_points": ["Conectores del discurso académico", "Nominalización"]},
                {"title": "Lección 4: Variedades del Español", "content": "Dialectos: español de América, voseo, diferencias léxicas.", "vocabulary": [{"word": "Dialecto", "translation": "Dialect"}, {"word": "Variante", "translation": "Variant"}, {"word": "Acento", "translation": "Accent"}, {"word": "Léxico", "translation": "Lexicon"}, {"word": "Regionalismo", "translation": "Regionalism"}], "grammar_points": ["Voseo argentino", "Diferencias España/América"]},
                {"title": "Lección 5: Periodismo y Medios", "content": "Análisis de noticias: titular, editorial, sesgo, fuentes.", "vocabulary": [{"word": "Periodismo", "translation": "Journalism"}, {"word": "Editorial", "translation": "Editorial"}, {"word": "Fuente", "translation": "Source"}, {"word": "Sesgo", "translation": "Bias"}, {"word": "Objetividad", "translation": "Objectivity"}], "grammar_points": ["Estilo periodístico", "Titulares y elipsis"]},
                {"title": "Lección 6: Humor y Sarcasmo", "content": "Entender ironía, dobles sentidos, chistes culturales.", "vocabulary": [{"word": "Ironía", "translation": "Irony"}, {"word": "Sarcasmo", "translation": "Sarcasm"}, {"word": "Doble sentido", "translation": "Double meaning"}, {"word": "Chiste", "translation": "Joke"}, {"word": "Ingenio", "translation": "Wit"}], "grammar_points": ["Entonación irónica", "Implicaturas"]},
            ],
            "C2": [
                {"title": "Lección 1: Literatura Clásica", "content": "Análisis de Cervantes, Garcilaso, Góngora: estilo, época, influencia.", "vocabulary": [{"word": "Clásico", "translation": "Classic"}, {"word": "Barroco", "translation": "Baroque"}, {"word": "Renacimiento", "translation": "Renaissance"}, {"word": "Siglo de Oro", "translation": "Golden Age"}, {"word": "Métrica", "translation": "Metrics"}], "grammar_points": ["Español antiguo", "Evolución lingüística"]},
                {"title": "Lección 2: Traducción Literaria", "content": "Técnicas de traducción: equivalencia, adaptación, préstamo.", "vocabulary": [{"word": "Traducción", "translation": "Translation"}, {"word": "Equivalencia", "translation": "Equivalence"}, {"word": "Adaptación", "translation": "Adaptation"}, {"word": "Fidelidad", "translation": "Fidelity"}, {"word": "Interpretación", "translation": "Interpretation"}], "grammar_points": ["Falsos amigos", "Calcos semánticos"]},
                {"title": "Lección 3: Lingüística Aplicada", "content": "Fonología, morfología, sintaxis, semántica, pragmática.", "vocabulary": [{"word": "Fonema", "translation": "Phoneme"}, {"word": "Morfema", "translation": "Morpheme"}, {"word": "Sintaxis", "translation": "Syntax"}, {"word": "Semántica", "translation": "Semantics"}, {"word": "Pragmática", "translation": "Pragmatics"}], "grammar_points": ["Análisis sintáctico", "Funciones del lenguaje"]},
                {"title": "Lección 4: Retórica y Oratoria", "content": "Discurso persuasivo: ethos, pathos, logos, figuras retóricas.", "vocabulary": [{"word": "Retórica", "translation": "Rhetoric"}, {"word": "Oratoria", "translation": "Oratory"}, {"word": "Persuasión", "translation": "Persuasion"}, {"word": "Elocuencia", "translation": "Eloquence"}, {"word": "Discurso", "translation": "Speech"}], "grammar_points": ["Figuras retóricas", "Estructura argumentativa"]},
                {"title": "Lección 5: Español Jurídico", "content": "Lenguaje legal: términos, documentos, contratos, legislación.", "vocabulary": [{"word": "Ley", "translation": "Law"}, {"word": "Contrato", "translation": "Contract"}, {"word": "Demanda", "translation": "Lawsuit"}, {"word": "Jurisprudencia", "translation": "Jurisprudence"}, {"word": "Cláusula", "translation": "Clause"}], "grammar_points": ["Lenguaje formal", "Fórmulas jurídicas"]},
                {"title": "Lección 6: Creación Literaria", "content": "Escritura creativa: narrativa, poesía, estilo propio.", "vocabulary": [{"word": "Narrativa", "translation": "Narrative"}, {"word": "Poesía", "translation": "Poetry"}, {"word": "Personaje", "translation": "Character"}, {"word": "Trama", "translation": "Plot"}, {"word": "Voz narrativa", "translation": "Narrative voice"}], "grammar_points": ["Recursos estilísticos", "Puntuación expresiva"]},
            ],
        },
        "english": {
            "A1": [
                {"title": "Lesson 1: Basic Greetings", "content": "Learn basic greetings: Hello, Good morning, Good afternoon, Good evening, Goodbye.", "vocabulary": [{"word": "Hello", "translation": "Hola"}, {"word": "Goodbye", "translation": "Adiós"}, {"word": "Thank you", "translation": "Gracias"}, {"word": "Please", "translation": "Por favor"}, {"word": "Yes/No", "translation": "Sí/No"}], "grammar_points": ["Pronouns: I, you, he/she", "Verb TO BE: am, is, are"]},
                {"title": "Lesson 2: Introductions", "content": "Learn to introduce yourself: My name is..., I am from..., I am... years old.", "vocabulary": [{"word": "Name", "translation": "Nombre"}, {"word": "Age", "translation": "Edad"}, {"word": "Country", "translation": "País"}, {"word": "City", "translation": "Ciudad"}, {"word": "Job", "translation": "Trabajo"}], "grammar_points": ["Verb TO BE questions", "Possessive adjectives"]},
                {"title": "Lesson 3: Numbers 1-20", "content": "Learn numbers from 1 to 20 in English.", "vocabulary": [{"word": "One", "translation": "Uno"}, {"word": "Ten", "translation": "Diez"}, {"word": "Twenty", "translation": "Veinte"}, {"word": "Zero", "translation": "Cero"}, {"word": "Number", "translation": "Número"}], "grammar_points": ["Cardinal numbers", "How many?"]},
                {"title": "Lesson 4: Basic Colors", "content": "Learn colors: red, blue, green, yellow, white, black.", "vocabulary": [{"word": "Red", "translation": "Rojo"}, {"word": "Blue", "translation": "Azul"}, {"word": "Green", "translation": "Verde"}, {"word": "Yellow", "translation": "Amarillo"}, {"word": "Black", "translation": "Negro"}], "grammar_points": ["Adjective position", "Color adjectives"]},
                {"title": "Lesson 5: Immediate Family", "content": "Family vocabulary: father, mother, brother, sister.", "vocabulary": [{"word": "Father", "translation": "Padre"}, {"word": "Mother", "translation": "Madre"}, {"word": "Brother", "translation": "Hermano"}, {"word": "Sister", "translation": "Hermana"}, {"word": "Family", "translation": "Familia"}], "grammar_points": ["Possessives: my, your, his/her", "Plural nouns"]},
                {"title": "Lesson 6: Classroom Objects", "content": "School vocabulary: book, notebook, pencil, table, chair.", "vocabulary": [{"word": "Book", "translation": "Libro"}, {"word": "Pencil", "translation": "Lápiz"}, {"word": "Table", "translation": "Mesa"}, {"word": "Chair", "translation": "Silla"}, {"word": "Board", "translation": "Pizarra"}], "grammar_points": ["Articles: a, an, the", "There is/are"]},
            ],
            "A2": [
                {"title": "Lesson 1: Daily Routine", "content": "Describe your day: I wake up, have breakfast, work, have dinner, go to bed.", "vocabulary": [{"word": "Wake up", "translation": "Despertarse"}, {"word": "Breakfast", "translation": "Desayuno"}, {"word": "Lunch", "translation": "Almuerzo"}, {"word": "Dinner", "translation": "Cena"}, {"word": "Go to bed", "translation": "Acostarse"}], "grammar_points": ["Present Simple routine", "Frequency adverbs"]},
                {"title": "Lesson 2: The House", "content": "Parts of the house: kitchen, bedroom, bathroom, living room, garden.", "vocabulary": [{"word": "Kitchen", "translation": "Cocina"}, {"word": "Bedroom", "translation": "Dormitorio"}, {"word": "Bathroom", "translation": "Baño"}, {"word": "Living room", "translation": "Salón"}, {"word": "Garden", "translation": "Jardín"}], "grammar_points": ["Prepositions of place", "There is/are"]},
                {"title": "Lesson 3: Shopping and Prices", "content": "At the shop: How much is it? I'll take this. Do you have...?", "vocabulary": [{"word": "Shop", "translation": "Tienda"}, {"word": "Price", "translation": "Precio"}, {"word": "Cheap", "translation": "Barato"}, {"word": "Expensive", "translation": "Caro"}, {"word": "Money", "translation": "Dinero"}], "grammar_points": ["Numbers 20-100", "How much/many"]},
                {"title": "Lesson 4: Weather", "content": "Climate: It's sunny, it's raining, it's snowing, it's cold, it's hot.", "vocabulary": [{"word": "Sun", "translation": "Sol"}, {"word": "Rain", "translation": "Lluvia"}, {"word": "Snow", "translation": "Nieve"}, {"word": "Wind", "translation": "Viento"}, {"word": "Cloud", "translation": "Nube"}], "grammar_points": ["It's + adjective", "Weather expressions"]},
                {"title": "Lesson 5: Past Simple", "content": "Talking about the past: Yesterday I went, ate, spoke, saw, was.", "vocabulary": [{"word": "Yesterday", "translation": "Ayer"}, {"word": "Last week", "translation": "La semana pasada"}, {"word": "Last year", "translation": "El año pasado"}, {"word": "Last night", "translation": "Anoche"}, {"word": "Before", "translation": "Antes"}], "grammar_points": ["Past Simple regular", "Past Simple irregular"]},
                {"title": "Lesson 6: Future Plans", "content": "Expressing plans: I'm going to travel, Tomorrow I will, Next year...", "vocabulary": [{"word": "Tomorrow", "translation": "Mañana"}, {"word": "Next", "translation": "Próximo"}, {"word": "Future", "translation": "Futuro"}, {"word": "Plan", "translation": "Plan"}, {"word": "Vacation", "translation": "Vacaciones"}], "grammar_points": ["Going to + infinitive", "Will future"]},
            ],
            "B1": [
                {"title": "Lesson 1: Life Experiences", "content": "Present Perfect: I have traveled, I have met, I have never...", "vocabulary": [{"word": "Experience", "translation": "Experiencia"}, {"word": "Trip", "translation": "Viaje"}, {"word": "Adventure", "translation": "Aventura"}, {"word": "Memory", "translation": "Recuerdo"}, {"word": "Opportunity", "translation": "Oportunidad"}], "grammar_points": ["Present Perfect", "Ever/never/already/yet"]},
                {"title": "Lesson 2: Giving Advice", "content": "Expressing advice: You should, I recommend, It's better to...", "vocabulary": [{"word": "Advice", "translation": "Consejo"}, {"word": "Recommend", "translation": "Recomendar"}, {"word": "Suggest", "translation": "Sugerir"}, {"word": "Suitable", "translation": "Adecuado"}, {"word": "Avoid", "translation": "Evitar"}], "grammar_points": ["Should/shouldn't", "Had better"]},
                {"title": "Lesson 3: Health and Wellness", "content": "At the doctor: It hurts, I have a fever, I need a prescription.", "vocabulary": [{"word": "Doctor", "translation": "Médico"}, {"word": "Illness", "translation": "Enfermedad"}, {"word": "Symptom", "translation": "Síntoma"}, {"word": "Medicine", "translation": "Medicamento"}, {"word": "Appointment", "translation": "Cita"}], "grammar_points": ["Expressing pain", "Medical vocabulary"]},
                {"title": "Lesson 4: Environment", "content": "Ecology: recycle, pollute, renewable energy, climate change.", "vocabulary": [{"word": "Environment", "translation": "Medio ambiente"}, {"word": "Recycle", "translation": "Reciclar"}, {"word": "Pollution", "translation": "Contaminación"}, {"word": "Nature", "translation": "Naturaleza"}, {"word": "Sustainable", "translation": "Sostenible"}], "grammar_points": ["Passive voice basic", "First conditional"]},
                {"title": "Lesson 5: Work World", "content": "Employment: interview, CV, experience, skills.", "vocabulary": [{"word": "Job", "translation": "Empleo"}, {"word": "Interview", "translation": "Entrevista"}, {"word": "Salary", "translation": "Sueldo"}, {"word": "Boss", "translation": "Jefe"}, {"word": "Colleague", "translation": "Compañero"}], "grammar_points": ["First conditional", "Cause connectors"]},
                {"title": "Lesson 6: Travel and Tourism", "content": "Planning trips: book, accommodation, itinerary, destination.", "vocabulary": [{"word": "Booking", "translation": "Reserva"}, {"word": "Accommodation", "translation": "Alojamiento"}, {"word": "Flight", "translation": "Vuelo"}, {"word": "Luggage", "translation": "Equipaje"}, {"word": "Tourist", "translation": "Turista"}], "grammar_points": ["Time clauses with WHEN", "Future in subordinates"]},
            ],
            "B2": [
                {"title": "Lesson 1: Debates and Opinions", "content": "Arguing: From my point of view, I consider that, however...", "vocabulary": [{"word": "Argument", "translation": "Argumento"}, {"word": "Perspective", "translation": "Perspectiva"}, {"word": "Defend", "translation": "Defender"}, {"word": "Refute", "translation": "Refutar"}, {"word": "Consensus", "translation": "Consenso"}], "grammar_points": ["Argumentative connectors", "Expressing opinions"]},
                {"title": "Lesson 2: Complex Conditionals", "content": "If I had known, I would have gone. If I had time, I would do it.", "vocabulary": [{"word": "Hypothesis", "translation": "Hipótesis"}, {"word": "Condition", "translation": "Condición"}, {"word": "Consequence", "translation": "Consecuencia"}, {"word": "Probability", "translation": "Probabilidad"}, {"word": "Assumption", "translation": "Suposición"}], "grammar_points": ["Second conditional", "Third conditional"]},
                {"title": "Lesson 3: Culture and Society", "content": "Social topics: immigration, globalization, traditions, identity.", "vocabulary": [{"word": "Society", "translation": "Sociedad"}, {"word": "Culture", "translation": "Cultura"}, {"word": "Tradition", "translation": "Tradición"}, {"word": "Globalization", "translation": "Globalización"}, {"word": "Identity", "translation": "Identidad"}], "grammar_points": ["Passive voice", "Relative clauses"]},
                {"title": "Lesson 4: Technology and Future", "content": "Innovation: artificial intelligence, social media, digital privacy.", "vocabulary": [{"word": "Technology", "translation": "Tecnología"}, {"word": "Innovation", "translation": "Innovación"}, {"word": "Digital", "translation": "Digital"}, {"word": "Privacy", "translation": "Privacidad"}, {"word": "Algorithm", "translation": "Algoritmo"}], "grammar_points": ["Future Perfect", "Probability expressions"]},
                {"title": "Lesson 5: Art and Literature", "content": "Cultural criticism: analyze, interpret, symbolism, metaphor.", "vocabulary": [{"word": "Work", "translation": "Obra"}, {"word": "Author", "translation": "Autor"}, {"word": "Style", "translation": "Estilo"}, {"word": "Criticism", "translation": "Crítica"}, {"word": "Influence", "translation": "Influencia"}], "grammar_points": ["Concessive clauses", "Although + clause"]},
                {"title": "Lesson 6: Economy and Business", "content": "Business world: investment, market, strategy, competition.", "vocabulary": [{"word": "Company", "translation": "Empresa"}, {"word": "Investment", "translation": "Inversión"}, {"word": "Market", "translation": "Mercado"}, {"word": "Profit", "translation": "Beneficio"}, {"word": "Competition", "translation": "Competencia"}], "grammar_points": ["Reported speech", "Business vocabulary"]},
            ],
            "C1": [
                {"title": "Lesson 1: Advanced Grammar Nuances", "content": "Subtle differences: wish/if only, used to/would, inversion.", "vocabulary": [{"word": "Nuance", "translation": "Matiz"}, {"word": "Subtlety", "translation": "Sutileza"}, {"word": "Ambiguity", "translation": "Ambigüedad"}, {"word": "Precision", "translation": "Precisión"}, {"word": "Register", "translation": "Registro"}], "grammar_points": ["Inversion", "Cleft sentences"]},
                {"title": "Lesson 2: Idiomatic Expressions", "content": "Idioms: to be over the moon, to cost an arm and a leg, to hit the nail on the head.", "vocabulary": [{"word": "Idiom", "translation": "Modismo"}, {"word": "Expression", "translation": "Expresión"}, {"word": "Colloquial", "translation": "Coloquial"}, {"word": "Figurative", "translation": "Figurado"}, {"word": "Literal", "translation": "Literal"}], "grammar_points": ["Fixed phrases", "Figurative language"]},
                {"title": "Lesson 3: Academic Writing", "content": "Writing essays: thesis, arguments, conclusions, citations.", "vocabulary": [{"word": "Essay", "translation": "Ensayo"}, {"word": "Thesis", "translation": "Tesis"}, {"word": "Hypothesis", "translation": "Hipótesis"}, {"word": "Bibliography", "translation": "Bibliografía"}, {"word": "Cite", "translation": "Citar"}], "grammar_points": ["Academic discourse connectors", "Nominalization"]},
                {"title": "Lesson 4: English Varieties", "content": "Dialects: British vs American, Australian English, regional differences.", "vocabulary": [{"word": "Dialect", "translation": "Dialecto"}, {"word": "Variant", "translation": "Variante"}, {"word": "Accent", "translation": "Acento"}, {"word": "Lexicon", "translation": "Léxico"}, {"word": "Regionalism", "translation": "Regionalismo"}], "grammar_points": ["British vs American spelling", "Vocabulary differences"]},
                {"title": "Lesson 5: Journalism and Media", "content": "News analysis: headline, editorial, bias, sources.", "vocabulary": [{"word": "Journalism", "translation": "Periodismo"}, {"word": "Editorial", "translation": "Editorial"}, {"word": "Source", "translation": "Fuente"}, {"word": "Bias", "translation": "Sesgo"}, {"word": "Objectivity", "translation": "Objetividad"}], "grammar_points": ["Journalistic style", "Headlines"]},
                {"title": "Lesson 6: Humor and Sarcasm", "content": "Understanding irony, double meanings, cultural jokes.", "vocabulary": [{"word": "Irony", "translation": "Ironía"}, {"word": "Sarcasm", "translation": "Sarcasmo"}, {"word": "Double meaning", "translation": "Doble sentido"}, {"word": "Joke", "translation": "Chiste"}, {"word": "Wit", "translation": "Ingenio"}], "grammar_points": ["Ironic intonation", "Implicatures"]},
            ],
            "C2": [
                {"title": "Lesson 1: Classic Literature", "content": "Analysis of Shakespeare, Milton, Austen: style, era, influence.", "vocabulary": [{"word": "Classic", "translation": "Clásico"}, {"word": "Victorian", "translation": "Victoriano"}, {"word": "Renaissance", "translation": "Renacimiento"}, {"word": "Canon", "translation": "Canon"}, {"word": "Metrics", "translation": "Métrica"}], "grammar_points": ["Archaic English", "Literary analysis"]},
                {"title": "Lesson 2: Literary Translation", "content": "Translation techniques: equivalence, adaptation, borrowing.", "vocabulary": [{"word": "Translation", "translation": "Traducción"}, {"word": "Equivalence", "translation": "Equivalencia"}, {"word": "Adaptation", "translation": "Adaptación"}, {"word": "Fidelity", "translation": "Fidelidad"}, {"word": "Interpretation", "translation": "Interpretación"}], "grammar_points": ["False friends", "Semantic calques"]},
                {"title": "Lesson 3: Applied Linguistics", "content": "Phonology, morphology, syntax, semantics, pragmatics.", "vocabulary": [{"word": "Phoneme", "translation": "Fonema"}, {"word": "Morpheme", "translation": "Morfema"}, {"word": "Syntax", "translation": "Sintaxis"}, {"word": "Semantics", "translation": "Semántica"}, {"word": "Pragmatics", "translation": "Pragmática"}], "grammar_points": ["Syntactic analysis", "Language functions"]},
                {"title": "Lesson 4: Rhetoric and Oratory", "content": "Persuasive speech: ethos, pathos, logos, rhetorical figures.", "vocabulary": [{"word": "Rhetoric", "translation": "Retórica"}, {"word": "Oratory", "translation": "Oratoria"}, {"word": "Persuasion", "translation": "Persuasión"}, {"word": "Eloquence", "translation": "Elocuencia"}, {"word": "Speech", "translation": "Discurso"}], "grammar_points": ["Rhetorical figures", "Argumentative structure"]},
                {"title": "Lesson 5: Legal English", "content": "Legal language: terms, documents, contracts, legislation.", "vocabulary": [{"word": "Law", "translation": "Ley"}, {"word": "Contract", "translation": "Contrato"}, {"word": "Lawsuit", "translation": "Demanda"}, {"word": "Jurisprudence", "translation": "Jurisprudencia"}, {"word": "Clause", "translation": "Cláusula"}], "grammar_points": ["Formal language", "Legal formulas"]},
                {"title": "Lesson 6: Creative Writing", "content": "Creative writing: narrative, poetry, personal style.", "vocabulary": [{"word": "Narrative", "translation": "Narrativa"}, {"word": "Poetry", "translation": "Poesía"}, {"word": "Character", "translation": "Personaje"}, {"word": "Plot", "translation": "Trama"}, {"word": "Voice", "translation": "Voz narrativa"}], "grammar_points": ["Stylistic resources", "Expressive punctuation"]},
            ],
        },
        "portuguese": {
            "A1": [
                {"title": "Lição 1: Saudações Básicas", "content": "Aprenda saudações básicas: Olá, Bom dia, Boa tarde, Boa noite, Tchau.", "vocabulary": [{"word": "Olá", "translation": "Hello"}, {"word": "Tchau", "translation": "Goodbye"}, {"word": "Obrigado/a", "translation": "Thank you"}, {"word": "Por favor", "translation": "Please"}, {"word": "Sim/Não", "translation": "Yes/No"}], "grammar_points": ["Pronomes: eu, tu, ele/ela", "Verbo SER: sou, és, é"]},
                {"title": "Lição 2: Apresentações", "content": "Aprenda a apresentar-se: Chamo-me..., Sou de..., Tenho... anos.", "vocabulary": [{"word": "Nome", "translation": "Name"}, {"word": "Idade", "translation": "Age"}, {"word": "País", "translation": "Country"}, {"word": "Cidade", "translation": "City"}, {"word": "Profissão", "translation": "Profession"}], "grammar_points": ["Verbo TER", "Verbo CHAMAR-SE"]},
                {"title": "Lição 3: Números 1-20", "content": "Aprenda os números de 1 a 20 em português.", "vocabulary": [{"word": "Um", "translation": "One"}, {"word": "Dez", "translation": "Ten"}, {"word": "Vinte", "translation": "Twenty"}, {"word": "Zero", "translation": "Zero"}, {"word": "Número", "translation": "Number"}], "grammar_points": ["Números cardinais", "Quantos?"]},
                {"title": "Lição 4: Cores Básicas", "content": "Aprenda as cores: vermelho, azul, verde, amarelo, branco, preto.", "vocabulary": [{"word": "Vermelho", "translation": "Red"}, {"word": "Azul", "translation": "Blue"}, {"word": "Verde", "translation": "Green"}, {"word": "Amarelo", "translation": "Yellow"}, {"word": "Preto", "translation": "Black"}], "grammar_points": ["Concordância de gênero", "Adjetivos de cor"]},
                {"title": "Lição 5: Família Imediata", "content": "Vocabulário de família: pai, mãe, irmão, irmã.", "vocabulary": [{"word": "Pai", "translation": "Father"}, {"word": "Mãe", "translation": "Mother"}, {"word": "Irmão", "translation": "Brother"}, {"word": "Irmã", "translation": "Sister"}, {"word": "Família", "translation": "Family"}], "grammar_points": ["Possessivos: meu, teu, seu", "Plural de substantivos"]},
                {"title": "Lição 6: Objetos da Sala", "content": "Vocabulário escolar: livro, caderno, lápis, mesa, cadeira.", "vocabulary": [{"word": "Livro", "translation": "Book"}, {"word": "Lápis", "translation": "Pencil"}, {"word": "Mesa", "translation": "Table"}, {"word": "Cadeira", "translation": "Chair"}, {"word": "Quadro", "translation": "Board"}], "grammar_points": ["Artigos: o, a, os, as", "Há + substantivo"]},
            ],
            "A2": [
                {"title": "Lição 1: Rotina Diária", "content": "Descreva o seu dia: Acordo, tomo o pequeno-almoço, trabalho, janto.", "vocabulary": [{"word": "Acordar", "translation": "To wake up"}, {"word": "Pequeno-almoço", "translation": "Breakfast"}, {"word": "Almoço", "translation": "Lunch"}, {"word": "Jantar", "translation": "Dinner"}, {"word": "Deitar", "translation": "To go to bed"}], "grammar_points": ["Verbos reflexivos", "Advérbios de frequência"]},
                {"title": "Lição 2: A Casa", "content": "Partes da casa: cozinha, quarto, casa de banho, sala, jardim.", "vocabulary": [{"word": "Cozinha", "translation": "Kitchen"}, {"word": "Quarto", "translation": "Bedroom"}, {"word": "Casa de banho", "translation": "Bathroom"}, {"word": "Sala", "translation": "Living room"}, {"word": "Jardim", "translation": "Garden"}], "grammar_points": ["Preposições de lugar", "Estar + localização"]},
                {"title": "Lição 3: Compras e Preços", "content": "Na loja: Quanto custa? Levo este. Tem...?", "vocabulary": [{"word": "Loja", "translation": "Shop"}, {"word": "Preço", "translation": "Price"}, {"word": "Barato", "translation": "Cheap"}, {"word": "Caro", "translation": "Expensive"}, {"word": "Dinheiro", "translation": "Money"}], "grammar_points": ["Números 20-100", "Quanto/Quantos"]},
                {"title": "Lição 4: O Tempo", "content": "Clima: Está sol, chove, neva, está frio, está calor.", "vocabulary": [{"word": "Sol", "translation": "Sun"}, {"word": "Chuva", "translation": "Rain"}, {"word": "Neve", "translation": "Snow"}, {"word": "Vento", "translation": "Wind"}, {"word": "Nuvem", "translation": "Cloud"}], "grammar_points": ["Expressões com ESTAR", "Verbos impessoais"]},
                {"title": "Lição 5: Passado Simples", "content": "Falar do passado: Ontem fui, comi, falei, vi, estive.", "vocabulary": [{"word": "Ontem", "translation": "Yesterday"}, {"word": "Semana passada", "translation": "Last week"}, {"word": "Ano passado", "translation": "Last year"}, {"word": "Anteontem", "translation": "Day before yesterday"}, {"word": "Antes", "translation": "Before"}], "grammar_points": ["Pretérito perfeito", "Marcadores temporais"]},
                {"title": "Lição 6: Planos Futuros", "content": "Expressar planos: Vou viajar, Amanhã irei, No próximo ano...", "vocabulary": [{"word": "Amanhã", "translation": "Tomorrow"}, {"word": "Próximo", "translation": "Next"}, {"word": "Futuro", "translation": "Future"}, {"word": "Plano", "translation": "Plan"}, {"word": "Férias", "translation": "Vacation"}], "grammar_points": ["IR + infinitivo", "Futuro simples"]},
            ],
            "B1": [
                {"title": "Lição 1: Experiências de Vida", "content": "Pretérito perfeito composto: Tenho viajado, tenho conhecido.", "vocabulary": [{"word": "Experiência", "translation": "Experience"}, {"word": "Viagem", "translation": "Trip"}, {"word": "Aventura", "translation": "Adventure"}, {"word": "Memória", "translation": "Memory"}, {"word": "Oportunidade", "translation": "Opportunity"}], "grammar_points": ["Pretérito perfeito composto", "Particípios"]},
                {"title": "Lição 2: Dar Conselhos", "content": "Expressar conselhos: Devias, recomendo, é melhor que...", "vocabulary": [{"word": "Conselho", "translation": "Advice"}, {"word": "Recomendar", "translation": "To recommend"}, {"word": "Sugerir", "translation": "To suggest"}, {"word": "Convir", "translation": "To be suitable"}, {"word": "Evitar", "translation": "To avoid"}], "grammar_points": ["Condicional simples", "Conjuntivo básico"]},
                {"title": "Lição 3: Saúde e Bem-estar", "content": "No médico: Dói-me, tenho febre, preciso de uma receita.", "vocabulary": [{"word": "Médico", "translation": "Doctor"}, {"word": "Doença", "translation": "Illness"}, {"word": "Sintoma", "translation": "Symptom"}, {"word": "Medicamento", "translation": "Medicine"}, {"word": "Consulta", "translation": "Appointment"}], "grammar_points": ["Verbo DOER", "Expressões de mal-estar"]},
                {"title": "Lição 4: Meio Ambiente", "content": "Ecologia: reciclar, poluir, energia renovável, alterações climáticas.", "vocabulary": [{"word": "Ambiente", "translation": "Environment"}, {"word": "Reciclar", "translation": "To recycle"}, {"word": "Poluição", "translation": "Pollution"}, {"word": "Natureza", "translation": "Nature"}, {"word": "Sustentável", "translation": "Sustainable"}], "grammar_points": ["Orações impessoais", "Voz passiva básica"]},
                {"title": "Lição 5: Mundo do Trabalho", "content": "Emprego: entrevista, currículo, experiência, competências.", "vocabulary": [{"word": "Emprego", "translation": "Job"}, {"word": "Entrevista", "translation": "Interview"}, {"word": "Salário", "translation": "Salary"}, {"word": "Chefe", "translation": "Boss"}, {"word": "Colega", "translation": "Colleague"}], "grammar_points": ["Orações condicionais tipo 1", "Conectores causais"]},
                {"title": "Lição 6: Viagens e Turismo", "content": "Planear viagens: reservar, alojamento, itinerário, destino.", "vocabulary": [{"word": "Reserva", "translation": "Booking"}, {"word": "Alojamento", "translation": "Accommodation"}, {"word": "Voo", "translation": "Flight"}, {"word": "Bagagem", "translation": "Luggage"}, {"word": "Turista", "translation": "Tourist"}], "grammar_points": ["Orações temporais com QUANDO", "Futuro em subordinadas"]},
            ],
            "B2": [
                {"title": "Lição 1: Debates e Opiniões", "content": "Argumentar: Do meu ponto de vista, considero que, no entanto...", "vocabulary": [{"word": "Argumento", "translation": "Argument"}, {"word": "Perspetiva", "translation": "Perspective"}, {"word": "Defender", "translation": "To defend"}, {"word": "Refutar", "translation": "To refute"}, {"word": "Consenso", "translation": "Consensus"}], "grammar_points": ["Conectores argumentativos", "Conjuntivo em opiniões"]},
                {"title": "Lição 2: Condicionais Complexos", "content": "Se tivesse sabido, teria ido. Se tivesse tempo, fá-lo-ia.", "vocabulary": [{"word": "Hipótese", "translation": "Hypothesis"}, {"word": "Condição", "translation": "Condition"}, {"word": "Consequência", "translation": "Consequence"}, {"word": "Probabilidade", "translation": "Probability"}, {"word": "Suposição", "translation": "Assumption"}], "grammar_points": ["Condicionais tipo 2 e 3", "Mais-que-perfeito do conjuntivo"]},
                {"title": "Lição 3: Cultura e Sociedade", "content": "Temas sociais: imigração, globalização, tradições, identidade.", "vocabulary": [{"word": "Sociedade", "translation": "Society"}, {"word": "Cultura", "translation": "Culture"}, {"word": "Tradição", "translation": "Tradition"}, {"word": "Globalização", "translation": "Globalization"}, {"word": "Identidade", "translation": "Identity"}], "grammar_points": ["Voz passiva", "Orações relativas"]},
                {"title": "Lição 4: Tecnologia e Futuro", "content": "Inovação: inteligência artificial, redes sociais, privacidade digital.", "vocabulary": [{"word": "Tecnologia", "translation": "Technology"}, {"word": "Inovação", "translation": "Innovation"}, {"word": "Digital", "translation": "Digital"}, {"word": "Privacidade", "translation": "Privacy"}, {"word": "Algoritmo", "translation": "Algorithm"}], "grammar_points": ["Futuro perfeito", "Expressões de probabilidade"]},
                {"title": "Lição 5: Arte e Literatura", "content": "Crítica cultural: analisar, interpretar, simbolismo, metáfora.", "vocabulary": [{"word": "Obra", "translation": "Work"}, {"word": "Autor", "translation": "Author"}, {"word": "Estilo", "translation": "Style"}, {"word": "Crítica", "translation": "Criticism"}, {"word": "Influência", "translation": "Influence"}], "grammar_points": ["Orações concessivas", "Embora + conjuntivo"]},
                {"title": "Lição 6: Economia e Negócios", "content": "Mundo empresarial: investimento, mercado, estratégia, concorrência.", "vocabulary": [{"word": "Empresa", "translation": "Company"}, {"word": "Investimento", "translation": "Investment"}, {"word": "Mercado", "translation": "Market"}, {"word": "Lucro", "translation": "Profit"}, {"word": "Concorrência", "translation": "Competition"}], "grammar_points": ["Discurso indireto", "Vocabulário de negócios"]},
            ],
            "C1": [
                {"title": "Lição 1: Matizes do Conjuntivo", "content": "Uso avançado: expressões de dúvida, desejo, emoção em contextos complexos.", "vocabulary": [{"word": "Matiz", "translation": "Nuance"}, {"word": "Subtileza", "translation": "Subtlety"}, {"word": "Ambiguidade", "translation": "Ambiguity"}, {"word": "Precisão", "translation": "Precision"}, {"word": "Registo", "translation": "Register"}], "grammar_points": ["Conjuntivo em orações independentes", "Alternância indicativo/conjuntivo"]},
                {"title": "Lição 2: Expressões Idiomáticas", "content": "Modismos: estar com a cabeça na lua, meter os pés pelas mãos.", "vocabulary": [{"word": "Modismo", "translation": "Idiom"}, {"word": "Expressão", "translation": "Expression"}, {"word": "Coloquial", "translation": "Colloquial"}, {"word": "Figurado", "translation": "Figurative"}, {"word": "Literal", "translation": "Literal"}], "grammar_points": ["Frases feitas", "Linguagem figurada"]},
                {"title": "Lição 3: Redação Académica", "content": "Escrever ensaios: tese, argumentos, conclusões, citações.", "vocabulary": [{"word": "Ensaio", "translation": "Essay"}, {"word": "Tese", "translation": "Thesis"}, {"word": "Hipótese", "translation": "Hypothesis"}, {"word": "Bibliografia", "translation": "Bibliography"}, {"word": "Citar", "translation": "To cite"}], "grammar_points": ["Conectores do discurso académico", "Nominalização"]},
                {"title": "Lição 4: Variedades do Português", "content": "Diferenças: português europeu vs brasileiro, diferenças lexicais.", "vocabulary": [{"word": "Dialeto", "translation": "Dialect"}, {"word": "Variante", "translation": "Variant"}, {"word": "Sotaque", "translation": "Accent"}, {"word": "Léxico", "translation": "Lexicon"}, {"word": "Regionalismo", "translation": "Regionalism"}], "grammar_points": ["Diferenças Portugal/Brasil", "Vocabulário diferente"]},
                {"title": "Lição 5: Jornalismo e Media", "content": "Análise de notícias: título, editorial, enviesamento, fontes.", "vocabulary": [{"word": "Jornalismo", "translation": "Journalism"}, {"word": "Editorial", "translation": "Editorial"}, {"word": "Fonte", "translation": "Source"}, {"word": "Enviesamento", "translation": "Bias"}, {"word": "Objetividade", "translation": "Objectivity"}], "grammar_points": ["Estilo jornalístico", "Títulos e elipse"]},
                {"title": "Lição 6: Humor e Sarcasmo", "content": "Entender ironia, duplos sentidos, piadas culturais.", "vocabulary": [{"word": "Ironia", "translation": "Irony"}, {"word": "Sarcasmo", "translation": "Sarcasm"}, {"word": "Duplo sentido", "translation": "Double meaning"}, {"word": "Piada", "translation": "Joke"}, {"word": "Engenho", "translation": "Wit"}], "grammar_points": ["Entoação irónica", "Implicaturas"]},
            ],
            "C2": [
                {"title": "Lição 1: Literatura Clássica", "content": "Análise de Camões, Pessoa, Saramago: estilo, época, influência.", "vocabulary": [{"word": "Clássico", "translation": "Classic"}, {"word": "Barroco", "translation": "Baroque"}, {"word": "Renascimento", "translation": "Renaissance"}, {"word": "Modernismo", "translation": "Modernism"}, {"word": "Métrica", "translation": "Metrics"}], "grammar_points": ["Português antigo", "Evolução linguística"]},
                {"title": "Lição 2: Tradução Literária", "content": "Técnicas de tradução: equivalência, adaptação, empréstimo.", "vocabulary": [{"word": "Tradução", "translation": "Translation"}, {"word": "Equivalência", "translation": "Equivalence"}, {"word": "Adaptação", "translation": "Adaptation"}, {"word": "Fidelidade", "translation": "Fidelity"}, {"word": "Interpretação", "translation": "Interpretation"}], "grammar_points": ["Falsos amigos", "Calcos semânticos"]},
                {"title": "Lição 3: Linguística Aplicada", "content": "Fonologia, morfologia, sintaxe, semântica, pragmática.", "vocabulary": [{"word": "Fonema", "translation": "Phoneme"}, {"word": "Morfema", "translation": "Morpheme"}, {"word": "Sintaxe", "translation": "Syntax"}, {"word": "Semântica", "translation": "Semantics"}, {"word": "Pragmática", "translation": "Pragmatics"}], "grammar_points": ["Análise sintática", "Funções da linguagem"]},
                {"title": "Lição 4: Retórica e Oratória", "content": "Discurso persuasivo: ethos, pathos, logos, figuras retóricas.", "vocabulary": [{"word": "Retórica", "translation": "Rhetoric"}, {"word": "Oratória", "translation": "Oratory"}, {"word": "Persuasão", "translation": "Persuasion"}, {"word": "Eloquência", "translation": "Eloquence"}, {"word": "Discurso", "translation": "Speech"}], "grammar_points": ["Figuras retóricas", "Estrutura argumentativa"]},
                {"title": "Lição 5: Português Jurídico", "content": "Linguagem legal: termos, documentos, contratos, legislação.", "vocabulary": [{"word": "Lei", "translation": "Law"}, {"word": "Contrato", "translation": "Contract"}, {"word": "Processo", "translation": "Lawsuit"}, {"word": "Jurisprudência", "translation": "Jurisprudence"}, {"word": "Cláusula", "translation": "Clause"}], "grammar_points": ["Linguagem formal", "Fórmulas jurídicas"]},
                {"title": "Lição 6: Criação Literária", "content": "Escrita criativa: narrativa, poesia, estilo próprio.", "vocabulary": [{"word": "Narrativa", "translation": "Narrative"}, {"word": "Poesia", "translation": "Poetry"}, {"word": "Personagem", "translation": "Character"}, {"word": "Enredo", "translation": "Plot"}, {"word": "Voz narrativa", "translation": "Narrative voice"}], "grammar_points": ["Recursos estilísticos", "Pontuação expressiva"]},
            ],
        },
        "german": {
            "A1": [
                {"title": "Lektion 1: Grundbegrüßungen", "content": "Grundlegende Begrüßungen: Hallo, Guten Morgen, Guten Tag, Guten Abend, Tschüss.", "vocabulary": [{"word": "Hallo", "translation": "Hello"}, {"word": "Tschüss", "translation": "Goodbye"}, {"word": "Danke", "translation": "Thank you"}, {"word": "Bitte", "translation": "Please"}, {"word": "Ja/Nein", "translation": "Yes/No"}], "grammar_points": ["Pronomen: ich, du, er/sie", "Verb SEIN: bin, bist, ist"]},
                {"title": "Lektion 2: Vorstellungen", "content": "Sich vorstellen: Ich heiße..., Ich komme aus..., Ich bin... Jahre alt.", "vocabulary": [{"word": "Name", "translation": "Name"}, {"word": "Alter", "translation": "Age"}, {"word": "Land", "translation": "Country"}, {"word": "Stadt", "translation": "City"}, {"word": "Beruf", "translation": "Profession"}], "grammar_points": ["Verb HABEN", "Verb HEIßEN"]},
                {"title": "Lektion 3: Zahlen 1-20", "content": "Zahlen von 1 bis 20 auf Deutsch lernen.", "vocabulary": [{"word": "Eins", "translation": "One"}, {"word": "Zehn", "translation": "Ten"}, {"word": "Zwanzig", "translation": "Twenty"}, {"word": "Null", "translation": "Zero"}, {"word": "Zahl", "translation": "Number"}], "grammar_points": ["Kardinalzahlen", "Wie viele?"]},
                {"title": "Lektion 4: Grundfarben", "content": "Farben lernen: rot, blau, grün, gelb, weiß, schwarz.", "vocabulary": [{"word": "Rot", "translation": "Red"}, {"word": "Blau", "translation": "Blue"}, {"word": "Grün", "translation": "Green"}, {"word": "Gelb", "translation": "Yellow"}, {"word": "Schwarz", "translation": "Black"}], "grammar_points": ["Adjektivdeklination Grundlagen", "Farbadjektive"]},
                {"title": "Lektion 5: Nahe Familie", "content": "Familienvokabular: Vater, Mutter, Bruder, Schwester.", "vocabulary": [{"word": "Vater", "translation": "Father"}, {"word": "Mutter", "translation": "Mother"}, {"word": "Bruder", "translation": "Brother"}, {"word": "Schwester", "translation": "Sister"}, {"word": "Familie", "translation": "Family"}], "grammar_points": ["Possessivpronomen: mein, dein, sein", "Plural der Substantive"]},
                {"title": "Lektion 6: Klassenzimmerobjekte", "content": "Schulvokabular: Buch, Heft, Bleistift, Tisch, Stuhl.", "vocabulary": [{"word": "Buch", "translation": "Book"}, {"word": "Bleistift", "translation": "Pencil"}, {"word": "Tisch", "translation": "Table"}, {"word": "Stuhl", "translation": "Chair"}, {"word": "Tafel", "translation": "Board"}], "grammar_points": ["Artikel: der, die, das", "Es gibt + Substantiv"]},
            ],
            "A2": [
                {"title": "Lektion 1: Tagesablauf", "content": "Beschreiben Sie Ihren Tag: Ich stehe auf, frühstücke, arbeite, esse zu Abend.", "vocabulary": [{"word": "Aufstehen", "translation": "To get up"}, {"word": "Frühstück", "translation": "Breakfast"}, {"word": "Mittagessen", "translation": "Lunch"}, {"word": "Abendessen", "translation": "Dinner"}, {"word": "Ins Bett gehen", "translation": "To go to bed"}], "grammar_points": ["Trennbare Verben", "Häufigkeitsadverbien"]},
                {"title": "Lektion 2: Das Haus", "content": "Teile des Hauses: Küche, Schlafzimmer, Badezimmer, Wohnzimmer, Garten.", "vocabulary": [{"word": "Küche", "translation": "Kitchen"}, {"word": "Schlafzimmer", "translation": "Bedroom"}, {"word": "Badezimmer", "translation": "Bathroom"}, {"word": "Wohnzimmer", "translation": "Living room"}, {"word": "Garten", "translation": "Garden"}], "grammar_points": ["Lokale Präpositionen", "Dativ mit Verben"]},
                {"title": "Lektion 3: Einkaufen und Preise", "content": "Im Geschäft: Was kostet das? Ich nehme das. Haben Sie...?", "vocabulary": [{"word": "Geschäft", "translation": "Shop"}, {"word": "Preis", "translation": "Price"}, {"word": "Billig", "translation": "Cheap"}, {"word": "Teuer", "translation": "Expensive"}, {"word": "Geld", "translation": "Money"}], "grammar_points": ["Zahlen 20-100", "Wie viel/viele"]},
                {"title": "Lektion 4: Das Wetter", "content": "Klima: Es ist sonnig, es regnet, es schneit, es ist kalt, es ist warm.", "vocabulary": [{"word": "Sonne", "translation": "Sun"}, {"word": "Regen", "translation": "Rain"}, {"word": "Schnee", "translation": "Snow"}, {"word": "Wind", "translation": "Wind"}, {"word": "Wolke", "translation": "Cloud"}], "grammar_points": ["Es ist + Adjektiv", "Wetterausdrücke"]},
                {"title": "Lektion 5: Präteritum", "content": "Über die Vergangenheit sprechen: Gestern ging ich, aß, sprach, sah.", "vocabulary": [{"word": "Gestern", "translation": "Yesterday"}, {"word": "Letzte Woche", "translation": "Last week"}, {"word": "Letztes Jahr", "translation": "Last year"}, {"word": "Gestern Abend", "translation": "Last night"}, {"word": "Früher", "translation": "Before"}], "grammar_points": ["Präteritum regelmäßig", "Präteritum unregelmäßig"]},
                {"title": "Lektion 6: Zukunftspläne", "content": "Pläne ausdrücken: Ich werde reisen, Morgen werde ich, Nächstes Jahr...", "vocabulary": [{"word": "Morgen", "translation": "Tomorrow"}, {"word": "Nächste", "translation": "Next"}, {"word": "Zukunft", "translation": "Future"}, {"word": "Plan", "translation": "Plan"}, {"word": "Urlaub", "translation": "Vacation"}], "grammar_points": ["Werden + Infinitiv", "Futur I"]},
            ],
            "B1": [
                {"title": "Lektion 1: Lebenserfahrungen", "content": "Perfekt: Ich habe gereist, ich habe kennengelernt, ich habe noch nie...", "vocabulary": [{"word": "Erfahrung", "translation": "Experience"}, {"word": "Reise", "translation": "Trip"}, {"word": "Abenteuer", "translation": "Adventure"}, {"word": "Erinnerung", "translation": "Memory"}, {"word": "Gelegenheit", "translation": "Opportunity"}], "grammar_points": ["Perfekt", "Partizip II"]},
                {"title": "Lektion 2: Ratschläge geben", "content": "Ratschläge ausdrücken: Du solltest, ich empfehle, es wäre besser...", "vocabulary": [{"word": "Ratschlag", "translation": "Advice"}, {"word": "Empfehlen", "translation": "To recommend"}, {"word": "Vorschlagen", "translation": "To suggest"}, {"word": "Geeignet", "translation": "Suitable"}, {"word": "Vermeiden", "translation": "To avoid"}], "grammar_points": ["Konjunktiv II", "Modalverben im Konjunktiv"]},
                {"title": "Lektion 3: Gesundheit und Wohlbefinden", "content": "Beim Arzt: Es tut mir weh, ich habe Fieber, ich brauche ein Rezept.", "vocabulary": [{"word": "Arzt", "translation": "Doctor"}, {"word": "Krankheit", "translation": "Illness"}, {"word": "Symptom", "translation": "Symptom"}, {"word": "Medikament", "translation": "Medicine"}, {"word": "Termin", "translation": "Appointment"}], "grammar_points": ["Weh tun", "Krankheitsausdrücke"]},
                {"title": "Lektion 4: Umwelt", "content": "Ökologie: recyceln, verschmutzen, erneuerbare Energie, Klimawandel.", "vocabulary": [{"word": "Umwelt", "translation": "Environment"}, {"word": "Recyceln", "translation": "To recycle"}, {"word": "Verschmutzung", "translation": "Pollution"}, {"word": "Natur", "translation": "Nature"}, {"word": "Nachhaltig", "translation": "Sustainable"}], "grammar_points": ["Passiv Grundlagen", "Wenn-Sätze"]},
                {"title": "Lektion 5: Arbeitswelt", "content": "Arbeit: Vorstellungsgespräch, Lebenslauf, Erfahrung, Fähigkeiten.", "vocabulary": [{"word": "Job", "translation": "Job"}, {"word": "Vorstellungsgespräch", "translation": "Interview"}, {"word": "Gehalt", "translation": "Salary"}, {"word": "Chef", "translation": "Boss"}, {"word": "Kollege", "translation": "Colleague"}], "grammar_points": ["Konditionalsätze Typ 1", "Kausale Konnektoren"]},
                {"title": "Lektion 6: Reisen und Tourismus", "content": "Reisen planen: buchen, Unterkunft, Reiseroute, Reiseziel.", "vocabulary": [{"word": "Buchung", "translation": "Booking"}, {"word": "Unterkunft", "translation": "Accommodation"}, {"word": "Flug", "translation": "Flight"}, {"word": "Gepäck", "translation": "Luggage"}, {"word": "Tourist", "translation": "Tourist"}], "grammar_points": ["Temporalsätze mit WENN", "Futur in Nebensätzen"]},
            ],
            "B2": [
                {"title": "Lektion 1: Debatten und Meinungen", "content": "Argumentieren: Meiner Meinung nach, ich bin der Ansicht, jedoch...", "vocabulary": [{"word": "Argument", "translation": "Argument"}, {"word": "Perspektive", "translation": "Perspective"}, {"word": "Verteidigen", "translation": "To defend"}, {"word": "Widerlegen", "translation": "To refute"}, {"word": "Konsens", "translation": "Consensus"}], "grammar_points": ["Argumentative Konnektoren", "Meinungsausdrücke"]},
                {"title": "Lektion 2: Komplexe Konditionalsätze", "content": "Wenn ich gewusst hätte, wäre ich gegangen. Wenn ich Zeit hätte...", "vocabulary": [{"word": "Hypothese", "translation": "Hypothesis"}, {"word": "Bedingung", "translation": "Condition"}, {"word": "Konsequenz", "translation": "Consequence"}, {"word": "Wahrscheinlichkeit", "translation": "Probability"}, {"word": "Annahme", "translation": "Assumption"}], "grammar_points": ["Konditionalsätze Typ 2 und 3", "Plusquamperfekt Konjunktiv"]},
                {"title": "Lektion 3: Kultur und Gesellschaft", "content": "Gesellschaftliche Themen: Einwanderung, Globalisierung, Traditionen.", "vocabulary": [{"word": "Gesellschaft", "translation": "Society"}, {"word": "Kultur", "translation": "Culture"}, {"word": "Tradition", "translation": "Tradition"}, {"word": "Globalisierung", "translation": "Globalization"}, {"word": "Identität", "translation": "Identity"}], "grammar_points": ["Passiv", "Relativsätze"]},
                {"title": "Lektion 4: Technologie und Zukunft", "content": "Innovation: künstliche Intelligenz, soziale Medien, digitale Privatsphäre.", "vocabulary": [{"word": "Technologie", "translation": "Technology"}, {"word": "Innovation", "translation": "Innovation"}, {"word": "Digital", "translation": "Digital"}, {"word": "Privatsphäre", "translation": "Privacy"}, {"word": "Algorithmus", "translation": "Algorithm"}], "grammar_points": ["Futur II", "Wahrscheinlichkeitsausdrücke"]},
                {"title": "Lektion 5: Kunst und Literatur", "content": "Kulturkritik: analysieren, interpretieren, Symbolik, Metapher.", "vocabulary": [{"word": "Werk", "translation": "Work"}, {"word": "Autor", "translation": "Author"}, {"word": "Stil", "translation": "Style"}, {"word": "Kritik", "translation": "Criticism"}, {"word": "Einfluss", "translation": "Influence"}], "grammar_points": ["Konzessivsätze", "Obwohl + Klausel"]},
                {"title": "Lektion 6: Wirtschaft und Geschäft", "content": "Geschäftswelt: Investition, Markt, Strategie, Wettbewerb.", "vocabulary": [{"word": "Unternehmen", "translation": "Company"}, {"word": "Investition", "translation": "Investment"}, {"word": "Markt", "translation": "Market"}, {"word": "Gewinn", "translation": "Profit"}, {"word": "Wettbewerb", "translation": "Competition"}], "grammar_points": ["Indirekte Rede", "Geschäftsvokabular"]},
            ],
            "C1": [
                {"title": "Lektion 1: Fortgeschrittene Grammatiknuancen", "content": "Subtile Unterschiede: Konjunktiv I vs II, erweitertes Passiv.", "vocabulary": [{"word": "Nuance", "translation": "Nuance"}, {"word": "Feinheit", "translation": "Subtlety"}, {"word": "Mehrdeutigkeit", "translation": "Ambiguity"}, {"word": "Präzision", "translation": "Precision"}, {"word": "Register", "translation": "Register"}], "grammar_points": ["Konjunktiv I", "Erweiterte Passivformen"]},
                {"title": "Lektion 2: Idiomatische Ausdrücke", "content": "Redewendungen: ins Fettnäpfchen treten, auf der Leitung stehen.", "vocabulary": [{"word": "Redewendung", "translation": "Idiom"}, {"word": "Ausdruck", "translation": "Expression"}, {"word": "Umgangssprachlich", "translation": "Colloquial"}, {"word": "Bildlich", "translation": "Figurative"}, {"word": "Wörtlich", "translation": "Literal"}], "grammar_points": ["Feste Wendungen", "Bildliche Sprache"]},
                {"title": "Lektion 3: Akademisches Schreiben", "content": "Aufsätze schreiben: These, Argumente, Schlussfolgerungen, Zitate.", "vocabulary": [{"word": "Aufsatz", "translation": "Essay"}, {"word": "These", "translation": "Thesis"}, {"word": "Hypothese", "translation": "Hypothesis"}, {"word": "Bibliographie", "translation": "Bibliography"}, {"word": "Zitieren", "translation": "To cite"}], "grammar_points": ["Akademische Diskurskonnektoren", "Nominalisierung"]},
                {"title": "Lektion 4: Deutsche Varietäten", "content": "Dialekte: Hochdeutsch, Schweizerdeutsch, Österreichisch, regionale Unterschiede.", "vocabulary": [{"word": "Dialekt", "translation": "Dialect"}, {"word": "Variante", "translation": "Variant"}, {"word": "Akzent", "translation": "Accent"}, {"word": "Lexikon", "translation": "Lexicon"}, {"word": "Regionalismus", "translation": "Regionalism"}], "grammar_points": ["Regionale Unterschiede", "Vokabularunterschiede"]},
                {"title": "Lektion 5: Journalismus und Medien", "content": "Nachrichtenanalyse: Überschrift, Leitartikel, Voreingenommenheit, Quellen.", "vocabulary": [{"word": "Journalismus", "translation": "Journalism"}, {"word": "Leitartikel", "translation": "Editorial"}, {"word": "Quelle", "translation": "Source"}, {"word": "Voreingenommenheit", "translation": "Bias"}, {"word": "Objektivität", "translation": "Objectivity"}], "grammar_points": ["Journalistischer Stil", "Überschriften"]},
                {"title": "Lektion 6: Humor und Sarkasmus", "content": "Ironie verstehen, Doppeldeutigkeiten, kulturelle Witze.", "vocabulary": [{"word": "Ironie", "translation": "Irony"}, {"word": "Sarkasmus", "translation": "Sarcasm"}, {"word": "Doppeldeutigkeit", "translation": "Double meaning"}, {"word": "Witz", "translation": "Joke"}, {"word": "Geist", "translation": "Wit"}], "grammar_points": ["Ironische Intonation", "Implikaturen"]},
            ],
            "C2": [
                {"title": "Lektion 1: Klassische Literatur", "content": "Analyse von Goethe, Schiller, Kafka: Stil, Epoche, Einfluss.", "vocabulary": [{"word": "Klassik", "translation": "Classic"}, {"word": "Romantik", "translation": "Romanticism"}, {"word": "Aufklärung", "translation": "Enlightenment"}, {"word": "Expressionismus", "translation": "Expressionism"}, {"word": "Metrik", "translation": "Metrics"}], "grammar_points": ["Althochdeutsch", "Sprachentwicklung"]},
                {"title": "Lektion 2: Literarische Übersetzung", "content": "Übersetzungstechniken: Äquivalenz, Adaption, Entlehnung.", "vocabulary": [{"word": "Übersetzung", "translation": "Translation"}, {"word": "Äquivalenz", "translation": "Equivalence"}, {"word": "Adaption", "translation": "Adaptation"}, {"word": "Treue", "translation": "Fidelity"}, {"word": "Interpretation", "translation": "Interpretation"}], "grammar_points": ["Falsche Freunde", "Semantische Lehnübersetzungen"]},
                {"title": "Lektion 3: Angewandte Linguistik", "content": "Phonologie, Morphologie, Syntax, Semantik, Pragmatik.", "vocabulary": [{"word": "Phonem", "translation": "Phoneme"}, {"word": "Morphem", "translation": "Morpheme"}, {"word": "Syntax", "translation": "Syntax"}, {"word": "Semantik", "translation": "Semantics"}, {"word": "Pragmatik", "translation": "Pragmatics"}], "grammar_points": ["Syntaktische Analyse", "Sprachfunktionen"]},
                {"title": "Lektion 4: Rhetorik und Redekunst", "content": "Überzeugende Rede: Ethos, Pathos, Logos, rhetorische Figuren.", "vocabulary": [{"word": "Rhetorik", "translation": "Rhetoric"}, {"word": "Redekunst", "translation": "Oratory"}, {"word": "Überzeugung", "translation": "Persuasion"}, {"word": "Eloquenz", "translation": "Eloquence"}, {"word": "Rede", "translation": "Speech"}], "grammar_points": ["Rhetorische Figuren", "Argumentationsstruktur"]},
                {"title": "Lektion 5: Juristisches Deutsch", "content": "Rechtssprache: Begriffe, Dokumente, Verträge, Gesetzgebung.", "vocabulary": [{"word": "Gesetz", "translation": "Law"}, {"word": "Vertrag", "translation": "Contract"}, {"word": "Klage", "translation": "Lawsuit"}, {"word": "Rechtsprechung", "translation": "Jurisprudence"}, {"word": "Klausel", "translation": "Clause"}], "grammar_points": ["Formelle Sprache", "Juristische Formeln"]},
                {"title": "Lektion 6: Kreatives Schreiben", "content": "Kreatives Schreiben: Erzählung, Poesie, eigener Stil.", "vocabulary": [{"word": "Erzählung", "translation": "Narrative"}, {"word": "Poesie", "translation": "Poetry"}, {"word": "Figur", "translation": "Character"}, {"word": "Handlung", "translation": "Plot"}, {"word": "Erzählstimme", "translation": "Narrative voice"}], "grammar_points": ["Stilistische Mittel", "Expressive Interpunktion"]},
            ],
        },
    }
    
    for lang, config in course_configs.items():
        for level, level_config in config["levels"].items():
            course = {
                "language": lang,
                "level": level,
                "title": level_config["title"],
                "description": level_config["desc"],
                "created_by": "system",
                "created_at": datetime.utcnow()
            }
            result = await db.courses.insert_one(course)
            course_id = str(result.inserted_id)
            courses_created += 1
            
            # Get level-specific lessons for this language and level
            lang_lessons = level_lessons.get(lang, level_lessons["english"])
            lessons_for_level = lang_lessons.get(level, lang_lessons["A1"])
            
            for order, lesson_data in enumerate(lessons_for_level):
                lesson = {
                    "course_id": course_id,
                    "title": lesson_data["title"],
                    "content": lesson_data["content"],
                    "vocabulary": lesson_data.get("vocabulary", []),
                    "grammar_points": lesson_data.get("grammar_points", []),
                    "order": order + 1,
                    "created_at": datetime.utcnow()
                }
                await db.lessons.insert_one(lesson)
                lessons_created += 1
    
    # Create flashcard decks for each language/level
    flashcard_data = {
        "spanish": {
            "A1": [
                {"word": "Hola", "translation": "Hello", "example": "¡Hola! ¿Cómo estás?"},
                {"word": "Gracias", "translation": "Thank you", "example": "Muchas gracias por tu ayuda."},
                {"word": "Por favor", "translation": "Please", "example": "Un café, por favor."},
                {"word": "Buenos días", "translation": "Good morning", "example": "Buenos días, ¿cómo está usted?"},
                {"word": "Adiós", "translation": "Goodbye", "example": "Adiós, hasta mañana."},
                {"word": "Sí", "translation": "Yes", "example": "Sí, entiendo."},
                {"word": "No", "translation": "No", "example": "No, gracias."},
                {"word": "Casa", "translation": "House", "example": "Mi casa es grande."},
                {"word": "Familia", "translation": "Family", "example": "Mi familia es pequeña."},
                {"word": "Amigo", "translation": "Friend", "example": "Juan es mi amigo."},
            ],
            "A2": [
                {"word": "Trabajo", "translation": "Work/Job", "example": "Mi trabajo es interesante."},
                {"word": "Comer", "translation": "To eat", "example": "Me gusta comer paella."},
                {"word": "Beber", "translation": "To drink", "example": "¿Quieres beber algo?"},
                {"word": "Comprar", "translation": "To buy", "example": "Voy a comprar pan."},
                {"word": "Dinero", "translation": "Money", "example": "No tengo dinero."},
                {"word": "Tiempo", "translation": "Time/Weather", "example": "No tengo tiempo."},
                {"word": "Calle", "translation": "Street", "example": "Vivo en esta calle."},
                {"word": "Tienda", "translation": "Shop", "example": "La tienda está cerrada."},
                {"word": "Cocina", "translation": "Kitchen", "example": "La cocina es grande."},
                {"word": "Dormir", "translation": "To sleep", "example": "Necesito dormir más."},
            ],
            "B1": [
                {"word": "Desarrollo", "translation": "Development", "example": "El desarrollo económico es importante."},
                {"word": "Ambiente", "translation": "Environment", "example": "Debemos cuidar el medio ambiente."},
                {"word": "Sociedad", "translation": "Society", "example": "Vivimos en una sociedad moderna."},
                {"word": "Conseguir", "translation": "To achieve/get", "example": "Quiero conseguir mis objetivos."},
                {"word": "Aunque", "translation": "Although", "example": "Aunque llueva, saldré."},
                {"word": "Sin embargo", "translation": "However", "example": "Es difícil, sin embargo lo intentaré."},
                {"word": "Realizar", "translation": "To carry out", "example": "Voy a realizar el proyecto."},
                {"word": "Mediante", "translation": "Through/By means of", "example": "Lo hice mediante mucho esfuerzo."},
                {"word": "Ámbito", "translation": "Field/Scope", "example": "Trabajo en el ámbito educativo."},
                {"word": "Proporcionar", "translation": "To provide", "example": "Te proporcionaré la información."},
            ],
            "B2": [
                {"word": "Imprescindible", "translation": "Essential", "example": "Es imprescindible llegar a tiempo."},
                {"word": "Abordar", "translation": "To address/tackle", "example": "Debemos abordar este problema."},
                {"word": "Conllevar", "translation": "To entail", "example": "Este trabajo conlleva responsabilidad."},
                {"word": "Prescindir", "translation": "To do without", "example": "No puedo prescindir de ti."},
                {"word": "Hallazgo", "translation": "Finding/Discovery", "example": "Fue un hallazgo importante."},
                {"word": "Matiz", "translation": "Nuance", "example": "Hay un matiz importante."},
                {"word": "Desglosar", "translation": "To break down", "example": "Voy a desglosar los datos."},
                {"word": "Subyacente", "translation": "Underlying", "example": "Hay un problema subyacente."},
                {"word": "Acarrear", "translation": "To bring about", "example": "Esto acarreará consecuencias."},
                {"word": "Cabal", "translation": "Complete/Thorough", "example": "Tiene un conocimiento cabal."},
            ],
            "C1": [
                {"word": "Escudriñar", "translation": "To scrutinize", "example": "Escudriñó cada detalle."},
                {"word": "Desdeñar", "translation": "To disdain", "example": "No hay que desdeñar su opinión."},
                {"word": "Acuñar", "translation": "To coin (a term)", "example": "Él acuñó ese término."},
                {"word": "Dilucidar", "translation": "To elucidate", "example": "Hay que dilucidar este asunto."},
                {"word": "Palmario", "translation": "Evident/Obvious", "example": "Es palmario que tenía razón."},
                {"word": "Ingente", "translation": "Enormous", "example": "Hizo un esfuerzo ingente."},
                {"word": "Fehacientemente", "translation": "Reliably/Conclusively", "example": "Quedó fehacientemente demostrado."},
                {"word": "Susodicho", "translation": "Aforementioned", "example": "El susodicho documento fue firmado."},
                {"word": "Recóndito", "translation": "Hidden/Remote", "example": "Encontró un lugar recóndito."},
                {"word": "Ineludible", "translation": "Unavoidable", "example": "Es una obligación ineludible."},
            ],
            "C2": [
                {"word": "Plañir", "translation": "To wail/lament", "example": "Se le oía plañir."},
                {"word": "Acervo", "translation": "Heritage/Collection", "example": "Es parte del acervo cultural."},
                {"word": "Sempiterno", "translation": "Everlasting", "example": "Su sempiterno optimismo."},
                {"word": "Prístino", "translation": "Pristine/Original", "example": "En su estado prístino."},
                {"word": "Anfibología", "translation": "Ambiguity", "example": "El texto tiene anfibología."},
                {"word": "Holgazanear", "translation": "To idle/loaf", "example": "No pares de holgazanear."},
                {"word": "Protervo", "translation": "Perverse/Obstinate", "example": "Actuó de manera proterva."},
                {"word": "Diatriba", "translation": "Diatribe", "example": "Lanzó una diatriba furiosa."},
                {"word": "Execrar", "translation": "To execrate", "example": "Execró sus acciones."},
                {"word": "Impoluto", "translation": "Spotless/Unblemished", "example": "Mantuvo un historial impoluto."},
            ],
        },
        "english": {
            "A1": [
                {"word": "Hello", "translation": "Hola", "example": "Hello, how are you?"},
                {"word": "Thank you", "translation": "Gracias", "example": "Thank you for your help."},
                {"word": "Please", "translation": "Por favor", "example": "A coffee, please."},
                {"word": "Good morning", "translation": "Buenos días", "example": "Good morning, everyone!"},
                {"word": "Goodbye", "translation": "Adiós", "example": "Goodbye, see you tomorrow."},
                {"word": "Yes", "translation": "Sí", "example": "Yes, I understand."},
                {"word": "No", "translation": "No", "example": "No, thank you."},
                {"word": "House", "translation": "Casa", "example": "My house is big."},
                {"word": "Family", "translation": "Familia", "example": "My family is small."},
                {"word": "Friend", "translation": "Amigo", "example": "John is my friend."},
            ],
            "A2": [
                {"word": "Work", "translation": "Trabajo", "example": "My work is interesting."},
                {"word": "Eat", "translation": "Comer", "example": "I like to eat pizza."},
                {"word": "Drink", "translation": "Beber", "example": "Do you want to drink something?"},
                {"word": "Buy", "translation": "Comprar", "example": "I'm going to buy bread."},
                {"word": "Money", "translation": "Dinero", "example": "I don't have money."},
                {"word": "Time", "translation": "Tiempo", "example": "I don't have time."},
                {"word": "Street", "translation": "Calle", "example": "I live on this street."},
                {"word": "Shop", "translation": "Tienda", "example": "The shop is closed."},
                {"word": "Kitchen", "translation": "Cocina", "example": "The kitchen is big."},
                {"word": "Sleep", "translation": "Dormir", "example": "I need to sleep more."},
            ],
            "B1": [
                {"word": "Development", "translation": "Desarrollo", "example": "Economic development is important."},
                {"word": "Environment", "translation": "Ambiente", "example": "We must protect the environment."},
                {"word": "Society", "translation": "Sociedad", "example": "We live in a modern society."},
                {"word": "Achieve", "translation": "Conseguir", "example": "I want to achieve my goals."},
                {"word": "Although", "translation": "Aunque", "example": "Although it's raining, I'll go out."},
                {"word": "However", "translation": "Sin embargo", "example": "It's difficult, however I'll try."},
                {"word": "Carry out", "translation": "Realizar", "example": "I'm going to carry out the project."},
                {"word": "Through", "translation": "Mediante", "example": "I did it through hard work."},
                {"word": "Field", "translation": "Ámbito", "example": "I work in the education field."},
                {"word": "Provide", "translation": "Proporcionar", "example": "I'll provide you with information."},
            ],
            "B2": [
                {"word": "Essential", "translation": "Imprescindible", "example": "It's essential to arrive on time."},
                {"word": "Address", "translation": "Abordar", "example": "We must address this problem."},
                {"word": "Entail", "translation": "Conllevar", "example": "This job entails responsibility."},
                {"word": "Dispense with", "translation": "Prescindir", "example": "I can't dispense with you."},
                {"word": "Finding", "translation": "Hallazgo", "example": "It was an important finding."},
                {"word": "Nuance", "translation": "Matiz", "example": "There's an important nuance."},
                {"word": "Break down", "translation": "Desglosar", "example": "I'm going to break down the data."},
                {"word": "Underlying", "translation": "Subyacente", "example": "There's an underlying problem."},
                {"word": "Bring about", "translation": "Acarrear", "example": "This will bring about consequences."},
                {"word": "Thorough", "translation": "Cabal", "example": "He has thorough knowledge."},
            ],
            "C1": [
                {"word": "Scrutinize", "translation": "Escudriñar", "example": "She scrutinized every detail."},
                {"word": "Disdain", "translation": "Desdeñar", "example": "Don't disdain their opinion."},
                {"word": "Coin", "translation": "Acuñar", "example": "He coined that term."},
                {"word": "Elucidate", "translation": "Dilucidar", "example": "We need to elucidate this matter."},
                {"word": "Evident", "translation": "Palmario", "example": "It's evident he was right."},
                {"word": "Enormous", "translation": "Ingente", "example": "He made an enormous effort."},
                {"word": "Conclusively", "translation": "Fehacientemente", "example": "It was conclusively proven."},
                {"word": "Aforementioned", "translation": "Susodicho", "example": "The aforementioned document was signed."},
                {"word": "Remote", "translation": "Recóndito", "example": "He found a remote place."},
                {"word": "Unavoidable", "translation": "Ineludible", "example": "It's an unavoidable obligation."},
            ],
            "C2": [
                {"word": "Wail", "translation": "Plañir", "example": "She could be heard wailing."},
                {"word": "Heritage", "translation": "Acervo", "example": "It's part of cultural heritage."},
                {"word": "Everlasting", "translation": "Sempiterno", "example": "His everlasting optimism."},
                {"word": "Pristine", "translation": "Prístino", "example": "In its pristine state."},
                {"word": "Ambiguity", "translation": "Anfibología", "example": "The text has ambiguity."},
                {"word": "Idle", "translation": "Holgazanear", "example": "Stop idling around."},
                {"word": "Perverse", "translation": "Protervo", "example": "He acted in a perverse manner."},
                {"word": "Diatribe", "translation": "Diatriba", "example": "He launched a furious diatribe."},
                {"word": "Execrate", "translation": "Execrar", "example": "He execrated their actions."},
                {"word": "Unblemished", "translation": "Impoluto", "example": "He maintained an unblemished record."},
            ],
        },
        "portuguese": {
            "A1": [
                {"word": "Olá", "translation": "Hello", "example": "Olá! Como vai você?"},
                {"word": "Obrigado/a", "translation": "Thank you", "example": "Muito obrigado pela ajuda."},
                {"word": "Por favor", "translation": "Please", "example": "Um café, por favor."},
                {"word": "Bom dia", "translation": "Good morning", "example": "Bom dia! Tudo bem?"},
                {"word": "Tchau", "translation": "Goodbye", "example": "Tchau, até amanhã!"},
                {"word": "Sim", "translation": "Yes", "example": "Sim, eu entendo."},
                {"word": "Não", "translation": "No", "example": "Não, obrigado."},
                {"word": "Casa", "translation": "House", "example": "A minha casa é grande."},
                {"word": "Família", "translation": "Family", "example": "A minha família é pequena."},
                {"word": "Amigo", "translation": "Friend", "example": "O João é meu amigo."},
            ],
            "A2": [
                {"word": "Trabalho", "translation": "Work", "example": "O meu trabalho é interessante."},
                {"word": "Comer", "translation": "To eat", "example": "Gosto de comer bacalhau."},
                {"word": "Beber", "translation": "To drink", "example": "Queres beber alguma coisa?"},
                {"word": "Comprar", "translation": "To buy", "example": "Vou comprar pão."},
                {"word": "Dinheiro", "translation": "Money", "example": "Não tenho dinheiro."},
                {"word": "Tempo", "translation": "Time", "example": "Não tenho tempo."},
                {"word": "Rua", "translation": "Street", "example": "Moro nesta rua."},
                {"word": "Loja", "translation": "Shop", "example": "A loja está fechada."},
                {"word": "Cozinha", "translation": "Kitchen", "example": "A cozinha é grande."},
                {"word": "Dormir", "translation": "To sleep", "example": "Preciso dormir mais."},
            ],
            "B1": [
                {"word": "Desenvolvimento", "translation": "Development", "example": "O desenvolvimento económico é importante."},
                {"word": "Ambiente", "translation": "Environment", "example": "Devemos cuidar do meio ambiente."},
                {"word": "Sociedade", "translation": "Society", "example": "Vivemos numa sociedade moderna."},
                {"word": "Conseguir", "translation": "To achieve", "example": "Quero conseguir os meus objetivos."},
                {"word": "Embora", "translation": "Although", "example": "Embora chova, vou sair."},
                {"word": "No entanto", "translation": "However", "example": "É difícil, no entanto vou tentar."},
                {"word": "Realizar", "translation": "To carry out", "example": "Vou realizar o projeto."},
                {"word": "Através", "translation": "Through", "example": "Fi-lo através de muito esforço."},
                {"word": "Âmbito", "translation": "Field", "example": "Trabalho no âmbito educativo."},
                {"word": "Fornecer", "translation": "To provide", "example": "Vou fornecer-te a informação."},
            ],
            "B2": [
                {"word": "Imprescindível", "translation": "Essential", "example": "É imprescindível chegar a tempo."},
                {"word": "Abordar", "translation": "To address", "example": "Devemos abordar este problema."},
                {"word": "Implicar", "translation": "To entail", "example": "Este trabalho implica responsabilidade."},
                {"word": "Prescindir", "translation": "To do without", "example": "Não posso prescindir de ti."},
                {"word": "Descoberta", "translation": "Discovery", "example": "Foi uma descoberta importante."},
                {"word": "Matiz", "translation": "Nuance", "example": "Há um matiz importante."},
                {"word": "Decompor", "translation": "To break down", "example": "Vou decompor os dados."},
                {"word": "Subjacente", "translation": "Underlying", "example": "Há um problema subjacente."},
                {"word": "Acarretar", "translation": "To bring about", "example": "Isto acarretará consequências."},
                {"word": "Completo", "translation": "Thorough", "example": "Tem um conhecimento completo."},
            ],
            "C1": [
                {"word": "Escrutinar", "translation": "To scrutinize", "example": "Escrutinou cada detalhe."},
                {"word": "Desdenhar", "translation": "To disdain", "example": "Não se deve desdenhar a opinião dele."},
                {"word": "Cunhar", "translation": "To coin", "example": "Ele cunhou esse termo."},
                {"word": "Elucidar", "translation": "To elucidate", "example": "É preciso elucidar este assunto."},
                {"word": "Evidente", "translation": "Evident", "example": "É evidente que tinha razão."},
                {"word": "Enorme", "translation": "Enormous", "example": "Fez um esforço enorme."},
                {"word": "Conclusivamente", "translation": "Conclusively", "example": "Ficou conclusivamente demonstrado."},
                {"word": "Supramencionado", "translation": "Aforementioned", "example": "O supramencionado documento foi assinado."},
                {"word": "Recôndito", "translation": "Remote", "example": "Encontrou um lugar recôndito."},
                {"word": "Inevitável", "translation": "Unavoidable", "example": "É uma obrigação inevitável."},
            ],
            "C2": [
                {"word": "Lamentar", "translation": "To wail", "example": "Ouvia-se lamentar."},
                {"word": "Acervo", "translation": "Heritage", "example": "Faz parte do acervo cultural."},
                {"word": "Sempiterno", "translation": "Everlasting", "example": "O seu sempiterno otimismo."},
                {"word": "Pristino", "translation": "Pristine", "example": "No seu estado pristino."},
                {"word": "Ambiguidade", "translation": "Ambiguity", "example": "O texto tem ambiguidade."},
                {"word": "Vadiar", "translation": "To idle", "example": "Não pares de vadiar."},
                {"word": "Perverso", "translation": "Perverse", "example": "Agiu de maneira perversa."},
                {"word": "Diatribe", "translation": "Diatribe", "example": "Lançou uma diatribe furiosa."},
                {"word": "Execrar", "translation": "To execrate", "example": "Execrou as suas ações."},
                {"word": "Impoluto", "translation": "Unblemished", "example": "Manteve um historial impoluto."},
            ],
        },
        "german": {
            "A1": [
                {"word": "Hallo", "translation": "Hello", "example": "Hallo! Wie geht's?"},
                {"word": "Danke", "translation": "Thank you", "example": "Vielen Dank für Ihre Hilfe."},
                {"word": "Bitte", "translation": "Please", "example": "Einen Kaffee, bitte."},
                {"word": "Guten Morgen", "translation": "Good morning", "example": "Guten Morgen! Wie geht es Ihnen?"},
                {"word": "Auf Wiedersehen", "translation": "Goodbye", "example": "Auf Wiedersehen, bis morgen!"},
                {"word": "Ja", "translation": "Yes", "example": "Ja, ich verstehe."},
                {"word": "Nein", "translation": "No", "example": "Nein, danke."},
                {"word": "Haus", "translation": "House", "example": "Mein Haus ist groß."},
                {"word": "Familie", "translation": "Family", "example": "Meine Familie ist klein."},
                {"word": "Freund", "translation": "Friend", "example": "Hans ist mein Freund."},
            ],
            "A2": [
                {"word": "Arbeit", "translation": "Work", "example": "Meine Arbeit ist interessant."},
                {"word": "Essen", "translation": "To eat", "example": "Ich esse gern Pizza."},
                {"word": "Trinken", "translation": "To drink", "example": "Möchten Sie etwas trinken?"},
                {"word": "Kaufen", "translation": "To buy", "example": "Ich kaufe Brot."},
                {"word": "Geld", "translation": "Money", "example": "Ich habe kein Geld."},
                {"word": "Zeit", "translation": "Time", "example": "Ich habe keine Zeit."},
                {"word": "Straße", "translation": "Street", "example": "Ich wohne in dieser Straße."},
                {"word": "Geschäft", "translation": "Shop", "example": "Das Geschäft ist geschlossen."},
                {"word": "Küche", "translation": "Kitchen", "example": "Die Küche ist groß."},
                {"word": "Schlafen", "translation": "To sleep", "example": "Ich muss mehr schlafen."},
            ],
            "B1": [
                {"word": "Entwicklung", "translation": "Development", "example": "Die wirtschaftliche Entwicklung ist wichtig."},
                {"word": "Umwelt", "translation": "Environment", "example": "Wir müssen die Umwelt schützen."},
                {"word": "Gesellschaft", "translation": "Society", "example": "Wir leben in einer modernen Gesellschaft."},
                {"word": "Erreichen", "translation": "To achieve", "example": "Ich will meine Ziele erreichen."},
                {"word": "Obwohl", "translation": "Although", "example": "Obwohl es regnet, gehe ich raus."},
                {"word": "Jedoch", "translation": "However", "example": "Es ist schwierig, jedoch versuche ich es."},
                {"word": "Durchführen", "translation": "To carry out", "example": "Ich werde das Projekt durchführen."},
                {"word": "Durch", "translation": "Through", "example": "Ich habe es durch harte Arbeit geschafft."},
                {"word": "Bereich", "translation": "Field", "example": "Ich arbeite im Bildungsbereich."},
                {"word": "Bereitstellen", "translation": "To provide", "example": "Ich werde dir die Information bereitstellen."},
            ],
            "B2": [
                {"word": "Unerlässlich", "translation": "Essential", "example": "Es ist unerlässlich, pünktlich zu sein."},
                {"word": "Angehen", "translation": "To address", "example": "Wir müssen dieses Problem angehen."},
                {"word": "Mit sich bringen", "translation": "To entail", "example": "Diese Arbeit bringt Verantwortung mit sich."},
                {"word": "Verzichten", "translation": "To do without", "example": "Ich kann nicht auf dich verzichten."},
                {"word": "Erkenntnis", "translation": "Finding", "example": "Es war eine wichtige Erkenntnis."},
                {"word": "Nuance", "translation": "Nuance", "example": "Es gibt eine wichtige Nuance."},
                {"word": "Aufschlüsseln", "translation": "To break down", "example": "Ich werde die Daten aufschlüsseln."},
                {"word": "Zugrunde liegend", "translation": "Underlying", "example": "Es gibt ein zugrunde liegendes Problem."},
                {"word": "Herbeiführen", "translation": "To bring about", "example": "Dies wird Konsequenzen herbeiführen."},
                {"word": "Gründlich", "translation": "Thorough", "example": "Er hat gründliche Kenntnisse."},
            ],
            "C1": [
                {"word": "Prüfen", "translation": "To scrutinize", "example": "Sie prüfte jedes Detail."},
                {"word": "Verachten", "translation": "To disdain", "example": "Man sollte seine Meinung nicht verachten."},
                {"word": "Prägen", "translation": "To coin", "example": "Er prägte diesen Begriff."},
                {"word": "Klären", "translation": "To elucidate", "example": "Wir müssen diese Angelegenheit klären."},
                {"word": "Offensichtlich", "translation": "Evident", "example": "Es ist offensichtlich, dass er recht hatte."},
                {"word": "Gewaltig", "translation": "Enormous", "example": "Er machte eine gewaltige Anstrengung."},
                {"word": "Schlüssig", "translation": "Conclusively", "example": "Es wurde schlüssig bewiesen."},
                {"word": "Vorgenannt", "translation": "Aforementioned", "example": "Das vorgenannte Dokument wurde unterzeichnet."},
                {"word": "Abgelegen", "translation": "Remote", "example": "Er fand einen abgelegenen Ort."},
                {"word": "Unvermeidlich", "translation": "Unavoidable", "example": "Es ist eine unvermeidliche Verpflichtung."},
            ],
            "C2": [
                {"word": "Wehklagen", "translation": "To wail", "example": "Man konnte sie wehklagen hören."},
                {"word": "Erbe", "translation": "Heritage", "example": "Es ist Teil des kulturellen Erbes."},
                {"word": "Ewig", "translation": "Everlasting", "example": "Sein ewiger Optimismus."},
                {"word": "Ursprünglich", "translation": "Pristine", "example": "In seinem ursprünglichen Zustand."},
                {"word": "Mehrdeutigkeit", "translation": "Ambiguity", "example": "Der Text hat Mehrdeutigkeit."},
                {"word": "Faulenzen", "translation": "To idle", "example": "Hör auf zu faulenzen."},
                {"word": "Verdorben", "translation": "Perverse", "example": "Er handelte auf verdorbene Weise."},
                {"word": "Schmährede", "translation": "Diatribe", "example": "Er hielt eine wütende Schmährede."},
                {"word": "Verfluchen", "translation": "To execrate", "example": "Er verfluchte ihre Handlungen."},
                {"word": "Makellos", "translation": "Unblemished", "example": "Er behielt eine makellose Bilanz."},
            ],
        },
    }
    
    flashcards_created = 0
    # Create individual flashcards in the flashcards collection
    for lang, levels in flashcard_data.items():
        for level, cards in levels.items():
            for card in cards:
                flashcard = {
                    "language": lang,
                    "level": level,
                    "word": card["word"],
                    "translation": card["translation"],
                    "example": card.get("example", ""),
                    "pronunciation": card.get("pronunciation", ""),
                    "created_by": "system",
                    "created_at": datetime.utcnow()
                }
                await db.flashcards.insert_one(flashcard)
                flashcards_created += 1
    
    # Create test user if not exists
    existing_user = await db.users.find_one({"email": "testuser123@test.com"})
    if not existing_user:
        test_user = {
            "name": "Test User",
            "email": "testuser123@test.com",
            "password_hash": hash_password("password123"),
            "role": "student",
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(test_user)
    
    # Create teacher user if not exists
    existing_teacher = await db.users.find_one({"email": "profesor@test.com"})
    if not existing_teacher:
        teacher_user = {
            "name": "Profesor Demo",
            "email": "profesor@test.com",
            "password_hash": hash_password("profesor123"),
            "role": "teacher",
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(teacher_user)
    
    return {
        "message": "Full database seeded successfully",
        "courses": courses_created,
        "lessons": lessons_created,
        "flashcard_decks": flashcards_created,
        "users_created": 2
    }

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

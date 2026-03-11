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
Always respond in a structured JSON format."""

        chat = LlmChat(
            api_key=api_key,
            session_id=f"exercise-{user_id}-{datetime.utcnow().timestamp()}",
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
Remember: EVERYTHING except vocabulary translations must be in {lang_info['instruction']}."""

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
            
            # Create lessons for this course
            templates = lesson_templates.get(lang, lesson_templates["english"])
            for order, lesson_template in enumerate(templates):
                lesson = {
                    "course_id": course_id,
                    "title": lesson_template["title"],
                    "content": f"{lesson_template['content']} (Nivel {level})",
                    "vocabulary": lesson_template.get("vocabulary", []),
                    "grammar_points": lesson_template.get("grammar_points", []),
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
            ],
        },
        "english": {
            "A1": [
                {"word": "Hello", "translation": "Hola", "example": "Hello, how are you?"},
                {"word": "Thank you", "translation": "Gracias", "example": "Thank you for your help."},
                {"word": "Please", "translation": "Por favor", "example": "A coffee, please."},
                {"word": "Good morning", "translation": "Buenos días", "example": "Good morning, everyone!"},
                {"word": "Goodbye", "translation": "Adiós", "example": "Goodbye, see you tomorrow."},
            ],
        },
        "portuguese": {
            "A1": [
                {"word": "Olá", "translation": "Hello", "example": "Olá! Como vai você?"},
                {"word": "Obrigado", "translation": "Thank you", "example": "Muito obrigado pela ajuda."},
                {"word": "Por favor", "translation": "Please", "example": "Um café, por favor."},
                {"word": "Bom dia", "translation": "Good morning", "example": "Bom dia! Tudo bem?"},
                {"word": "Tchau", "translation": "Goodbye", "example": "Tchau, até amanhã!"},
            ],
        },
        "german": {
            "A1": [
                {"word": "Hallo", "translation": "Hello", "example": "Hallo! Wie geht's?"},
                {"word": "Danke", "translation": "Thank you", "example": "Vielen Dank für Ihre Hilfe."},
                {"word": "Bitte", "translation": "Please", "example": "Einen Kaffee, bitte."},
                {"word": "Guten Morgen", "translation": "Good morning", "example": "Guten Morgen! Wie geht es Ihnen?"},
                {"word": "Auf Wiedersehen", "translation": "Goodbye", "example": "Auf Wiedersehen, bis morgen!"},
            ],
        },
    }
    
    flashcards_created = 0
    for lang, levels in flashcard_data.items():
        for level, cards in levels.items():
            deck = {
                "title": f"{lang.capitalize()} {level} Flashcards",
                "language": lang,
                "level": level,
                "cards": cards,
                "created_by": "system",
                "created_at": datetime.utcnow()
            }
            await db.flashcard_decks.insert_one(deck)
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

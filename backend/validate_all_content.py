"""Comprehensive validation: 5 languages x 6 levels - check for placeholder/missing content."""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

PLACEHOLDER_PATTERNS = [
    "Wort 1", "Wort 2", "Wort 3", "Mot 1", "Mot 2", "Mot 3",
    "Palavra 1", "Palavra 2", "Word 1", "Word 2", "Palabra 1", "Palabra 2",
    "Beispiel 1", "Exemple 1", "Example 1", "Ejemplo 1", "Exemplo 1",
    "Placeholder", "placeholder", "TODO", "Lorem ipsum",
    "Wort", "Mot ", "Grammar point"
]

LANGUAGES = ["spanish", "english", "portuguese", "german", "french"]
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def check_placeholders(text):
    """Return list of placeholder patterns found in text."""
    if not text:
        return ["EMPTY"]
    found = []
    for p in PLACEHOLDER_PATTERNS:
        if p in str(text):
            found.append(p)
    return found


async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    total_issues = 0
    total_ok = 0
    
    print("=" * 80)
    print("VALIDACION COMPLETA: 5 IDIOMAS x 6 NIVELES")
    print("=" * 80)
    
    for lang in LANGUAGES:
        print(f"\n{'='*60}")
        print(f"IDIOMA: {lang.upper()}")
        print(f"{'='*60}")
        
        for level in LEVELS:
            course = await db.courses.find_one({"language": lang, "level": level})
            if not course:
                print(f"  [{level}] FALTA CURSO!")
                total_issues += 1
                continue
            
            lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
            if not lessons:
                print(f"  [{level}] SIN LECCIONES!")
                total_issues += 1
                continue
            
            level_issues = []
            for i, lesson in enumerate(lessons):
                # Check content
                content = lesson.get("content", "")
                content_issues = check_placeholders(content)
                content_len = len(str(content)) if content else 0
                
                # Check vocabulary
                vocab = lesson.get("vocabulary", [])
                vocab_count = len(vocab) if vocab else 0
                vocab_issues = []
                for v in (vocab or []):
                    word = v.get("word", "")
                    vi = check_placeholders(word)
                    if vi:
                        vocab_issues.extend(vi)
                    example = v.get("example", "")
                    ei = check_placeholders(example)
                    if ei:
                        vocab_issues.extend(ei)
                
                # Check grammar
                grammar = lesson.get("grammar_points", [])
                grammar_count = len(grammar) if grammar else 0
                grammar_issues = []
                for g in (grammar or []):
                    gi = check_placeholders(str(g))
                    if gi:
                        grammar_issues.extend(gi)
                
                has_issues = False
                issue_details = []
                
                if content_issues and content_issues != []:
                    if content_issues == ["EMPTY"]:
                        issue_details.append(f"content=VACIO")
                        has_issues = True
                    else:
                        issue_details.append(f"content_placeholder={content_issues}")
                        has_issues = True
                
                if content_len < 50:
                    issue_details.append(f"content_corto({content_len}chars)")
                    has_issues = True
                
                if vocab_count < 3:
                    issue_details.append(f"vocab_insuficiente({vocab_count})")
                    has_issues = True
                
                if vocab_issues:
                    issue_details.append(f"vocab_placeholder={vocab_issues}")
                    has_issues = True
                
                if grammar_count < 1:
                    issue_details.append(f"sin_gramatica")
                    has_issues = True
                
                if grammar_issues:
                    issue_details.append(f"grammar_placeholder={grammar_issues}")
                    has_issues = True
                
                if has_issues:
                    level_issues.append((i, lesson.get("title", "?"), issue_details))
                    total_issues += 1
                else:
                    total_ok += 1
            
            if level_issues:
                print(f"  [{level}] {len(lessons)} lecciones - {len(level_issues)} CON PROBLEMAS:")
                for idx, title, details in level_issues:
                    print(f"    Leccion {idx}: {title}")
                    for d in details:
                        print(f"      -> {d}")
            else:
                print(f"  [{level}] {len(lessons)} lecciones - OK")
    
    # Also check flashcards
    print(f"\n{'='*60}")
    print("FLASHCARDS")
    print(f"{'='*60}")
    for lang in LANGUAGES:
        for level in LEVELS:
            cards = await db.flashcards.find({"language": lang, "level": level}).to_list(None)
            card_count = len(cards) if cards else 0
            issues = []
            for c in (cards or []):
                front = c.get("front", "")
                fi = check_placeholders(front)
                if fi:
                    issues.append(f"front: {front}")
            if card_count == 0:
                print(f"  {lang}-{level}: SIN FLASHCARDS!")
                total_issues += 1
            elif issues:
                print(f"  {lang}-{level}: {card_count} cards, PLACEHOLDERS: {issues}")
                total_issues += 1
            else:
                print(f"  {lang}-{level}: {card_count} cards - OK")
                total_ok += 1
    
    # Check quizzes
    print(f"\n{'='*60}")
    print("QUIZZES")
    print(f"{'='*60}")
    for lang in LANGUAGES:
        for level in LEVELS:
            course = await db.courses.find_one({"language": lang, "level": level})
            if not course:
                continue
            quiz = await db.quizzes.find_one({"course_id": str(course["_id"])})
            if not quiz:
                print(f"  {lang}-{level}: SIN QUIZ!")
                total_issues += 1
            else:
                q_count = len(quiz.get("questions", []))
                print(f"  {lang}-{level}: {q_count} preguntas - OK")
                total_ok += 1
    
    print(f"\n{'='*80}")
    print(f"RESUMEN: {total_ok} OK | {total_issues} PROBLEMAS")
    print(f"{'='*80}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

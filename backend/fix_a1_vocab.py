"""Fix placeholder vocabulary in German A1 lessons 1-5 and French A1 lessons 1-5."""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

# German A1 lessons 1-5 vocabulary (lesson 0 is already good)
GERMAN_A1_VOCAB = {
    1: {  # Zahlen und Alter
        "vocab": [
            {"word": "Eins", "translation": "One", "example": "Ich habe eins."},
            {"word": "Zehn", "translation": "Ten", "example": "Ich bin zehn Jahre alt."},
            {"word": "Zwanzig", "translation": "Twenty", "example": "Das kostet zwanzig Euro."},
            {"word": "Wie alt?", "translation": "How old?", "example": "Wie alt bist du?"},
            {"word": "Hundert", "translation": "Hundred", "example": "Das Haus ist hundert Jahre alt."},
            {"word": "Nummer", "translation": "Number", "example": "Meine Nummer ist drei."}
        ],
        "grammar": [
            "Zahlen 1-100: eins, zwei, drei... zehn, elf, zwölf... zwanzig, dreißig...",
            "Alter: Ich bin ... Jahre alt. Wie alt bist du?",
            "Verb SEIN: ich bin, du bist, er/sie ist, wir sind, ihr seid, sie sind"
        ]
    },
    2: {  # Die Familie
        "vocab": [
            {"word": "Die Mutter", "translation": "Mother", "example": "Meine Mutter heißt Anna."},
            {"word": "Der Vater", "translation": "Father", "example": "Mein Vater arbeitet viel."},
            {"word": "Der Bruder", "translation": "Brother", "example": "Mein Bruder ist zehn Jahre alt."},
            {"word": "Die Schwester", "translation": "Sister", "example": "Meine Schwester geht zur Schule."},
            {"word": "Die Großeltern", "translation": "Grandparents", "example": "Meine Großeltern wohnen in Berlin."},
            {"word": "Das Kind", "translation": "Child", "example": "Das Kind spielt im Park."}
        ],
        "grammar": [
            "Possessivpronomen: mein/meine, dein/deine, sein/seine, ihr/ihre",
            "Artikel: der (maskulin), die (feminin), das (neutrum)",
            "Verb HABEN: ich habe, du hast, er/sie hat, wir haben"
        ]
    },
    3: {  # Berufe
        "vocab": [
            {"word": "Der Lehrer", "translation": "Teacher (m)", "example": "Der Lehrer unterrichtet Deutsch."},
            {"word": "Der Arzt", "translation": "Doctor (m)", "example": "Der Arzt hilft den Patienten."},
            {"word": "Die Ingenieurin", "translation": "Engineer (f)", "example": "Die Ingenieurin baut Brücken."},
            {"word": "Der Koch", "translation": "Cook", "example": "Der Koch arbeitet im Restaurant."},
            {"word": "Die Polizistin", "translation": "Police officer (f)", "example": "Die Polizistin hilft den Leuten."},
            {"word": "Der Student", "translation": "Student", "example": "Der Student lernt an der Universität."}
        ],
        "grammar": [
            "Maskulin/Feminin Berufe: Lehrer/Lehrerin, Arzt/Ärztin, Koch/Köchin",
            "Verb ARBEITEN: ich arbeite, du arbeitest, er/sie arbeitet",
            "Fragen: Was bist du von Beruf? — Ich bin Lehrer."
        ]
    },
    4: {  # Essen und Trinken
        "vocab": [
            {"word": "Das Brot", "translation": "Bread", "example": "Ich esse Brot zum Frühstück."},
            {"word": "Der Kaffee", "translation": "Coffee", "example": "Ich trinke gern Kaffee."},
            {"word": "Das Wasser", "translation": "Water", "example": "Ich möchte ein Glas Wasser, bitte."},
            {"word": "Der Apfel", "translation": "Apple", "example": "Der Apfel ist rot und lecker."},
            {"word": "Das Fleisch", "translation": "Meat", "example": "Ich esse kein Fleisch."},
            {"word": "Die Milch", "translation": "Milk", "example": "Die Milch ist im Kühlschrank."}
        ],
        "grammar": [
            "Verben ESSEN und TRINKEN: ich esse/trinke, du isst/trinkst",
            "MÖCHTEN (would like): Ich möchte einen Kaffee, bitte.",
            "Akkusativ: einen (m), eine (f), ein (n) — Ich möchte einen Apfel."
        ]
    },
    5: {  # Tagesablauf
        "vocab": [
            {"word": "Aufstehen", "translation": "To get up", "example": "Ich stehe um 7 Uhr auf."},
            {"word": "Frühstücken", "translation": "To have breakfast", "example": "Ich frühstücke um 8 Uhr."},
            {"word": "Arbeiten", "translation": "To work", "example": "Ich arbeite von 9 bis 17 Uhr."},
            {"word": "Mittagessen", "translation": "Lunch", "example": "Das Mittagessen ist um 12 Uhr."},
            {"word": "Schlafen", "translation": "To sleep", "example": "Ich schlafe um 22 Uhr."},
            {"word": "Die Uhrzeit", "translation": "The time", "example": "Wie viel Uhr ist es? — Es ist drei Uhr."}
        ],
        "grammar": [
            "Trennbare Verben: aufstehen (ich stehe auf), anfangen (ich fange an)",
            "Uhrzeiten: Es ist acht Uhr. Um halb neun. Viertel vor zehn.",
            "Tageszeiten: morgens, mittags, nachmittags, abends, nachts"
        ]
    }
}

# French A1 lessons 1-5 vocabulary (lesson 0 is already good)
FRENCH_A1_VOCAB = {
    1: {  # Nombres et Âge
        "vocab": [
            {"word": "Un", "translation": "One", "example": "J'ai un frère."},
            {"word": "Dix", "translation": "Ten", "example": "J'ai dix ans."},
            {"word": "Vingt", "translation": "Twenty", "example": "Ça coûte vingt euros."},
            {"word": "Quel âge?", "translation": "How old?", "example": "Quel âge avez-vous ?"},
            {"word": "Cent", "translation": "Hundred", "example": "Il y a cent élèves."},
            {"word": "Numéro", "translation": "Number", "example": "Mon numéro de téléphone est..."}
        ],
        "grammar": [
            "Nombres 1-100: un, deux, trois... dix, onze, douze... vingt, trente...",
            "L'âge avec AVOIR: J'ai ... ans. Quel âge as-tu ?",
            "Verbe AVOIR: j'ai, tu as, il/elle a, nous avons, vous avez, ils/elles ont"
        ]
    },
    2: {  # La Famille
        "vocab": [
            {"word": "La mère", "translation": "Mother", "example": "Ma mère s'appelle Marie."},
            {"word": "Le père", "translation": "Father", "example": "Mon père travaille beaucoup."},
            {"word": "Le frère", "translation": "Brother", "example": "Mon frère a dix ans."},
            {"word": "La soeur", "translation": "Sister", "example": "Ma soeur va à l'école."},
            {"word": "Les grands-parents", "translation": "Grandparents", "example": "Mes grands-parents habitent à Lyon."},
            {"word": "L'enfant", "translation": "Child", "example": "L'enfant joue dans le parc."}
        ],
        "grammar": [
            "Adjectifs possessifs: mon/ma/mes, ton/ta/tes, son/sa/ses",
            "Articles définis: le (masculin), la (féminin), les (pluriel)",
            "Verbe ÊTRE: je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont"
        ]
    },
    3: {  # Les Professions
        "vocab": [
            {"word": "Le professeur", "translation": "Teacher", "example": "Le professeur enseigne le français."},
            {"word": "Le médecin", "translation": "Doctor", "example": "Le médecin aide les patients."},
            {"word": "L'ingénieur", "translation": "Engineer", "example": "L'ingénieur construit des ponts."},
            {"word": "Le cuisinier", "translation": "Cook", "example": "Le cuisinier travaille au restaurant."},
            {"word": "L'avocat(e)", "translation": "Lawyer", "example": "L'avocate travaille au tribunal."},
            {"word": "L'étudiant(e)", "translation": "Student", "example": "L'étudiant étudie à l'université."}
        ],
        "grammar": [
            "Masculin/Féminin des professions: acteur/actrice, boulanger/boulangère",
            "Verbe TRAVAILLER: je travaille, tu travailles, il/elle travaille",
            "Question: Quelle est votre profession ? — Je suis professeur."
        ]
    },
    4: {  # Nourriture et Boissons
        "vocab": [
            {"word": "Le pain", "translation": "Bread", "example": "Je mange du pain au petit déjeuner."},
            {"word": "Le café", "translation": "Coffee", "example": "Je bois du café le matin."},
            {"word": "L'eau", "translation": "Water", "example": "Je voudrais un verre d'eau, s'il vous plaît."},
            {"word": "La pomme", "translation": "Apple", "example": "La pomme est rouge et délicieuse."},
            {"word": "La viande", "translation": "Meat", "example": "Je ne mange pas de viande."},
            {"word": "Le lait", "translation": "Milk", "example": "Le lait est dans le réfrigérateur."}
        ],
        "grammar": [
            "Verbes MANGER et BOIRE: je mange/bois, tu manges/bois",
            "Articles partitifs: du (m), de la (f), de l' (voyelle), des (pl)",
            "JE VOUDRAIS (I would like): Je voudrais un croissant, s'il vous plaît."
        ]
    },
    5: {  # Routine Quotidienne
        "vocab": [
            {"word": "Se lever", "translation": "To get up", "example": "Je me lève à 7 heures."},
            {"word": "Petit déjeuner", "translation": "Breakfast", "example": "Je prends le petit déjeuner à 8 heures."},
            {"word": "Travailler", "translation": "To work", "example": "Je travaille de 9h à 17h."},
            {"word": "Déjeuner", "translation": "Lunch", "example": "Le déjeuner est à midi."},
            {"word": "Dormir", "translation": "To sleep", "example": "Je dors à 22 heures."},
            {"word": "L'heure", "translation": "The time", "example": "Quelle heure est-il ? — Il est trois heures."}
        ],
        "grammar": [
            "Verbes pronominaux: se lever (je me lève), se coucher (je me couche)",
            "L'heure: Il est huit heures. Il est midi. Il est minuit.",
            "Moments de la journée: le matin, l'après-midi, le soir, la nuit"
        ]
    }
}


async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    updated = 0
    
    # Fix German A1 lessons 1-5
    course = await db.courses.find_one({"language": "german", "level": "A1"})
    if course:
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for idx, fix in GERMAN_A1_VOCAB.items():
            if idx < len(lessons):
                await db.lessons.update_one(
                    {"_id": lessons[idx]["_id"]},
                    {"$set": {"vocabulary": fix["vocab"], "grammar_points": fix["grammar"]}}
                )
                updated += 1
        print(f"Fixed german-A1: {len(GERMAN_A1_VOCAB)} lessons")
    
    # Fix French A1 lessons 1-5
    course = await db.courses.find_one({"language": "french", "level": "A1"})
    if course:
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for idx, fix in FRENCH_A1_VOCAB.items():
            if idx < len(lessons):
                await db.lessons.update_one(
                    {"_id": lessons[idx]["_id"]},
                    {"$set": {"vocabulary": fix["vocab"], "grammar_points": fix["grammar"]}}
                )
                updated += 1
        print(f"Fixed french-A1: {len(FRENCH_A1_VOCAB)} lessons")
    
    print(f"\nTotal updated: {updated}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

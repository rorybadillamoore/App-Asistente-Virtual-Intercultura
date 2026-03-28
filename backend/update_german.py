"""Update German lessons to align with Menschen textbook series (Hueber)."""
import asyncio, os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

GERMAN_CONTENT = {
    "A1": [
        {
            "title": "Inhalt 1: Begrüßung und Vorstellung",
            "content": "Menschen A1, Modul 1 - Lektion 1: Hallo! Ich bin Nicole. In dieser Lektion lernen Sie, sich vorzustellen, andere zu begrüßen und persönliche Informationen auszutauschen. In Deutschland gibt es formelle (Sie) und informelle (du) Anredeformen. Bei der Begrüßung verwendet man je nach Tageszeit 'Guten Morgen', 'Guten Tag' oder 'Guten Abend'.",
            "vocabulary": [
                {"word": "Guten Tag", "translation": "Good day", "example": "Guten Tag, ich bin Thomas."},
                {"word": "Wie heißen Sie?", "translation": "What is your name? (formal)", "example": "Wie heißen Sie? — Ich heiße Maria Schmidt."},
                {"word": "Woher kommen Sie?", "translation": "Where are you from?", "example": "Woher kommen Sie? — Ich komme aus Brasilien."},
                {"word": "Freut mich", "translation": "Nice to meet you", "example": "Freut mich, Sie kennenzulernen."},
                {"word": "Auf Wiedersehen", "translation": "Goodbye (formal)", "example": "Auf Wiedersehen, bis morgen!"},
                {"word": "Tschüss", "translation": "Bye (informal)", "example": "Tschüss, bis bald!"}
            ],
            "grammar_points": [
                "Verb SEIN: ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie/Sie sind",
                "W-Fragen: Wie? Woher? Was? Wer? — Wie heißen Sie?",
                "Formell (Sie) vs. Informell (du): Wie heißen Sie? vs. Wie heißt du?"
            ]
        },
        {
            "title": "Inhalt 2: Familie und Freunde",
            "content": "Menschen A1, Modul 1 - Lektion 2-3: Meine Familie. Sprechen Sie über Ihre Familie, Familienbeziehungen und Freunde. Lernen Sie Possessivartikel und die Zahlen 1-100. Die deutsche Familie heute ist vielfältig: Kleinfamilien, Patchworkfamilien und Wohngemeinschaften.",
            "vocabulary": [
                {"word": "Die Eltern", "translation": "Parents", "example": "Meine Eltern leben in München."},
                {"word": "Der Bruder", "translation": "Brother", "example": "Mein Bruder ist 25 Jahre alt."},
                {"word": "Die Schwester", "translation": "Sister", "example": "Meine Schwester studiert Medizin."},
                {"word": "Verheiratet", "translation": "Married", "example": "Bist du verheiratet? — Ja, seit drei Jahren."},
                {"word": "Das Kind", "translation": "Child", "example": "Wir haben zwei Kinder."},
                {"word": "Der Freund", "translation": "Friend/Boyfriend", "example": "Das ist mein bester Freund."}
            ],
            "grammar_points": [
                "Possessivartikel: mein/meine, dein/deine, sein/seine, ihr/ihre",
                "Verb HABEN: ich habe, du hast, er/sie hat, wir haben, ihr habt, sie haben",
                "Zahlen 1-100: eins, zwei, drei... zwanzig, einundzwanzig... hundert"
            ]
        },
        {
            "title": "Inhalt 3: Einkaufen und Lebensmittel",
            "content": "Menschen A1, Modul 2 - Lektion 4-6: Einkaufen. Lernen Sie, auf dem Markt, im Supermarkt und in Geschäften einzukaufen. Preise, Mengen und Lebensmittel. In Deutschland sind Bäckereien und Wochenmärkte sehr beliebt. Der Akkusativ wird für direkte Objekte verwendet.",
            "vocabulary": [
                {"word": "Das Brot", "translation": "Bread", "example": "Ich hätte gern ein Brot, bitte."},
                {"word": "Die Milch", "translation": "Milk", "example": "Wir brauchen noch Milch."},
                {"word": "Das Gemüse", "translation": "Vegetables", "example": "Das Gemüse ist heute sehr frisch."},
                {"word": "Wie viel kostet...?", "translation": "How much does... cost?", "example": "Wie viel kostet ein Kilo Äpfel?"},
                {"word": "Der Supermarkt", "translation": "Supermarket", "example": "Ich gehe zum Supermarkt einkaufen."},
                {"word": "Die Kasse", "translation": "Cash register", "example": "Bitte zahlen Sie an der Kasse."}
            ],
            "grammar_points": [
                "Akkusativ: den (m), die (f), das (n), die (pl) — Ich kaufe den Kuchen.",
                "Verb MÖCHTEN: Ich möchte einen Kaffee. Möchten Sie etwas trinken?",
                "Mengenangaben: ein Kilo, ein Liter, eine Flasche, ein Stück, 100 Gramm"
            ]
        },
        {
            "title": "Inhalt 4: Wohnung und Möbel",
            "content": "Menschen A1, Modul 3 - Lektion 7-8: Meine Wohnung. Beschreiben Sie Ihre Wohnung, Zimmer und Möbel. In Deutschland ist das Mieten sehr verbreitet. Lernen Sie Wohnungsanzeigen zu lesen und Ortsangaben zu machen. Der Dativ wird bei lokalen Präpositionen verwendet.",
            "vocabulary": [
                {"word": "Die Küche", "translation": "Kitchen", "example": "Die Küche ist klein, aber modern."},
                {"word": "Das Schlafzimmer", "translation": "Bedroom", "example": "Das Schlafzimmer hat ein großes Fenster."},
                {"word": "Das Bad", "translation": "Bathroom", "example": "Das Bad ist neben dem Schlafzimmer."},
                {"word": "Der Tisch", "translation": "Table", "example": "Der Tisch steht in der Mitte des Zimmers."},
                {"word": "Die Miete", "translation": "Rent", "example": "Die Miete beträgt 800 Euro im Monat."},
                {"word": "Gemütlich", "translation": "Cozy", "example": "Das Wohnzimmer ist sehr gemütlich."}
            ],
            "grammar_points": [
                "Lokale Präpositionen + Dativ: in, auf, an, neben, unter, über, vor, hinter, zwischen",
                "Dativ: dem (m/n), der (f), den (pl) — Das Buch liegt auf dem Tisch.",
                "Es gibt + Akkusativ: Es gibt einen Balkon. Es gibt keine Garage."
            ]
        },
        {
            "title": "Inhalt 5: Tagesablauf und Uhrzeiten",
            "content": "Menschen A1, Modul 4 - Lektion 9-10: Mein Tag. Beschreiben Sie Ihren Tagesablauf, Uhrzeiten und Gewohnheiten. In Deutschland ist Pünktlichkeit sehr wichtig. Trennbare Verben wie 'aufstehen' und 'anfangen' sind typisch für die deutsche Sprache.",
            "vocabulary": [
                {"word": "Aufstehen", "translation": "To get up", "example": "Ich stehe um sechs Uhr auf."},
                {"word": "Frühstücken", "translation": "To have breakfast", "example": "Wir frühstücken um halb acht."},
                {"word": "Die Uhr", "translation": "Clock/Time", "example": "Wie viel Uhr ist es? — Es ist zehn Uhr."},
                {"word": "Feierabend", "translation": "End of work", "example": "Ich habe um fünf Uhr Feierabend."},
                {"word": "Pünktlich", "translation": "Punctual", "example": "In Deutschland ist man immer pünktlich."},
                {"word": "Der Termin", "translation": "Appointment", "example": "Ich habe einen Termin beim Arzt."}
            ],
            "grammar_points": [
                "Trennbare Verben: aufstehen (ich stehe auf), anfangen (ich fange an), einkaufen (ich kaufe ein)",
                "Uhrzeiten: Es ist acht Uhr. Halb neun. Viertel vor/nach zehn.",
                "Temporale Präpositionen: um (Uhrzeit), am (Tag), im (Monat), von...bis"
            ]
        },
        {
            "title": "Inhalt 6: Freizeit und Hobbys",
            "content": "Menschen A1, Modul 4 - Lektion 11-12: Freizeit und Hobbys. Was machen Sie in Ihrer Freizeit? Sport, Musik, Lesen, Reisen. Deutsche Freizeitaktivitäten: Wandern, Radfahren, Vereine. Lernen Sie das Perfekt für vergangene Aktivitäten.",
            "vocabulary": [
                {"word": "Wandern", "translation": "Hiking", "example": "Am Wochenende gehen wir wandern."},
                {"word": "Schwimmen", "translation": "Swimming", "example": "Ich schwimme gern im Freibad."},
                {"word": "Lesen", "translation": "Reading", "example": "In meiner Freizeit lese ich gern Romane."},
                {"word": "Das Kino", "translation": "Cinema", "example": "Gehen wir heute Abend ins Kino?"},
                {"word": "Der Verein", "translation": "Club/Association", "example": "Ich bin Mitglied im Sportverein."},
                {"word": "Rad fahren", "translation": "Cycling", "example": "Viele Deutsche fahren mit dem Rad zur Arbeit."}
            ],
            "grammar_points": [
                "Perfekt: haben/sein + Partizip II — Ich habe Fußball gespielt. Ich bin gewandert.",
                "Partizip II: ge-...-t (gemacht, gespielt) / ge-...-en (gegangen, geschwommen)",
                "Gern/lieber/am liebsten: Ich spiele gern Tennis. Ich wandere lieber."
            ]
        }
    ],
    "A2": [
        {
            "title": "Inhalt 1: Berufe und Arbeitswelt",
            "content": "Menschen A2, Modul 1 - Lektion 1-3: Arbeit und Beruf. Sprechen Sie über Ihren Beruf, Arbeitsplatz und Berufserfahrung. Das deutsche Ausbildungssystem ist weltweit bekannt: duale Ausbildung kombiniert Theorie und Praxis. Lernen Sie Nebensätze mit 'weil' und 'dass'.",
            "vocabulary": [
                {"word": "Die Ausbildung", "translation": "Vocational training", "example": "Eine Ausbildung dauert normalerweise drei Jahre."},
                {"word": "Das Gehalt", "translation": "Salary", "example": "Das Gehalt wird am Ende des Monats überwiesen."},
                {"word": "Die Bewerbung", "translation": "Application", "example": "Ich schreibe eine Bewerbung für die Stelle."},
                {"word": "Der Lebenslauf", "translation": "CV/Resume", "example": "Bitte schicken Sie Ihren Lebenslauf per E-Mail."},
                {"word": "Das Vorstellungsgespräch", "translation": "Job interview", "example": "Mein Vorstellungsgespräch ist nächste Woche."},
                {"word": "Berufserfahrung", "translation": "Work experience", "example": "Haben Sie Berufserfahrung in diesem Bereich?"}
            ],
            "grammar_points": [
                "Nebensätze mit WEIL: Ich lerne Deutsch, weil ich in Deutschland arbeiten möchte.",
                "Nebensätze mit DASS: Ich glaube, dass die Ausbildung wichtig ist.",
                "Konjunktion WENN: Wenn ich eine gute Note habe, bekomme ich die Stelle."
            ]
        },
        {
            "title": "Inhalt 2: Wohnen und Umziehen",
            "content": "Menschen A2, Modul 1-2: Wohnen. Wohnungssuche in Deutschland, Umzug und Einrichtung. Lernen Sie WG-Anzeigen zu verstehen und selbst zu schreiben. Wechselpräpositionen (Akkusativ für Bewegung, Dativ für Position) sind ein zentrales Thema.",
            "vocabulary": [
                {"word": "Die Wohngemeinschaft (WG)", "translation": "Shared apartment", "example": "Ich suche ein Zimmer in einer WG."},
                {"word": "Umziehen", "translation": "To move (house)", "example": "Wir ziehen nächsten Monat um."},
                {"word": "Die Einrichtung", "translation": "Furnishing", "example": "Die Einrichtung der Wohnung ist modern."},
                {"word": "Die Nebenkosten", "translation": "Additional costs", "example": "Die Nebenkosten betragen 150 Euro."},
                {"word": "Der Vermieter", "translation": "Landlord", "example": "Der Vermieter ist sehr freundlich."},
                {"word": "Einziehen", "translation": "To move in", "example": "Wann können wir einziehen?"}
            ],
            "grammar_points": [
                "Wechselpräpositionen: Wohin? (Akkusativ) vs. Wo? (Dativ) — Ich stelle die Lampe auf den Tisch. Die Lampe steht auf dem Tisch.",
                "Verben mit Wechselpräpositionen: stellen/stehen, legen/liegen, hängen/hängen",
                "Adjektivdeklination mit unbestimmtem Artikel: ein großes Zimmer, eine kleine Küche"
            ]
        },
        {
            "title": "Inhalt 3: Gesundheit und Körper",
            "content": "Menschen A2, Modul 2: Gesundheit. Beim Arzt, Körperteile, Krankheiten und gesunde Lebensweise. Das deutsche Gesundheitssystem: Krankenversicherung, Hausarzt und Facharzt. Imperative für Ratschläge.",
            "vocabulary": [
                {"word": "Der Arzt / Die Ärztin", "translation": "Doctor", "example": "Ich muss zum Arzt gehen."},
                {"word": "Das Rezept", "translation": "Prescription", "example": "Der Arzt hat mir ein Rezept gegeben."},
                {"word": "Die Erkältung", "translation": "Cold", "example": "Ich habe eine starke Erkältung."},
                {"word": "Kopfschmerzen", "translation": "Headache", "example": "Ich habe seit heute Morgen Kopfschmerzen."},
                {"word": "Die Apotheke", "translation": "Pharmacy", "example": "Sie können das Medikament in der Apotheke kaufen."},
                {"word": "Die Krankenkasse", "translation": "Health insurance", "example": "In Deutschland braucht jeder eine Krankenkasse."}
            ],
            "grammar_points": [
                "Imperativ: Nehmen Sie Tabletten! Trink viel Wasser! Ruh dich aus!",
                "Modalverben: sollen (Rat), müssen (Pflicht), dürfen (Erlaubnis) — Du sollst zum Arzt gehen.",
                "Reflexive Verben: sich fühlen, sich ausruhen, sich erkälten — Ich fühle mich nicht gut."
            ]
        },
        {
            "title": "Inhalt 4: Reisen und Verkehr",
            "content": "Menschen A2, Modul 3: Unterwegs. Reiseplanung, Verkehrsmittel und Orientierung. Deutschland hat ein ausgezeichnetes Zugnetz (Deutsche Bahn). Lernen Sie Fahrkarten zu kaufen, nach dem Weg zu fragen und Reiseerzählungen zu verstehen.",
            "vocabulary": [
                {"word": "Die Fahrkarte", "translation": "Ticket", "example": "Ich brauche eine Fahrkarte nach Berlin."},
                {"word": "Der Bahnhof", "translation": "Train station", "example": "Der Zug fährt vom Hauptbahnhof ab."},
                {"word": "Umsteigen", "translation": "To transfer/change", "example": "Sie müssen in Frankfurt umsteigen."},
                {"word": "Die Verspätung", "translation": "Delay", "example": "Der Zug hat 20 Minuten Verspätung."},
                {"word": "Das Gleis", "translation": "Platform/Track", "example": "Der Zug fährt auf Gleis 5 ab."},
                {"word": "Hin und zurück", "translation": "Round trip", "example": "Einmal München hin und zurück, bitte."}
            ],
            "grammar_points": [
                "Komparativ und Superlativ: schneller, am schnellsten / besser, am besten",
                "Lokale Präpositionen: nach (Städte/Länder), in (Länder mit Artikel), zu (Personen/Gebäude)",
                "Perfekt mit SEIN: gehen-gegangen, fahren-gefahren, fliegen-geflogen, kommen-gekommen"
            ]
        },
        {
            "title": "Inhalt 5: Feste und Traditionen",
            "content": "Menschen A2, Modul 3-4: Feste feiern. Deutsche Feste und Traditionen: Weihnachten, Ostern, Karneval, Oktoberfest. Einladungen schreiben und beantworten. Kulturelle Unterschiede in Deutschland, Österreich und der Schweiz.",
            "vocabulary": [
                {"word": "Weihnachten", "translation": "Christmas", "example": "An Weihnachten besuchen wir die Familie."},
                {"word": "Ostern", "translation": "Easter", "example": "Zu Ostern suchen die Kinder Eier im Garten."},
                {"word": "Das Oktoberfest", "translation": "Oktoberfest", "example": "Das Oktoberfest in München ist weltberühmt."},
                {"word": "Feiern", "translation": "To celebrate", "example": "Wir feiern morgen Geburtstag."},
                {"word": "Die Einladung", "translation": "Invitation", "example": "Vielen Dank für die Einladung!"},
                {"word": "Herzlichen Glückwunsch", "translation": "Congratulations", "example": "Herzlichen Glückwunsch zum Geburtstag!"}
            ],
            "grammar_points": [
                "Konjunktionen: deshalb, trotzdem, sonst — Ich bin müde, trotzdem gehe ich zur Party.",
                "Temporale Nebensätze: als (einmalig), wenn (wiederholt) — Als ich Kind war... Wenn Weihnachten kommt...",
                "Dativ-Verben: gefallen, schmecken, gehören — Das Geschenk gefällt mir sehr."
            ]
        },
        {
            "title": "Inhalt 6: Medien und Alltag",
            "content": "Menschen A2, Modul 4: Medien und Kommunikation. Zeitungen, Fernsehen, Internet und soziale Medien in Deutschland. Lernen Sie über Medienkonsumgewohnheiten zu sprechen und E-Mails zu schreiben. Relativsätze zur Beschreibung.",
            "vocabulary": [
                {"word": "Die Nachrichten", "translation": "News", "example": "Ich schaue jeden Abend die Nachrichten."},
                {"word": "Die Zeitung", "translation": "Newspaper", "example": "Liest du noch die Zeitung oder nur online?"},
                {"word": "Das Handy", "translation": "Mobile phone", "example": "Mein Handy hat keinen Akku mehr."},
                {"word": "Die Sendung", "translation": "TV program", "example": "Diese Sendung ist sehr informativ."},
                {"word": "Herunterladen", "translation": "To download", "example": "Ich lade die App auf mein Handy herunter."},
                {"word": "Der Bildschirm", "translation": "Screen", "example": "Der Bildschirm ist zu klein zum Lesen."}
            ],
            "grammar_points": [
                "Relativsätze: Der Mann, der dort steht, ist mein Nachbar. Das Buch, das ich lese, ist spannend.",
                "Relativpronomen: der/die/das (Nom.), den/die/das (Akk.), dem/der/dem (Dat.)",
                "Verben mit Präpositionen: sich interessieren für, sich freuen auf/über, denken an"
            ]
        }
    ],
    "B1": [
        {
            "title": "Inhalt 1: Zukunftspläne",
            "content": "Menschen B1, Modul 1: Zukunft und Pläne. Sprechen Sie über Ihre Ziele, Träume und Pläne für die Zukunft. Das deutsche Bildungssystem und Karrieremöglichkeiten. Konjunktiv II für hypothetische Situationen und höfliche Bitten.",
            "vocabulary": [
                {"word": "Das Ziel", "translation": "Goal", "example": "Mein Ziel ist es, fließend Deutsch zu sprechen."},
                {"word": "Der Traum", "translation": "Dream", "example": "Mein Traum ist eine Weltreise."},
                {"word": "Das Studium", "translation": "Studies", "example": "Nach dem Studium möchte ich im Ausland arbeiten."},
                {"word": "Die Zukunft", "translation": "Future", "example": "In Zukunft möchte ich mein eigenes Unternehmen gründen."},
                {"word": "Sich bewerben", "translation": "To apply", "example": "Ich bewerbe mich um ein Stipendium."},
                {"word": "Die Gelegenheit", "translation": "Opportunity", "example": "Das ist eine tolle Gelegenheit!"}
            ],
            "grammar_points": [
                "Konjunktiv II: ich würde, ich hätte, ich wäre, ich könnte — Ich würde gern in Berlin leben.",
                "Finalsätze mit UM...ZU und DAMIT: Ich lerne Deutsch, um in Deutschland zu studieren.",
                "Futur I: werden + Infinitiv — Ich werde nächstes Jahr nach Deutschland fliegen."
            ]
        },
        {
            "title": "Inhalt 2: Gesellschaft und Zusammenleben",
            "content": "Menschen B1, Modul 2: Zusammenleben. Nachbarschaft, interkulturelle Begegnungen und gesellschaftliche Regeln in Deutschland. Diskutieren Sie über Integration, Ehrenamt und soziales Engagement.",
            "vocabulary": [
                {"word": "Der Nachbar", "translation": "Neighbor", "example": "Unsere Nachbarn sind sehr hilfsbereit."},
                {"word": "Das Ehrenamt", "translation": "Volunteer work", "example": "Viele Deutsche engagieren sich im Ehrenamt."},
                {"word": "Die Integration", "translation": "Integration", "example": "Sprache ist der Schlüssel zur Integration."},
                {"word": "Der Respekt", "translation": "Respect", "example": "Respekt und Toleranz sind wichtig für das Zusammenleben."},
                {"word": "Die Regel", "translation": "Rule", "example": "In Deutschland gibt es viele Regeln im Alltag."},
                {"word": "Die Mülltrennung", "translation": "Waste separation", "example": "Mülltrennung ist in Deutschland sehr wichtig."}
            ],
            "grammar_points": [
                "Infinitiv mit ZU: Es ist wichtig, die Regeln zu kennen. Ich habe keine Lust, aufzuräumen.",
                "Indirekte Fragen: Können Sie mir sagen, wo der Bahnhof ist? Ich weiß nicht, ob er kommt.",
                "Passiv Präsens: Die Miete wird am Ersten bezahlt. Der Müll wird getrennt."
            ]
        },
        {
            "title": "Inhalt 3: Natur und Umwelt",
            "content": "Menschen B1, Modul 2-3: Natur und Umwelt. Umweltschutz, Recycling und Nachhaltigkeit in Deutschland. Die Energiewende und erneuerbare Energien. Diskutieren Sie über Klimawandel und umweltfreundliches Verhalten.",
            "vocabulary": [
                {"word": "Der Umweltschutz", "translation": "Environmental protection", "example": "Umweltschutz beginnt im Alltag."},
                {"word": "Erneuerbare Energie", "translation": "Renewable energy", "example": "Deutschland investiert stark in erneuerbare Energien."},
                {"word": "Der Klimawandel", "translation": "Climate change", "example": "Der Klimawandel ist eine globale Herausforderung."},
                {"word": "Nachhaltig", "translation": "Sustainable", "example": "Wir sollten nachhaltiger leben."},
                {"word": "Recyceln", "translation": "To recycle", "example": "In Deutschland recycelt man Papier, Glas und Plastik."},
                {"word": "Der Strom", "translation": "Electricity", "example": "Unser Strom kommt aus Windenergie."}
            ],
            "grammar_points": [
                "Passiv Präteritum: Die Fabrik wurde geschlossen. Die Bäume wurden gepflanzt.",
                "Konnektoren: einerseits... andererseits, je... desto, sowohl... als auch",
                "Verben mit Präpositionen: sich engagieren für, protestieren gegen, sorgen für"
            ]
        },
        {
            "title": "Inhalt 4: Kulturleben",
            "content": "Menschen B1, Modul 3: Kultur. Kunst, Musik, Literatur und Theater in den deutschsprachigen Ländern. Von Bach bis Kraftwerk, von Goethe bis Herta Müller. Lernen Sie über kulturelle Veranstaltungen zu sprechen und Rezensionen zu schreiben.",
            "vocabulary": [
                {"word": "Die Ausstellung", "translation": "Exhibition", "example": "Die Ausstellung im Museum war beeindruckend."},
                {"word": "Das Konzert", "translation": "Concert", "example": "Wir gehen am Samstag ins Konzert."},
                {"word": "Der Roman", "translation": "Novel", "example": "Hast du den neuesten Roman von Juli Zeh gelesen?"},
                {"word": "Die Aufführung", "translation": "Performance", "example": "Die Theateraufführung war ausverkauft."},
                {"word": "Beeindruckend", "translation": "Impressive", "example": "Die Architektur ist wirklich beeindruckend."},
                {"word": "Empfehlen", "translation": "To recommend", "example": "Ich empfehle dir diesen Film."}
            ],
            "grammar_points": [
                "Adjektivdeklination ohne Artikel: kalter Kaffee, frische Luft, gutes Essen",
                "Präteritum der Modalverben: konnte, musste, wollte, durfte, sollte",
                "Konjunktionen: obwohl, während, bevor, nachdem — Obwohl es regnete, gingen wir ins Theater."
            ]
        },
        {
            "title": "Inhalt 5: Politik und Geschichte",
            "content": "Menschen B1, Modul 4: Geschichte und Politik. Die Wiedervereinigung, die Berliner Mauer, die EU und das politische System Deutschlands. Diskutieren Sie über historische Ereignisse und aktuelle politische Themen.",
            "vocabulary": [
                {"word": "Die Wiedervereinigung", "translation": "Reunification", "example": "Die Wiedervereinigung war 1990."},
                {"word": "Die Mauer", "translation": "Wall", "example": "Die Berliner Mauer fiel am 9. November 1989."},
                {"word": "Die Demokratie", "translation": "Democracy", "example": "Deutschland ist eine parlamentarische Demokratie."},
                {"word": "Die Wahl", "translation": "Election", "example": "Die nächsten Wahlen sind im Herbst."},
                {"word": "Der Bundestag", "translation": "Federal Parliament", "example": "Der Bundestag tagt in Berlin."},
                {"word": "Das Grundgesetz", "translation": "Constitution", "example": "Das Grundgesetz garantiert die Menschenrechte."}
            ],
            "grammar_points": [
                "Präteritum: Die Mauer fiel. Der Krieg endete. Deutschland wurde wiedervereinigt.",
                "Temporale Nebensätze: Nachdem die Mauer gefallen war, feierten die Menschen.",
                "Plusquamperfekt: Bevor die Mauer fiel, hatte Deutschland 40 Jahre geteilt existiert."
            ]
        },
        {
            "title": "Inhalt 6: Arbeit im Ausland",
            "content": "Menschen B1, Modul 4: Arbeiten international. Erfahrungen im Ausland, interkulturelle Kommunikation und Arbeitskultur. Vergleichen Sie Arbeitskulturen und diskutieren Sie über Vor- und Nachteile der Globalisierung.",
            "vocabulary": [
                {"word": "Das Ausland", "translation": "Abroad", "example": "Ich habe zwei Jahre im Ausland gearbeitet."},
                {"word": "Die Erfahrung", "translation": "Experience", "example": "Die Erfahrung im Ausland war sehr bereichernd."},
                {"word": "Interkulturell", "translation": "Intercultural", "example": "Interkulturelle Kompetenz ist im Beruf wichtig."},
                {"word": "Der Vorteil", "translation": "Advantage", "example": "Ein Vorteil ist, dass man neue Kulturen kennenlernt."},
                {"word": "Der Nachteil", "translation": "Disadvantage", "example": "Ein Nachteil ist die Entfernung von der Familie."},
                {"word": "Sich anpassen", "translation": "To adapt", "example": "Man muss sich an die neue Kultur anpassen."}
            ],
            "grammar_points": [
                "Konjunktiv II für irreale Bedingungen: Wenn ich mehr Geld hätte, würde ich reisen.",
                "Doppelkonjunktionen: nicht nur... sondern auch, weder... noch, entweder... oder",
                "Indirekte Rede: Er sagte, er sei zufrieden. Sie meinte, sie hätte viel gelernt."
            ]
        }
    ],
    "B2": [
        {"title": "Inhalt 1: Wissenschaft und Forschung", "content": "Niveau B2. Wissenschaftliche Entdeckungen, Technologie und Innovation in Deutschland. Von der Relativitätstheorie bis zur modernen KI-Forschung. Lernen Sie, über komplexe Sachverhalte zu diskutieren und wissenschaftliche Texte zu verstehen.", "vocabulary": [{"word": "Die Forschung", "translation": "Research", "example": "Die Forschung an Universitäten wird staatlich gefördert."}, {"word": "Die Entdeckung", "translation": "Discovery", "example": "Röntgens Entdeckung revolutionierte die Medizin."}, {"word": "Der Fortschritt", "translation": "Progress", "example": "Der technologische Fortschritt verändert unseren Alltag."}, {"word": "Die Studie", "translation": "Study", "example": "Laut einer aktuellen Studie..."}, {"word": "Nachweisen", "translation": "To prove/demonstrate", "example": "Die Hypothese konnte nachgewiesen werden."}, {"word": "Die Erkenntnis", "translation": "Insight/Finding", "example": "Neue Erkenntnisse zeigen, dass..."}], "grammar_points": ["Partizip I und II als Adjektive: die wachsende Wirtschaft, die entwickelten Länder", "Nominalisierung: forschen→Forschung, entdecken→Entdeckung, erkennen→Erkenntnis", "Passiv mit Modalverben: Das Problem muss gelöst werden. Die Studie kann veröffentlicht werden."]},
        {"title": "Inhalt 2: Medien und Meinungsbildung", "content": "Niveau B2. Kritischer Umgang mit Medien: Fake News, Meinungsfreiheit, Pressefreiheit und der Einfluss sozialer Medien. Analysieren Sie Zeitungsartikel und formulieren Sie eigene Standpunkte.", "vocabulary": [{"word": "Die Meinungsfreiheit", "translation": "Freedom of opinion", "example": "Die Meinungsfreiheit ist ein Grundrecht."}, {"word": "Die Pressefreiheit", "translation": "Freedom of the press", "example": "Die Pressefreiheit ist in der Verfassung verankert."}, {"word": "Manipulieren", "translation": "To manipulate", "example": "Soziale Medien können die Meinung manipulieren."}, {"word": "Der Standpunkt", "translation": "Point of view", "example": "Meines Erachtens ist dieser Standpunkt problematisch."}, {"word": "Kritisch", "translation": "Critical", "example": "Man sollte Nachrichten kritisch hinterfragen."}, {"word": "Die Quelle", "translation": "Source", "example": "Überprüfen Sie immer die Quelle einer Nachricht."}], "grammar_points": ["Konjunktiv I für indirekte Rede: Der Minister sagte, die Lage sei stabil.", "Konzessivsätze: Obgleich, wenngleich, auch wenn — Obgleich die Kritik berechtigt ist...", "Nomen-Verb-Verbindungen: eine Entscheidung treffen, Einfluss nehmen, in Frage stellen"]},
        {"title": "Inhalt 3: Wirtschaft und Globalisierung", "content": "Niveau B2. Die deutsche Wirtschaft: Mittelstand, Export, Automobilindustrie und Industrie 4.0. Globalisierung, Handelsbeziehungen und wirtschaftliche Herausforderungen. Fachsprache für berufliche Kontexte.", "vocabulary": [{"word": "Der Mittelstand", "translation": "SMEs/Small businesses", "example": "Der Mittelstand ist das Rückgrat der deutschen Wirtschaft."}, {"word": "Der Export", "translation": "Export", "example": "Deutschland ist einer der größten Exporteure weltweit."}, {"word": "Die Inflation", "translation": "Inflation", "example": "Die Inflation hat die Lebenshaltungskosten erhöht."}, {"word": "Wettbewerbsfähig", "translation": "Competitive", "example": "Deutsche Unternehmen sind international wettbewerbsfähig."}, {"word": "Die Lieferkette", "translation": "Supply chain", "example": "Die Pandemie hat die Lieferketten gestört."}, {"word": "Nachhaltig wirtschaften", "translation": "Sustainable business", "example": "Immer mehr Firmen wirtschaften nachhaltig."}], "grammar_points": ["Partizipialkonstruktionen: Die im letzten Jahr durchgeführte Studie zeigt...", "Subjektive Bedeutung der Modalverben: Das dürfte stimmen. Er will das gesagt haben.", "Feste Wendungen: zum Ausdruck bringen, in Betracht ziehen, zur Verfügung stehen"]},
        {"title": "Inhalt 4: Kunst und Philosophie", "content": "Niveau B2. Deutsche Philosophie und Kunst: Kant, Hegel, Nietzsche, Bauhaus, Expressionismus. Analysieren Sie kunsthistorische Texte und philosophische Grundbegriffe auf Deutsch.", "vocabulary": [{"word": "Die Aufklärung", "translation": "Enlightenment", "example": "Kant ist der wichtigste Denker der Aufklärung."}, {"word": "Das Bauhaus", "translation": "Bauhaus", "example": "Das Bauhaus revolutionierte Design und Architektur."}, {"word": "Der Expressionismus", "translation": "Expressionism", "example": "Der Expressionismus drückt starke Emotionen aus."}, {"word": "Die Vernunft", "translation": "Reason", "example": "Kant stellte die Vernunft ins Zentrum."}, {"word": "Das Gesamtkunstwerk", "translation": "Total work of art", "example": "Wagner strebte das Gesamtkunstwerk an."}, {"word": "Die Ästhetik", "translation": "Aesthetics", "example": "Die Ästhetik des Bauhaus ist minimalistisch."}], "grammar_points": ["Erweitertes Partizip: Der von Kant entwickelte kategorische Imperativ...", "Subjunktionen für komplexe Satzgefüge: insofern als, sofern, es sei denn", "Genitiv in akademischen Texten: des Künstlers, der Epoche, des Werkes"]},
        {"title": "Inhalt 5: Recht und Gesellschaft", "content": "Niveau B2. Das deutsche Rechtssystem, Grundrechte und gesellschaftliche Debatten. Mietrecht, Arbeitsrecht und Verbraucherschutz im Alltag. Argumentieren Sie differenziert über kontroverse Themen.", "vocabulary": [{"word": "Das Grundrecht", "translation": "Fundamental right", "example": "Jeder Mensch hat Grundrechte."}, {"word": "Der Verbraucherschutz", "translation": "Consumer protection", "example": "Der Verbraucherschutz ist in Deutschland sehr stark."}, {"word": "Das Urteil", "translation": "Verdict/Judgment", "example": "Das Gericht hat ein wichtiges Urteil gesprochen."}, {"word": "Die Klage", "translation": "Lawsuit", "example": "Er hat eine Klage gegen den Vermieter eingereicht."}, {"word": "Der Anspruch", "translation": "Claim/Entitlement", "example": "Sie hat Anspruch auf Elternzeit."}, {"word": "Verpflichten", "translation": "To obligate", "example": "Das Gesetz verpflichtet zur Mülltrennung."}], "grammar_points": ["Passiv mit werden/sein: Das Gesetz wird verabschiedet (Vorgang) / ist verabschiedet (Zustand)", "Konditionalsätze: Falls, sofern, vorausgesetzt dass — Falls das Gesetz geändert wird...", "Nominalstil: die Verabschiedung des Gesetzes, die Einhaltung der Vorschriften"]},
        {"title": "Inhalt 6: Interkulturelle Kompetenz", "content": "Niveau B2. Leben in einer multikulturellen Gesellschaft. Migration, Integration und kulturelle Vielfalt in Deutschland. Vergleichen Sie kulturelle Werte und diskutieren Sie über Vorurteile und Stereotype.", "vocabulary": [{"word": "Die Vielfalt", "translation": "Diversity", "example": "Kulturelle Vielfalt bereichert die Gesellschaft."}, {"word": "Das Vorurteil", "translation": "Prejudice", "example": "Vorurteile entstehen oft durch Unwissenheit."}, {"word": "Die Toleranz", "translation": "Tolerance", "example": "Toleranz ist die Grundlage des Zusammenlebens."}, {"word": "Die Einwanderung", "translation": "Immigration", "example": "Deutschland hat eine lange Geschichte der Einwanderung."}, {"word": "Diskriminierung", "translation": "Discrimination", "example": "Diskriminierung darf nicht toleriert werden."}, {"word": "Die Gleichberechtigung", "translation": "Equal rights", "example": "Gleichberechtigung ist ein wichtiges Ziel."}], "grammar_points": ["Konzessive Konnektoren: dennoch, nichtsdestotrotz, gleichwohl", "Subjektive Modalverben: Er soll gesagt haben... Sie will nichts gewusst haben.", "Textproduktion: Erörterung — These, Argumente, Beispiele, Fazit"]}
    ],
    "C1": [
        {"title": "Inhalt 1: Akademisches Deutsch", "content": "Niveau C1. Wissenschaftliches Schreiben: Hausarbeiten, Seminararbeiten und Präsentationen. Zitierregeln, Quellenarbeit und akademischer Stil. DaF-Prüfungen (TestDaF, DSH) auf C1-Niveau.", "vocabulary": [{"word": "Die Hausarbeit", "translation": "Term paper", "example": "Die Hausarbeit muss bis Ende des Semesters abgegeben werden."}, {"word": "Die These", "translation": "Thesis", "example": "Die These des Autors ist überzeugend."}, {"word": "Belegen", "translation": "To substantiate", "example": "Diese Aussage muss mit Quellen belegt werden."}, {"word": "Erörtern", "translation": "To discuss/analyze", "example": "In dieser Arbeit wird die Frage erörtert, ob..."}, {"word": "Die Schlussfolgerung", "translation": "Conclusion", "example": "Die Schlussfolgerung fasst die Ergebnisse zusammen."}, {"word": "Kritisch hinterfragen", "translation": "To critically question", "example": "Man sollte Statistiken immer kritisch hinterfragen."}], "grammar_points": ["Wissenschaftlicher Stil: Unpersönlichkeit, Nominalisierung, Passiv", "Konjunktiv I in wissenschaftlichen Texten: Der Autor behaupte, die These sei...", "Komplexe Satzstrukturen: Kausal-, Konditional-, Konzessiv- und Finalsätze"]},
        {"title": "Inhalt 2: Deutsche Literatur", "content": "Niveau C1. Literarische Epochen: Sturm und Drang, Klassik, Romantik, Realismus, Moderne. Textanalyse von Goethe, Schiller, Kafka, Thomas Mann und Herta Müller. Interpretation literarischer Texte.", "vocabulary": [{"word": "Die Epoche", "translation": "Epoch/Era", "example": "Jede literarische Epoche hat ihre eigenen Merkmale."}, {"word": "Die Interpretation", "translation": "Interpretation", "example": "Die Interpretation dieses Gedichts ist vielschichtig."}, {"word": "Die Metapher", "translation": "Metaphor", "example": "Kafkas Werke sind voller Metaphern."}, {"word": "Der Erzähler", "translation": "Narrator", "example": "Der Erzähler in Manns 'Tod in Venedig' ist allwissend."}, {"word": "Die Novelle", "translation": "Novella", "example": "Die Verwandlung von Kafka ist eine berühmte Novelle."}, {"word": "Das Motiv", "translation": "Motif", "example": "Das Motiv der Sehnsucht ist typisch für die Romantik."}], "grammar_points": ["Literarische Analyse: Erzählperspektive, Stilmittel, Symbolik", "Konjunktiv II in literarischen Texten: Es war, als hätte die Welt aufgehört zu atmen.", "Intertextualität: Bezüge zwischen literarischen Werken erkennen und beschreiben"]},
        {"title": "Inhalt 3: Politische Diskurse", "content": "Niveau C1. Politische Rhetorik, Wahlkampf und Mediendiskurse in Deutschland. Analysieren Sie politische Reden und entwickeln Sie differenzierte Argumentationen zu aktuellen Debatten.", "vocabulary": [{"word": "Die Rhetorik", "translation": "Rhetoric", "example": "Politische Rhetorik beeinflusst die öffentliche Meinung."}, {"word": "Der Diskurs", "translation": "Discourse", "example": "Der gesellschaftliche Diskurs über Migration ist komplex."}, {"word": "Die Debatte", "translation": "Debate", "example": "Die Debatte im Bundestag war hitzig."}, {"word": "Plädieren", "translation": "To plead/advocate", "example": "Er plädierte für mehr soziale Gerechtigkeit."}, {"word": "Die Wahlkampagne", "translation": "Election campaign", "example": "Die Wahlkampagne konzentrierte sich auf Wirtschaftsthemen."}, {"word": "Polarisieren", "translation": "To polarize", "example": "Das Thema polarisiert die Gesellschaft."}], "grammar_points": ["Rhetorische Mittel: Anapher, Klimax, rhetorische Frage, Antithese", "Modalpartikeln: doch, ja, halt, eben, mal — Das ist doch klar! Komm mal her!", "Kausale Zusammenhänge: aufgrund, angesichts, infolge + Genitiv"]},
        {"title": "Inhalt 4: Psychologie und Sozialwissenschaften", "content": "Niveau C1. Psychologische Grundbegriffe, soziale Dynamiken und gesellschaftliche Strukturen. Verstehen Sie Fachtexte aus den Sozialwissenschaften.", "vocabulary": [{"word": "Die Wahrnehmung", "translation": "Perception", "example": "Die Wahrnehmung wird durch Erfahrungen beeinflusst."}, {"word": "Das Verhalten", "translation": "Behavior", "example": "Menschliches Verhalten wird von vielen Faktoren bestimmt."}, {"word": "Die Identität", "translation": "Identity", "example": "Die Identitätsbildung ist ein lebenslanger Prozess."}, {"word": "Sozialisieren", "translation": "To socialize", "example": "Kinder werden in der Familie und Schule sozialisiert."}, {"word": "Die Norm", "translation": "Norm", "example": "Gesellschaftliche Normen verändern sich im Laufe der Zeit."}, {"word": "Das Phänomen", "translation": "Phenomenon", "example": "Das Phänomen der sozialen Isolation nimmt zu."}], "grammar_points": ["Fachsprachliche Nominalkonstruktionen: die Beeinträchtigung der Wahrnehmung", "Funktionsverbgefüge: in Erscheinung treten, zum Ausdruck kommen, in Betracht ziehen", "Konsekutivsätze: so... dass, derart... dass — Die Studie war so umfangreich, dass..."]},
        {"title": "Inhalt 5: Ethik und Technologie", "content": "Niveau C1. Ethische Fragen der modernen Technologie: KI, Datenschutz, Biotechnologie und Transhumanismus. Erörtern Sie komplexe moralische Dilemmata auf Deutsch.", "vocabulary": [{"word": "Die Künstliche Intelligenz", "translation": "Artificial Intelligence", "example": "KI verändert die Arbeitswelt grundlegend."}, {"word": "Der Datenschutz", "translation": "Data protection", "example": "Die DSGVO schützt personenbezogene Daten."}, {"word": "Die Biotechnologie", "translation": "Biotechnology", "example": "Die Biotechnologie eröffnet neue medizinische Möglichkeiten."}, {"word": "Das Dilemma", "translation": "Dilemma", "example": "Autonomes Fahren wirft ethische Dilemmata auf."}, {"word": "Verantwortungsvoll", "translation": "Responsible", "example": "KI muss verantwortungsvoll eingesetzt werden."}, {"word": "Die Regulierung", "translation": "Regulation", "example": "Es braucht klare Regulierungen für neue Technologien."}], "grammar_points": ["Erweiterte Partizipialattribute: Die von der EU verabschiedete Datenschutzverordnung...", "Irreale Vergleichssätze: als ob, als wenn — Er tat, als ob er nichts wüsste.", "Modale Satzadverbien: zweifellos, vermutlich, angeblich, offensichtlich"]},
        {"title": "Inhalt 6: Stilistik und Textproduktion", "content": "Niveau C1. Fortgeschrittene Textproduktion: Feuilleton, Essay, Kommentar und Rezension. Entwickeln Sie einen eigenen Schreibstil und beherrschen Sie verschiedene Textregister.", "vocabulary": [{"word": "Das Feuilleton", "translation": "Arts/Culture section", "example": "Der Artikel im Feuilleton war brillant geschrieben."}, {"word": "Der Essay", "translation": "Essay", "example": "Ein guter Essay verbindet Analyse mit persönlicher Reflexion."}, {"word": "Die Rezension", "translation": "Review", "example": "Die Rezension des neuen Romans war sehr positiv."}, {"word": "Der Kommentar", "translation": "Commentary", "example": "Der politische Kommentar war scharf und treffend."}, {"word": "Formulieren", "translation": "To formulate", "example": "Man muss seine Gedanken klar formulieren."}, {"word": "Die Nuance", "translation": "Nuance", "example": "Die Nuancen der Sprache machen den Unterschied."}], "grammar_points": ["Register: formell, informell, umgangssprachlich, fachsprachlich, literarisch", "Stilmittel in der Textproduktion: Ironie, Understatement, Übertreibung", "Kohäsionsmittel: Pronominalisierung, Substitution, Konnektoren, Themenprogression"]}
    ],
    "C2": [
        {"title": "Inhalt 1: Sprachphilosophie", "content": "Niveau C2. Die Beziehung zwischen Sprache, Denken und Wirklichkeit. Wittgenstein, Heidegger und die Sprachphilosophie. Sapir-Whorf-Hypothese und die Grenzen der Sprache.", "vocabulary": [{"word": "Die Sprachphilosophie", "translation": "Philosophy of language", "example": "Wittgenstein revolutionierte die Sprachphilosophie."}, {"word": "Die Bedeutung", "translation": "Meaning", "example": "Die Bedeutung eines Wortes ist sein Gebrauch in der Sprache."}, {"word": "Der Diskurs", "translation": "Discourse", "example": "Foucault analysierte die Macht des Diskurses."}, {"word": "Die Hermeneutik", "translation": "Hermeneutics", "example": "Die Hermeneutik ist die Kunst der Textauslegung."}, {"word": "Die Pragmatik", "translation": "Pragmatics", "example": "Die Pragmatik untersucht Sprache im Kontext."}, {"word": "Das Paradigma", "translation": "Paradigm", "example": "Kuhn sprach von Paradigmenwechseln in der Wissenschaft."}], "grammar_points": ["Philosophische Terminologie auf Deutsch: Dasein, Zeitgeist, Weltanschauung, Angst", "Hypotaktische Satzstrukturen: verschachtelte Nebensätze in akademischen Texten", "Modalpartikel als Diskursmarker: Die Sprache beeinflusst ja bekanntlich unser Denken."]},
        {"title": "Inhalt 2: Zeitgenössische Literatur", "content": "Niveau C2. Moderne deutschsprachige Literatur: W.G. Sebald, Elfriede Jelinek, Daniel Kehlmann, Jenny Erpenbeck. Literaturkritik und -theorie auf höchstem Niveau.", "vocabulary": [{"word": "Die Erzähltechnik", "translation": "Narrative technique", "example": "Sebalds Erzähltechnik verbindet Fiktion und Dokumentation."}, {"word": "Die Dekonstruktion", "translation": "Deconstruction", "example": "Jelinek dekonstruiert gesellschaftliche Mythen."}, {"word": "Vielschichtig", "translation": "Multi-layered", "example": "Der Roman ist thematisch vielschichtig."}, {"word": "Die Verfremdung", "translation": "Alienation effect", "example": "Brecht nutzte Verfremdungseffekte im Theater."}, {"word": "Die Rezeption", "translation": "Reception", "example": "Die Rezeption des Werkes war kontrovers."}, {"word": "Das Narrativ", "translation": "Narrative", "example": "Das vorherrschende Narrativ wird in Frage gestellt."}], "grammar_points": ["Literaturwissenschaftliche Terminologie: Intertextualität, Metafiktion, Polyphonie", "Konjunktiv in literarischer Sprache: Es sei, wie es wolle. Man möge bedenken, dass...", "Stilanalyse: Syntax, Wortwahl, Rhythmus und Klang in literarischen Texten"]},
        {"title": "Inhalt 3: Linguistik und Sprachgeschichte", "content": "Niveau C2. Die Geschichte der deutschen Sprache: vom Althochdeutschen zum Neuhochdeutschen. Sprachwandel, Dialekte und die Zukunft des Deutschen in einer globalisierten Welt.", "vocabulary": [{"word": "Der Sprachwandel", "translation": "Language change", "example": "Sprachwandel ist ein natürlicher Prozess."}, {"word": "Der Dialekt", "translation": "Dialect", "example": "Bayerisch und Sächsisch sind bekannte Dialekte."}, {"word": "Die Standardsprache", "translation": "Standard language", "example": "Die Standardsprache basiert auf dem Hochdeutschen."}, {"word": "Die Entlehnung", "translation": "Borrowing", "example": "Viele Anglizismen sind Entlehnungen aus dem Englischen."}, {"word": "Die Etymologie", "translation": "Etymology", "example": "Die Etymologie erforscht die Herkunft der Wörter."}, {"word": "Zweisprachig", "translation": "Bilingual", "example": "In Südtirol sind viele Menschen zweisprachig."}], "grammar_points": ["Historische Grammatik: Wie sich Kasus, Tempus und Syntax verändert haben", "Dialektale Varianten: Ich bin's (Standardsprache) vs. I bin's (Bayerisch)", "Anglizismen und Neologismen: downloaden, googeln, posten, liken"]},
        {"title": "Inhalt 4: Wirtschaft und Geopolitik", "content": "Niveau C2. Deutschland in der Weltwirtschaft und Geopolitik. EU-Politik, NATO, Handelskonflikte und die Rolle Deutschlands als Wirtschaftsmacht. Analyse von Fachartikeln und Positionspapieren.", "vocabulary": [{"word": "Die Hegemonie", "translation": "Hegemony", "example": "Die wirtschaftliche Hegemonie verschiebt sich global."}, {"word": "Die Souveränität", "translation": "Sovereignty", "example": "Nationale Souveränität und europäische Integration."}, {"word": "Die Sanktion", "translation": "Sanction", "example": "Wirtschaftssanktionen sind ein politisches Instrument."}, {"word": "Multilateral", "translation": "Multilateral", "example": "Deutschland setzt auf multilaterale Diplomatie."}, {"word": "Die Handelsbeziehung", "translation": "Trade relationship", "example": "Die Handelsbeziehungen zu China sind komplex."}, {"word": "Die Energiewende", "translation": "Energy transition", "example": "Die Energiewende ist ein geopolitisches Thema."}], "grammar_points": ["Fachsprache der Politik und Wirtschaft: Terminologie und Formulierungen", "Komplexe Genitivkonstruktionen: des im letzten Jahr abgeschlossenen Abkommens", "Rhetorische Strategien in politischen Texten: Euphemismus, Framing, Agenda-Setting"]},
        {"title": "Inhalt 5: Kulturkritik und Ästhetik", "content": "Niveau C2. Kritische Theorie: Adorno, Benjamin, Habermas. Kulturkritik, Ästhetik und Gesellschaftsanalyse. Die Frankfurter Schule und ihr Einfluss auf die moderne Geisteswissenschaft.", "vocabulary": [{"word": "Die Kulturkritik", "translation": "Cultural criticism", "example": "Adornos Kulturkritik bleibt aktuell."}, {"word": "Die Ästhetik", "translation": "Aesthetics", "example": "Benjamins Aufsatz über das Kunstwerk und die technische Reproduzierbarkeit."}, {"word": "Die Aufklärung", "translation": "Enlightenment", "example": "Die Dialektik der Aufklärung ist ein Schlüsselwerk."}, {"word": "Die Emanzipation", "translation": "Emancipation", "example": "Habermas versteht Vernunft als Instrument der Emanzipation."}, {"word": "Der Diskurs", "translation": "Discourse", "example": "Der herrschaftsfreie Diskurs ist ein Ideal."}, {"word": "Die Ideologie", "translation": "Ideology", "example": "Ideologiekritik entlarvt verborgene Machstrukturen."}], "grammar_points": ["Philosophische Fachsprache: Verdinglichung, Entfremdung, Kommunikatives Handeln", "Hochkomplexe Satzperioden: wie in akademischen Texten der Geisteswissenschaften", "Lexikalische Differenzierung: Synonyme, Antonyme und semantische Nuancen"]},
        {"title": "Inhalt 6: Meisterschaft der Sprache", "content": "Niveau C2. Stilistische Perfektion: Ironie, Humor, Satire und sprachliches Feingefühl. Beherrschen Sie alle Register der deutschen Sprache — von der Umgangssprache bis zur Wissenschaftssprache.", "vocabulary": [{"word": "Die Satire", "translation": "Satire", "example": "Kurt Tucholsky war ein Meister der politischen Satire."}, {"word": "Der Sprachwitz", "translation": "Wordplay/Wit", "example": "Deutsche Kabarettisten sind für ihren Sprachwitz bekannt."}, {"word": "Die Ironie", "translation": "Irony", "example": "Ironie erfordert ein tiefes Verständnis der Sprache."}, {"word": "Das Feingefühl", "translation": "Sensitivity/Finesse", "example": "Sprachliches Feingefühl entwickelt sich mit der Erfahrung."}, {"word": "Die Redewendung", "translation": "Idiom", "example": "Deutsche Redewendungen sind kulturell geprägt."}, {"word": "Die Eloquenz", "translation": "Eloquence", "example": "Eloquenz ist die Kunst, überzeugend zu sprechen."}], "grammar_points": ["Alle Sprachregister: Umgangssprache, Jugendsprache, Fachsprache, gehobenes Deutsch", "Pragmatische Kompetenz: Ironie, Understatement, Höflichkeitsstrategien, Humor", "Muttersprachliche Idiomatik: Sprichwörter, Redewendungen, Kollokationen"]}
    ]
}

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = 0
    for level, lessons_data in GERMAN_CONTENT.items():
        course = await db.courses.find_one({"language": "german", "level": level})
        if not course:
            print(f"Course german-{level} not found!")
            continue
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for i, data in enumerate(lessons_data):
            if i < len(lessons):
                await db.lessons.update_one(
                    {"_id": lessons[i]["_id"]},
                    {"$set": {"title": data["title"], "content": data["content"], "vocabulary": data["vocabulary"], "grammar_points": data["grammar_points"]}}
                )
                total += 1
        print(f"Updated german-{level}: {min(len(lessons_data), len(lessons))} lessons")
    print(f"\nTotal German lessons updated: {total}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

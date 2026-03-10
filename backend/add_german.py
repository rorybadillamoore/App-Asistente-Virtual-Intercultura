"""
Script para agregar el idioma Alemán a la aplicación.
12 cursos (2 por nivel), 36 lecciones, 60 flashcards.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'polyglot_academy')]

# ============== CURSOS DE ALEMÁN ==============
GERMAN_COURSES = {
    "A1": {
        "basic": {
            "title": "Deutsch Grundlagen",
            "desc": "Grundlagen der deutschen Sprache: Begrüßungen, Vorstellungen und wichtiger Wortschatz.",
            "lessons": [
                {
                    "title": "Begrüßungen und Vorstellungen",
                    "content": """## Grundlegende Begrüßungen
Begrüßungen sind wichtig, um ein Gespräch zu beginnen.

### Formelle Begrüßungen:
- Guten Morgen (morgens)
- Guten Tag (tagsüber)
- Guten Abend (abends)

### Informelle Begrüßungen:
- Hallo!
- Hi!
- Wie geht's?

## Sich vorstellen
- Ich heiße [Name]
- Ich bin [Name]
- Freut mich! / Sehr erfreut!

### Beispieldialog:
A: Hallo! Ich heiße Maria. Und du?
B: Hallo Maria, ich bin Hans. Freut mich.
A: Freut mich auch. Woher kommst du?
B: Ich komme aus Deutschland. Und du?
A: Ich komme aus Österreich.""",
                    "vocabulary": [
                        {"term": "Hallo", "definition": "Hello (informal)", "example": "Hallo! Wie geht es dir?"},
                        {"term": "Guten Tag", "definition": "Good day (formal)", "example": "Guten Tag, Herr Müller."},
                        {"term": "Ich heiße", "definition": "My name is", "example": "Ich heiße Anna."},
                        {"term": "Freut mich", "definition": "Nice to meet you", "example": "Freut mich, Sie kennenzulernen."},
                        {"term": "Wie geht's?", "definition": "How are you?", "example": "Hallo, wie geht's?"},
                        {"term": "Woher kommst du?", "definition": "Where are you from?", "example": "Woher kommst du?"},
                    ],
                    "grammar_points": ["Verb SEIN: ich bin, du bist, er/sie ist", "Verb HEIßEN: ich heiße, du heißt", "Personalpronomen: ich, du, er, sie"]
                },
                {
                    "title": "Zahlen und Farben",
                    "content": """## Zahlen von 1 bis 20
1-eins, 2-zwei, 3-drei, 4-vier, 5-fünf, 6-sechs, 7-sieben, 8-acht, 9-neun, 10-zehn
11-elf, 12-zwölf, 13-dreizehn, 14-vierzehn, 15-fünfzehn, 16-sechzehn, 17-siebzehn, 18-achtzehn, 19-neunzehn, 20-zwanzig

## Die Farben
Rot, Blau, Grün, Gelb, Orange, Lila, Rosa, Braun, Schwarz, Weiß, Grau

### Beispiele:
- Das Auto ist rot.
- Das Haus ist weiß.
- Ich habe drei blaue Bücher.""",
                    "vocabulary": [
                        {"term": "Rot", "definition": "Red", "example": "Der Apfel ist rot."},
                        {"term": "Blau", "definition": "Blue", "example": "Der Himmel ist blau."},
                        {"term": "Grün", "definition": "Green", "example": "Das Gras ist grün."},
                        {"term": "Eins", "definition": "One", "example": "Ich habe einen Bruder."},
                        {"term": "Zehn", "definition": "Ten", "example": "Es ist zehn Uhr."},
                    ],
                    "grammar_points": ["Adjektivdeklination Grundlagen", "Bestimmte Artikel: der, die, das", "Plural der Substantive"]
                },
                {
                    "title": "Die Familie",
                    "content": """## Familienmitglieder

### Kernfamilie:
- Vater / Papa
- Mutter / Mama
- Sohn / Tochter
- Bruder / Schwester

### Erweiterte Familie:
- Großvater / Opa
- Großmutter / Oma
- Onkel / Tante
- Cousin / Cousine

### Beispiel:
"Meine Familie ist groß. Ich habe zwei Brüder. Meine Eltern heißen Karl und Maria." """,
                    "vocabulary": [
                        {"term": "Vater", "definition": "Father", "example": "Mein Vater arbeitet viel."},
                        {"term": "Mutter", "definition": "Mother", "example": "Meine Mutter kocht gut."},
                        {"term": "Bruder", "definition": "Brother", "example": "Ich habe einen älteren Bruder."},
                        {"term": "Großvater", "definition": "Grandfather", "example": "Mein Großvater ist 80 Jahre alt."},
                    ],
                    "grammar_points": ["Possessivpronomen: mein, dein, sein/ihr", "Verb HABEN: ich habe, du hast", "Akkusativ: einen Bruder"]
                }
            ]
        },
        "practical": {
            "title": "Deutsch Praktisch A1",
            "desc": "Alltagssituationen: im Restaurant, nach dem Weg fragen, einkaufen.",
            "lessons": [
                {
                    "title": "Im Restaurant",
                    "content": """## Essen bestellen

### Nützliche Sätze:
- Ich hätte gern einen Tisch für zwei.
- Kann ich die Speisekarte sehen?
- Ich möchte... / Ich hätte gern...
- Was empfehlen Sie?
- Die Rechnung, bitte.

### Typische Gerichte:
- Vorspeisen: Suppe, Salat
- Hauptgerichte: Fleisch, Fisch, Pasta
- Nachspeisen: Eis, Kuchen, Obst
- Getränke: Wasser, Wein, Kaffee, Bier

### Beispieldialog:
Kellner: Guten Abend, haben Sie reserviert?
Gast: Nein, haben Sie einen Tisch für zwei?
Kellner: Ja, hier bitte. Hier ist die Speisekarte.
Gast: Danke. Was empfehlen Sie?
Kellner: Der Fisch ist heute sehr gut.
Gast: Gut, ich nehme den Fisch und einen Salat.""",
                    "vocabulary": [
                        {"term": "Speisekarte", "definition": "Menu", "example": "Kann ich die Speisekarte haben?"},
                        {"term": "Rechnung", "definition": "Bill", "example": "Die Rechnung, bitte."},
                        {"term": "Trinkgeld", "definition": "Tip", "example": "Ich gebe Trinkgeld."},
                        {"term": "Reservierung", "definition": "Reservation", "example": "Ich habe eine Reservierung."},
                    ],
                    "grammar_points": ["Konjunktiv II: ich hätte, ich möchte", "Modalverben: können, möchten", "Akkusativ: den Fisch, einen Salat"]
                },
                {
                    "title": "Nach dem Weg fragen",
                    "content": """## Wegbeschreibung

### Nützliche Fragen:
- Wo ist...?
- Wie komme ich zu...?
- Ist es weit/nah?
- Können Sie das wiederholen?

### Richtungen:
- Geradeaus
- Rechts / Links
- An der Ecke
- Neben / Gegenüber

### Dialog:
A: Entschuldigung, wo ist die Apotheke?
B: Gehen Sie geradeaus und dann rechts.
A: Ist es weit?
B: Nein, etwa fünf Minuten zu Fuß.
A: Vielen Dank.
B: Bitte schön.""",
                    "vocabulary": [
                        {"term": "Geradeaus", "definition": "Straight ahead", "example": "Gehen Sie geradeaus."},
                        {"term": "Ecke", "definition": "Corner", "example": "An der Ecke links."},
                        {"term": "Nah", "definition": "Near", "example": "Es ist ganz nah."},
                        {"term": "Abbiegen", "definition": "To turn", "example": "Biegen Sie rechts ab."},
                    ],
                    "grammar_points": ["Imperativ: gehen Sie, biegen Sie ab", "Präpositionen mit Dativ: zu, bei", "Lokale Präpositionen"]
                },
                {
                    "title": "Einkaufen",
                    "content": """## Im Geschäft

### Im Kleidungsgeschäft:
- Haben Sie das in einer anderen Größe?
- Kann ich das anprobieren?
- Wo ist die Umkleidekabine?
- Es passt mir gut/nicht.
- Ich nehme es.

### Im Supermarkt:
- Wo finde ich...?
- Was kostet das?
- Haben Sie Tüten?
- Kann ich mit Karte zahlen?""",
                    "vocabulary": [
                        {"term": "Umkleidekabine", "definition": "Fitting room", "example": "Die Umkleidekabine ist dort."},
                        {"term": "Größe", "definition": "Size", "example": "Welche Größe haben Sie?"},
                        {"term": "Anprobieren", "definition": "To try on", "example": "Kann ich das anprobieren?"},
                        {"term": "Bargeld", "definition": "Cash", "example": "Ich zahle bar."},
                    ],
                    "grammar_points": ["Reflexive Verben: sich anziehen", "Dativpronomen: mir, dir", "Modalverb können"]
                }
            ]
        }
    },
    "A2": {
        "basic": {
            "title": "Deutsch Elementar",
            "desc": "Alltägliche Gespräche, Einkaufen und grundlegende Beschreibungen.",
            "lessons": [
                {"title": "Pläne machen", "content": "## Verabredungen\n\nEinladen, zusagen, absagen, Details vereinbaren.\n\nMöchtest du ins Kino gehen?\nHast du am Samstag Zeit?\nWann und wo treffen wir uns?", "vocabulary": [{"term": "Verabredung", "definition": "Appointment/Date", "example": "Wir haben eine Verabredung."}], "grammar_points": ["Futur mit werden", "Temporale Präpositionen"]},
                {"title": "Über die Vergangenheit sprechen", "content": "## Erfahrungen erzählen\n\nWas hast du gestern gemacht?\nWie war dein Wochenende?\nIch bin nach Berlin gefahren.", "vocabulary": [{"term": "Gestern", "definition": "Yesterday", "example": "Gestern war ich im Kino."}], "grammar_points": ["Perfekt mit haben/sein", "Partizip II"]},
                {"title": "Menschen beschreiben", "content": "## Aussehen und Charakter\n\nGroß, klein, schlank, dick\nBlond, brünett, rothaarig\nFreundlich, lustig, intelligent", "vocabulary": [{"term": "Groß", "definition": "Tall", "example": "Er ist sehr groß."}], "grammar_points": ["Adjektivdeklination", "Vergleiche: größer als"]}
            ]
        },
        "practical": {
            "title": "Deutsch Konversation A2",
            "desc": "Konversationsübungen: Pläne, Vergangenheit, Beschreibungen.",
            "lessons": [
                {"title": "Freizeit und Hobbys", "content": "## Über Hobbys sprechen\n\nWas machst du gern?\nIch spiele gern Fußball.\nMein Hobby ist Fotografieren.", "vocabulary": [{"term": "Hobby", "definition": "Hobby", "example": "Mein Hobby ist Lesen."}], "grammar_points": ["Gern + Verb", "Akkusativ nach spielen"]},
                {"title": "Wohnen", "content": "## Die Wohnung\n\nZimmer: Küche, Bad, Schlafzimmer, Wohnzimmer\nMöbel: Tisch, Stuhl, Bett, Schrank", "vocabulary": [{"term": "Wohnung", "definition": "Apartment", "example": "Meine Wohnung ist klein."}], "grammar_points": ["Wechselpräpositionen", "Dativ/Akkusativ"]},
                {"title": "Gesundheit", "content": "## Beim Arzt\n\nKörperteile: Kopf, Arm, Bein, Rücken\nIch habe Kopfschmerzen.\nMir ist schlecht.", "vocabulary": [{"term": "Kopfschmerzen", "definition": "Headache", "example": "Ich habe starke Kopfschmerzen."}], "grammar_points": ["Dativ mit Körperteilen", "Verb wehtun"]}
            ]
        }
    },
    "B1": {
        "basic": {
            "title": "Deutsch Mittelstufe",
            "desc": "Meinungen ausdrücken, Erfahrungen erzählen, Reisesituationen.",
            "lessons": [
                {"title": "Meinungen ausdrücken", "content": "## Seine Meinung sagen\n\nIch denke, dass...\nMeiner Meinung nach...\nIch bin der Meinung, dass...\n\nZustimmen: Ich stimme zu, Da hast du recht\nWidersprechen: Ich bin anderer Meinung", "vocabulary": [{"term": "Meinung", "definition": "Opinion", "example": "Meiner Meinung nach ist das richtig."}], "grammar_points": ["Nebensätze mit dass", "Konjunktiv II für höfliche Meinungen"]},
                {"title": "Reisen", "content": "## Reiseplanung\n\nAm Flughafen: Einchecken, Boarding, Gepäck\nIm Hotel: Reservierung, Beschwerden\nIch möchte ein Zimmer reservieren.", "vocabulary": [{"term": "Flug", "definition": "Flight", "example": "Mein Flug geht um 10 Uhr."}], "grammar_points": ["Konjunktiv II: ich würde", "Relativsätze"]},
                {"title": "Arbeit und Beruf", "content": "## Berufsleben\n\nBerufe: Arzt, Lehrer, Ingenieur\nBewerbung, Vorstellungsgespräch, Lebenslauf", "vocabulary": [{"term": "Beruf", "definition": "Profession", "example": "Was ist Ihr Beruf?"}], "grammar_points": ["Passiv", "Infinitiv mit zu"]}
            ]
        },
        "practical": {
            "title": "Deutsch für Reisende B1",
            "desc": "Reisesituationen: Flughäfen, Hotels, Notfälle.",
            "lessons": [
                {"title": "Am Flughafen", "content": "## Flugreisen\n\nEinchecken, Sicherheitskontrolle, Boarding\nMein Flug hat Verspätung.\nWo ist Gate B5?", "vocabulary": [{"term": "Verspätung", "definition": "Delay", "example": "Der Flug hat zwei Stunden Verspätung."}], "grammar_points": ["Passiv Präsens", "Temporale Nebensätze"]},
                {"title": "Im Hotel", "content": "## Unterkunft\n\nReservierung, Ein-/Auschecken\nProbleme melden, Beschwerden\nKönnte ich ein anderes Zimmer haben?", "vocabulary": [{"term": "Unterkunft", "definition": "Accommodation", "example": "Ich suche eine günstige Unterkunft."}], "grammar_points": ["Konjunktiv II für Höflichkeit", "Indirekte Fragen"]},
                {"title": "Notfälle", "content": "## Im Notfall\n\nBeim Arzt, in der Apotheke\nPolizei rufen, Unfall melden\nIch brauche einen Arzt!", "vocabulary": [{"term": "Notfall", "definition": "Emergency", "example": "Das ist ein Notfall!"}], "grammar_points": ["Imperativ", "Modalverben: müssen, sollen"]}
            ]
        }
    },
    "B2": {
        "basic": {
            "title": "Deutsch Oberstufe",
            "desc": "Komplexe Texte, Debatten und fließender Ausdruck.",
            "lessons": [
                {"title": "Diskussionen führen", "content": "## Argumentieren\n\nThese aufstellen, Argumente präsentieren\nEinerseits... andererseits...\nDarüber hinaus, Außerdem, Jedoch", "vocabulary": [{"term": "Argument", "definition": "Argument", "example": "Das ist ein gutes Argument."}], "grammar_points": ["Konnektoren", "Nominalisierung"]},
                {"title": "Medien und Nachrichten", "content": "## Aktuelle Ereignisse\n\nZeitung, Fernsehen, Internet\nSchlagzeilen, Artikel, Berichte\nLaut Medienberichten...", "vocabulary": [{"term": "Schlagzeile", "definition": "Headline", "example": "Die Schlagzeile heute ist..."}], "grammar_points": ["Passiv Perfekt", "Indirekte Rede"]},
                {"title": "Umwelt und Gesellschaft", "content": "## Gesellschaftliche Themen\n\nKlimawandel, Nachhaltigkeit\nSoziale Probleme, Lösungen\nEs ist wichtig, dass wir handeln.", "vocabulary": [{"term": "Nachhaltigkeit", "definition": "Sustainability", "example": "Nachhaltigkeit ist wichtig."}], "grammar_points": ["Konjunktiv I für indirekte Rede", "Partizipialkonstruktionen"]}
            ]
        },
        "practical": {
            "title": "Geschäftsdeutsch B2",
            "desc": "Professionelle Kommunikation: Meetings, Verhandlungen, Präsentationen.",
            "lessons": [
                {"title": "Geschäftsmeetings", "content": "## Besprechungen\n\nTagesordnung, Protokoll\nIch möchte vorschlagen, dass...\nKönnten wir zum nächsten Punkt kommen?", "vocabulary": [{"term": "Tagesordnung", "definition": "Agenda", "example": "Der erste Punkt der Tagesordnung..."}], "grammar_points": ["Konjunktiv II für Vorschläge", "Formelle Sprache"]},
                {"title": "Verhandlungen", "content": "## Verhandlungstechniken\n\nAngebote, Gegenangebote\nKompromisse finden\nWir könnten uns in der Mitte treffen.", "vocabulary": [{"term": "Verhandlung", "definition": "Negotiation", "example": "Die Verhandlungen waren erfolgreich."}], "grammar_points": ["Konzessivsätze: obwohl", "Bedingungssätze"]},
                {"title": "Präsentationen", "content": "## Effektive Präsentationen\n\nStruktur, Visualisierung\nIch möchte Ihre Aufmerksamkeit auf... lenken.\nZusammenfassend lässt sich sagen...", "vocabulary": [{"term": "Folie", "definition": "Slide", "example": "Auf dieser Folie sehen Sie..."}], "grammar_points": ["Textgliederung", "Passiv in Präsentationen"]}
            ]
        }
    },
    "C1": {
        "basic": {
            "title": "Deutsch Fortgeschritten",
            "desc": "Flexibler Sprachgebrauch in akademischen und beruflichen Kontexten.",
            "lessons": [
                {
                    "title": "Fortgeschrittene Argumentation",
                    "content": """## Argumentationstechniken

### Aufbau einer Argumentation:
1. These formulieren
2. Argumente mit Belegen präsentieren
3. Gegenargumente entkräften
4. Schlussfolgerung ziehen

### Wichtige Konnektoren:
- Hinzufügend: Darüber hinaus, Ferner, Überdies
- Kontrastierend: Hingegen, Dennoch, Nichtsdestotrotz
- Schlussfolgernd: Folglich, Demzufolge, Somit

### Ausdrücke für Argumentation:
- Es ist unbestreitbar, dass...
- Man muss berücksichtigen, dass...
- Es liegt auf der Hand, dass...
- Angesichts der Tatsache, dass...""",
                    "vocabulary": [
                        {"term": "Unbestreitbar", "definition": "Undeniable", "example": "Es ist unbestreitbar, dass..."},
                        {"term": "Nichtsdestotrotz", "definition": "Nevertheless", "example": "Nichtsdestotrotz müssen wir handeln."},
                        {"term": "Demzufolge", "definition": "Consequently", "example": "Demzufolge ist es notwendig..."},
                        {"term": "Angesichts", "definition": "In view of", "example": "Angesichts der Lage..."},
                        {"term": "Hinzufügen", "definition": "To add", "example": "Ich möchte hinzufügen, dass..."},
                        {"term": "Entkräften", "definition": "To refute", "example": "Dieses Argument lässt sich entkräften."},
                    ],
                    "grammar_points": ["Partizipialattribute", "Konjunktiv I in wissenschaftlichen Texten", "Nominalisierungen"]
                },
                {
                    "title": "Wissenschaftssprache",
                    "content": """## Akademisches Schreiben

### Struktur wissenschaftlicher Arbeiten:
- Zusammenfassung/Abstract
- Einleitung mit Fragestellung
- Theoretischer Rahmen
- Methodik
- Ergebnisse
- Diskussion
- Fazit

### Wissenschaftliche Verben:
- analysieren, untersuchen, erforschen
- belegen, nachweisen, bestätigen
- schlussfolgern, ableiten

### Zitieren:
- Laut Müller (2023)...
- Wie Schmidt (2022) feststellt...
- Nach Ansicht von...""",
                    "vocabulary": [
                        {"term": "Hypothese", "definition": "Hypothesis", "example": "Die Hypothese wurde bestätigt."},
                        {"term": "Ergebnis", "definition": "Result", "example": "Die Ergebnisse zeigen, dass..."},
                        {"term": "Schlussfolgerung", "definition": "Conclusion", "example": "Die Schlussfolgerung ist eindeutig."},
                        {"term": "Belegen", "definition": "To prove/substantiate", "example": "Die Daten belegen diese These."},
                        {"term": "Untersuchen", "definition": "To examine", "example": "Wir untersuchen den Zusammenhang."},
                    ],
                    "grammar_points": ["Passiv in wissenschaftlichen Texten", "Unpersönliche Konstruktionen", "Komplexe Nebensätze"]
                },
                {
                    "title": "Kulturelle Nuancen",
                    "content": """## Redewendungen und Sprachvariation

### Deutsche Redewendungen:
- Da liegt der Hund begraben → Das ist der Kern des Problems
- Jemandem einen Bären aufbinden → Jemanden anlügen
- Die Katze aus dem Sack lassen → Ein Geheimnis verraten
- Ins Fettnäpfchen treten → Einen Fehler machen

### Sprachregister:
- Formell: Sie, Sehr geehrte Damen und Herren
- Informell: Du, Hallo zusammen
- Umgangssprachlich: Hey, Was geht?

### Regionale Varianten:
- Deutschland: Brötchen, Tüte, Kartoffel
- Österreich: Semmel, Sackerl, Erdapfel
- Schweiz: Brötli, Sack, Härdöpfel""",
                    "vocabulary": [
                        {"term": "Redewendung", "definition": "Idiom", "example": "Das ist eine bekannte Redewendung."},
                        {"term": "Umgangssprache", "definition": "Colloquial language", "example": "Das ist umgangssprachlich."},
                        {"term": "Nuance", "definition": "Nuance", "example": "Es gibt einen feinen Nuance."},
                        {"term": "Dialekt", "definition": "Dialect", "example": "Bayerisch ist ein Dialekt."},
                    ],
                    "grammar_points": ["Modalpartikeln: ja, doch, mal, eben", "Konjunktiv II in Redewendungen", "Registerunterschiede"]
                }
            ]
        },
        "practical": {
            "title": "Akademisches Deutsch C1",
            "desc": "Akademische Fähigkeiten: Debatten, Aufsätze, Forschung.",
            "lessons": [
                {"title": "Debattieren", "content": "## Debattiertechniken\n\nStandpunkte vertreten und widerlegen\nRedezeit einhalten\nZusammenfassend möchte ich betonen...", "vocabulary": [{"term": "Widerlegen", "definition": "To refute", "example": "Diesen Punkt kann ich widerlegen."}], "grammar_points": ["Konzessivsätze", "Adversative Konnektoren"]},
                {"title": "Aufsätze schreiben", "content": "## Der wissenschaftliche Aufsatz\n\nThese, Argumentation, Belege\nZitierweise, Quellenangabe\nAbschließend lässt sich feststellen...", "vocabulary": [{"term": "These", "definition": "Thesis", "example": "Meine These ist, dass..."}], "grammar_points": ["Wissenschaftlicher Stil", "Textverknüpfung"]},
                {"title": "Forschungsmethoden", "content": "## Wissenschaftliches Arbeiten\n\nHypothesen aufstellen\nDaten erheben und analysieren\nErgebnisse interpretieren", "vocabulary": [{"term": "Stichprobe", "definition": "Sample", "example": "Die Stichprobe umfasst 100 Teilnehmer."}], "grammar_points": ["Passiv der Vorgangspassiv", "Fachsprachliche Ausdrücke"]}
            ]
        }
    },
    "C2": {
        "basic": {
            "title": "Deutsch Perfektion",
            "desc": "Vollständige Beherrschung mit kulturellen und literarischen Nuancen.",
            "lessons": [
                {
                    "title": "Literarischer Stil",
                    "content": """## Literaturanalyse

### Rhetorische Figuren:
- Metapher: Übertragene Bedeutung
- Vergleich: Expliziter Vergleich mit "wie"
- Hyperbel: Übertreibung
- Personifikation: Vermenschlichung
- Ironie: Das Gegenteil sagen

### Literarische Gattungen:
- Epik: Roman, Erzählung, Novelle
- Lyrik: Gedicht, Sonett
- Dramatik: Tragödie, Komödie

### Deutsche Literaturepochen:
- Weimarer Klassik: Goethe, Schiller
- Romantik: Novalis, E.T.A. Hoffmann
- Expressionismus: Kafka, Benn
- Moderne: Grass, Böll""",
                    "vocabulary": [
                        {"term": "Metapher", "definition": "Metaphor", "example": "Das Leben ist eine Reise (Metapher)."},
                        {"term": "Erzähler", "definition": "Narrator", "example": "Der allwissende Erzähler..."},
                        {"term": "Handlung", "definition": "Plot", "example": "Die Handlung ist komplex."},
                        {"term": "Motiv", "definition": "Motif", "example": "Das Motiv der Reise..."},
                        {"term": "Stilmittel", "definition": "Stylistic device", "example": "Welche Stilmittel werden verwendet?"},
                    ],
                    "grammar_points": ["Konjunktiv I in literarischen Texten", "Stilistische Inversion", "Historische Grammatikformen"]
                },
                {
                    "title": "Dialekte und Varietäten",
                    "content": """## Deutsche Sprachvariation

### Hochdeutsch vs. Dialekte:
- Standarddeutsch als Schriftsprache
- Regionale Aussprache und Wortschatz

### Wichtige Dialektgruppen:
- Niederdeutsch (Plattdeutsch)
- Mitteldeutsch (Hessisch, Thüringisch)
- Oberdeutsch (Bairisch, Alemannisch)

### Nationale Varietäten:
- Bundesdeutsch
- Österreichisches Deutsch
- Schweizer Hochdeutsch

### Soziolekte und Fachsprachen:
- Jugendsprache
- Fachsprachen (Medizin, Recht, Technik)""",
                    "vocabulary": [
                        {"term": "Varietät", "definition": "Variety", "example": "Das österreichische Deutsch ist eine Varietät."},
                        {"term": "Mundart", "definition": "Dialect", "example": "Er spricht Mundart."},
                        {"term": "Standardsprache", "definition": "Standard language", "example": "Die Standardsprache ist normiert."},
                        {"term": "Soziolekt", "definition": "Sociolect", "example": "Jugendsprache ist ein Soziolekt."},
                    ],
                    "grammar_points": ["Dialektale Grammatik", "Variation in der Morphologie", "Phonetische Unterschiede"]
                },
                {
                    "title": "Professionelle Kommunikation",
                    "content": """## Kommunikation auf höchstem Niveau

### Präsentationen für Führungskräfte:
- Strategische Kommunikation
- Stakeholder-Management
- Krisenmanagement

### Diplomatische Sprache:
- Höflichkeitsformen der höchsten Stufe
- Indirekte Kommunikation
- Interkulturelle Sensibilität

### Formelle Korrespondenz:
- Geschäftsbriefe auf höchstem Niveau
- Vertragssprache
- Protokollarische Dokumente""",
                    "vocabulary": [
                        {"term": "Konsens", "definition": "Consensus", "example": "Wir haben einen Konsens erreicht."},
                        {"term": "Vorbehalt", "definition": "Reservation", "example": "Unter Vorbehalt der Genehmigung..."},
                        {"term": "Verbindlich", "definition": "Binding", "example": "Diese Vereinbarung ist verbindlich."},
                        {"term": "Protokoll", "definition": "Protocol/Minutes", "example": "Das Protokoll der Sitzung..."},
                    ],
                    "grammar_points": ["Juristische Fachsprache", "Diplomatischer Konjunktiv", "Formelle Textsortenmerkmale"]
                }
            ]
        },
        "practical": {
            "title": "Literarisches Deutsch C2",
            "desc": "Literatur und Kultur: Textanalyse, kreatives Schreiben, Kritik.",
            "lessons": [
                {"title": "Textanalyse", "content": "## Literaturkritik\n\nHistorischer Kontext, Stilanalyse\nInterpretation, Intertextualität\nDer Text lässt sich als... interpretieren.", "vocabulary": [{"term": "Intertextualität", "definition": "Intertextuality", "example": "Es gibt Intertextualität mit Goethe."}], "grammar_points": ["Analytischer Stil", "Fachterminologie"]},
                {"title": "Kreatives Schreiben", "content": "## Schreibtechniken\n\nErzählperspektive, Figurenentwicklung\nDialoge, Beschreibungen\nSpannung aufbauen", "vocabulary": [{"term": "Perspektive", "definition": "Perspective", "example": "Die Ich-Perspektive..."}], "grammar_points": ["Narrative Tempora", "Stilistische Variation"]},
                {"title": "Lyrik", "content": "## Gedichtanalyse und -schreiben\n\nMetrum, Reim, rhetorische Figuren\nInterpretation und Wirkung\nLyrisches Ich", "vocabulary": [{"term": "Metrum", "definition": "Meter", "example": "Das Metrum ist jambisch."}], "grammar_points": ["Poetische Freiheiten", "Lyrische Formen"]}
            ]
        }
    }
}

# ============== FLASHCARDS ALEMÁN ==============
GERMAN_FLASHCARDS = {
    "A1": [
        {"word": "Hallo", "translation": "Hello", "example": "Hallo! Wie geht es dir?", "pronunciation": "HA-lo"},
        {"word": "Danke", "translation": "Thank you", "example": "Danke schön!", "pronunciation": "DAN-ke"},
        {"word": "Bitte", "translation": "Please/You're welcome", "example": "Bitte schön!", "pronunciation": "BI-te"},
        {"word": "Guten Tag", "translation": "Good day", "example": "Guten Tag, Herr Müller.", "pronunciation": "GOO-ten tahk"},
        {"word": "Auf Wiedersehen", "translation": "Goodbye", "example": "Auf Wiedersehen!", "pronunciation": "owf VEE-der-zay-en"},
        {"word": "Ja", "translation": "Yes", "example": "Ja, das stimmt.", "pronunciation": "yah"},
        {"word": "Nein", "translation": "No", "example": "Nein, danke.", "pronunciation": "nine"},
        {"word": "Wasser", "translation": "Water", "example": "Ein Glas Wasser, bitte.", "pronunciation": "VA-ser"},
        {"word": "Haus", "translation": "House", "example": "Das Haus ist groß.", "pronunciation": "hows"},
        {"word": "Familie", "translation": "Family", "example": "Meine Familie ist klein.", "pronunciation": "fa-MEE-lee-e"},
    ],
    "A2": [
        {"word": "Arbeiten", "translation": "To work", "example": "Ich arbeite in einem Büro.", "pronunciation": "AR-by-ten"},
        {"word": "Essen", "translation": "To eat", "example": "Ich esse gern Pizza.", "pronunciation": "E-sen"},
        {"word": "Kaufen", "translation": "To buy", "example": "Ich kaufe Brot.", "pronunciation": "KOW-fen"},
        {"word": "Schön", "translation": "Beautiful", "example": "Das Kleid ist sehr schön.", "pronunciation": "shurn"},
        {"word": "Billig", "translation": "Cheap", "example": "Das Buch ist billig.", "pronunciation": "BI-likh"},
        {"word": "Teuer", "translation": "Expensive", "example": "Das Auto ist teuer.", "pronunciation": "TOY-er"},
        {"word": "Immer", "translation": "Always", "example": "Ich komme immer pünktlich.", "pronunciation": "I-mer"},
        {"word": "Nie", "translation": "Never", "example": "Ich esse nie Fleisch.", "pronunciation": "nee"},
        {"word": "Nah", "translation": "Near", "example": "Die Bank ist nah.", "pronunciation": "nah"},
        {"word": "Weit", "translation": "Far", "example": "Meine Arbeit ist weit.", "pronunciation": "vite"},
    ],
    "B1": [
        {"word": "Entwickeln", "translation": "To develop", "example": "Ich möchte meine Fähigkeiten entwickeln.", "pronunciation": "ent-VI-keln"},
        {"word": "Erreichen", "translation": "To achieve", "example": "Ich werde mein Ziel erreichen.", "pronunciation": "er-RY-khen"},
        {"word": "Verbessern", "translation": "To improve", "example": "Ich muss mein Deutsch verbessern.", "pronunciation": "fer-BE-sern"},
        {"word": "Obwohl", "translation": "Although", "example": "Obwohl es regnet, gehe ich raus.", "pronunciation": "op-VOHL"},
        {"word": "Jedoch", "translation": "However", "example": "Es gefällt mir; jedoch ist es teuer.", "pronunciation": "ye-DOHKH"},
        {"word": "Während", "translation": "While", "example": "Ich lerne während ich arbeite.", "pronunciation": "VE-rent"},
        {"word": "Hoffnung", "translation": "Hope", "example": "Ich habe Hoffnung für die Zukunft.", "pronunciation": "HOF-noong"},
        {"word": "Sorgen", "translation": "To worry", "example": "Mach dir keine Sorgen.", "pronunciation": "ZOR-gen"},
        {"word": "Genießen", "translation": "To enjoy", "example": "Ich genieße die Musik sehr.", "pronunciation": "ge-NEE-sen"},
        {"word": "Verwirklichen", "translation": "To realize/accomplish", "example": "Ich werde meinen Traum verwirklichen.", "pronunciation": "fer-VIRK-li-khen"},
    ],
    "B2": [
        {"word": "Unerlässlich", "translation": "Essential", "example": "Wasser ist unerlässlich zum Leben.", "pronunciation": "UN-er-les-likh"},
        {"word": "Nutzen", "translation": "To use/benefit", "example": "Du solltest diese Gelegenheit nutzen.", "pronunciation": "NU-tsen"},
        {"word": "Hervorheben", "translation": "To highlight", "example": "Ich möchte diesen Punkt hervorheben.", "pronunciation": "her-FOR-hay-ben"},
        {"word": "Trotzdem", "translation": "Nevertheless", "example": "Trotzdem bin ich glücklich.", "pronunciation": "TROTS-daym"},
        {"word": "Ebenfalls", "translation": "Likewise", "example": "Ebenfalls müssen wir andere Faktoren berücksichtigen.", "pronunciation": "AY-ben-fals"},
        {"word": "Hinterfragen", "translation": "To question", "example": "Es ist wichtig, Nachrichten zu hinterfragen.", "pronunciation": "HIN-ter-frah-gen"},
        {"word": "Bereitstellen", "translation": "To provide", "example": "Ich werde alle Informationen bereitstellen.", "pronunciation": "be-RITE-shte-len"},
        {"word": "Aufrechterhalten", "translation": "To maintain", "example": "Ich halte meine Meinung aufrecht.", "pronunciation": "OWF-rekht-er-hal-ten"},
        {"word": "Ansprechen", "translation": "To address", "example": "Wir müssen dieses Problem ansprechen.", "pronunciation": "AN-shpre-khen"},
        {"word": "Verknüpfen", "translation": "To link", "example": "Wir müssen Theorie und Praxis verknüpfen.", "pronunciation": "fer-KNÜP-fen"},
    ],
    "C1": [
        {"word": "Ergreifend", "translation": "Moving/touching", "example": "Es ist eine ergreifende Erinnerung.", "pronunciation": "er-GRY-fent"},
        {"word": "Eigenart", "translation": "Idiosyncrasy", "example": "Jede Kultur hat ihre Eigenart.", "pronunciation": "EYE-gen-art"},
        {"word": "Ergründen", "translation": "To fathom/scrutinize", "example": "Man muss die Daten sorgfältig ergründen.", "pronunciation": "er-GRÜN-den"},
        {"word": "Zugrundeliegen", "translation": "To underlie", "example": "Mehrere Faktoren liegen diesem Phänomen zugrunde.", "pronunciation": "tsu-GRUN-de-lee-gen"},
        {"word": "Erläutern", "translation": "To elucidate", "example": "Der Professor erläuterte das komplexe Konzept.", "pronunciation": "er-LOY-tern"},
        {"word": "Mit sich bringen", "translation": "To entail", "example": "Dieses Projekt bringt große Verantwortung mit sich.", "pronunciation": "mit zikh BRING-en"},
        {"word": "Verdeutlichen", "translation": "To clarify", "example": "Ich werde versuchen, dies zu verdeutlichen.", "pronunciation": "fer-DOYT-li-khen"},
        {"word": "Verachten", "translation": "To disdain", "example": "Man sollte andere Meinungen nicht verachten.", "pronunciation": "fer-AKH-ten"},
        {"word": "Inhärent", "translation": "Inherent", "example": "Kreativität ist dem Menschen inhärent.", "pronunciation": "in-he-RENT"},
        {"word": "Umgehen", "translation": "To sidestep", "example": "Wir können dieses Problem nicht umgehen.", "pronunciation": "UM-gay-en"},
    ],
    "C2": [
        {"word": "Buntscheckig", "translation": "Motley", "example": "Es war eine buntscheckige Gruppe.", "pronunciation": "BUNT-she-kikh"},
        {"word": "Schroff", "translation": "Curt/brusque", "example": "Seine Antwort war schroff.", "pronunciation": "shrof"},
        {"word": "Eingefleischt", "translation": "Staunch/inveterate", "example": "Er ist ein eingefleischter Verteidiger.", "pronunciation": "EYN-ge-flysht"},
        {"word": "Verborgen", "translation": "Hidden", "example": "Wir erkundeten verborgene Orte.", "pronunciation": "fer-BOR-gen"},
        {"word": "Immerwährend", "translation": "Everlasting", "example": "Ihre Liebe ist immerwährend.", "pronunciation": "I-mer-ve-rent"},
        {"word": "Unberührt", "translation": "Pristine", "example": "Der Wald war in unberührtem Zustand.", "pronunciation": "UN-be-rürt"},
        {"word": "Einwilligung", "translation": "Acquiescence", "example": "Seine Einwilligung überraschte alle.", "pronunciation": "EYN-vi-li-goong"},
        {"word": "Gewohnheitsrecht", "translation": "Customary law", "example": "Es ist ein Gewohnheitsrecht.", "pronunciation": "ge-VOHN-hytes-rekht"},
        {"word": "Abscheulich", "translation": "Execrable", "example": "Sein Verhalten war abscheulich.", "pronunciation": "AP-shoy-likh"},
        {"word": "Groll", "translation": "Resentment", "example": "Er hegt noch immer Groll.", "pronunciation": "grol"},
    ]
}

async def add_german():
    """Agregar el idioma alemán a la base de datos."""
    
    total_courses = 0
    total_lessons = 0
    total_flashcards = 0
    
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    print("🇩🇪 Agregando idioma Alemán...\n")
    
    for level in levels:
        level_data = GERMAN_COURSES[level]
        
        # Crear curso básico
        basic = level_data["basic"]
        course_doc = {
            "language": "german",
            "level": level,
            "title": basic["title"],
            "description": basic["desc"],
            "created_by": "system",
            "created_at": datetime.utcnow()
        }
        result = await db.courses.insert_one(course_doc)
        course_id = str(result.inserted_id)
        total_courses += 1
        
        for i, lesson in enumerate(basic["lessons"]):
            lesson_doc = {
                "course_id": course_id,
                "title": lesson["title"],
                "content": lesson["content"].strip(),
                "vocabulary": lesson.get("vocabulary", []),
                "grammar_points": lesson.get("grammar_points", []),
                "order": i + 1,
                "created_at": datetime.utcnow()
            }
            await db.lessons.insert_one(lesson_doc)
            total_lessons += 1
        
        print(f"  ✓ {level}: {basic['title']}")
        
        # Crear curso práctico
        practical = level_data["practical"]
        course_doc = {
            "language": "german",
            "level": level,
            "title": practical["title"],
            "description": practical["desc"],
            "created_by": "system",
            "created_at": datetime.utcnow()
        }
        result = await db.courses.insert_one(course_doc)
        course_id = str(result.inserted_id)
        total_courses += 1
        
        for i, lesson in enumerate(practical["lessons"]):
            lesson_doc = {
                "course_id": course_id,
                "title": lesson["title"],
                "content": lesson["content"].strip() if isinstance(lesson["content"], str) else lesson["content"],
                "vocabulary": lesson.get("vocabulary", []),
                "grammar_points": lesson.get("grammar_points", []),
                "order": i + 1,
                "created_at": datetime.utcnow()
            }
            await db.lessons.insert_one(lesson_doc)
            total_lessons += 1
        
        print(f"  ✓ {level}: {practical['title']}")
        
        # Crear flashcards
        flashcards = GERMAN_FLASHCARDS[level]
        for card in flashcards:
            flashcard_doc = {
                "language": "german",
                "level": level,
                "word": card["word"],
                "translation": card["translation"],
                "example": card["example"],
                "pronunciation": card["pronunciation"],
                "created_by": "system",
                "created_at": datetime.utcnow()
            }
            await db.flashcards.insert_one(flashcard_doc)
            total_flashcards += 1
    
    print(f"\n✅ Alemán agregado exitosamente:")
    print(f"   - {total_courses} cursos")
    print(f"   - {total_lessons} lecciones")
    print(f"   - {total_flashcards} flashcards")

if __name__ == "__main__":
    asyncio.run(add_german())

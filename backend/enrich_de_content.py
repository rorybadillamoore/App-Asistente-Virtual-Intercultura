"""Enrich German lessons with real educational content aligned to Menschen textbook."""
import asyncio, os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

DE_RICH = {
"A1": [
"""Willkommen zu Ihrer ersten Deutschstunde! In dieser Lektion lernen Sie, wie man sich auf Deutsch begrüßt und vorstellt.

Begrüßungen: 'Guten Morgen' (good morning, bis ~10 Uhr), 'Guten Tag' (good day, formell), 'Hallo' (hello, informell), 'Guten Abend' (good evening). Verabschiedungen: 'Tschüss' (bye, informell), 'Auf Wiedersehen' (formal goodbye), 'Bis morgen' (see you tomorrow), 'Gute Nacht' (good night).

Sich vorstellen: 'Ich heiße Maria' (My name is Maria), 'Ich bin Peter' (I am Peter). Fragen: 'Wie heißen Sie?' (formal) / 'Wie heißt du?' (informal) — What's your name? 'Woher kommen Sie?' — Where are you from? 'Ich komme aus Costa Rica'.

Wichtige Verben — Konjugation von 'sein' (to be): ich bin, du bist, er/sie ist, wir sind, ihr seid, sie/Sie sind. 'heißen' (to be called): ich heiße, du heißt, er/sie heißt.

Kulturhinweis: In Deutschland sagt man 'Sie' (formal you) zu Fremden und Älteren. 'Du' verwendet man unter Freunden und Familienmitgliedern. Im Geschäftsleben ist 'Sie' Standard.""",

"""Lernen Sie den Wortschatz rund um Familie und Freundschaften.

Die Familie: der Vater (father), die Mutter (mother), der Bruder (brother), die Schwester (sister), der Sohn (son), die Tochter (daughter), die Eltern (parents), die Großeltern (grandparents), der Onkel (uncle), die Tante (aunt), der Cousin/die Cousine (cousin).

Possessivartikel: mein/meine (my), dein/deine (your), sein/seine (his), ihr/ihre (her). 'Mein Vater heißt Hans' (My father's name is Hans). 'Meine Schwester ist 20 Jahre alt' (My sister is 20 years old).

'Haben' (to have): ich habe, du hast, er/sie hat, wir haben, ihr habt, sie haben. 'Ich habe zwei Brüder und eine Schwester' (I have two brothers and one sister). 'Hast du Kinder?' — 'Ja, ich habe einen Sohn' (Do you have children? Yes, I have a son).

Familienstand: ledig (single), verheiratet (married), geschieden (divorced), verwitwet (widowed). 'Ich bin verheiratet und habe zwei Kinder'.""",

"""Lernen Sie, wie man auf Deutsch einkauft und über Lebensmittel spricht.

Im Supermarkt: das Brot (bread), die Milch (milk), der Käse (cheese), die Butter (butter), das Ei/die Eier (egg/eggs), das Fleisch (meat), der Fisch (fish), das Obst (fruit), das Gemüse (vegetables), das Wasser (water), der Saft (juice).

Obst und Gemüse: der Apfel (apple), die Banane (banana), die Orange (orange), die Tomate (tomato), die Kartoffel (potato), die Zwiebel (onion), die Gurke (cucumber), der Salat (lettuce).

Einkaufsdialoge: 'Was möchten Sie?' (What would you like?). 'Ich hätte gern ein Kilo Äpfel' (I'd like a kilo of apples). 'Was kostet das?' (How much is that?). 'Das macht 3,50 Euro' (That's 3.50 euros). 'Sonst noch etwas?' (Anything else?). 'Nein, danke. Das ist alles' (No, thanks. That's all).

Bestimmte Artikel: der (maskulin), die (feminin), das (neutrum). 'Der Apfel ist rot', 'Die Milch ist frisch', 'Das Brot ist lecker'. Unbestimmte Artikel: ein/eine/ein. Plural hat keinen unbestimmten Artikel.""",

"""In dieser Lektion lernen Sie Wörter für die Wohnung und Möbel.

Die Wohnung: das Zimmer (room), die Küche (kitchen), das Badezimmer (bathroom), das Schlafzimmer (bedroom), das Wohnzimmer (living room), der Flur (hallway), der Balkon (balcony), der Keller (basement), der Garten (garden).

Möbel: der Tisch (table), der Stuhl (chair), das Sofa (sofa), das Bett (bed), der Schrank (wardrobe), das Regal (shelf), die Lampe (lamp), der Kühlschrank (fridge), der Herd (stove), die Waschmaschine (washing machine).

Beschreibung: 'Meine Wohnung hat drei Zimmer' (My apartment has three rooms). 'Die Küche ist klein aber modern' (The kitchen is small but modern). 'Im Wohnzimmer steht ein großes Sofa' (There is a big sofa in the living room).

Präpositionen: in (in), auf (on), unter (under), neben (next to), zwischen (between), vor (in front of), hinter (behind). Dativ nach Wo-Fragen: 'Wo ist das Buch?' — 'Das Buch ist auf dem Tisch' (auf + dem = Dativ). 'Die Lampe steht neben dem Bett'.""",

"""Lernen Sie, über Ihren Tagesablauf zu sprechen und die Uhrzeit zu sagen.

Tagesablauf: aufstehen (to get up), frühstücken (to have breakfast), arbeiten (to work), Mittagessen (to have lunch), kochen (to cook), fernsehen (to watch TV), schlafen gehen (to go to sleep).

Trennbare Verben: 'Ich stehe um 7 Uhr auf' (I get up at 7). 'aufstehen' trennt sich: auf|stehen. Weitere: an|fangen (to begin), ein|kaufen (to shop), fern|sehen (to watch TV), zurück|kommen (to come back). 'Der Film fängt um 20 Uhr an'.

Die Uhrzeit: 'Wie spät ist es?' / 'Wie viel Uhr ist es?' — 'Es ist acht Uhr' (8:00). 'Es ist halb neun' (8:30 — half before 9!). 'Es ist Viertel nach zehn' (10:15). 'Es ist Viertel vor zwölf' (11:45). Achtung: 'halb neun' = 8:30, nicht 9:30!

Mein Tag: 'Ich stehe um sieben Uhr auf. Dann frühstücke ich und trinke Kaffee. Um acht Uhr fahre ich zur Arbeit. Ich arbeite von 9 bis 17 Uhr. Abends koche ich und sehe fern. Um 23 Uhr gehe ich schlafen.'

Adverbien der Häufigkeit: immer (always), oft (often), manchmal (sometimes), selten (rarely), nie (never).""",

"""Lernen Sie, über Freizeit und Hobbys zu sprechen.

Hobbys: lesen (to read), schwimmen (to swim), kochen (to cook), tanzen (to dance), reisen (to travel), Musik hören (to listen to music), Fußball spielen (to play football), Fahrrad fahren (to ride a bike), fotografieren (to take photos), wandern (to hike).

Mögen und gern: 'Ich spiele gern Fußball' (I like playing football — 'gern' after the verb). 'Ich lese gern Bücher' (I like reading books). 'Mein Hobby ist Schwimmen'. Frage: 'Was machst du in deiner Freizeit?' (What do you do in your free time?).

Modalverb 'können' (can): ich kann, du kannst, er/sie kann, wir können. 'Kannst du schwimmen?' — 'Ja, ich kann gut schwimmen'. 'Ich kann Gitarre spielen' (I can play guitar). Das Modalverb steht an Position 2, das Vollverb am Ende: 'Ich kann morgen nicht kommen'.

Sport: Tennis spielen, joggen, Yoga machen, ins Fitnessstudio gehen. 'Am Wochenende gehe ich oft wandern' (On weekends I often go hiking). 'Im Sommer schwimme ich gern im See' (In summer I like swimming in the lake).

Tageszeiten: morgens (in the morning), mittags (at noon), nachmittags (in the afternoon), abends (in the evening). 'Morgens lese ich die Zeitung. Abends sehe ich fern'."""
],
"A2": [
"""Lernen Sie den Wortschatz für Berufe und den Arbeitsplatz.

Berufe: der Arzt/die Ärztin (doctor), der Lehrer/die Lehrerin (teacher), der Ingenieur/die Ingenieurin (engineer), der Koch/die Köchin (cook), der Verkäufer/die Verkäuferin (salesperson), der Anwalt/die Anwältin (lawyer), der Krankenpfleger/die Krankenpflegerin (nurse).

Feminine Formen: Viele Berufe bilden die weibliche Form mit '-in': Lehrer → Lehrerin, Arzt → Ärztin, Koch → Köchin. 'Was sind Sie von Beruf?' — 'Ich bin Lehrerin'. 'Wo arbeiten Sie?' — 'Ich arbeite in einer Schule'.

Arbeitsvokabular: das Büro (office), der Chef (boss), der Kollege (colleague), das Gehalt (salary), die Besprechung (meeting), Überstunden machen (to work overtime), Urlaub nehmen (to take vacation).

Perfekt (Vergangenheit): haben + Partizip II. 'Ich habe studiert' (I studied). 'Er hat als Ingenieur gearbeitet' (He worked as an engineer). Regelm. Partizip: ge-...-t (gemacht, gelernt, gearbeitet). Unregelm.: ge-...-en (geschrieben, gelesen, gesprochen). 'Ich habe Medizin studiert und als Arzt gearbeitet'.""",

"""Lernen Sie, über Wohnen und Umzüge zu sprechen.

Wohnungssuche: 'Ich suche eine Wohnung' (I'm looking for an apartment). 'Die Miete beträgt 800 Euro pro Monat' (The rent is 800 euros per month). 'Die Wohnung hat 2 Zimmer, Küche und Bad' (2ZKB). 'Die Nebenkosten sind inklusive' (Utilities included).

Umzug: umziehen (to move), die Kisten packen (to pack boxes), die Möbel transportieren (to transport furniture), streichen (to paint), renovieren (to renovate). 'Wir sind letztes Jahr umgezogen' (We moved last year). 'Die neue Wohnung ist größer als die alte' (The new apartment is bigger than the old one).

Komparativ und Superlativ: groß → größer → am größten (big, bigger, biggest). klein → kleiner → am kleinsten. teuer → teurer → am teuersten. gut → besser → am besten. 'Berlin ist größer als München'. 'Hamburg ist die schönste Stadt'.

Wohnformen: die WG (Wohngemeinschaft — shared apartment, sehr beliebt bei Studenten), das Eigenheim (own home), die Mietwohnung (rental apartment). 'In Deutschland mieten die meisten Leute ihre Wohnung'.""",

"""Lernen Sie den Wortschatz für Gesundheit und einen Arztbesuch.

Körperteile: der Kopf (head), der Arm (arm), das Bein (leg), die Hand (hand), der Fuß (foot), der Rücken (back), der Bauch (stomach), das Auge (eye), das Ohr (ear), der Mund (mouth), die Nase (nose).

Beim Arzt: 'Ich habe Kopfschmerzen' (I have a headache). 'Mir ist schlecht' (I feel nauseous). 'Ich habe Fieber' (I have a fever). 'Ich habe Husten und Schnupfen' (I have a cough and a cold). 'Wo tut es weh?' (Where does it hurt?). 'Seit wann haben Sie die Beschwerden?' (Since when do you have the symptoms?).

Modalverben: 'Sie sollen viel Wasser trinken' (You should drink lots of water). 'Sie dürfen keinen Sport machen' (You must not do sports). 'Sie müssen diese Tabletten dreimal täglich nehmen' (You must take these tablets three times daily).

Imperativ: 'Nehmen Sie die Medizin!' (Take the medicine!). 'Ruhen Sie sich aus!' (Rest!). 'Trinken Sie viel Tee!' (Drink lots of tea!). Reflexive Verben: sich fühlen (to feel), sich ausruhen (to rest). 'Ich fühle mich nicht gut'. 'Gute Besserung!' (Get well soon!).""",

"""Lernen Sie den Wortschatz rund um Reisen und Verkehrsmittel.

Verkehrsmittel: der Zug (train), der Bus (bus), die Straßenbahn (tram), das Flugzeug (airplane), das Auto (car), das Fahrrad (bicycle), die U-Bahn (subway), die S-Bahn (suburban train). 'Ich fahre mit dem Zug nach Berlin' (I'm taking the train to Berlin).

Am Bahnhof: 'Eine Fahrkarte nach München, bitte' (A ticket to Munich, please). 'Einfach oder hin und zurück?' (One way or round trip?). 'Wann fährt der nächste Zug?' (When does the next train leave?). 'Von welchem Gleis fährt der Zug?' (From which platform?). 'Muss ich umsteigen?' (Do I need to change trains?).

Präpositionen mit Dativ: mit dem Bus (by bus), mit der Bahn (by train), mit dem Flugzeug (by plane). Aber: zu Fuß (on foot). 'Wie komme ich zum Bahnhof?' — 'Gehen Sie geradeaus und dann links' (Go straight and then left).

Im Hotel: 'Ich habe ein Zimmer reserviert' (I reserved a room). 'Ein Einzelzimmer oder Doppelzimmer?' (Single or double room?). 'Ist das Frühstück inklusive?' (Is breakfast included?). 'Wann ist der Check-out?' (When is check-out?).

Perfekt mit 'sein': Bewegungsverben: 'Ich bin nach Berlin gefahren' (I went/drove to Berlin). 'Wir sind nach Spanien geflogen' (We flew to Spain). 'Er ist zu Hause geblieben' (He stayed at home).""",

"""Lernen Sie die wichtigsten deutschen Feste und Traditionen kennen.

Weihnachten (Christmas): der Adventskalender (24 Türchen bis Weihnachten), der Weihnachtsmarkt (Christmas market — Glühwein, Lebkuchen, Bratwurst), der Heiligabend (24. Dezember — Bescherung/gift giving). 'Frohe Weihnachten!' (Merry Christmas!). 'Was wünscht du dir zu Weihnachten?' (What do you wish for Christmas?).

Oktoberfest: 'Das Oktoberfest in München ist das größte Volksfest der Welt' — Bier, Brezeln, Weißwurst, Dirndl und Lederhosen. 'O'zapft is!' (It's tapped! — Eröffnungsruf).

Karneval/Fasching: besonders in Köln und Düsseldorf. Kostüme, Umzüge, 'Alaaf!' (Köln) und 'Helau!' (Düsseldorf). 'Rosenmontag ist der Höhepunkt des Karnevals'.

Ostern (Easter): Ostereier suchen (egg hunt), der Osterhase (Easter bunny), das Osterlamm. 'Frohe Ostern!' Tag der Deutschen Einheit: 3. Oktober — 'Die Wiedervereinigung war 1990'.

Nebensätze mit 'weil' (because): 'Ich mag Weihnachten, weil es so gemütlich ist' (I like Christmas because it's so cozy). Das Verb geht ans Ende: 'Wir feiern, weil wir Geburtstag haben'.""",

"""Lernen Sie über Medien und digitalen Alltag in Deutschland zu sprechen.

Medien: die Zeitung (newspaper), die Zeitschrift (magazine), das Fernsehen (television), das Radio (radio), das Internet (internet), die sozialen Medien (social media), die App (app), die Webseite (website).

Im Alltag: 'Ich lese morgens die Nachrichten online' (I read the news online in the morning). 'Hast du die E-Mail bekommen?' (Did you get the email?). 'Ich habe den Film auf Netflix gesehen' (I watched the movie on Netflix).

Meinungen äußern: 'Ich finde, dass...' (I think that...), 'Meiner Meinung nach...' (In my opinion...), 'Ich glaube, dass...' (I believe that...). 'Ich finde, dass soziale Medien manchmal stressig sind'. 'Meiner Meinung nach ist die Zeitung zuverlässiger als Instagram'.

Nebensätze mit 'dass' (that): Das Verb geht ans Ende! 'Ich glaube, dass das Internet wichtig ist'. 'Sie sagt, dass sie keine Zeit hat'. 'Wir wissen, dass die Prüfung schwer ist'.

Höfliche Bitten: 'Könnten Sie mir bitte die Adresse schicken?' (Could you please send me the address?). Konjunktiv II: 'Ich würde gern...' (I would like to), 'Könntest du...?' (Could you...?)."""
],
"B1": [
"""Lernen Sie, über Zukunftspläne und Wünsche zu sprechen.

Zukunft ausdrücken: 'Ich werde nächstes Jahr nach Deutschland ziehen' (I will move to Germany next year). Futur I: werden + Infinitiv. ich werde, du wirst, er/sie wird, wir werden. 'Was wirst du nach dem Studium machen?' — 'Ich werde wahrscheinlich einen Master machen'.

Berufliche Ziele: 'Ich möchte mich beruflich weiterentwickeln' (I want to develop professionally). 'In fünf Jahren möchte ich mein eigenes Unternehmen gründen' (In 5 years I want to start my own company). 'Ich plane, einen MBA zu machen' (I plan to do an MBA).

Konjunktiv II (Wünsche): 'Wenn ich mehr Zeit hätte, würde ich eine Weltreise machen' (If I had more time, I would travel the world). 'Ich wünschte, ich könnte besser Deutsch sprechen'. Irreale Bedingungen: 'Wenn ich reich wäre, würde ich ein Haus am See kaufen'.

Infinitiv mit 'zu': 'Ich habe vor, Deutsch zu lernen' (I intend to learn German). 'Es ist wichtig, Fremdsprachen zu sprechen'. 'Ich versuche, jeden Tag zu üben'. Nach Modalverben kein 'zu': 'Ich will Deutsch lernen' (kein 'zu').

Lebensplanung: heiraten (to marry), Kinder bekommen (to have children), in Rente gehen (to retire). 'Wir planen, nächstes Jahr zu heiraten'.""",

"""Diskutieren Sie über gesellschaftliche Themen und das Zusammenleben.

Gesellschaft: die Gleichberechtigung (equality), die Integration (integration), die Vielfalt (diversity), das Ehrenamt (volunteering), die Nachbarschaft (neighbourhood). 'Deutschland ist ein multikulturelles Land' (Germany is a multicultural country).

Integration: 'In Deutschland leben Menschen aus über 200 Nationen'. 'Der Integrationskurs umfasst einen Sprach- und einen Orientierungskurs'. 'Integration bedeutet, die Sprache zu lernen und die Gesellschaft mitzugestalten'.

Generationenkonflikte: 'Die ältere Generation findet, dass die Jugend zu viel am Handy ist'. 'Junge Leute meinen, dass die Älteren die Digitalisierung nicht verstehen'. 'Man muss voneinander lernen'.

Relativsätze: 'Die Menschen, die in der Stadt leben, haben mehr Angebote'. 'Das ist der Verein, der Flüchtlingen hilft'. 'Die Nachbarin, mit der ich mich unterhalte, kommt aus Syrien'. Das Relativpronomen richtet sich nach Genus und Kasus.

Diskutieren: 'Einerseits... andererseits...' (On one hand... on the other...). 'Ich stimme zu, dass...' (I agree that...). 'Das sehe ich anders' (I see it differently). 'Welche Lösung schlagen Sie vor?' (What solution do you suggest?).""",

"""Sprechen Sie über Natur, Umwelt und Nachhaltigkeit.

Umweltprobleme: der Klimawandel (climate change), die Erderwärmung (global warming), die Luftverschmutzung (air pollution), das Artensterben (species extinction), der Plastikmüll (plastic waste). 'Die Durchschnittstemperatur steigt jedes Jahr'.

Lösungen: Müll trennen (to sort waste), recyceln (to recycle), öffentliche Verkehrsmittel benutzen, Energie sparen (to save energy), erneuerbare Energien (renewable energy — Sonne, Wind, Wasser). 'In Deutschland trennt man den Müll in Papier, Plastik, Glas und Restmüll'.

Das Pfandsystem: 'In Deutschland gibt es ein Flaschenpfand. Plastikflaschen kosten 25 Cent Pfand. Man bringt die leeren Flaschen zum Automaten im Supermarkt zurück'.

Passiv: 'In Deutschland wird viel recycelt' (A lot is recycled in Germany). Bildung: werden + Partizip II. 'Plastik wird in der gelben Tonne gesammelt'. 'Neue Bäume werden gepflanzt'. 'Solarenergie wird immer beliebter'.

Natur: der Wald (forest), der See (lake), der Fluss (river), das Meer (sea), der Berg (mountain), die Wiese (meadow). 'Der Schwarzwald ist ein beliebtes Wandergebiet'. 'Die Nordsee und die Ostsee sind in Norddeutschland'.""",

"""Entdecken Sie das kulturelle Leben in den deutschsprachigen Ländern.

Musik: Beethoven, Bach, Mozart (Österreich), Wagner. 'Beethoven wurde in Bonn geboren und lebte in Wien'. Moderne Musik: Rammstein (Industrialrock), Kraftwerk (Elektro-Pioniere), Nena ('99 Luftballons'). 'Die Berliner Philharmoniker sind weltberühmt'.

Literatur: Goethe ('Faust'), Schiller ('Die Räuber'), die Brüder Grimm (Märchen — Aschenputtel, Rotkäppchen, Hänsel und Gretel). 'Die Brüder Grimm haben die berühmtesten Märchen der Welt gesammelt'.

Theater und Kino: 'Das Berliner Ensemble wurde von Bertolt Brecht gegründet'. Deutscher Film: 'Das Leben der Anderen' (Oscar), 'Good Bye, Lenin!', 'Der Untergang'. 'Das deutsche Kino genießt internationalen Ruf'.

Museen: Pergamonmuseum und Museumsinsel (Berlin — UNESCO), Deutsches Museum (München — Technik), Pinakothek (München — Kunst). 'Die Museumsinsel in Berlin gehört zum UNESCO-Weltkulturerbe'.

Präteritum (schriftliche Vergangenheit): war (was), hatte (had), ging (went), kam (came), schrieb (wrote). 'Goethe schrieb Faust'. 'Mozart komponierte über 600 Werke'. Im Schriftdeutschen bevorzugt man das Präteritum.""",

"""Lernen Sie über die politische Geschichte Deutschlands zu sprechen.

Wichtige Daten: 1871 — Gründung des Deutschen Reichs. 1918 — Ende des Ersten Weltkriegs und Ende der Monarchie. 1933-1945 — Nationalsozialismus und Zweiter Weltkrieg. 1949 — Gründung von BRD und DDR. 1961 — Bau der Berliner Mauer. 1989 — Fall der Mauer. 1990 — Wiedervereinigung.

Die Berliner Mauer: 'Die Mauer teilte Berlin von 1961 bis 1989'. 'Am 9. November 1989 wurde die Mauer geöffnet'. 'Die East Side Gallery ist heute ein Denkmal mit Kunstwerken auf der ehemaligen Mauer'.

Politisches System: Der Bundestag (Parlament), der Bundeskanzler (chancellor), der Bundespräsident (president — repräsentative Rolle). '16 Bundesländer bilden die Bundesrepublik Deutschland'. 'Wahlen finden alle vier Jahre statt'.

Konjunktionen: 'Nachdem die Mauer gefallen war, feierte ganz Deutschland' (After the wall fell...). 'Bevor Deutschland wiedervereinigt wurde, gab es zwei deutsche Staaten' (Before Germany was reunited...). Plusquamperfekt: 'Nachdem er den Vertrag unterschrieben hatte, reiste er ab'.""",

"""Lernen Sie, über das Arbeiten im Ausland und internationale Erfahrungen zu sprechen.

Motivation: 'Ich möchte im Ausland arbeiten, um meine Sprachkenntnisse zu verbessern' (to improve my language skills). 'Auslandserfahrung ist gut für den Lebenslauf' (International experience is good for the CV). 'Ich suche neue Herausforderungen' (I'm looking for new challenges).

Bewerbung: der Lebenslauf (CV), das Anschreiben (cover letter), das Vorstellungsgespräch (job interview), die Qualifikation (qualification), die Berufserfahrung (work experience). 'Hiermit bewerbe ich mich um die Stelle als...' (I hereby apply for the position of...).

Arbeitsgenehmigung: 'Als EU-Bürger braucht man keine Arbeitserlaubnis in Deutschland'. 'Nicht-EU-Bürger benötigen ein Visum und eine Arbeitserlaubnis'. 'Die Blaue Karte EU ist für Fachkräfte mit Hochschulabschluss'.

Erfahrungen teilen: 'Als ich in Berlin gearbeitet habe, habe ich viel gelernt' (When I worked in Berlin, I learned a lot). 'Die größte Herausforderung war die Sprache' (The biggest challenge was the language). 'Es hat sich gelohnt' (It was worth it).

Indirekte Rede: 'Er sagte, er arbeite gern in Deutschland' (He said he liked working in Germany). Finalsätze: 'Ich lerne Deutsch, um in Deutschland zu studieren'. 'damit' + Nebensatz: 'Ich lerne Deutsch, damit ich bessere Chancen habe'."""
],
"B2": [
"""Diskutieren Sie über Wissenschaft und Forschung in der deutschsprachigen Welt.

Deutsche Wissenschaftler: Albert Einstein (Relativitätstheorie), Max Planck (Quantenphysik), Robert Koch (Tuberkulose-Bazillus), Werner Heisenberg (Unschärferelation). 'Deutschland hat über 80 Nobelpreisträger'. Die Max-Planck-Gesellschaft und die Fraunhofer-Gesellschaft sind weltweit führende Forschungsinstitutionen.

Universität: 'Deutschland bietet kostenlose Hochschulbildung an vielen öffentlichen Universitäten'. Die Technische Universität München, die Humboldt-Universität zu Berlin und die Universität Heidelberg gehören zu den besten Europas. 'Der Master dauert in der Regel zwei Jahre'.

Forschungsvokabular: die Hypothese (hypothesis), das Experiment (experiment), die Studie (study), das Ergebnis (result), der Beweis (proof), die These (thesis). 'Die Studie zeigt, dass...' 'Die Ergebnisse bestätigen die Hypothese'.

Nominalisierung: 'Die Entwicklung der Technologie schreitet voran' (statt: Die Technologie entwickelt sich). 'Die Erforschung des Weltraums ist teuer'. Partizip I als Adjektiv: 'die wachsende Bevölkerung', 'die steigenden Temperaturen', 'der entscheidende Faktor'.""",

"""Analysieren Sie die Rolle der Medien und ihre Auswirkungen auf die Meinungsbildung.

Deutsche Medienlandschaft: ARD und ZDF (öffentlich-rechtliches Fernsehen — finanziert durch den Rundfunkbeitrag von 18,36€ pro Monat). Private Sender: RTL, ProSieben, Sat.1. Zeitungen: Süddeutsche Zeitung, Frankfurter Allgemeine, Die Zeit, Der Spiegel. 'Die Bild-Zeitung ist die meistgelesene Zeitung Deutschlands'.

Medienkritik: 'Fake News verbreiten sich schneller als seriöse Nachrichten'. 'Man muss Quellen überprüfen, bevor man Informationen teilt'. 'Die Pressefreiheit ist im Grundgesetz garantiert (Artikel 5)'.

Meinungen begründen: 'Es lässt sich nicht leugnen, dass...' (It cannot be denied that...). 'Es steht außer Frage, dass...' (There is no question that...). 'Man darf nicht vergessen, dass...' (One must not forget that...).

Konjunktiv I (indirekte Rede): 'Der Minister sagte, die Regierung sei bereit' (The minister said the government was ready). 'Die Studie zeige, dass...' sei, habe, könne, müsse. 'Laut Experten sei die Lage ernst'. Passiv Perfekt: 'Das Problem ist erkannt worden'. 'Die Maßnahmen sind beschlossen worden'.""",

"""Diskutieren Sie über Wirtschaft und die Auswirkungen der Globalisierung.

Deutsche Wirtschaft: 'Deutschland ist die größte Volkswirtschaft Europas und die viertgrößte der Welt'. Schlüsselbranchen: Automobilindustrie (VW, BMW, Mercedes-Benz, Porsche), Maschinenbau, Chemieindustrie (BASF, Bayer), Technologie (SAP, Siemens). 'Made in Germany' ist weltweit ein Qualitätssiegel.

Der Mittelstand: 'Kleine und mittlere Unternehmen (KMU) bilden das Rückgrat der deutschen Wirtschaft'. 'Familienunternehmen wie Bosch und Henkel existieren seit über 100 Jahren'. 'Die duale Ausbildung (Lehre) kombiniert Theorie und Praxis'.

Globalisierung: Vorteile — internationaler Handel, kultureller Austausch, Technologietransfer. Nachteile — Arbeitsplatzverlagerung, Umweltprobleme, wachsende Ungleichheit. 'Die Globalisierung hat Gewinner und Verlierer'.

Wirtschaftssprache: die Bilanz (balance sheet), der Umsatz (revenue), der Gewinn (profit), die Investition (investment), die Inflation (inflation), die Arbeitslosenquote (unemployment rate).

Konzessivsätze: 'Obwohl die Wirtschaft wächst, steigt die Ungleichheit' (Although the economy grows, inequality rises). 'Trotz des Wirtschaftswachstums gibt es Armut'. Doppelte Verneinung vermeiden: 'nicht unerheblich' = erheblich (considerable).""",

"""Erkunden Sie deutsche Philosophie und Kunstgeschichte.

Philosophen: Immanuel Kant (Kritik der reinen Vernunft — 'Handle so, dass die Maxime deines Willens jederzeit zugleich als Prinzip einer allgemeinen Gesetzgebung gelten könne'). Friedrich Nietzsche ('Gott ist tot', der Übermensch, der Wille zur Macht). Georg Hegel (Dialektik: These, Antithese, Synthese). Karl Marx (Das Kapital, historischer Materialismus).

Kunst: Albrecht Dürer (Renaissance — Meister des Kupferstichs), Caspar David Friedrich (Romantik — 'Der Wanderer über dem Nebelmeer'), der Bauhaus-Stil (Weimar/Dessau — Verbindung von Kunst und Industrie, gegründet 1919 von Walter Gropius). 'Das Bauhaus revolutionierte Design und Architektur weltweit'.

Expressionismus: Die Brücke (Kirchner, Nolde) und Der Blaue Reiter (Kandinsky, Marc, Klee). 'Der Expressionismus drückte innere Gefühle durch verzerrte Formen und kräftige Farben aus'.

Erweitertes Partizip: 'Die von Kant entwickelte Ethik beeinflusst bis heute das philosophische Denken'. 'Das im 20. Jahrhundert gegründete Bauhaus prägt die moderne Architektur'. Subjektive Modalverben: 'Er soll ein Genie gewesen sein' (He is said to have been a genius).""",

"""Diskutieren Sie über Recht und gesellschaftliche Normen in Deutschland.

Das Grundgesetz (1949): 'Die Würde des Menschen ist unantastbar' (Artikel 1). Grundrechte: Meinungsfreiheit, Religionsfreiheit, Pressefreiheit, Versammlungsfreiheit, Gleichheit vor dem Gesetz. 'Das Grundgesetz ist die Verfassung der Bundesrepublik Deutschland'.

Rechtssystem: Zivilrecht (civil law), Strafrecht (criminal law), Verwaltungsrecht (administrative law). 'Jeder hat das Recht auf einen fairen Prozess'. 'In Deutschland gibt es kein Jury-System'.

Gesellschaftliche Themen: 'Die Ehe für alle wurde 2017 in Deutschland eingeführt' (Same-sex marriage was legalized in 2017). 'Cannabis ist seit 2024 teillegalisiert'. 'Sterbehilfe ist ein kontroverses Thema'. 'Datenschutz — Die DSGVO schützt persönliche Daten'.

Argumentation: 'Auf der einen Seite... auf der anderen Seite...' 'Dem ist entgegenzuhalten, dass...' (It must be countered that...). 'Das Argument greift zu kurz' (The argument falls short). 'Es bedarf einer differenzierten Betrachtung' (A nuanced view is needed).

Nomen-Verb-Verbindungen: 'eine Entscheidung treffen' (to make a decision), 'zur Diskussion stehen' (to be up for discussion), 'in Kraft treten' (to come into effect), 'Stellung nehmen zu' (to take a position on).""",

"""Entwickeln Sie interkulturelle Kompetenzen für den deutschsprachigen Raum.

Kulturelle Unterschiede: Pünktlichkeit ist extrem wichtig in Deutschland. 'Fünf Minuten zu spät gilt als unhöflich'. Direkte Kommunikation: 'Deutsche sagen oft direkt ihre Meinung — das ist nicht unhöflich, sondern ehrlich'. Planung: 'In Deutschland plant man Treffen oft Wochen im Voraus'.

Geschäftskultur: 'Man siezt sich im Beruf, bis das Du angeboten wird'. 'Smalltalk ist weniger üblich als in Lateinamerika'. 'Titel sind wichtig: Herr Doktor, Frau Professor'. 'Visitenkarten werden sorgfältig ausgetauscht'.

D-A-CH: Deutschland, Österreich, Schweiz — drei Länder, eine Sprache, viele Unterschiede. Schweizerdeutsch: 'Grüezi' (Hallo), 'Velo' (Fahrrad), 'Natel' (Handy). Österreichisch: 'Servus' (Hallo/Tschüss), 'Erdäpfel' (Kartoffeln), 'Paradeiser' (Tomaten).

Sprachliche Feinheiten: 'Es gibt kein direktes Äquivalent für das deutsche Wort Gemütlichkeit — es beschreibt ein Gefühl von Behaglichkeit und Wärme'. 'Feierabend' (the time after work), 'Wanderlust' (desire to travel).

Erweitertes Attribut: 'Die seit Jahren andauernde Diskussion über die Integration', 'Das von der Regierung verabschiedete Gesetz'. Funktionsverbgefüge: 'in Frage stellen' (to question), 'zum Ausdruck bringen' (to express), 'in Betracht ziehen' (to consider)."""
],
"C1": [
"""Entwickeln Sie akademische Schreibkompetenzen auf Deutsch.

Wissenschaftliches Schreiben: Unpersönlich und objektiv. Statt 'Ich denke, dass...' → 'Es ist anzunehmen, dass...' Statt 'Man kann sagen...' → 'Es lässt sich feststellen, dass...' 'Die vorliegende Arbeit befasst sich mit...' (This paper deals with...).

Gliederung einer Seminararbeit: 1. Einleitung (Fragestellung, These, Methodik), 2. Hauptteil (Argumentation mit Belegen), 3. Schluss (Zusammenfassung, Ausblick). 'Ziel der vorliegenden Untersuchung ist es, ...' 'Im Folgenden wird dargelegt, dass...'

Zitieren: Direktes Zitat: 'Laut Habermas (1981) ist „kommunikatives Handeln" grundlegend'. Indirektes Zitat (Konjunktiv I): 'Habermas argumentiert, die Gesellschaft basiere auf kommunikativem Handeln'. 'Vgl.' (vergleiche = cf.), 'ebd.' (ebenda = ibid.).

Konnektoren: 'Demzufolge...' (consequently), 'Daraus ergibt sich...' (From this it follows), 'Angesichts der Tatsache, dass...' (Given the fact that), 'Unter Berücksichtigung von...' (Taking into account). 'Zusammenfassend lässt sich sagen, dass...' (In summary, it can be said that...).

Nominalisierter Stil: 'Die Durchführung des Experiments' (statt: das Experiment durchführen), 'Die Auswertung der Daten zeigt...' (statt: Wenn man die Daten auswertet, sieht man...).""",

"""Entdecken Sie Meisterwerke der deutschen Literatur.

Goethe (1749-1832): 'Faust' — das wichtigste Werk der deutschen Literatur. Faust schließt einen Pakt mit dem Teufel Mephistopheles. Berühmtes Zitat: 'Zwei Seelen wohnen, ach! in meiner Brust'. 'Die Leiden des jungen Werthers' — Briefroman, löste eine Selbstmordwelle aus ('Werther-Effekt').

Franz Kafka (1883-1924): 'Die Verwandlung' — Gregor Samsa erwacht als Käfer. 'Der Prozess' — Josef K. wird verhaftet, ohne den Grund zu kennen. Kafkas Werk thematisiert Entfremdung, Bürokratie und Machtlosigkeit. Das Adjektiv 'kafkaesk' beschreibt absurde, bedrohliche Situationen.

Thomas Mann (1875-1955): 'Der Zauberberg', 'Buddenbrooks' (Nobelpreis 1929). 'Buddenbrooks' schildert den Verfall einer Lübecker Kaufmannsfamilie über vier Generationen.

Moderne Literatur: Günter Grass ('Die Blechtrommel'), Heinrich Böll ('Die verlorene Ehre der Katharina Blum'), Herta Müller (Nobelpreis 2009), Elfriede Jelinek (Nobelpreis 2004, Österreich).

Konjunktiv II der Vergangenheit: 'Hätte Faust den Pakt nicht geschlossen, wäre er nicht verdammt worden'. Konzessiv: 'So brillant sein Werk auch sein mag, bleibt Kafka ein rätselhafter Autor'.""",

"""Analysieren Sie politische Diskurse und Rhetorik im deutschen Kontext.

Politische Parteien: SPD (sozialdemokratisch), CDU/CSU (konservativ), Grüne (ökologisch), FDP (liberal), Die Linke (sozialistisch), AfD (rechtspopulistisch). 'Die Fünf-Prozent-Hürde verhindert, dass Kleinstparteien in den Bundestag einziehen'.

Wahlsystem: 'Deutschland hat ein Verhältniswahlrecht mit Erst- und Zweitstimme'. 'Die Erststimme wählt den Direktkandidaten, die Zweitstimme die Partei'. 'Koalitionsregierungen sind in Deutschland die Norm'. 'Große Koalition' (CDU+SPD), 'Ampel' (SPD+Grüne+FDP).

EU und Deutschland: 'Deutschland ist Gründungsmitglied der EU'. 'Der Euro wurde 2002 eingeführt'. 'Das Europäische Parlament tagt in Straßburg und Brüssel'. 'Freizügigkeit ermöglicht es EU-Bürgern, in jedem Mitgliedsstaat zu leben und zu arbeiten'.

Rhetorische Mittel: Anapher ('Wir werden kämpfen, wir werden siegen'), rhetorische Frage ('Können wir uns das leisten?'), Euphemismus ('Freisetzung' statt Entlassung), Ironie.

Subjektive Bedeutung der Modalverben: 'Er will das gesagt haben' (He claims to have said that). 'Sie soll die Beste sein' (She is said to be the best). 'Das dürfte stimmen' (That is probably true).""",

"""Vertiefen Sie Ihr Verständnis von Psychologie und Sozialwissenschaften auf Deutsch.

Sigmund Freud (Österreich): Begründer der Psychoanalyse. Das Unbewusste, das Es (id), das Ich (ego), das Über-Ich (superego). Traumdeutung, Verdrängung, Ödipuskomplex. 'Freud hat unser Verständnis der menschlichen Psyche revolutioniert'.

Soziologische Konzepte: Gemeinschaft vs. Gesellschaft (Ferdinand Tönnies), die Frankfurter Schule (Adorno, Horkheimer — Kritische Theorie), Max Weber (Bürokratie, protestantische Ethik). 'Weber unterschied zwischen Zweckrationalität und Wertrationalität'.

Fachterminologie: die Wahrnehmung (perception), das Verhalten (behavior), die Motivation (motivation), die Identität (identity), die Sozialisation (socialization), das Vorurteil (prejudice), die Stigmatisierung (stigmatization).

Textwiedergabe: 'Der Autor vertritt die These, dass...' (The author argues that...). 'Im Gegensatz dazu behauptet X, dass...' (In contrast, X claims that...). 'Diese Ansicht wird durch folgende Argumente gestützt...' (This view is supported by the following arguments...).

Appositionen und Einschübe: 'Freud, der Begründer der Psychoanalyse, wurde 1856 in Freiberg geboren'. 'Die Studie — die erste ihrer Art — zeigt überraschende Ergebnisse'.""",

"""Diskutieren Sie über ethische Fragen im Zusammenhang mit Technologie.

Künstliche Intelligenz: 'Kann KI kreativ sein oder ahmt sie nur menschliche Muster nach?' 'Wer trägt die Verantwortung, wenn ein autonomes Fahrzeug einen Unfall verursacht?' 'Die Europäische KI-Verordnung reguliert den Einsatz von KI in der EU'.

Datenschutz: 'Die DSGVO (Datenschutz-Grundverordnung) ist das strengste Datenschutzgesetz der Welt'. 'Das Recht auf Vergessenwerden erlaubt es, persönliche Daten löschen zu lassen'. 'Big Data vs. Privatsphäre — wo liegt die Grenze?'.

Bioethik: 'Gentechnik könnte Krankheiten heilen, birgt aber Risiken der Eugenik'. 'Embryonenforschung ist in Deutschland streng reguliert'. 'Das Embryonenschutzgesetz verbietet die Erzeugung von Embryonen zu Forschungszwecken'.

Arbeit und Automatisierung: 'Bis 2030 könnten Millionen Arbeitsplätze durch Automatisierung wegfallen'. 'Das bedingungslose Grundeinkommen wird als mögliche Lösung diskutiert'.

Komplexe Satzstrukturen: 'Es stellt sich die Frage, inwieweit die technologische Entwicklung mit ethischen Grundsätzen vereinbar ist'. Modalpartikeln: 'Das ist doch klar' (that's obvious), 'Das mag ja sein, aber...' (That may well be, but...). 'Angesichts der rasanten Entwicklung erscheint es dringend geboten, klare Regeln aufzustellen'.""",

"""Perfektionieren Sie Ihren schriftlichen Stil und Ihre Textproduktion.

Textsorten: der Aufsatz (essay), die Erörterung (discussion), der Kommentar (commentary), die Rezension (review), der Bericht (report), die Zusammenfassung (summary). Jede Textsorte hat eigene Konventionen und Register.

Stilmittel: Vergleich ('wie ein Blitz'), Metapher ('Das Schiff des Staates'), Personifikation ('Die Zeit heilt alle Wunden'), Alliteration ('Milch macht müde Männer munter'), Antithese ('Arm und Reich').

Formulierungen für akademische Texte: 'Es sei darauf hingewiesen, dass...' (It should be pointed out that). 'Hieraus lässt sich ableiten, dass...' (From this it can be deduced that). 'Es bleibt festzuhalten, dass...' (It remains to note that).

Kohärenz und Kohäsion: Thematische Progression (Thema-Rhema), Rekurrenz (Wiederholung von Schlüsselbegriffen), Pro-Formen (er, dieser, solche), Konnektoren (folglich, demnach, insofern, indes).

Register: ultra-formal (juristisch/diplomatisch), formal (akademisch), semiformal (Geschäftsbrief), informell (E-Mail an Kollegen), umgangssprachlich (WhatsApp). 'Die Wahl des richtigen Registers ist entscheidend für die Wirkung eines Textes'."""
],
"C2": [
"""Erkunden Sie die Philosophie der Sprache und das Wesen der Bedeutung.

Ludwig Wittgenstein (Österreich): 'Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt' (Tractatus Logico-Philosophicus). Der frühe Wittgenstein sah Sprache als Abbild der Realität. Der späte Wittgenstein (Philosophische Untersuchungen) sprach von 'Sprachspielen' — Bedeutung entsteht durch Gebrauch, nicht durch Abbildung.

Martin Heidegger: 'Die Sprache ist das Haus des Seins'. Für Heidegger erschließt sich das Sein durch die Sprache. Etymologische Reflexion: 'Dasein' = Da-sein = Da (there) + sein (to be) — das In-der-Welt-Sein.

Wilhelm von Humboldt: 'Die Sprache ist kein Werk (Ergon), sondern eine Tätigkeit (Energeia)'. Jede Sprache bietet eine eigene Weltansicht. Die Sapir-Whorf-Hypothese baut auf Humboldts Ideen auf.

Sprechakttheorie: Austin und Searle — Sprache als Handlung. Lokutionärer Akt (was gesagt wird), illokutionärer Akt (was gemeint wird), perlokutionärer Akt (was bewirkt wird). 'Ist es kalt hier?' kann eine Feststellung, eine Bitte oder ein Vorwurf sein.

Hermeneutik: Hans-Georg Gadamer — der 'hermeneutische Zirkel': Um einen Text zu verstehen, muss man das Ganze kennen, aber das Ganze versteht man nur durch die Teile.""",

"""Analysieren Sie zeitgenössische deutschsprachige Literatur und ihre Themen.

W.G. Sebald (1944-2001): 'Austerlitz' — ein Mann sucht nach seiner jüdischen Identität. Sebald vermischt Fiktion, Fotografie und Erinnerung. 'Die Ausgewanderten' thematisiert Exil und Verlust. Sein Stil: lange, mäandernde Sätze ohne Absätze — eine Prosa des Erinnerns.

Herta Müller (geb. 1953, Nobelpreis 2009): Aufgewachsen in der deutschsprachigen Minderheit Rumäniens. 'Atemschaukel' — ein Roman über sowjetische Arbeitslager. 'Mit dem scharfen Auge der Poesie beschreibt Müller die Landschaft der Entrechteten'.

Daniel Kehlmann (geb. 1975): 'Die Vermessung der Welt' — Alexander von Humboldt und Carl Friedrich Gauß als komisches Duo. Der Roman wurde in 40 Sprachen übersetzt. 'Tyll' — ein Schelmenroman im Dreißigjährigen Krieg.

Jenny Erpenbeck (geb. 1967): 'Gehen, ging, gegangen' — ein Professor trifft auf afrikanische Flüchtlinge in Berlin. Das Buch stellt unbequeme Fragen über Empathie und Gleichgültigkeit.

Erzähltechniken: erlebte Rede, Stream of Consciousness, unzuverlässiger Erzähler, Mise en abyme (Erzählung in der Erzählung). 'Der postmoderne Roman hinterfragt die Möglichkeit einer objektiven Wahrheit'.""",

"""Vertiefen Sie Ihre Kenntnisse in Linguistik und Sprachgeschichte des Deutschen.

Vom Althochdeutschen zum Neuhochdeutschen: Althochdeutsch (750-1050): 'Heliand', 'Hildebrandslied'. Mittelhochdeutsch (1050-1350): 'Nibelungenlied', Minnesang (Walther von der Vogelweide). Frühneuhochdeutsch (1350-1650): Luthers Bibelübersetzung standardisierte die Sprache.

Lautverschiebungen: Die zweite germanische Lautverschiebung unterscheidet Hochdeutsch von Niederdeutsch. Englisch 'water' = Deutsch 'Wasser', Englisch 'make' = Deutsch 'machen', Englisch 'that' = Deutsch 'das'. 'Diese Lautverschiebung fand zwischen dem 3. und 8. Jahrhundert statt'.

Soziolinguistik: Code-Switching (Wechsel zwischen Dialekt und Hochdeutsch), Kiezdeutsch ('Ich geh Schule' — Jugendsprache in urbanen Gebieten), gendern ('Studierende' statt 'Studenten', Gendersternchen: 'Lehrer*innen').

Pragmatik: Modalpartikeln sind typisch deutsch und schwer zu übersetzen — doch (indeed/contrary), ja (as you know), mal (softener), eben (just the way it is), halt (well), eigentlich (actually). 'Kommst du doch mit?' 'Das ist ja interessant!' 'Mach mal die Tür zu'.

Sprachtypologie: Deutsch ist eine SOV-Sprache (Subjekt-Objekt-Verb in Nebensätzen). Agglutinierende Komposita: 'Donaudampfschifffahrtsgesellschaftskapitän'. V2-Stellung im Hauptsatz.""",

"""Diskutieren Sie über Wirtschaft und Geopolitik aus deutschsprachiger Perspektive.

Deutschland in Europa: 'Als größte Volkswirtschaft der EU trägt Deutschland besondere Verantwortung'. Die Eurokrise, die Flüchtlingskrise 2015, die COVID-Pandemie und der Ukraine-Krieg haben die EU grundlegend verändert. 'Die Zeitenwende (turning point) markiert eine neue Ära der deutschen Außenpolitik'.

Energiewende: 'Deutschland hat sich von der Atomenergie verabschiedet (letztes AKW abgeschaltet 2023)'. 'Erneuerbare Energien machen über 50% des Stroms aus'. 'Die Abhängigkeit von russischem Gas war eine strategische Schwachstelle'.

Wirtschaftliche Herausforderungen: Fachkräftemangel, demografischer Wandel, Digitalisierung, Deindustrialisierung. 'Die deutsche Automobilindustrie steht vor der größten Transformation ihrer Geschichte' (Elektromobilität).

Geopolitik: NATO, EU-Erweiterung, transatlantische Beziehungen, China als systemischer Rivale. 'Die regelbasierte internationale Ordnung steht unter Druck'. 'Multipolarität ersetzt die unipolare Weltordnung'.

Komplexe Nebensätze: 'Angesichts der Tatsache, dass die geopolitischen Spannungen zunehmen, erscheint es unumgänglich, die Verteidigungsausgaben zu erhöhen, zumal die bisherigen Investitionen bei Weitem nicht ausreichen'. Nominaler Stil, Passiv, Konjunktiv I.""",

"""Setzen Sie sich mit Kulturkritik und ästhetischer Theorie auseinander.

Die Frankfurter Schule: Theodor W. Adorno und Max Horkheimer — 'Dialektik der Aufklärung' (1944). These: Die Aufklärung, die den Menschen befreien sollte, hat neue Formen der Unterdrückung hervorgebracht. 'Kulturindustrie' — Massenkultur als Instrument sozialer Kontrolle.

Adorno: 'Nach Auschwitz ein Gedicht zu schreiben, ist barbarisch'. Kulturkritik als moralische Notwendigkeit. Die 'negative Dialektik' — Denken gegen das System, ohne ein neues System zu errichten.

Walter Benjamin: 'Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit' (1935). Die 'Aura' des Originals geht durch Reproduktion verloren. 'Geschichtsphilosophische Thesen' — 'Der Engel der Geschichte wird vom Sturm des Fortschritts vorangetrieben'.

Ästhetik: das Erhabene (Kant — das Gefühl vor der Übermacht der Natur), das Schöne (Harmonie und Form), das Groteske (Verzerrung und Übertreibung). 'Die ästhetische Erfahrung entzieht sich der begrifflichen Fixierung'.

Abstrakte Argumentation: 'Wenn die Kultur zur Ware wird, verliert sie ihren emanzipatorischen Charakter'. 'Es ist fraglich, ob eine wirklich autonome Kunst unter den Bedingungen des Kapitalismus möglich ist'. Verschachtelter Satzbau als Stilmerkmal.""",

"""Erreichen Sie die höchste Stufe der Sprachbeherrschung im Deutschen.

Sprachmeisterschaft: Auf C2-Niveau verstehen Sie praktisch alles, was Sie lesen oder hören. Sie können Informationen aus verschiedenen Quellen zusammenfassen und dabei Begründungen und Erklärungen in einer zusammenhängenden Darstellung wiedergeben.

Idiomatische Wendungen: 'Da liegt der Hund begraben' (That's the crux of the matter). 'Jemandem reinen Wein einschenken' (to tell someone the plain truth). 'Auf dem Holzweg sein' (to be on the wrong track). 'Den Nagel auf den Kopf treffen' (to hit the nail on the head). 'Etwas auf die lange Bank schieben' (to procrastinate).

Stilistische Variationen: Parataktischer Stil (kurze Hauptsätze — Hemingway-Stil) vs. hypotaktischer Stil (verschachtelte Nebensätze — Thomas Mann). 'Der Mensch ist frei geboren, und überall liegt er in Ketten' (Rousseau, dt. Übers.).

Register-Perfektion: Amtsdeutsch ('Hiermit wird Ihnen mitgeteilt, dass Ihr Antrag stattgegeben wurde'), Wissenschaftsdeutsch ('Die Ergebnisse legen nahe, dass...'), Journalistisch ('Wie aus gut informierten Kreisen verlautet...'), Umgangssprache ('Ey, das ist echt krass!').

Sprichwörter: 'Übung macht den Meister' (Practice makes perfect). 'Wer den Pfennig nicht ehrt, ist des Talers nicht wert' (Look after the pennies...). 'Morgenstund hat Gold im Mund' (The early bird catches the worm). 'Aller Anfang ist schwer' (Every beginning is hard)."""
]
}

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = 0
    for level, contents in DE_RICH.items():
        course = await db.courses.find_one({"language": "german", "level": level})
        if not course: continue
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for i, content in enumerate(contents):
            if i < len(lessons):
                await db.lessons.update_one({"_id": lessons[i]["_id"]}, {"$set": {"content": content}})
                total += 1
        print(f"Enriched german-{level}: {min(len(contents), len(lessons))} lessons")
    print(f"\nTotal: {total}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

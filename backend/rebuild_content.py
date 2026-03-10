"""
Script para crear contenido correctamente por idioma y nivel.
Elimina todo y recrea desde cero con contenido apropiado.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

# ============== CONTENIDO EN ESPAÑOL ==============
SPANISH_CONTENT = {
    "A1": {
        "lessons": [
            {
                "title": "Saludos y Presentaciones",
                "content": """## Saludos Básicos
Los saludos son fundamentales para iniciar cualquier conversación.

### Saludos formales:
- Buenos días (mañana)
- Buenas tardes (tarde)
- Buenas noches (noche)

### Saludos informales:
- ¡Hola!
- ¿Qué tal?
- ¿Cómo estás?

## Presentaciones
- Me llamo [nombre]
- Soy [nombre]
- Mucho gusto / Encantado(a)

### Ejemplo de diálogo:
A: ¡Hola! Me llamo María. ¿Y tú?
B: Hola María, soy Juan. Mucho gusto.
A: Encantada. ¿De dónde eres?
B: Soy de México.""",
                "vocabulary": [
                    {"term": "Hola", "definition": "Saludo informal", "example": "¡Hola! ¿Cómo estás?"},
                    {"term": "Buenos días", "definition": "Saludo formal de la mañana", "example": "Buenos días, señor García."},
                    {"term": "Me llamo", "definition": "Mi nombre es", "example": "Me llamo Ana."},
                    {"term": "Mucho gusto", "definition": "Expresión al conocer a alguien", "example": "Mucho gusto en conocerte."},
                    {"term": "¿Cómo estás?", "definition": "Pregunta por el estado", "example": "Hola, ¿cómo estás?"},
                    {"term": "¿De dónde eres?", "definition": "Pregunta por el origen", "example": "¿De dónde eres?"},
                ],
                "grammar_points": ["Verbo SER: soy, eres, es", "Verbo LLAMARSE: me llamo, te llamas", "Artículos: el, la, los, las"]
            },
            {
                "title": "Números y Colores",
                "content": """## Los Números del 1 al 20
1-uno, 2-dos, 3-tres, 4-cuatro, 5-cinco, 6-seis, 7-siete, 8-ocho, 9-nueve, 10-diez
11-once, 12-doce, 13-trece, 14-catorce, 15-quince, 16-dieciséis, 17-diecisiete, 18-dieciocho, 19-diecinueve, 20-veinte

## Los Colores
Rojo, Azul, Verde, Amarillo, Naranja, Morado, Rosa, Marrón, Negro, Blanco, Gris

### Ejemplos:
- El coche es rojo.
- La casa es blanca.
- Tengo tres libros azules.""",
                "vocabulary": [
                    {"term": "Rojo", "definition": "Color rojo", "example": "La manzana es roja."},
                    {"term": "Azul", "definition": "Color azul", "example": "El cielo es azul."},
                    {"term": "Verde", "definition": "Color verde", "example": "La hierba es verde."},
                    {"term": "Uno", "definition": "Número 1", "example": "Tengo un hermano."},
                    {"term": "Diez", "definition": "Número 10", "example": "Son las diez."},
                ],
                "grammar_points": ["Concordancia de género: rojo/roja", "Concordancia de número: azul/azules", "Números cardinales"]
            },
            {
                "title": "La Familia",
                "content": """## Miembros de la Familia

### Familia Nuclear:
- Padre / Papá
- Madre / Mamá
- Hijo / Hija
- Hermano / Hermana

### Familia Extendida:
- Abuelo / Abuela
- Tío / Tía
- Primo / Prima

### Ejemplo:
"Mi familia es grande. Tengo dos hermanos. Mis padres se llaman Carlos y María." """,
                "vocabulary": [
                    {"term": "Padre", "definition": "Papá", "example": "Mi padre trabaja mucho."},
                    {"term": "Madre", "definition": "Mamá", "example": "Mi madre cocina bien."},
                    {"term": "Hermano", "definition": "Hermano varón", "example": "Tengo un hermano mayor."},
                    {"term": "Abuelo", "definition": "Padre de tu padre/madre", "example": "Mi abuelo tiene 80 años."},
                ],
                "grammar_points": ["Posesivos: mi, tu, su", "Verbo TENER: tengo, tienes, tiene", "Plural: hermano → hermanos"]
            }
        ]
    },
    "A2": {
        "lessons": [
            {
                "title": "Ir de Compras",
                "content": """## En la Tienda

### Frases útiles:
- ¿Cuánto cuesta esto?
- ¿Tiene esto en otro color?
- Me lo llevo
- ¿Puedo pagar con tarjeta?

### Vocabulario de ropa:
Camisa, Pantalón, Vestido, Falda, Zapatos, Chaqueta

### Diálogo:
Cliente: ¿Cuánto cuesta esta camisa?
Vendedor: Cuesta 25 euros.
Cliente: Me la llevo.""",
                "vocabulary": [
                    {"term": "¿Cuánto cuesta?", "definition": "Pregunta por el precio", "example": "¿Cuánto cuesta este libro?"},
                    {"term": "Barato", "definition": "De bajo precio", "example": "Este es muy barato."},
                    {"term": "Caro", "definition": "De alto precio", "example": "Es demasiado caro."},
                    {"term": "Talla", "definition": "Tamaño de ropa", "example": "¿Qué talla usas?"},
                ],
                "grammar_points": ["Verbo COSTAR: cuesta, cuestan", "Pronombres: lo, la, los, las", "Comparativos: más caro que"]
            },
            {
                "title": "Rutina Diaria",
                "content": """## Mi Día Típico

### Verbos reflexivos:
- Despertarse, Levantarse, Ducharse, Vestirse, Acostarse

### Expresiones de tiempo:
- Por la mañana, Por la tarde, Por la noche
- Temprano, Tarde

### Ejemplo:
"Me despierto a las 7. Me levanto y me ducho. Desayuno a las 7:30. Trabajo de 9 a 5." """,
                "vocabulary": [
                    {"term": "Despertarse", "definition": "Dejar de dormir", "example": "Me despierto a las 6."},
                    {"term": "Levantarse", "definition": "Salir de la cama", "example": "Me levanto temprano."},
                    {"term": "Desayunar", "definition": "Comer por la mañana", "example": "Desayuno café."},
                    {"term": "Acostarse", "definition": "Ir a la cama", "example": "Me acuesto a las 11."},
                ],
                "grammar_points": ["Verbos reflexivos: me levanto", "La hora: Son las dos", "Preposiciones: a las, de... a..."]
            },
            {
                "title": "El Clima",
                "content": """## El Tiempo

### Expresiones:
- Hace sol / Hace calor / Hace frío / Hace viento
- Llueve / Nieva / Está nublado

### Las Estaciones:
Primavera, Verano, Otoño, Invierno

### Diálogo:
A: ¿Qué tiempo hace hoy?
B: Hace sol pero un poco de viento.""",
                "vocabulary": [
                    {"term": "Hace sol", "definition": "Hay sol", "example": "Hoy hace mucho sol."},
                    {"term": "Hace frío", "definition": "La temperatura es baja", "example": "En invierno hace frío."},
                    {"term": "Llueve", "definition": "Cae agua del cielo", "example": "Llueve mucho en abril."},
                    {"term": "Verano", "definition": "Estación calurosa", "example": "En verano hace calor."},
                ],
                "grammar_points": ["Verbo HACER para clima", "Verbos impersonales: llueve", "Futuro: va a llover"]
            }
        ]
    },
    "B1": {
        "lessons": [
            {
                "title": "Expresar Opiniones",
                "content": """## Cómo dar tu opinión

### Frases para opinar:
- Creo que... / Pienso que...
- En mi opinión...
- Me parece que...

### Para estar de acuerdo:
- Estoy de acuerdo / Tienes razón

### Para estar en desacuerdo:
- No estoy de acuerdo / No lo veo así""",
                "vocabulary": [
                    {"term": "Creo que", "definition": "Expresar opinión", "example": "Creo que es buena idea."},
                    {"term": "Estoy de acuerdo", "definition": "Concordar", "example": "Estoy de acuerdo contigo."},
                    {"term": "Sin embargo", "definition": "Pero", "example": "Me gusta, sin embargo es caro."},
                    {"term": "Aunque", "definition": "A pesar de que", "example": "Aunque llueve, salgo."},
                ],
                "grammar_points": ["Subjuntivo con opinión", "Conectores: pero, sin embargo", "Conectores: además, también"]
            },
            {
                "title": "Viajes y Turismo",
                "content": """## Planificar un Viaje

### En el aeropuerto:
- Facturar equipaje
- Puerta de embarque
- Tarjeta de embarque

### En el hotel:
- Reservar habitación
- Check-in / Check-out
- ¿Está incluido el desayuno?""",
                "vocabulary": [
                    {"term": "Reservar", "definition": "Apartar con anticipación", "example": "Quiero reservar una habitación."},
                    {"term": "Vuelo", "definition": "Viaje en avión", "example": "Mi vuelo sale a las 10."},
                    {"term": "Equipaje", "definition": "Maletas", "example": "Llevo poco equipaje."},
                    {"term": "Pasaporte", "definition": "Documento de viaje", "example": "Necesitas tu pasaporte."},
                ],
                "grammar_points": ["Condicional: Quisiera, Me gustaría", "Futuro: viajaré", "Condicional: Si tengo dinero..."]
            },
            {
                "title": "Salud y Bienestar",
                "content": """## En el Médico

### Partes del cuerpo:
Cabeza, Ojos, Nariz, Boca, Brazos, Piernas, Espalda

### Síntomas:
- Me duele la cabeza
- Tengo fiebre / Estoy resfriado
- Tengo tos

### En la farmacia:
- Necesito algo para...
- ¿Necesito receta?""",
                "vocabulary": [
                    {"term": "Me duele", "definition": "Sentir dolor", "example": "Me duele la espalda."},
                    {"term": "Fiebre", "definition": "Temperatura alta", "example": "Tengo 38 de fiebre."},
                    {"term": "Resfriado", "definition": "Enfermedad común", "example": "Estoy resfriado."},
                    {"term": "Receta", "definition": "Orden del médico", "example": "Necesito una receta."},
                ],
                "grammar_points": ["Verbo DOLER: me duele", "Estar + participio", "Tener + sustantivo"]
            }
        ]
    },
    "B2": {
        "lessons": [
            {"title": "El Mundo Laboral", "content": "## Vocabulario Profesional\n\nBuscar trabajo, CV, Entrevista, Jefe, Reunión, Sueldo, Vacaciones", "vocabulary": [{"term": "Solicitar", "definition": "Pedir formalmente", "example": "Voy a solicitar el puesto."}], "grammar_points": ["Voz pasiva", "Perífrasis verbales"]},
            {"title": "Actualidad y Noticias", "content": "## Medios de Comunicación\n\nPeriódico, Revista, Televisión, Radio, Redes sociales, Titular, Artículo", "vocabulary": [{"term": "Noticia", "definition": "Información nueva", "example": "Es una noticia importante."}], "grammar_points": ["Estilo indirecto", "Conectores causales"]},
            {"title": "Cultura y Tradiciones", "content": "## Festividades\n\nNavidad, Semana Santa, Día de los Muertos, Carnaval, Costumbres, Tradiciones", "vocabulary": [{"term": "Costumbre", "definition": "Hábito tradicional", "example": "Es una costumbre familiar."}], "grammar_points": ["Imperfecto descriptivo", "Se impersonal"]}
        ]
    },
    "C1": {
        "lessons": [
            {"title": "Argumentación Avanzada", "content": "## Técnicas de Argumentación\n\nConectores: Además, Asimismo, Sin embargo, No obstante, En conclusión", "vocabulary": [{"term": "Cabe destacar", "definition": "Es importante notar", "example": "Cabe destacar su importancia."}], "grammar_points": ["Subjuntivo concesivo", "Nominalizaciones"]},
            {"title": "Lenguaje Académico", "content": "## Escritura Académica\n\nResumen, Introducción, Metodología, Conclusiones, Bibliografía, Citar fuentes", "vocabulary": [{"term": "Hipótesis", "definition": "Suposición inicial", "example": "La hipótesis fue confirmada."}], "grammar_points": ["Voz pasiva académica", "Impersonal con SE"]},
            {"title": "Matices Culturales", "content": "## Expresiones Idiomáticas\n\nEstar en las nubes, Costar un ojo de la cara, Ser pan comido, Meter la pata", "vocabulary": [{"term": "Modismo", "definition": "Expresión idiomática", "example": "Es un modismo muy usado."}], "grammar_points": ["Diminutivos afectivos", "Diferencias ser/estar"]}
        ]
    },
    "C2": {
        "lessons": [
            {"title": "Registro Literario", "content": "## Análisis Literario\n\nMetáfora, Símil, Hipérbole, Personificación, Novela, Poesía, Teatro", "vocabulary": [{"term": "Prosa", "definition": "Texto no versificado", "example": "Escribe en prosa poética."}], "grammar_points": ["Pretérito anterior", "Futuro de conjetura"]},
            {"title": "Dialectos y Variantes", "content": "## Variación del Español\n\nEspañol peninsular, Español latinoamericano, Seseo, Voseo, Registros lingüísticos", "vocabulary": [{"term": "Dialecto", "definition": "Variedad regional", "example": "Cada región tiene su dialecto."}], "grammar_points": ["Variación pronominal", "Diferencias verbales"]},
            {"title": "Comunicación Profesional", "content": "## Comunicación de Alto Nivel\n\nPresentaciones, Negociación, Informes ejecutivos, Correspondencia formal", "vocabulary": [{"term": "Consenso", "definition": "Acuerdo general", "example": "Llegamos a un consenso."}], "grammar_points": ["Condicional de cortesía", "Estructuras formales"]}
        ]
    }
}

# ============== CONTENIDO EN INGLÉS ==============
ENGLISH_CONTENT = {
    "A1": {
        "lessons": [
            {
                "title": "Greetings and Introductions",
                "content": """## Basic Greetings
Greetings are essential for starting any conversation.

### Formal greetings:
- Good morning
- Good afternoon
- Good evening

### Informal greetings:
- Hi! / Hello!
- How are you?
- What's up?

## Introductions
- My name is [name]
- I'm [name]
- Nice to meet you

### Example dialogue:
A: Hi! My name is Mary. And you?
B: Hello Mary, I'm John. Nice to meet you.
A: Nice to meet you too. Where are you from?
B: I'm from the United States.""",
                "vocabulary": [
                    {"term": "Hello", "definition": "Common greeting", "example": "Hello! How are you?"},
                    {"term": "Good morning", "definition": "Morning greeting", "example": "Good morning, Mr. Smith."},
                    {"term": "My name is", "definition": "Introducing yourself", "example": "My name is Sarah."},
                    {"term": "Nice to meet you", "definition": "Polite expression when meeting someone", "example": "Nice to meet you!"},
                    {"term": "How are you?", "definition": "Asking about someone's wellbeing", "example": "Hi, how are you?"},
                    {"term": "Where are you from?", "definition": "Asking about origin", "example": "Where are you from?"},
                ],
                "grammar_points": ["Verb TO BE: I am, you are, he/she is", "Subject pronouns: I, you, he, she", "Articles: a, an, the"]
            },
            {
                "title": "Numbers and Colors",
                "content": """## Numbers 1 to 20
1-one, 2-two, 3-three, 4-four, 5-five, 6-six, 7-seven, 8-eight, 9-nine, 10-ten
11-eleven, 12-twelve, 13-thirteen, 14-fourteen, 15-fifteen, 16-sixteen, 17-seventeen, 18-eighteen, 19-nineteen, 20-twenty

## Colors
Red, Blue, Green, Yellow, Orange, Purple, Pink, Brown, Black, White, Gray

### Examples:
- The car is red.
- The house is white.
- I have three blue books.""",
                "vocabulary": [
                    {"term": "Red", "definition": "Color of fire", "example": "The apple is red."},
                    {"term": "Blue", "definition": "Color of the sky", "example": "The sky is blue."},
                    {"term": "Green", "definition": "Color of grass", "example": "The grass is green."},
                    {"term": "One", "definition": "Number 1", "example": "I have one brother."},
                    {"term": "Ten", "definition": "Number 10", "example": "It's ten o'clock."},
                ],
                "grammar_points": ["Adjective placement: before nouns", "Plural nouns: book → books", "Cardinal numbers"]
            },
            {
                "title": "The Family",
                "content": """## Family Members

### Immediate Family:
- Father / Dad
- Mother / Mom
- Son / Daughter
- Brother / Sister

### Extended Family:
- Grandfather / Grandmother
- Uncle / Aunt
- Cousin

### Example:
"My family is big. I have two brothers. My parents are called Carlos and Maria." """,
                "vocabulary": [
                    {"term": "Father", "definition": "Male parent", "example": "My father works a lot."},
                    {"term": "Mother", "definition": "Female parent", "example": "My mother cooks well."},
                    {"term": "Brother", "definition": "Male sibling", "example": "I have an older brother."},
                    {"term": "Grandfather", "definition": "Father's or mother's father", "example": "My grandfather is 80 years old."},
                ],
                "grammar_points": ["Possessive adjectives: my, your, his/her", "Verb HAVE: I have, you have", "Plural nouns"]
            }
        ]
    },
    "A2": {
        "lessons": [
            {
                "title": "Going Shopping",
                "content": """## At the Store

### Useful phrases:
- How much does this cost?
- Do you have this in another color?
- I'll take it
- Can I pay by card?

### Clothing vocabulary:
Shirt, Pants, Dress, Skirt, Shoes, Jacket

### Dialogue:
Customer: How much does this shirt cost?
Salesperson: It costs 25 dollars.
Customer: I'll take it.""",
                "vocabulary": [
                    {"term": "How much?", "definition": "Asking about price", "example": "How much does this book cost?"},
                    {"term": "Cheap", "definition": "Low price", "example": "This is very cheap."},
                    {"term": "Expensive", "definition": "High price", "example": "It's too expensive."},
                    {"term": "Size", "definition": "Clothing measurement", "example": "What size do you wear?"},
                ],
                "grammar_points": ["Question words: How much, How many", "Object pronouns: it, them", "Comparatives: cheaper than"]
            },
            {
                "title": "Daily Routine",
                "content": """## My Typical Day

### Daily actions:
- Wake up, Get up, Take a shower, Get dressed, Go to bed

### Time expressions:
- In the morning, In the afternoon, At night
- Early, Late

### Example:
"I wake up at 7. I get up and take a shower. I have breakfast at 7:30. I work from 9 to 5." """,
                "vocabulary": [
                    {"term": "Wake up", "definition": "Stop sleeping", "example": "I wake up at 6."},
                    {"term": "Get up", "definition": "Get out of bed", "example": "I get up early."},
                    {"term": "Have breakfast", "definition": "Eat morning meal", "example": "I have breakfast at 7."},
                    {"term": "Go to bed", "definition": "Go to sleep", "example": "I go to bed at 11."},
                ],
                "grammar_points": ["Present simple for routines", "Time expressions: at, in, on", "Adverbs of frequency"]
            },
            {
                "title": "The Weather",
                "content": """## Weather

### Expressions:
- It's sunny / It's hot / It's cold / It's windy
- It's raining / It's snowing / It's cloudy

### Seasons:
Spring, Summer, Fall/Autumn, Winter

### Dialogue:
A: What's the weather like today?
B: It's sunny but a bit windy.""",
                "vocabulary": [
                    {"term": "Sunny", "definition": "With sun", "example": "It's very sunny today."},
                    {"term": "Cold", "definition": "Low temperature", "example": "It's cold in winter."},
                    {"term": "Raining", "definition": "Water falling from sky", "example": "It's raining a lot."},
                    {"term": "Summer", "definition": "Hot season", "example": "It's hot in summer."},
                ],
                "grammar_points": ["It's + adjective for weather", "Present continuous for current weather", "Going to for predictions"]
            }
        ]
    },
    "B1": {
        "lessons": [
            {"title": "Expressing Opinions", "content": "## How to Give Your Opinion\n\nI think that... / I believe that... / In my opinion... / It seems to me that...\n\nAgreeing: I agree / You're right\nDisagreeing: I don't agree / I see it differently", "vocabulary": [{"term": "I think", "definition": "Express opinion", "example": "I think it's a good idea."}], "grammar_points": ["Modal verbs for opinion", "Connectors: however, although"]},
            {"title": "Travel and Tourism", "content": "## Planning a Trip\n\nAt the airport: Check-in, Boarding gate, Boarding pass, Security check\n\nAt the hotel: Book a room, Check-in/out, Is breakfast included?", "vocabulary": [{"term": "Book", "definition": "Reserve in advance", "example": "I want to book a room."}], "grammar_points": ["Would like to + verb", "Future: will travel"]},
            {"title": "Health and Wellness", "content": "## At the Doctor\n\nBody parts: Head, Eyes, Arms, Legs, Back\n\nSymptoms: I have a headache / I have a fever / I have a cold", "vocabulary": [{"term": "Headache", "definition": "Pain in head", "example": "I have a terrible headache."}], "grammar_points": ["Have + illness", "Feel + adjective"]}
        ]
    },
    "B2": {
        "lessons": [
            {"title": "The Workplace", "content": "## Professional Vocabulary\n\nJob search, CV/Resume, Interview, Boss, Meeting, Salary, Vacation", "vocabulary": [{"term": "Apply", "definition": "Request formally", "example": "I'll apply for the position."}], "grammar_points": ["Passive voice", "Phrasal verbs"]},
            {"title": "Current Events", "content": "## Media\n\nNewspaper, Magazine, Television, Radio, Social media, Headline, Article", "vocabulary": [{"term": "News", "definition": "New information", "example": "This is important news."}], "grammar_points": ["Reported speech", "Causal connectors"]},
            {"title": "Culture and Traditions", "content": "## Holidays and Customs\n\nChristmas, Easter, Thanksgiving, Halloween, Customs, Traditions", "vocabulary": [{"term": "Custom", "definition": "Traditional practice", "example": "It's a family custom."}], "grammar_points": ["Past continuous", "Impersonal 'one'"]}
        ]
    },
    "C1": {
        "lessons": [
            {"title": "Advanced Argumentation", "content": "## Argumentation Techniques\n\nConnectors: Furthermore, Moreover, However, Nevertheless, In conclusion", "vocabulary": [{"term": "It should be noted", "definition": "Important to mention", "example": "It should be noted that..."}], "grammar_points": ["Subjunctive mood", "Nominalizations"]},
            {"title": "Academic Language", "content": "## Academic Writing\n\nAbstract, Introduction, Methodology, Conclusions, Bibliography, Citing sources", "vocabulary": [{"term": "Hypothesis", "definition": "Initial assumption", "example": "The hypothesis was confirmed."}], "grammar_points": ["Academic passive", "Impersonal structures"]},
            {"title": "Cultural Nuances", "content": "## Idioms\n\nTo be on cloud nine, To cost an arm and a leg, A piece of cake, To let the cat out of the bag", "vocabulary": [{"term": "Idiom", "definition": "Fixed expression", "example": "It's a common idiom."}], "grammar_points": ["Colloquial expressions", "Register variations"]}
        ]
    },
    "C2": {
        "lessons": [
            {"title": "Literary Register", "content": "## Literary Analysis\n\nMetaphor, Simile, Hyperbole, Personification, Novel, Poetry, Drama", "vocabulary": [{"term": "Prose", "definition": "Non-verse text", "example": "Written in poetic prose."}], "grammar_points": ["Literary past tenses", "Subjunctive in literature"]},
            {"title": "Dialects and Variants", "content": "## English Variation\n\nBritish English, American English, Australian English, Regional accents, Registers", "vocabulary": [{"term": "Dialect", "definition": "Regional variety", "example": "Each region has its dialect."}], "grammar_points": ["Spelling differences", "Vocabulary differences"]},
            {"title": "Professional Communication", "content": "## High-Level Communication\n\nPresentations, Negotiations, Executive reports, Formal correspondence", "vocabulary": [{"term": "Consensus", "definition": "General agreement", "example": "We reached a consensus."}], "grammar_points": ["Diplomatic language", "Formal structures"]}
        ]
    }
}

# ============== CONTENIDO EN PORTUGUÉS ==============
PORTUGUESE_CONTENT = {
    "A1": {
        "lessons": [
            {
                "title": "Saudações e Apresentações",
                "content": """## Saudações Básicas
As saudações são fundamentais para iniciar qualquer conversa.

### Saudações formais:
- Bom dia (manhã)
- Boa tarde (tarde)
- Boa noite (noite)

### Saudações informais:
- Olá! / Oi!
- Tudo bem?
- Como vai?

## Apresentações
- Meu nome é [nome]
- Eu sou [nome]
- Muito prazer / Prazer em conhecê-lo

### Exemplo de diálogo:
A: Olá! Meu nome é Maria. E você?
B: Oi Maria, eu sou João. Muito prazer.
A: Prazer. De onde você é?
B: Eu sou do Brasil.""",
                "vocabulary": [
                    {"term": "Olá", "definition": "Saudação comum", "example": "Olá! Tudo bem?"},
                    {"term": "Bom dia", "definition": "Saudação da manhã", "example": "Bom dia, senhor Silva."},
                    {"term": "Meu nome é", "definition": "Apresentar-se", "example": "Meu nome é Ana."},
                    {"term": "Muito prazer", "definition": "Expressão ao conhecer alguém", "example": "Muito prazer em conhecê-lo!"},
                    {"term": "Tudo bem?", "definition": "Perguntar como está", "example": "Oi, tudo bem?"},
                    {"term": "De onde você é?", "definition": "Perguntar sobre origem", "example": "De onde você é?"},
                ],
                "grammar_points": ["Verbo SER: eu sou, você é, ele/ela é", "Pronomes pessoais: eu, você, ele, ela", "Artigos: o, a, os, as"]
            },
            {
                "title": "Números e Cores",
                "content": """## Números de 1 a 20
1-um, 2-dois, 3-três, 4-quatro, 5-cinco, 6-seis, 7-sete, 8-oito, 9-nove, 10-dez
11-onze, 12-doze, 13-treze, 14-quatorze, 15-quinze, 16-dezesseis, 17-dezessete, 18-dezoito, 19-dezenove, 20-vinte

## Cores
Vermelho, Azul, Verde, Amarelo, Laranja, Roxo, Rosa, Marrom, Preto, Branco, Cinza

### Exemplos:
- O carro é vermelho.
- A casa é branca.
- Eu tenho três livros azuis.""",
                "vocabulary": [
                    {"term": "Vermelho", "definition": "Cor do fogo", "example": "A maçã é vermelha."},
                    {"term": "Azul", "definition": "Cor do céu", "example": "O céu é azul."},
                    {"term": "Verde", "definition": "Cor da grama", "example": "A grama é verde."},
                    {"term": "Um", "definition": "Número 1", "example": "Eu tenho um irmão."},
                    {"term": "Dez", "definition": "Número 10", "example": "São dez horas."},
                ],
                "grammar_points": ["Concordância de gênero: vermelho/vermelha", "Concordância de número: azul/azuis", "Números cardinais"]
            },
            {
                "title": "A Família",
                "content": """## Membros da Família

### Família Nuclear:
- Pai / Papai
- Mãe / Mamãe
- Filho / Filha
- Irmão / Irmã

### Família Extensa:
- Avô / Avó
- Tio / Tia
- Primo / Prima

### Exemplo:
"Minha família é grande. Eu tenho dois irmãos. Meus pais se chamam Carlos e Maria." """,
                "vocabulary": [
                    {"term": "Pai", "definition": "Genitor masculino", "example": "Meu pai trabalha muito."},
                    {"term": "Mãe", "definition": "Genitora feminina", "example": "Minha mãe cozinha bem."},
                    {"term": "Irmão", "definition": "Filho do mesmo pai/mãe", "example": "Eu tenho um irmão mais velho."},
                    {"term": "Avô", "definition": "Pai do pai ou da mãe", "example": "Meu avô tem 80 anos."},
                ],
                "grammar_points": ["Possessivos: meu, seu, dele/dela", "Verbo TER: eu tenho, você tem", "Plural: irmão → irmãos"]
            }
        ]
    },
    "A2": {
        "lessons": [
            {"title": "Fazer Compras", "content": "## Na Loja\n\nFrases úteis: Quanto custa? / Tem em outra cor? / Vou levar / Posso pagar com cartão?\n\nRoupa: Camisa, Calça, Vestido, Saia, Sapatos", "vocabulary": [{"term": "Quanto custa?", "definition": "Perguntar o preço", "example": "Quanto custa este livro?"}], "grammar_points": ["Verbo CUSTAR", "Pronomes objeto"]},
            {"title": "Rotina Diária", "content": "## Meu Dia Típico\n\nVerbos: Acordar, Levantar, Tomar banho, Vestir-se, Dormir\n\nTempo: De manhã, À tarde, À noite", "vocabulary": [{"term": "Acordar", "definition": "Parar de dormir", "example": "Eu acordo às 6."}], "grammar_points": ["Verbos reflexivos", "Horas"]},
            {"title": "O Clima", "content": "## O Tempo\n\nExpressões: Está sol / Está calor / Está frio / Está chovendo / Está nevando\n\nEstações: Primavera, Verão, Outono, Inverno", "vocabulary": [{"term": "Está sol", "definition": "Faz sol", "example": "Hoje está muito sol."}], "grammar_points": ["Estar + clima", "Verbos impessoais"]}
        ]
    },
    "B1": {
        "lessons": [
            {"title": "Expressar Opiniões", "content": "## Como Dar Sua Opinião\n\nEu acho que... / Na minha opinião... / Me parece que...\n\nConcordar: Concordo / Você tem razão\nDiscordar: Não concordo / Não vejo assim", "vocabulary": [{"term": "Eu acho que", "definition": "Expressar opinião", "example": "Eu acho que é uma boa ideia."}], "grammar_points": ["Subjuntivo com opinião", "Conectores"]},
            {"title": "Viagens e Turismo", "content": "## Planejar uma Viagem\n\nNo aeroporto: Check-in, Portão de embarque, Cartão de embarque\n\nNo hotel: Reservar quarto, Check-in/out", "vocabulary": [{"term": "Reservar", "definition": "Guardar com antecedência", "example": "Quero reservar um quarto."}], "grammar_points": ["Condicional", "Futuro"]},
            {"title": "Saúde e Bem-estar", "content": "## No Médico\n\nPartes do corpo: Cabeça, Olhos, Braços, Pernas, Costas\n\nSintomas: Estou com dor de cabeça / Estou com febre / Estou resfriado", "vocabulary": [{"term": "Dor de cabeça", "definition": "Dor na cabeça", "example": "Estou com muita dor de cabeça."}], "grammar_points": ["Estar com + sintoma", "Sentir-se + adjetivo"]}
        ]
    },
    "B2": {
        "lessons": [
            {"title": "O Mundo do Trabalho", "content": "## Vocabulário Profissional\n\nProcurar emprego, Currículo, Entrevista, Chefe, Reunião, Salário, Férias", "vocabulary": [{"term": "Candidatar-se", "definition": "Solicitar formalmente", "example": "Vou me candidatar à vaga."}], "grammar_points": ["Voz passiva", "Verbos compostos"]},
            {"title": "Atualidades", "content": "## Mídia\n\nJornal, Revista, Televisão, Rádio, Redes sociais, Manchete, Artigo", "vocabulary": [{"term": "Notícia", "definition": "Informação nova", "example": "É uma notícia importante."}], "grammar_points": ["Discurso indireto", "Conectores causais"]},
            {"title": "Cultura e Tradições", "content": "## Festas e Costumes\n\nNatal, Páscoa, Carnaval, Festas Juninas, Costumes, Tradições", "vocabulary": [{"term": "Costume", "definition": "Prática tradicional", "example": "É um costume familiar."}], "grammar_points": ["Imperfeito", "Se impessoal"]}
        ]
    },
    "C1": {
        "lessons": [
            {"title": "Argumentação Avançada", "content": "## Técnicas de Argumentação\n\nConectores: Além disso, Ademais, No entanto, Contudo, Em conclusão", "vocabulary": [{"term": "Cabe destacar", "definition": "É importante notar", "example": "Cabe destacar que..."}], "grammar_points": ["Subjuntivo", "Nominalizações"]},
            {"title": "Linguagem Acadêmica", "content": "## Escrita Acadêmica\n\nResumo, Introdução, Metodologia, Conclusões, Bibliografia, Citar fontes", "vocabulary": [{"term": "Hipótese", "definition": "Suposição inicial", "example": "A hipótese foi confirmada."}], "grammar_points": ["Voz passiva acadêmica", "Estruturas impessoais"]},
            {"title": "Nuances Culturais", "content": "## Expressões Idiomáticas\n\nEstar nas nuvens, Custar os olhos da cara, Ser moleza, Meter os pés pelas mãos", "vocabulary": [{"term": "Expressão idiomática", "definition": "Frase com sentido figurado", "example": "É uma expressão idiomática."}], "grammar_points": ["Expressões coloquiais", "Variação de registro"]}
        ]
    },
    "C2": {
        "lessons": [
            {"title": "Registro Literário", "content": "## Análise Literária\n\nMetáfora, Símile, Hipérbole, Personificação, Romance, Poesia, Teatro", "vocabulary": [{"term": "Prosa", "definition": "Texto não versificado", "example": "Escrito em prosa poética."}], "grammar_points": ["Tempos literários", "Subjuntivo na literatura"]},
            {"title": "Dialetos e Variantes", "content": "## Variação do Português\n\nPortuguês brasileiro, Português europeu, Português africano, Sotaques regionais", "vocabulary": [{"term": "Dialeto", "definition": "Variedade regional", "example": "Cada região tem seu dialeto."}], "grammar_points": ["Diferenças pronominais", "Diferenças verbais"]},
            {"title": "Comunicação Profissional", "content": "## Comunicação de Alto Nível\n\nApresentações, Negociação, Relatórios executivos, Correspondência formal", "vocabulary": [{"term": "Consenso", "definition": "Acordo geral", "example": "Chegamos a um consenso."}], "grammar_points": ["Linguagem diplomática", "Estruturas formais"]}
        ]
    }
}

# Definición de cursos
COURSES = {
    "spanish": {
        "A1": {"title": "Español Básico", "desc": "Fundamentos del español: saludos, presentaciones y vocabulario esencial."},
        "A2": {"title": "Español Elemental", "desc": "Conversaciones cotidianas, compras y descripciones básicas."},
        "B1": {"title": "Español Intermedio", "desc": "Expresar opiniones, narrar experiencias y situaciones de viaje."},
        "B2": {"title": "Español Intermedio Alto", "desc": "Textos complejos, debates y expresión fluida."},
        "C1": {"title": "Español Avanzado", "desc": "Uso flexible del idioma en contextos académicos y profesionales."},
        "C2": {"title": "Español Maestría", "desc": "Dominio total del español con matices culturales y literarios."}
    },
    "english": {
        "A1": {"title": "Basic English", "desc": "English foundations: greetings, introductions and essential vocabulary."},
        "A2": {"title": "Elementary English", "desc": "Daily conversations, shopping and basic descriptions."},
        "B1": {"title": "Intermediate English", "desc": "Express opinions, narrate experiences and travel situations."},
        "B2": {"title": "Upper Intermediate English", "desc": "Complex texts, debates and fluent expression."},
        "C1": {"title": "Advanced English", "desc": "Flexible language use in academic and professional contexts."},
        "C2": {"title": "Mastery English", "desc": "Full command of English with cultural and literary nuances."}
    },
    "portuguese": {
        "A1": {"title": "Português Básico", "desc": "Fundamentos do português: saudações, apresentações e vocabulário essencial."},
        "A2": {"title": "Português Elementar", "desc": "Conversas cotidianas, compras e descrições básicas."},
        "B1": {"title": "Português Intermediário", "desc": "Expressar opiniões, narrar experiências e situações de viagem."},
        "B2": {"title": "Português Intermediário Superior", "desc": "Textos complexos, debates e expressão fluente."},
        "C1": {"title": "Português Avançado", "desc": "Uso flexível do idioma em contextos acadêmicos e profissionais."},
        "C2": {"title": "Português Maestria", "desc": "Domínio total do português com nuances culturais e literárias."}
    }
}

LESSON_CONTENT_MAP = {
    "spanish": SPANISH_CONTENT,
    "english": ENGLISH_CONTENT,
    "portuguese": PORTUGUESE_CONTENT
}

async def rebuild_all_content():
    """Eliminar todo y recrear con contenido correcto por idioma."""
    
    # Limpiar todo
    await db.courses.delete_many({})
    await db.lessons.delete_many({})
    
    print("🗑️ Base de datos limpiada")
    
    course_count = 0
    lesson_count = 0
    
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    for language in ["spanish", "english", "portuguese"]:
        content_data = LESSON_CONTENT_MAP[language]
        
        for level in levels:
            # Crear curso
            course_info = COURSES[language][level]
            course_doc = {
                "language": language,
                "level": level,
                "title": course_info["title"],
                "description": course_info["desc"],
                "created_by": "system",
                "created_at": datetime.utcnow()
            }
            result = await db.courses.insert_one(course_doc)
            course_id = str(result.inserted_id)
            course_count += 1
            
            # Crear lecciones para este curso
            if level in content_data:
                lessons = content_data[level]["lessons"]
                for i, lesson_data in enumerate(lessons):
                    lesson_doc = {
                        "course_id": course_id,
                        "title": lesson_data["title"],
                        "content": lesson_data["content"].strip(),
                        "vocabulary": lesson_data.get("vocabulary", []),
                        "grammar_points": lesson_data.get("grammar_points", []),
                        "order": i + 1,
                        "created_at": datetime.utcnow()
                    }
                    await db.lessons.insert_one(lesson_doc)
                    lesson_count += 1
            
            print(f"  ✓ {language.upper()} {level}: {course_info['title']}")
    
    print(f"\n✅ Contenido creado:")
    print(f"   - {course_count} cursos")
    print(f"   - {lesson_count} lecciones")

if __name__ == "__main__":
    asyncio.run(rebuild_all_content())

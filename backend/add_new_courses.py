"""
Script para agregar cursos adicionales sin modificar los existentes.
Nuevos cursos enfocados en práctica y conversación.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'polyglot_academy')]

# ============== NUEVOS CURSOS EN ESPAÑOL ==============
SPANISH_NEW_COURSES = {
    "A1": {
        "title": "Español Práctico A1",
        "desc": "Situaciones cotidianas: en el restaurante, en la calle, de compras.",
        "lessons": [
            {
                "title": "En el Restaurante",
                "content": """## Pedir Comida en un Restaurante

### Vocabulario del Restaurante:
- Mesa, Silla, Menú/Carta
- Camarero/a, Cliente
- Cuenta, Propina

### Frases para Pedir:
- Quisiera una mesa para dos, por favor.
- ¿Puedo ver el menú?
- Quiero / Me gustaría...
- ¿Qué me recomienda?
- La cuenta, por favor.

### Platos Comunes:
- Entrantes: Sopa, Ensalada
- Principales: Carne, Pescado, Pasta
- Postres: Helado, Tarta, Fruta
- Bebidas: Agua, Vino, Café

### Diálogo Ejemplo:
Camarero: Buenas tardes, ¿tienen reserva?
Cliente: No, ¿tiene mesa para dos?
Camarero: Sí, por aquí. Aquí tienen el menú.
Cliente: Gracias. ¿Qué me recomienda?
Camarero: El pescado está muy bueno hoy.
Cliente: Perfecto, el pescado y una ensalada.
Camarero: ¿Para beber?
Cliente: Agua, por favor.""",
                "vocabulary": [
                    {"term": "Menú", "definition": "Lista de platos", "example": "¿Puedo ver el menú?"},
                    {"term": "Cuenta", "definition": "Lo que hay que pagar", "example": "La cuenta, por favor."},
                    {"term": "Propina", "definition": "Dinero extra para el camarero", "example": "Dejé propina."},
                    {"term": "Reserva", "definition": "Mesa apartada", "example": "Tengo una reserva."},
                ],
                "grammar_points": ["Quisiera + infinitivo", "¿Puedo + infinitivo?", "Verbos: querer, pedir"]
            },
            {
                "title": "Pidiendo Direcciones",
                "content": """## Cómo Pedir y Dar Direcciones

### Preguntas Útiles:
- ¿Dónde está...?
- ¿Cómo llego a...?
- ¿Está lejos/cerca?
- ¿Puede repetir, por favor?

### Direcciones:
- Recto / Todo recto
- A la derecha / A la izquierda
- En la esquina
- Al lado de / Enfrente de
- Primera/Segunda calle

### Lugares de la Ciudad:
- Banco, Farmacia, Hospital
- Supermercado, Panadería
- Estación de metro/tren
- Parada de autobús

### Diálogo:
A: Perdone, ¿dónde está la farmacia?
B: Siga todo recto y gire a la derecha.
A: ¿Está lejos?
B: No, está a cinco minutos andando.
A: Muchas gracias.
B: De nada.""",
                "vocabulary": [
                    {"term": "Recto", "definition": "En línea recta", "example": "Siga todo recto."},
                    {"term": "Esquina", "definition": "Donde se cruzan dos calles", "example": "Está en la esquina."},
                    {"term": "Cerca", "definition": "A poca distancia", "example": "Está muy cerca."},
                    {"term": "Girar", "definition": "Cambiar de dirección", "example": "Gire a la derecha."},
                ],
                "grammar_points": ["Imperativo: siga, gire, cruce", "Preposiciones de lugar", "Estar para ubicación"]
            },
            {
                "title": "De Compras",
                "content": """## Comprando en Tiendas

### En la Tienda de Ropa:
- ¿Tienen esto en otra talla?
- ¿Puedo probármelo?
- ¿Dónde están los probadores?
- Me queda grande/pequeño
- Me lo llevo

### En el Supermercado:
- ¿Dónde está/están...?
- ¿Cuánto cuesta esto?
- ¿Tienen bolsas?
- ¿Puedo pagar con tarjeta?

### Tallas y Medidas:
- Pequeño (S), Mediano (M), Grande (L)
- ¿Qué talla usa?
- Número de zapato

### Colores y Materiales:
- ¿Lo tiene en azul/negro/blanco?
- Es de algodón/lana/cuero

### Diálogo:
Cliente: Hola, busco una camiseta.
Vendedor: ¿De qué color?
Cliente: Azul, talla M.
Vendedor: Aquí tiene. El probador está al fondo.
Cliente: Gracias. Me queda bien, me la llevo.""",
                "vocabulary": [
                    {"term": "Probador", "definition": "Lugar para probarse ropa", "example": "El probador está ahí."},
                    {"term": "Talla", "definition": "Tamaño de ropa", "example": "¿Qué talla usa?"},
                    {"term": "Me queda", "definition": "Cómo me sienta la ropa", "example": "Me queda perfecto."},
                    {"term": "Efectivo", "definition": "Dinero en billetes/monedas", "example": "Pago en efectivo."},
                ],
                "grammar_points": ["Pronombres: me lo, me la", "Verbos: quedar, probar", "Demostrativos: este, ese"]
            }
        ]
    },
    "A2": {
        "title": "Conversación A2",
        "desc": "Práctica de conversación: citas, planes y comunicación social.",
        "lessons": [
            {
                "title": "Haciendo Planes",
                "content": """## Quedar con Amigos

### Invitar:
- ¿Quieres ir al cine?
- ¿Te apetece tomar un café?
- ¿Qué tal si vamos a...?
- ¿Tienes planes para el sábado?

### Aceptar:
- ¡Sí, claro! / ¡Vale!
- Me parece bien
- ¡Genial! ¿A qué hora?

### Rechazar:
- Lo siento, no puedo
- Tengo otro compromiso
- ¿Qué tal otro día?

### Acordar Detalles:
- ¿Dónde quedamos?
- ¿A qué hora?
- Te recojo a las...
- Nos vemos en...

### Diálogo:
Ana: ¿Tienes planes para el viernes?
Luis: No, ¿por qué?
Ana: ¿Te apetece ir al cine?
Luis: ¡Sí, genial! ¿Qué película?
Ana: Hay una de acción nueva.
Luis: Perfecto. ¿A qué hora quedamos?
Ana: A las 7 en la puerta del cine.
Luis: Vale, nos vemos allí.""",
                "vocabulary": [
                    {"term": "Quedar", "definition": "Acordar encontrarse", "example": "¿Dónde quedamos?"},
                    {"term": "Apetecer", "definition": "Tener ganas de", "example": "¿Te apetece un café?"},
                    {"term": "Compromiso", "definition": "Obligación previa", "example": "Tengo un compromiso."},
                    {"term": "Recoger", "definition": "Ir a buscar a alguien", "example": "Te recojo a las 8."},
                ],
                "grammar_points": ["Presente para planes futuros", "Ir a + infinitivo", "Verbos reflexivos: quedarse"]
            },
            {
                "title": "Hablando del Pasado",
                "content": """## Contar Experiencias

### Preguntar sobre el Pasado:
- ¿Qué hiciste ayer?
- ¿Cómo fue tu fin de semana?
- ¿Has estado alguna vez en...?
- ¿Cuándo fuiste a...?

### Contar Experiencias:
- Ayer fui a...
- El fin de semana pasado...
- Una vez visité...
- Hace dos años viví en...

### Expresiones de Tiempo:
- Ayer, Anteayer
- La semana pasada
- El mes/año pasado
- Hace + tiempo

### Verbos Irregulares Comunes:
- Ir → fui, fuiste, fue
- Ser → fui, fuiste, fue
- Hacer → hice, hiciste, hizo
- Estar → estuve, estuviste

### Diálogo:
María: ¿Qué hiciste el fin de semana?
Pedro: Fui a la playa con mi familia.
María: ¡Qué bien! ¿Hizo buen tiempo?
Pedro: Sí, hizo sol. ¿Y tú?
María: Yo me quedé en casa, vi una película.""",
                "vocabulary": [
                    {"term": "Ayer", "definition": "El día anterior a hoy", "example": "Ayer fui al cine."},
                    {"term": "Anteayer", "definition": "Dos días antes", "example": "Anteayer llovió."},
                    {"term": "Hace", "definition": "Tiempo transcurrido", "example": "Hace dos años viví aquí."},
                    {"term": "Pasado", "definition": "Anterior, que ya ocurrió", "example": "El mes pasado viajé."},
                ],
                "grammar_points": ["Pretérito indefinido regular", "Pretérito indefinido irregular", "Marcadores temporales"]
            },
            {
                "title": "Describiendo Personas",
                "content": """## Describir Físico y Personalidad

### Aspecto Físico:
- Alto/a, Bajo/a, Mediano/a
- Delgado/a, Gordo/a
- Pelo: rubio, moreno, pelirrojo, canoso
- Ojos: azules, verdes, marrones, negros
- Joven, Mayor

### Personalidad:
- Simpático/a, Antipático/a
- Amable, Educado/a
- Tímido/a, Extrovertido/a
- Inteligente, Gracioso/a
- Trabajador/a, Perezoso/a

### Estructuras:
- Es alto y tiene el pelo negro.
- Tiene los ojos azules.
- Es muy simpática.
- Parece ser amable.

### Diálogo:
A: ¿Cómo es tu nuevo compañero?
B: Es alto, moreno y tiene barba.
A: ¿Y de carácter?
B: Es muy simpático y gracioso.
A: ¿Se parece a alguien famoso?
B: Sí, un poco a Antonio Banderas.""",
                "vocabulary": [
                    {"term": "Alto", "definition": "De gran estatura", "example": "Mi hermano es muy alto."},
                    {"term": "Moreno", "definition": "De pelo o piel oscura", "example": "Es morena de ojos verdes."},
                    {"term": "Simpático", "definition": "Agradable, amable", "example": "Es muy simpático."},
                    {"term": "Gracioso", "definition": "Que hace reír", "example": "Es muy gracioso."},
                ],
                "grammar_points": ["Ser para características permanentes", "Tener para describir partes", "Concordancia de adjetivos"]
            }
        ]
    },
    "B1": {
        "title": "Español para Viajeros B1",
        "desc": "Situaciones de viaje: aeropuertos, hoteles, emergencias.",
        "lessons": [
            {"title": "En el Aeropuerto", "content": "## Viajando en Avión\n\nFrases esenciales: Facturar equipaje, Puerta de embarque, Vuelo retrasado, Control de pasaportes, Aduanas.\n\nDiálogo en check-in, seguridad y embarque.", "vocabulary": [{"term": "Facturar", "definition": "Registrar equipaje", "example": "Voy a facturar mi maleta."}], "grammar_points": ["Futuro simple", "Oraciones condicionales"]},
            {"title": "En el Hotel", "content": "## Alojamiento\n\nReservas, check-in/out, problemas con la habitación, servicios del hotel, quejas y reclamaciones.", "vocabulary": [{"term": "Reserva", "definition": "Habitación apartada", "example": "Tengo una reserva a nombre de..."}], "grammar_points": ["Condicional de cortesía", "Pretérito perfecto"]},
            {"title": "Emergencias", "content": "## Situaciones de Emergencia\n\nEn el médico, en la farmacia, pérdida de documentos, llamar a la policía, accidentes.", "vocabulary": [{"term": "Urgencias", "definition": "Servicio de emergencia", "example": "Lléveme a urgencias."}], "grammar_points": ["Imperativo", "Necesitar + infinitivo"]}
        ]
    },
    "B2": {
        "title": "Español de Negocios B2",
        "desc": "Comunicación profesional: reuniones, negociaciones, presentaciones.",
        "lessons": [
            {"title": "Reuniones de Trabajo", "content": "## Participar en Reuniones\n\nConvocar reuniones, establecer agenda, moderar discusiones, tomar decisiones, redactar actas.", "vocabulary": [{"term": "Orden del día", "definition": "Agenda de la reunión", "example": "El primer punto del orden del día..."}], "grammar_points": ["Subjuntivo para sugerencias", "Conectores formales"]},
            {"title": "Negociaciones", "content": "## Técnicas de Negociación\n\nPropuestas, contraofertass, llegar a acuerdos, ceder y mantener posiciones.", "vocabulary": [{"term": "Contraoferta", "definition": "Propuesta alternativa", "example": "Nuestra contraoferta es..."}], "grammar_points": ["Condicional para propuestas", "Aunque + subjuntivo"]},
            {"title": "Presentaciones", "content": "## Hacer Presentaciones Efectivas\n\nEstructura, recursos visuales, captar atención, responder preguntas.", "vocabulary": [{"term": "Diapositiva", "definition": "Slide de presentación", "example": "En esta diapositiva vemos..."}], "grammar_points": ["Marcadores de discurso", "Voz pasiva"]}
        ]
    },
    "C1": {
        "title": "Español Académico C1",
        "desc": "Habilidades académicas: debates, ensayos, investigación.",
        "lessons": [
            {"title": "Participar en Debates", "content": "## Técnicas de Debate\n\nPresentar argumentos, refutar, defender posiciones, turnos de palabra, conclusiones.", "vocabulary": [{"term": "Refutar", "definition": "Contradecir con argumentos", "example": "Quisiera refutar ese punto."}], "grammar_points": ["Subjuntivo en debates", "Conectores contraargumentativos"]},
            {"title": "Escribir Ensayos", "content": "## El Ensayo Académico\n\nTesis, argumentación, citas, bibliografía, estilo académico formal.", "vocabulary": [{"term": "Tesis", "definition": "Idea principal a defender", "example": "Mi tesis es que..."}], "grammar_points": ["Impersonal académico", "Nominalizaciones"]},
            {"title": "Investigación", "content": "## Metodología de Investigación\n\nHipótesis, metodología, análisis de datos, conclusiones, presentación de resultados.", "vocabulary": [{"term": "Muestra", "definition": "Grupo seleccionado para estudio", "example": "La muestra incluye 100 participantes."}], "grammar_points": ["Voz pasiva de proceso", "Verbos de investigación"]}
        ]
    },
    "C2": {
        "title": "Español Literario C2",
        "desc": "Literatura y cultura: análisis literario, escritura creativa, crítica.",
        "lessons": [
            {"title": "Análisis de Textos", "content": "## Crítica Literaria\n\nContexto histórico, análisis estilístico, interpretación, intertextualidad, valoración crítica.", "vocabulary": [{"term": "Intertextualidad", "definition": "Referencias entre obras", "example": "Hay intertextualidad con Cervantes."}], "grammar_points": ["Estilo indirecto libre", "Registro literario"]},
            {"title": "Escritura Creativa", "content": "## Técnicas Narrativas\n\nVoz narrativa, punto de vista, diálogos, descripciones, ritmo narrativo.", "vocabulary": [{"term": "Narrador", "definition": "Voz que cuenta", "example": "El narrador omnisciente..."}], "grammar_points": ["Tiempos narrativos", "Estilo directo e indirecto"]},
            {"title": "Poesía", "content": "## Análisis y Creación Poética\n\nMétrica, rima, figuras retóricas, movimientos poéticos, creación de poemas.", "vocabulary": [{"term": "Métrica", "definition": "Medida del verso", "example": "Versos de once sílabas."}], "grammar_points": ["Licencias poéticas", "Figuras retóricas"]}
        ]
    }
}

# ============== NUEVOS CURSOS EN INGLÉS ==============
ENGLISH_NEW_COURSES = {
    "A1": {
        "title": "Practical English A1",
        "desc": "Everyday situations: restaurants, directions, shopping.",
        "lessons": [
            {
                "title": "At the Restaurant",
                "content": """## Ordering Food at a Restaurant

### Restaurant Vocabulary:
- Table, Chair, Menu
- Waiter/Waitress, Customer
- Bill, Tip

### Phrases for Ordering:
- I'd like a table for two, please.
- Can I see the menu?
- I'll have... / I'd like...
- What do you recommend?
- The bill, please.

### Common Dishes:
- Starters: Soup, Salad
- Main courses: Meat, Fish, Pasta
- Desserts: Ice cream, Cake, Fruit
- Drinks: Water, Wine, Coffee

### Example Dialogue:
Waiter: Good evening, do you have a reservation?
Customer: No, do you have a table for two?
Waiter: Yes, this way please. Here's the menu.
Customer: Thank you. What do you recommend?
Waiter: The fish is very good today.
Customer: Perfect, I'll have the fish and a salad.
Waiter: Anything to drink?
Customer: Water, please.""",
                "vocabulary": [
                    {"term": "Menu", "definition": "List of dishes", "example": "Can I see the menu?"},
                    {"term": "Bill", "definition": "What you pay", "example": "The bill, please."},
                    {"term": "Tip", "definition": "Extra money for waiter", "example": "I left a tip."},
                    {"term": "Reservation", "definition": "Booked table", "example": "I have a reservation."},
                ],
                "grammar_points": ["I'd like + noun/infinitive", "Can I + infinitive?", "Verbs: want, order"]
            },
            {
                "title": "Asking for Directions",
                "content": """## How to Ask and Give Directions

### Useful Questions:
- Where is...?
- How do I get to...?
- Is it far/near?
- Could you repeat, please?

### Directions:
- Straight / Go straight
- Turn right / Turn left
- On the corner
- Next to / Opposite
- First/Second street

### Places in the City:
- Bank, Pharmacy, Hospital
- Supermarket, Bakery
- Metro/Train station
- Bus stop

### Dialogue:
A: Excuse me, where is the pharmacy?
B: Go straight and turn right.
A: Is it far?
B: No, it's a five-minute walk.
A: Thank you very much.
B: You're welcome.""",
                "vocabulary": [
                    {"term": "Straight", "definition": "In a direct line", "example": "Go straight ahead."},
                    {"term": "Corner", "definition": "Where two streets meet", "example": "It's on the corner."},
                    {"term": "Near", "definition": "Close by", "example": "It's very near."},
                    {"term": "Turn", "definition": "Change direction", "example": "Turn right."},
                ],
                "grammar_points": ["Imperative: go, turn, take", "Prepositions of place", "There is/are"]
            },
            {
                "title": "Shopping",
                "content": """## Buying in Stores

### At the Clothing Store:
- Do you have this in another size?
- Can I try it on?
- Where are the fitting rooms?
- It's too big/small
- I'll take it

### At the Supermarket:
- Where is/are...?
- How much is this?
- Do you have bags?
- Can I pay by card?

### Sizes:
- Small (S), Medium (M), Large (L)
- What size are you?
- Shoe size

### Colors and Materials:
- Do you have it in blue/black/white?
- It's made of cotton/wool/leather""",
                "vocabulary": [
                    {"term": "Fitting room", "definition": "Place to try on clothes", "example": "The fitting room is there."},
                    {"term": "Size", "definition": "Clothing measurement", "example": "What size are you?"},
                    {"term": "It fits", "definition": "How clothes look on you", "example": "It fits perfectly."},
                    {"term": "Cash", "definition": "Money in notes/coins", "example": "I'll pay cash."},
                ],
                "grammar_points": ["Object pronouns: it, them", "Verbs: fit, try on", "Demonstratives: this, that"]
            }
        ]
    },
    "A2": {
        "title": "Conversation A2",
        "desc": "Conversation practice: making plans, past events, descriptions.",
        "lessons": [
            {"title": "Making Plans", "content": "## Meeting Friends\n\nInviting, accepting, declining, arranging details, confirming plans.", "vocabulary": [{"term": "Meet up", "definition": "Get together", "example": "Let's meet up tomorrow."}], "grammar_points": ["Going to for plans", "Present continuous for arrangements"]},
            {"title": "Talking About the Past", "content": "## Sharing Experiences\n\nAsking about past, telling stories, time expressions, irregular verbs.", "vocabulary": [{"term": "Yesterday", "definition": "The day before today", "example": "I went shopping yesterday."}], "grammar_points": ["Past simple regular", "Past simple irregular"]},
            {"title": "Describing People", "content": "## Physical Appearance and Personality\n\nHeight, build, hair, eyes, character traits.", "vocabulary": [{"term": "Tall", "definition": "Of great height", "example": "He's very tall."}], "grammar_points": ["Be for characteristics", "Have for features"]}
        ]
    },
    "B1": {
        "title": "English for Travelers B1",
        "desc": "Travel situations: airports, hotels, emergencies.",
        "lessons": [
            {"title": "At the Airport", "content": "## Traveling by Plane\n\nCheck-in, security, boarding, customs, delays.", "vocabulary": [{"term": "Check-in", "definition": "Register for flight", "example": "Online check-in is available."}], "grammar_points": ["Future simple", "First conditional"]},
            {"title": "At the Hotel", "content": "## Accommodation\n\nReservations, room problems, hotel services, complaints.", "vocabulary": [{"term": "Booking", "definition": "Reservation", "example": "I have a booking under..."}], "grammar_points": ["Would for requests", "Present perfect"]},
            {"title": "Emergencies", "content": "## Emergency Situations\n\nDoctor, pharmacy, lost documents, police, accidents.", "vocabulary": [{"term": "Emergency", "definition": "Urgent situation", "example": "Call emergency services."}], "grammar_points": ["Imperative", "Need to + infinitive"]}
        ]
    },
    "B2": {
        "title": "Business English B2",
        "desc": "Professional communication: meetings, negotiations, presentations.",
        "lessons": [
            {"title": "Business Meetings", "content": "## Participating in Meetings\n\nSetting agenda, moderating, decision-making, minutes.", "vocabulary": [{"term": "Agenda", "definition": "Meeting plan", "example": "The first item on the agenda..."}], "grammar_points": ["Subjunctive for suggestions", "Formal connectors"]},
            {"title": "Negotiations", "content": "## Negotiation Techniques\n\nProposals, counteroffers, reaching agreements, compromising.", "vocabulary": [{"term": "Counteroffer", "definition": "Alternative proposal", "example": "Our counteroffer is..."}], "grammar_points": ["Conditional for proposals", "Although clauses"]},
            {"title": "Presentations", "content": "## Effective Presentations\n\nStructure, visuals, engaging audience, Q&A.", "vocabulary": [{"term": "Slide", "definition": "Presentation page", "example": "On this slide we see..."}], "grammar_points": ["Discourse markers", "Passive voice"]}
        ]
    },
    "C1": {
        "title": "Academic English C1",
        "desc": "Academic skills: debates, essays, research.",
        "lessons": [
            {"title": "Debating", "content": "## Debate Techniques\n\nPresenting arguments, refuting, defending positions, conclusions.", "vocabulary": [{"term": "Refute", "definition": "Argue against", "example": "I'd like to refute that point."}], "grammar_points": ["Subjunctive in debates", "Counter-argumentative connectors"]},
            {"title": "Essay Writing", "content": "## Academic Essays\n\nThesis, argumentation, citations, bibliography, formal style.", "vocabulary": [{"term": "Thesis", "definition": "Main argument", "example": "My thesis is that..."}], "grammar_points": ["Academic impersonal", "Nominalizations"]},
            {"title": "Research", "content": "## Research Methodology\n\nHypothesis, methodology, data analysis, conclusions.", "vocabulary": [{"term": "Sample", "definition": "Selected group for study", "example": "The sample includes 100 participants."}], "grammar_points": ["Process passive", "Research verbs"]}
        ]
    },
    "C2": {
        "title": "Literary English C2",
        "desc": "Literature and culture: literary analysis, creative writing, criticism.",
        "lessons": [
            {"title": "Text Analysis", "content": "## Literary Criticism\n\nHistorical context, stylistic analysis, interpretation, intertextuality.", "vocabulary": [{"term": "Intertextuality", "definition": "References between works", "example": "There's intertextuality with Shakespeare."}], "grammar_points": ["Free indirect speech", "Literary register"]},
            {"title": "Creative Writing", "content": "## Narrative Techniques\n\nNarrative voice, point of view, dialogues, descriptions.", "vocabulary": [{"term": "Narrator", "definition": "Voice telling story", "example": "The omniscient narrator..."}], "grammar_points": ["Narrative tenses", "Direct and indirect speech"]},
            {"title": "Poetry", "content": "## Poetic Analysis and Creation\n\nMeter, rhyme, figures of speech, poetic movements.", "vocabulary": [{"term": "Meter", "definition": "Verse measurement", "example": "Iambic pentameter."}], "grammar_points": ["Poetic license", "Rhetorical figures"]}
        ]
    }
}

# ============== NUEVOS CURSOS EN PORTUGUÉS ==============
PORTUGUESE_NEW_COURSES = {
    "A1": {
        "title": "Português Prático A1",
        "desc": "Situações cotidianas: restaurantes, direções, compras.",
        "lessons": [
            {
                "title": "No Restaurante",
                "content": """## Pedir Comida no Restaurante

### Vocabulário do Restaurante:
- Mesa, Cadeira, Menu/Cardápio
- Garçom/Garçonete, Cliente
- Conta, Gorjeta

### Frases para Pedir:
- Queria uma mesa para dois, por favor.
- Posso ver o cardápio?
- Quero / Gostaria de...
- O que você recomenda?
- A conta, por favor.

### Pratos Comuns:
- Entradas: Sopa, Salada
- Principais: Carne, Peixe, Massa
- Sobremesas: Sorvete, Bolo, Fruta
- Bebidas: Água, Vinho, Café

### Diálogo Exemplo:
Garçom: Boa noite, têm reserva?
Cliente: Não, tem mesa para dois?
Garçom: Sim, por aqui. Aqui está o cardápio.
Cliente: Obrigado. O que você recomenda?
Garçom: O peixe está muito bom hoje.
Cliente: Perfeito, quero o peixe e uma salada.""",
                "vocabulary": [
                    {"term": "Cardápio", "definition": "Lista de pratos", "example": "Posso ver o cardápio?"},
                    {"term": "Conta", "definition": "O que se paga", "example": "A conta, por favor."},
                    {"term": "Gorjeta", "definition": "Dinheiro extra para garçom", "example": "Deixei gorjeta."},
                    {"term": "Reserva", "definition": "Mesa reservada", "example": "Tenho uma reserva."},
                ],
                "grammar_points": ["Queria + infinitivo", "Posso + infinitivo?", "Verbos: querer, pedir"]
            },
            {"title": "Pedindo Direções", "content": "## Como Pedir e Dar Direções\n\nPerguntas úteis, direções, lugares da cidade, diálogos práticos.", "vocabulary": [{"term": "Reto", "definition": "Em linha reta", "example": "Siga em frente."}], "grammar_points": ["Imperativo", "Preposições de lugar"]},
            {"title": "Fazendo Compras", "content": "## Comprando em Lojas\n\nNa loja de roupa, no supermercado, tamanhos, cores e materiais.", "vocabulary": [{"term": "Provador", "definition": "Lugar para provar roupa", "example": "O provador é ali."}], "grammar_points": ["Pronomes objeto", "Demonstrativos"]}
        ]
    },
    "A2": {
        "title": "Conversação A2",
        "desc": "Prática de conversação: planos, passado, descrições.",
        "lessons": [
            {"title": "Fazendo Planos", "content": "## Combinar com Amigos\n\nConvidar, aceitar, recusar, combinar detalhes.", "vocabulary": [{"term": "Combinar", "definition": "Marcar encontro", "example": "Vamos combinar?"}], "grammar_points": ["Ir + infinitivo", "Presente para planos"]},
            {"title": "Falando do Passado", "content": "## Contar Experiências\n\nPerguntar sobre passado, contar histórias, expressões de tempo.", "vocabulary": [{"term": "Ontem", "definition": "O dia anterior", "example": "Ontem fui ao cinema."}], "grammar_points": ["Pretérito perfeito", "Verbos irregulares"]},
            {"title": "Descrevendo Pessoas", "content": "## Aparência e Personalidade\n\nAltura, corpo, cabelo, olhos, traços de caráter.", "vocabulary": [{"term": "Alto", "definition": "De grande estatura", "example": "Ele é muito alto."}], "grammar_points": ["Ser para características", "Ter para descrever"]}
        ]
    },
    "B1": {
        "title": "Português para Viajantes B1",
        "desc": "Situações de viagem: aeroportos, hotéis, emergências.",
        "lessons": [
            {"title": "No Aeroporto", "content": "## Viajando de Avião\n\nCheck-in, segurança, embarque, alfândega, atrasos.", "vocabulary": [{"term": "Embarque", "definition": "Entrar no avião", "example": "O embarque é às 10h."}], "grammar_points": ["Futuro simples", "Condicionais"]},
            {"title": "No Hotel", "content": "## Hospedagem\n\nReservas, problemas no quarto, serviços, reclamações.", "vocabulary": [{"term": "Reserva", "definition": "Quarto reservado", "example": "Tenho uma reserva em nome de..."}], "grammar_points": ["Condicional de cortesia", "Pretérito perfeito composto"]},
            {"title": "Emergências", "content": "## Situações de Emergência\n\nMédico, farmácia, documentos perdidos, polícia.", "vocabulary": [{"term": "Urgência", "definition": "Situação urgente", "example": "Leve-me à urgência."}], "grammar_points": ["Imperativo", "Precisar + infinitivo"]}
        ]
    },
    "B2": {
        "title": "Português de Negócios B2",
        "desc": "Comunicação profissional: reuniões, negociações, apresentações.",
        "lessons": [
            {"title": "Reuniões de Trabalho", "content": "## Participar em Reuniões\n\nMarcar reuniões, agenda, moderar, decisões, atas.", "vocabulary": [{"term": "Pauta", "definition": "Agenda da reunião", "example": "O primeiro ponto da pauta..."}], "grammar_points": ["Conjuntivo para sugestões", "Conectores formais"]},
            {"title": "Negociações", "content": "## Técnicas de Negociação\n\nPropostas, contrapropostas, acordos, concessões.", "vocabulary": [{"term": "Contraproposta", "definition": "Proposta alternativa", "example": "Nossa contraproposta é..."}], "grammar_points": ["Condicional para propostas", "Embora + conjuntivo"]},
            {"title": "Apresentações", "content": "## Fazer Apresentações Eficazes\n\nEstrutura, recursos visuais, captar atenção, perguntas.", "vocabulary": [{"term": "Slide", "definition": "Página de apresentação", "example": "Neste slide vemos..."}], "grammar_points": ["Marcadores de discurso", "Voz passiva"]}
        ]
    },
    "C1": {
        "title": "Português Acadêmico C1",
        "desc": "Habilidades acadêmicas: debates, ensaios, pesquisa.",
        "lessons": [
            {"title": "Participar em Debates", "content": "## Técnicas de Debate\n\nApresentar argumentos, refutar, defender posições.", "vocabulary": [{"term": "Refutar", "definition": "Contradizer com argumentos", "example": "Gostaria de refutar esse ponto."}], "grammar_points": ["Conjuntivo em debates", "Conectores contra-argumentativos"]},
            {"title": "Escrever Ensaios", "content": "## O Ensaio Acadêmico\n\nTese, argumentação, citações, bibliografia.", "vocabulary": [{"term": "Tese", "definition": "Ideia principal", "example": "Minha tese é que..."}], "grammar_points": ["Impessoal acadêmico", "Nominalizações"]},
            {"title": "Pesquisa", "content": "## Metodologia de Pesquisa\n\nHipótese, metodologia, análise de dados, conclusões.", "vocabulary": [{"term": "Amostra", "definition": "Grupo selecionado", "example": "A amostra inclui 100 participantes."}], "grammar_points": ["Voz passiva de processo", "Verbos de pesquisa"]}
        ]
    },
    "C2": {
        "title": "Português Literário C2",
        "desc": "Literatura e cultura: análise literária, escrita criativa, crítica.",
        "lessons": [
            {"title": "Análise de Textos", "content": "## Crítica Literária\n\nContexto histórico, análise estilística, interpretação.", "vocabulary": [{"term": "Intertextualidade", "definition": "Referências entre obras", "example": "Há intertextualidade com Camões."}], "grammar_points": ["Discurso indireto livre", "Registro literário"]},
            {"title": "Escrita Criativa", "content": "## Técnicas Narrativas\n\nVoz narrativa, ponto de vista, diálogos, descrições.", "vocabulary": [{"term": "Narrador", "definition": "Voz que conta", "example": "O narrador onisciente..."}], "grammar_points": ["Tempos narrativos", "Discurso direto e indireto"]},
            {"title": "Poesia", "content": "## Análise e Criação Poética\n\nMétrica, rima, figuras de linguagem, movimentos poéticos.", "vocabulary": [{"term": "Métrica", "definition": "Medida do verso", "example": "Versos de dez sílabas."}], "grammar_points": ["Licenças poéticas", "Figuras de linguagem"]}
        ]
    }
}

async def add_new_courses():
    """Agregar nuevos cursos sin modificar los existentes."""
    
    courses_map = {
        "spanish": SPANISH_NEW_COURSES,
        "english": ENGLISH_NEW_COURSES,
        "portuguese": PORTUGUESE_NEW_COURSES
    }
    
    total_courses = 0
    total_lessons = 0
    
    for language, levels_data in courses_map.items():
        for level, course_data in levels_data.items():
            # Crear nuevo curso
            course_doc = {
                "language": language,
                "level": level,
                "title": course_data["title"],
                "description": course_data["desc"],
                "created_by": "system",
                "created_at": datetime.utcnow()
            }
            result = await db.courses.insert_one(course_doc)
            course_id = str(result.inserted_id)
            total_courses += 1
            
            # Crear lecciones
            for i, lesson_data in enumerate(course_data["lessons"]):
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
                total_lessons += 1
            
            print(f"  ✓ {language.upper()} {level}: {course_data['title']}")
    
    print(f"\n✅ Nuevos cursos agregados: {total_courses}")
    print(f"✅ Nuevas lecciones agregadas: {total_lessons}")

if __name__ == "__main__":
    asyncio.run(add_new_courses())

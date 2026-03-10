"""
Script para actualizar lecciones con vocabulario y contenido real.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

# Contenido detallado por nivel para cada lección
LESSON_CONTENT = {
    "A1": {
        "Saludos y Presentaciones": {
            "content": """
## Saludos Básicos
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
Para presentarte, usa estas estructuras:
- Me llamo [nombre]
- Soy [nombre]
- Mucho gusto / Encantado(a)

### Ejemplo de diálogo:
A: ¡Hola! Me llamo María. ¿Y tú?
B: Hola María, soy Juan. Mucho gusto.
A: Encantada. ¿De dónde eres?
B: Soy de México. ¿Y tú?
A: Soy de España.
            """,
            "vocabulary": [
                {"term": "Hola", "definition": "Saludo informal", "example": "¡Hola! ¿Cómo estás?"},
                {"term": "Buenos días", "definition": "Saludo formal de la mañana", "example": "Buenos días, señor García."},
                {"term": "Buenas tardes", "definition": "Saludo formal de la tarde", "example": "Buenas tardes a todos."},
                {"term": "Buenas noches", "definition": "Saludo de la noche", "example": "Buenas noches, hasta mañana."},
                {"term": "Me llamo", "definition": "Mi nombre es", "example": "Me llamo Ana."},
                {"term": "Mucho gusto", "definition": "Expresión al conocer a alguien", "example": "Mucho gusto en conocerte."},
                {"term": "¿Cómo te llamas?", "definition": "Pregunta por el nombre", "example": "Hola, ¿cómo te llamas?"},
                {"term": "¿De dónde eres?", "definition": "Pregunta por el origen", "example": "¿De dónde eres? Soy de Colombia."},
            ],
            "grammar_points": [
                "Verbo SER: soy, eres, es, somos, son",
                "Verbo LLAMARSE: me llamo, te llamas, se llama",
                "Artículos: el, la, los, las"
            ]
        },
        "Números y Colores": {
            "content": """
## Los Números del 1 al 20
1 - uno, 2 - dos, 3 - tres, 4 - cuatro, 5 - cinco
6 - seis, 7 - siete, 8 - ocho, 9 - nueve, 10 - diez
11 - once, 12 - doce, 13 - trece, 14 - catorce, 15 - quince
16 - dieciséis, 17 - diecisiete, 18 - dieciocho, 19 - diecinueve, 20 - veinte

## Números del 21 al 100
21 - veintiuno, 30 - treinta, 40 - cuarenta, 50 - cincuenta
60 - sesenta, 70 - setenta, 80 - ochenta, 90 - noventa, 100 - cien

## Los Colores
- Rojo, Azul, Verde, Amarillo, Naranja
- Morado, Rosa, Marrón, Negro, Blanco, Gris

### Ejemplos:
- El coche es rojo.
- La casa es blanca.
- Tengo tres libros azules.
            """,
            "vocabulary": [
                {"term": "Rojo", "definition": "Color red", "example": "La manzana es roja."},
                {"term": "Azul", "definition": "Color blue", "example": "El cielo es azul."},
                {"term": "Verde", "definition": "Color green", "example": "La hierba es verde."},
                {"term": "Amarillo", "definition": "Color yellow", "example": "El sol es amarillo."},
                {"term": "Blanco", "definition": "Color white", "example": "La nieve es blanca."},
                {"term": "Negro", "definition": "Color black", "example": "El gato es negro."},
                {"term": "Uno", "definition": "Number 1", "example": "Tengo un hermano."},
                {"term": "Diez", "definition": "Number 10", "example": "Son las diez de la mañana."},
            ],
            "grammar_points": [
                "Concordancia de género: rojo/roja, blanco/blanca",
                "Concordancia de número: azul/azules",
                "Números cardinales y su uso"
            ]
        },
        "La Familia": {
            "content": """
## Miembros de la Familia

### Familia Nuclear:
- Padre / Papá - Father
- Madre / Mamá - Mother
- Hijo / Hija - Son / Daughter
- Hermano / Hermana - Brother / Sister

### Familia Extendida:
- Abuelo / Abuela - Grandfather / Grandmother
- Tío / Tía - Uncle / Aunt
- Primo / Prima - Cousin
- Sobrino / Sobrina - Nephew / Niece

### Relaciones:
- Esposo / Esposa - Husband / Wife
- Novio / Novia - Boyfriend / Girlfriend

## Ejemplo de descripción familiar:
"Mi familia es grande. Tengo dos hermanos y una hermana. Mis padres se llaman Carlos y María. Mis abuelos viven en el campo."
            """,
            "vocabulary": [
                {"term": "Padre", "definition": "Father, male parent", "example": "Mi padre trabaja en un banco."},
                {"term": "Madre", "definition": "Mother, female parent", "example": "Mi madre cocina muy bien."},
                {"term": "Hermano", "definition": "Brother", "example": "Tengo un hermano mayor."},
                {"term": "Hermana", "definition": "Sister", "example": "Mi hermana estudia medicina."},
                {"term": "Abuelo", "definition": "Grandfather", "example": "Mi abuelo tiene 80 años."},
                {"term": "Abuela", "definition": "Grandmother", "example": "Mi abuela hace pasteles deliciosos."},
                {"term": "Tío", "definition": "Uncle", "example": "Mi tío vive en Madrid."},
                {"term": "Prima", "definition": "Female cousin", "example": "Mi prima es muy simpática."},
            ],
            "grammar_points": [
                "Posesivos: mi, tu, su, nuestro",
                "Verbo TENER: tengo, tienes, tiene",
                "Plural de sustantivos: hermano → hermanos"
            ]
        }
    },
    "A2": {
        "Ir de Compras": {
            "content": """
## En la Tienda

### Frases útiles para comprar:
- ¿Cuánto cuesta esto? - How much does this cost?
- ¿Tiene esto en otro color/talla? - Do you have this in another color/size?
- Me lo llevo - I'll take it
- ¿Puedo pagar con tarjeta? - Can I pay by card?
- ¿Dónde está la caja? - Where is the checkout?

### Vocabulario de ropa:
- Camisa, Pantalón, Vestido, Falda, Zapatos
- Chaqueta, Abrigo, Bufanda, Sombrero

### Tallas:
- Pequeño (S), Mediano (M), Grande (L), Extra Grande (XL)

### Diálogo ejemplo:
Cliente: Buenos días, ¿cuánto cuesta esta camisa?
Vendedor: Cuesta 25 euros.
Cliente: ¿La tiene en azul?
Vendedor: Sí, aquí tiene.
Cliente: Perfecto, me la llevo.
            """,
            "vocabulary": [
                {"term": "¿Cuánto cuesta?", "definition": "How much does it cost?", "example": "¿Cuánto cuesta este libro?"},
                {"term": "Barato", "definition": "Cheap, inexpensive", "example": "Este restaurante es muy barato."},
                {"term": "Caro", "definition": "Expensive", "example": "El hotel es demasiado caro."},
                {"term": "Talla", "definition": "Size (clothing)", "example": "¿Qué talla usas?"},
                {"term": "Probador", "definition": "Fitting room", "example": "El probador está al fondo."},
                {"term": "Efectivo", "definition": "Cash", "example": "Pago en efectivo."},
                {"term": "Tarjeta", "definition": "Card (credit/debit)", "example": "¿Aceptan tarjeta?"},
                {"term": "Descuento", "definition": "Discount", "example": "Hay un 20% de descuento."},
            ],
            "grammar_points": [
                "Verbo COSTAR: cuesta, cuestan",
                "Pronombres de objeto: lo, la, los, las",
                "Comparativos: más caro que, menos barato que"
            ]
        },
        "Rutina Diaria": {
            "content": """
## Mi Día Típico

### Verbos reflexivos:
- Despertarse - to wake up
- Levantarse - to get up
- Ducharse - to shower
- Vestirse - to get dressed
- Acostarse - to go to bed

### Expresiones de tiempo:
- Por la mañana - in the morning
- Por la tarde - in the afternoon
- Por la noche - at night
- Temprano - early
- Tarde - late

### Ejemplo de rutina:
"Me despierto a las 7 de la mañana. Me levanto y me ducho. Desayuno a las 7:30. Salgo de casa a las 8. Trabajo de 9 a 5. Ceno a las 8 de la noche y me acuesto a las 11."
            """,
            "vocabulary": [
                {"term": "Despertarse", "definition": "To wake up", "example": "Me despierto a las 6."},
                {"term": "Levantarse", "definition": "To get up", "example": "Me levanto inmediatamente."},
                {"term": "Desayunar", "definition": "To have breakfast", "example": "Desayuno café y tostadas."},
                {"term": "Almorzar", "definition": "To have lunch", "example": "Almuerzo a la 1."},
                {"term": "Cenar", "definition": "To have dinner", "example": "Ceno con mi familia."},
                {"term": "Acostarse", "definition": "To go to bed", "example": "Me acuesto temprano."},
                {"term": "Temprano", "definition": "Early", "example": "Llego temprano al trabajo."},
                {"term": "Tarde", "definition": "Late", "example": "Hoy llegué tarde."},
            ],
            "grammar_points": [
                "Verbos reflexivos: me levanto, te levantas, se levanta",
                "La hora: Son las dos, Es la una",
                "Preposiciones de tiempo: a las, de... a..."
            ]
        },
        "El Clima y las Estaciones": {
            "content": """
## El Tiempo Atmosférico

### Expresiones del clima:
- Hace sol - It's sunny
- Hace calor - It's hot
- Hace frío - It's cold
- Hace viento - It's windy
- Llueve - It's raining
- Nieva - It's snowing
- Está nublado - It's cloudy

### Las Estaciones:
- Primavera (marzo-mayo)
- Verano (junio-agosto)
- Otoño (septiembre-noviembre)
- Invierno (diciembre-febrero)

### Diálogo:
A: ¿Qué tiempo hace hoy?
B: Hace sol pero un poco de viento.
A: ¿Y mañana?
B: Dicen que va a llover.
            """,
            "vocabulary": [
                {"term": "Hace sol", "definition": "It's sunny", "example": "Hoy hace mucho sol."},
                {"term": "Hace frío", "definition": "It's cold", "example": "En invierno hace mucho frío."},
                {"term": "Hace calor", "definition": "It's hot", "example": "En verano hace calor."},
                {"term": "Llueve", "definition": "It's raining", "example": "Llueve mucho en abril."},
                {"term": "Nieva", "definition": "It's snowing", "example": "Nieva en las montañas."},
                {"term": "Primavera", "definition": "Spring", "example": "Las flores salen en primavera."},
                {"term": "Verano", "definition": "Summer", "example": "Vamos a la playa en verano."},
                {"term": "Invierno", "definition": "Winter", "example": "El invierno es muy frío."},
            ],
            "grammar_points": [
                "Verbo HACER para clima: hace frío, hace calor",
                "Verbos impersonales: llueve, nieva",
                "Futuro próximo: va a llover"
            ]
        }
    },
    "B1": {
        "Expresar Opiniones": {
            "content": """
## Cómo Expresar tu Opinión

### Frases para dar opiniones:
- Creo que... - I think that...
- Pienso que... - I think that...
- En mi opinión... - In my opinion...
- Me parece que... - It seems to me that...
- Desde mi punto de vista... - From my point of view...

### Para estar de acuerdo:
- Estoy de acuerdo - I agree
- Tienes razón - You're right
- Exactamente - Exactly
- Por supuesto - Of course

### Para estar en desacuerdo:
- No estoy de acuerdo - I don't agree
- No lo veo así - I don't see it that way
- Depende - It depends
- No necesariamente - Not necessarily

### Ejemplo:
A: Creo que aprender idiomas es muy importante hoy en día.
B: Estoy totalmente de acuerdo. En mi opinión, es esencial para encontrar trabajo.
            """,
            "vocabulary": [
                {"term": "Creo que", "definition": "I think that", "example": "Creo que es una buena idea."},
                {"term": "Estoy de acuerdo", "definition": "I agree", "example": "Estoy de acuerdo contigo."},
                {"term": "Sin embargo", "definition": "However", "example": "Me gusta, sin embargo es caro."},
                {"term": "Aunque", "definition": "Although", "example": "Aunque llueve, salgo a correr."},
                {"term": "Por lo tanto", "definition": "Therefore", "example": "Estudié mucho, por lo tanto aprobé."},
                {"term": "Además", "definition": "Furthermore", "example": "Es inteligente, además es simpático."},
                {"term": "En cambio", "definition": "On the other hand", "example": "Juan estudia, en cambio Pedro no."},
                {"term": "A pesar de", "definition": "Despite", "example": "A pesar de todo, soy feliz."},
            ],
            "grammar_points": [
                "Subjuntivo con expresiones de opinión: No creo que sea...",
                "Conectores de contraste: pero, sin embargo, aunque",
                "Conectores de adición: además, también, asimismo"
            ]
        },
        "Viajes y Turismo": {
            "content": """
## Planificar un Viaje

### En el aeropuerto:
- Facturar el equipaje - To check in luggage
- Puerta de embarque - Boarding gate
- Tarjeta de embarque - Boarding pass
- Control de seguridad - Security check
- Vuelo con escala - Connecting flight

### En el hotel:
- Reservar una habitación - To book a room
- Habitación individual/doble - Single/double room
- Check-in / Check-out
- ¿Está incluido el desayuno? - Is breakfast included?

### Frases útiles:
- Quisiera reservar... - I would like to book...
- ¿Cuánto cuesta por noche? - How much per night?
- ¿A qué hora es el check-out? - What time is check-out?
- ¿Dónde puedo alquilar un coche? - Where can I rent a car?
            """,
            "vocabulary": [
                {"term": "Reservar", "definition": "To book/reserve", "example": "Quiero reservar una habitación."},
                {"term": "Vuelo", "definition": "Flight", "example": "Mi vuelo sale a las 10."},
                {"term": "Equipaje", "definition": "Luggage", "example": "Llevo poco equipaje."},
                {"term": "Pasaporte", "definition": "Passport", "example": "Necesitas tu pasaporte."},
                {"term": "Alojamiento", "definition": "Accommodation", "example": "Busco alojamiento barato."},
                {"term": "Turista", "definition": "Tourist", "example": "Soy turista en esta ciudad."},
                {"term": "Excursión", "definition": "Excursion/tour", "example": "Hicimos una excursión."},
                {"term": "Recuerdos", "definition": "Souvenirs", "example": "Compré muchos recuerdos."},
            ],
            "grammar_points": [
                "Condicional de cortesía: Quisiera, Me gustaría",
                "Futuro simple: viajaré, visitaré",
                "Oraciones condicionales: Si tengo dinero, viajaré"
            ]
        },
        "Salud y Bienestar": {
            "content": """
## En el Médico

### Partes del cuerpo:
- Cabeza, Ojos, Nariz, Boca, Oídos
- Cuello, Hombros, Brazos, Manos
- Espalda, Pecho, Estómago
- Piernas, Rodillas, Pies

### Síntomas comunes:
- Me duele la cabeza - I have a headache
- Tengo fiebre - I have a fever
- Estoy resfriado - I have a cold
- Me siento mareado - I feel dizzy
- Tengo tos - I have a cough

### En la farmacia:
- Necesito algo para... - I need something for...
- ¿Tiene aspirinas? - Do you have aspirin?
- ¿Necesito receta? - Do I need a prescription?
            """,
            "vocabulary": [
                {"term": "Me duele", "definition": "It hurts me", "example": "Me duele la espalda."},
                {"term": "Fiebre", "definition": "Fever", "example": "Tengo 38 grados de fiebre."},
                {"term": "Resfriado", "definition": "Cold (illness)", "example": "Estoy muy resfriado."},
                {"term": "Receta", "definition": "Prescription", "example": "El médico me dio una receta."},
                {"term": "Pastilla", "definition": "Pill", "example": "Tomo dos pastillas al día."},
                {"term": "Cita", "definition": "Appointment", "example": "Tengo cita con el médico."},
                {"term": "Urgencias", "definition": "Emergency room", "example": "Fui a urgencias anoche."},
                {"term": "Alergia", "definition": "Allergy", "example": "Tengo alergia al polen."},
            ],
            "grammar_points": [
                "Verbo DOLER: me duele, me duelen",
                "Estar + participio: estoy cansado, estoy enfermo",
                "Tener + sustantivo: tengo fiebre, tengo tos"
            ]
        }
    },
    "B2": {
        "El Mundo Laboral": {
            "content": """
## Vocabulario Profesional

### Buscar trabajo:
- Curriculum vitae (CV) / Hoja de vida
- Carta de presentación - Cover letter
- Entrevista de trabajo - Job interview
- Oferta de empleo - Job offer
- Candidato/a - Candidate

### En la oficina:
- Reunión - Meeting
- Plazo de entrega - Deadline
- Jefe/a - Boss
- Compañero/a de trabajo - Colleague
- Departamento - Department

### Frases profesionales:
- Adjunto mi CV - I attach my CV
- Tengo experiencia en... - I have experience in...
- Mis puntos fuertes son... - My strengths are...
- Estoy disponible para... - I am available for...
            """,
            "vocabulary": [
                {"term": "Solicitar", "definition": "To apply for", "example": "Voy a solicitar el puesto."},
                {"term": "Contratar", "definition": "To hire", "example": "Van a contratar a 5 personas."},
                {"term": "Despedir", "definition": "To fire", "example": "Lo despidieron ayer."},
                {"term": "Ascender", "definition": "To promote", "example": "Me ascendieron a gerente."},
                {"term": "Sueldo", "definition": "Salary", "example": "El sueldo es negociable."},
                {"term": "Jornada", "definition": "Work day/shift", "example": "Trabajo jornada completa."},
                {"term": "Vacaciones", "definition": "Vacation/holidays", "example": "Tengo 3 semanas de vacaciones."},
                {"term": "Jubilarse", "definition": "To retire", "example": "Mi padre se jubiló a los 65."},
            ],
            "grammar_points": [
                "Oraciones de relativo: La empresa que me contrató...",
                "Voz pasiva: El candidato fue seleccionado",
                "Perífrasis verbales: Voy a solicitar, Acabo de terminar"
            ]
        },
        "Actualidad y Noticias": {
            "content": """
## Medios de Comunicación

### Tipos de medios:
- Periódico / Diario - Newspaper
- Revista - Magazine
- Televisión - Television
- Radio - Radio
- Redes sociales - Social media
- Prensa digital - Digital press

### Secciones del periódico:
- Portada - Front page
- Editorial - Editorial
- Política - Politics
- Economía - Economy
- Deportes - Sports
- Cultura - Culture
- Sociedad - Society

### Vocabulario periodístico:
- Titular - Headline
- Artículo - Article
- Periodista - Journalist
- Entrevista - Interview
- Fuente - Source
            """,
            "vocabulary": [
                {"term": "Noticia", "definition": "News item", "example": "Es una noticia importante."},
                {"term": "Acontecimiento", "definition": "Event", "example": "Fue un acontecimiento histórico."},
                {"term": "Informar", "definition": "To inform/report", "example": "El periodista informó sobre el tema."},
                {"term": "Opinar", "definition": "To give an opinion", "example": "¿Qué opinas del asunto?"},
                {"term": "Debatir", "definition": "To debate", "example": "Van a debatir sobre economía."},
                {"term": "Publicar", "definition": "To publish", "example": "Publicaron la entrevista ayer."},
                {"term": "Actualidad", "definition": "Current affairs", "example": "Es un tema de actualidad."},
                {"term": "Tendencia", "definition": "Trend", "example": "Es una tendencia en redes."},
            ],
            "grammar_points": [
                "Estilo indirecto: Dijo que..., Afirmó que...",
                "Pasado continuo vs. pasado simple",
                "Conectores causales: porque, ya que, debido a"
            ]
        },
        "Cultura y Tradiciones": {
            "content": """
## Festividades y Costumbres

### Celebraciones importantes:
- Navidad - Christmas
- Semana Santa - Holy Week
- Día de los Muertos (México)
- Feria de Abril (España)
- Carnaval

### Tradiciones:
- Costumbre - Custom
- Tradición - Tradition
- Folklore - Folklore
- Patrimonio cultural - Cultural heritage

### Comida tradicional:
- Paella (España)
- Tacos (México)
- Feijoada (Brasil)
- Asado (Argentina)
- Ceviche (Perú)

### Expresiones:
- Celebrar una fiesta
- Mantener las tradiciones
- Honrar a los antepasados
            """,
            "vocabulary": [
                {"term": "Costumbre", "definition": "Custom/habit", "example": "Es una costumbre familiar."},
                {"term": "Celebrar", "definition": "To celebrate", "example": "Celebramos la Navidad juntos."},
                {"term": "Heredar", "definition": "To inherit", "example": "Heredamos estas tradiciones."},
                {"term": "Antepasados", "definition": "Ancestors", "example": "Honramos a nuestros antepasados."},
                {"term": "Festividad", "definition": "Holiday/festivity", "example": "Es una festividad nacional."},
                {"term": "Gastronomía", "definition": "Gastronomy", "example": "La gastronomía peruana es famosa."},
                {"term": "Artesanía", "definition": "Handicrafts", "example": "Compré artesanía local."},
                {"term": "Folclore", "definition": "Folklore", "example": "El folclore es muy rico aquí."},
            ],
            "grammar_points": [
                "Imperfecto para describir tradiciones",
                "Se impersonal: Se celebra, Se come",
                "Oraciones temporales: Cuando era niño..."
            ]
        }
    },
    "C1": {
        "Argumentación Avanzada": {
            "content": """
## Técnicas de Argumentación

### Estructurar un argumento:
1. Introducción - Presentar la tesis
2. Desarrollo - Exponer argumentos
3. Contraargumentos - Considerar otras perspectivas
4. Conclusión - Reafirmar la posición

### Conectores argumentativos:
- Para añadir: Además, Asimismo, Por otra parte
- Para contrastar: Sin embargo, No obstante, Por el contrario
- Para concluir: En conclusión, En definitiva, Para resumir
- Para ejemplificar: Por ejemplo, Es decir, En concreto

### Expresiones para argumentar:
- Cabe destacar que... - It should be noted that...
- Es preciso señalar... - It is necessary to point out...
- Conviene recordar que... - It is worth remembering that...
- No cabe duda de que... - There is no doubt that...
            """,
            "vocabulary": [
                {"term": "Cabe destacar", "definition": "It should be noted", "example": "Cabe destacar su importancia."},
                {"term": "No obstante", "definition": "Nevertheless", "example": "No obstante, hay excepciones."},
                {"term": "En definitiva", "definition": "In short/ultimately", "example": "En definitiva, es la mejor opción."},
                {"term": "Por consiguiente", "definition": "Consequently", "example": "Por consiguiente, debemos actuar."},
                {"term": "A raíz de", "definition": "As a result of", "example": "A raíz de esto, cambió la ley."},
                {"term": "En aras de", "definition": "For the sake of", "example": "En aras de la claridad..."},
                {"term": "De ahí que", "definition": "Hence", "example": "De ahí que sea necesario..."},
                {"term": "Subyacer", "definition": "To underlie", "example": "Una idea subyace a este concepto."},
            ],
            "grammar_points": [
                "Subjuntivo en oraciones concesivas: Aunque sea...",
                "Oraciones condicionales complejas",
                "Nominalizaciones: el desarrollo, la implementación"
            ]
        },
        "Lenguaje Académico": {
            "content": """
## Escritura Académica

### Estructura de un ensayo:
- Resumen / Abstract
- Introducción
- Marco teórico
- Metodología
- Resultados
- Discusión
- Conclusiones
- Bibliografía

### Verbos académicos:
- Analizar, Examinar, Investigar
- Demostrar, Evidenciar, Comprobar
- Argumentar, Sostener, Afirmar
- Concluir, Determinar, Establecer

### Citar fuentes:
- Según [autor]... - According to [author]...
- [Autor] sostiene que... - [Author] maintains that...
- Como señala [autor]... - As [author] points out...
            """,
            "vocabulary": [
                {"term": "Hipótesis", "definition": "Hypothesis", "example": "La hipótesis fue confirmada."},
                {"term": "Metodología", "definition": "Methodology", "example": "Usamos metodología cualitativa."},
                {"term": "Evidenciar", "definition": "To demonstrate/show", "example": "Los datos evidencian el cambio."},
                {"term": "Contrastar", "definition": "To contrast/compare", "example": "Debemos contrastar las fuentes."},
                {"term": "Bibliografía", "definition": "Bibliography", "example": "Consulta la bibliografía."},
                {"term": "Citar", "definition": "To cite/quote", "example": "Es necesario citar las fuentes."},
                {"term": "Tesis", "definition": "Thesis", "example": "Mi tesis trata sobre lingüística."},
                {"term": "Corroborar", "definition": "To corroborate", "example": "Los estudios corroboran esto."},
            ],
            "grammar_points": [
                "Voz pasiva académica: Se ha demostrado que...",
                "Impersonal con SE: Se puede observar...",
                "Tiempos verbales en escritura académica"
            ]
        },
        "Matices Culturales": {
            "content": """
## Expresiones Idiomáticas

### Modismos comunes:
- Estar en las nubes - To be daydreaming
- Costar un ojo de la cara - To cost an arm and a leg
- Ser pan comido - To be a piece of cake
- Meter la pata - To put your foot in it
- Tomar el pelo - To pull someone's leg

### Diferencias regionales:
- España: Coche, Móvil, Ordenador
- Latinoamérica: Carro, Celular, Computadora

### Registros lingüísticos:
- Formal: Usted, Le agradecería...
- Informal: Tú, ¿Me puedes...?
- Coloquial: Tío/a, ¿Qué onda?
            """,
            "vocabulary": [
                {"term": "Modismo", "definition": "Idiom", "example": "Es un modismo muy usado."},
                {"term": "Coloquial", "definition": "Colloquial", "example": "Es una expresión coloquial."},
                {"term": "Jerga", "definition": "Slang/jargon", "example": "La jerga juvenil cambia mucho."},
                {"term": "Matiz", "definition": "Nuance", "example": "Hay un matiz importante aquí."},
                {"term": "Connotación", "definition": "Connotation", "example": "Tiene una connotación negativa."},
                {"term": "Eufemismo", "definition": "Euphemism", "example": "Usó un eufemismo."},
                {"term": "Ironía", "definition": "Irony", "example": "Lo dijo con ironía."},
                {"term": "Sarcasmo", "definition": "Sarcasm", "example": "Detecté su sarcasmo."},
            ],
            "grammar_points": [
                "Uso de diminutivos con valor afectivo",
                "Diferencias entre ser y estar con adjetivos",
                "Uso de subjuntivo en expresiones idiomáticas"
            ]
        }
    },
    "C2": {
        "Registro Literario": {
            "content": """
## Análisis Literario

### Figuras retóricas:
- Metáfora - Metaphor
- Símil - Simile
- Hipérbole - Hyperbole
- Personificación - Personification
- Aliteración - Alliteration
- Anáfora - Anaphora

### Géneros literarios:
- Novela - Novel
- Cuento - Short story
- Poesía - Poetry
- Teatro - Drama
- Ensayo - Essay

### Movimientos literarios:
- Realismo
- Modernismo
- Vanguardias
- Boom latinoamericano
- Literatura contemporánea
            """,
            "vocabulary": [
                {"term": "Prosa", "definition": "Prose", "example": "Escribe en prosa poética."},
                {"term": "Verso", "definition": "Verse", "example": "El poema tiene versos alejandrinos."},
                {"term": "Estrofa", "definition": "Stanza", "example": "Cada estrofa tiene cuatro versos."},
                {"term": "Narrador", "definition": "Narrator", "example": "El narrador es omnisciente."},
                {"term": "Desenlace", "definition": "Denouement", "example": "El desenlace es inesperado."},
                {"term": "Trama", "definition": "Plot", "example": "La trama es muy compleja."},
                {"term": "Leitmotiv", "definition": "Leitmotif", "example": "El agua es el leitmotiv."},
                {"term": "Intertextualidad", "definition": "Intertextuality", "example": "Hay intertextualidad con Borges."},
            ],
            "grammar_points": [
                "Pretérito anterior: Hubo llegado cuando...",
                "Futuro de conjetura: Serán las tres",
                "Subjuntivo en oraciones independientes"
            ]
        },
        "Dialectos y Variantes": {
            "content": """
## Variación Lingüística del Español

### Español peninsular:
- Distinción de /s/ y /θ/
- Uso de vosotros
- Leísmo aceptado

### Español latinoamericano:
- Seseo generalizado
- Ustedes para plural
- Voseo (Argentina, Uruguay, Centroamérica)

### Características regionales:
- México: Uso de "mero", diminutivos frecuentes
- Argentina: Voseo, pronunciación de ll/y como sh
- Caribe: Aspiración de /s/, lambdacismo
- Andes: Conservación de consonantes

### Registros:
- Culto, Estándar, Coloquial, Vulgar
            """,
            "vocabulary": [
                {"term": "Dialecto", "definition": "Dialect", "example": "Cada región tiene su dialecto."},
                {"term": "Variante", "definition": "Variant", "example": "Es una variante del español."},
                {"term": "Seseo", "definition": "Pronouncing c/z as s", "example": "El seseo es común en América."},
                {"term": "Voseo", "definition": "Use of 'vos'", "example": "En Argentina usan el voseo."},
                {"term": "Arcaísmo", "definition": "Archaism", "example": "Es un arcaísmo en desuso."},
                {"term": "Neologismo", "definition": "Neologism", "example": "Internet creó muchos neologismos."},
                {"term": "Préstamo", "definition": "Loanword", "example": "Software es un préstamo del inglés."},
                {"term": "Calco", "definition": "Calque", "example": "Rascacielos es un calco."},
            ],
            "grammar_points": [
                "Variación en el sistema pronominal",
                "Diferencias en el uso de tiempos verbales",
                "Variación sintáctica regional"
            ]
        },
        "Comunicación Profesional": {
            "content": """
## Comunicación de Alto Nivel

### Presentaciones ejecutivas:
- Captar la atención del público
- Estructurar el mensaje claramente
- Usar datos y evidencias
- Manejar preguntas difíciles
- Cerrar con impacto

### Negociación:
- Preparación exhaustiva
- Escucha activa
- Identificar intereses comunes
- Proponer soluciones win-win
- Cerrar acuerdos

### Comunicación escrita formal:
- Informes ejecutivos
- Propuestas comerciales
- Comunicados de prensa
- Correspondencia institucional
            """,
            "vocabulary": [
                {"term": "Interlocutor", "definition": "Interlocutor", "example": "Mi interlocutor era el CEO."},
                {"term": "Consenso", "definition": "Consensus", "example": "Llegamos a un consenso."},
                {"term": "Dictamen", "definition": "Expert opinion/ruling", "example": "El dictamen fue favorable."},
                {"term": "Protocolo", "definition": "Protocol", "example": "Seguimos el protocolo establecido."},
                {"term": "Cláusula", "definition": "Clause", "example": "La cláusula es vinculante."},
                {"term": "Subsanar", "definition": "To rectify/remedy", "example": "Debemos subsanar el error."},
                {"term": "Diligencia", "definition": "Diligence", "example": "Actuó con diligencia."},
                {"term": "Salvaguardar", "definition": "To safeguard", "example": "Hay que salvaguardar los intereses."},
            ],
            "grammar_points": [
                "Condicional de cortesía profesional",
                "Estructuras impersonales formales",
                "Nominalización en textos formales"
            ]
        }
    }
}

async def update_lessons():
    """Actualizar todas las lecciones con contenido real."""
    
    updated = 0
    
    for level, lessons_data in LESSON_CONTENT.items():
        for title, content_data in lessons_data.items():
            # Buscar la lección por título (funciona para todos los idiomas)
            result = await db.lessons.update_many(
                {"title": title},
                {"$set": {
                    "content": content_data["content"].strip(),
                    "vocabulary": content_data["vocabulary"],
                    "grammar_points": content_data["grammar_points"]
                }}
            )
            updated += result.modified_count
            
    print(f"✅ Lecciones actualizadas: {updated}")
    
    # Verificar
    sample = await db.lessons.find_one({"title": "Saludos y Presentaciones"})
    if sample:
        print(f"Ejemplo - Vocabulario: {len(sample.get('vocabulary', []))} palabras")
        print(f"Ejemplo - Gramática: {len(sample.get('grammar_points', []))} puntos")

if __name__ == "__main__":
    asyncio.run(update_lessons())

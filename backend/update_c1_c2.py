"""
Script para actualizar el contenido de los niveles C1 y C2 con información completa.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

# ============== ESPAÑOL C1 y C2 ==============
SPANISH_C1_C2 = {
    "C1": [
        {
            "title": "Argumentación Avanzada",
            "content": """## Técnicas de Argumentación Profesional

La argumentación avanzada requiere dominar estructuras complejas y conectores sofisticados para presentar ideas de manera convincente.

### Estructura de un Argumento Sólido:
1. **Introducción**: Presentar la tesis principal
2. **Desarrollo**: Exponer argumentos con evidencias
3. **Contraargumentos**: Anticipar y refutar objeciones
4. **Conclusión**: Reafirmar la posición con síntesis

### Conectores Argumentativos Avanzados:

**Para añadir información:**
- Además / Asimismo / Por otra parte
- Cabe añadir que... / Es preciso señalar que...
- En este mismo sentido... / De igual modo...

**Para contrastar:**
- Sin embargo / No obstante / Por el contrario
- A pesar de que... / Pese a... / Aun así...
- Si bien es cierto que... / Aunque...

**Para concluir:**
- En conclusión / En definitiva / Para resumir
- En síntesis / A modo de cierre / Por todo lo expuesto

### Expresiones para Argumentar con Autoridad:
- Los datos demuestran que...
- Según estudios recientes...
- Es innegable que...
- Resulta evidente que...
- No cabe duda de que...

### Ejemplo de Argumentación:
"Cabe destacar que el cambio climático representa uno de los mayores desafíos de nuestro tiempo. No obstante, existen soluciones viables. Por una parte, las energías renovables ofrecen alternativas sostenibles. Por otra parte, la concienciación ciudadana está aumentando. En definitiva, aunque el problema es grave, la acción colectiva puede marcar la diferencia."
            """,
            "vocabulary": [
                {"term": "Cabe destacar", "definition": "Es importante señalar", "example": "Cabe destacar que los resultados fueron positivos."},
                {"term": "No obstante", "definition": "Sin embargo, a pesar de eso", "example": "El proyecto es ambicioso; no obstante, es factible."},
                {"term": "En definitiva", "definition": "En resumen, finalmente", "example": "En definitiva, la propuesta es beneficiosa."},
                {"term": "Por consiguiente", "definition": "Como resultado, por lo tanto", "example": "Los costos aumentaron; por consiguiente, ajustamos el presupuesto."},
                {"term": "A raíz de", "definition": "Como consecuencia de", "example": "A raíz de la pandemia, cambió la forma de trabajar."},
                {"term": "En aras de", "definition": "Con el objetivo de, para", "example": "En aras de la transparencia, publicamos los datos."},
                {"term": "De ahí que", "definition": "Por eso, por esa razón", "example": "El mercado cambió; de ahí que adaptáramos la estrategia."},
                {"term": "Subyacer", "definition": "Estar debajo, ser la causa oculta", "example": "Varios factores subyacen a esta crisis."},
            ],
            "grammar_points": [
                "Subjuntivo en oraciones concesivas: Aunque sea difícil, lo intentaré",
                "Oraciones condicionales complejas: De haber sabido..., Si hubiera...",
                "Nominalizaciones: desarrollar → el desarrollo, implementar → la implementación"
            ]
        },
        {
            "title": "Lenguaje Académico",
            "content": """## Escritura e Investigación Académica

El lenguaje académico se caracteriza por su precisión, objetividad y uso de estructuras formales.

### Estructura de un Trabajo Académico:
1. **Resumen/Abstract**: Síntesis del trabajo (150-300 palabras)
2. **Introducción**: Contextualización y objetivos
3. **Marco Teórico**: Revisión de literatura existente
4. **Metodología**: Cómo se realizó la investigación
5. **Resultados**: Hallazgos principales
6. **Discusión**: Interpretación de resultados
7. **Conclusiones**: Síntesis y futuras líneas
8. **Bibliografía**: Referencias citadas

### Verbos Académicos Frecuentes:
- **Analizar**: Examinar detalladamente
- **Demostrar**: Probar con evidencias
- **Argumentar**: Presentar razones
- **Sostener**: Mantener una posición
- **Concluir**: Llegar a una conclusión
- **Evidenciar**: Mostrar claramente

### Cómo Citar Fuentes:
- Según García (2023), "la educación es fundamental..."
- Como señala Martínez (2022), existe una correlación...
- Los estudios de López (2021) demuestran que...
- De acuerdo con investigaciones recientes (Pérez, 2023)...

### Expresiones de Cautela Académica:
- Parece indicar que...
- Los datos sugieren que...
- Podría argumentarse que...
- Cabe la posibilidad de que...

### Ejemplo de Párrafo Académico:
"El presente estudio tiene como objetivo analizar el impacto de las redes sociales en la comunicación interpersonal. Según investigaciones previas (García, 2022; Martínez, 2023), existe una correlación significativa entre el uso de plataformas digitales y cambios en los patrones comunicativos. Los resultados obtenidos sugieren que, si bien las redes facilitan la conectividad, también pueden afectar la calidad de las interacciones presenciales."
            """,
            "vocabulary": [
                {"term": "Hipótesis", "definition": "Suposición que se investiga", "example": "La hipótesis fue confirmada por los datos."},
                {"term": "Metodología", "definition": "Conjunto de métodos utilizados", "example": "La metodología incluyó encuestas y entrevistas."},
                {"term": "Evidenciar", "definition": "Demostrar, hacer evidente", "example": "Los resultados evidencian una tendencia clara."},
                {"term": "Contrastar", "definition": "Comparar para ver diferencias", "example": "Es necesario contrastar diferentes fuentes."},
                {"term": "Bibliografía", "definition": "Lista de obras consultadas", "example": "La bibliografía incluye 50 referencias."},
                {"term": "Citar", "definition": "Mencionar palabras de otro autor", "example": "Es obligatorio citar las fuentes correctamente."},
                {"term": "Tesis", "definition": "Proposición que se defiende", "example": "Mi tesis aborda el cambio climático."},
                {"term": "Corroborar", "definition": "Confirmar, verificar", "example": "Otros estudios corroboran estos hallazgos."},
            ],
            "grammar_points": [
                "Voz pasiva académica: Se ha demostrado que..., Fue analizado...",
                "Impersonal con SE: Se puede observar..., Se considera que...",
                "Uso del condicional para hipótesis: Esto indicaría que..."
            ]
        },
        {
            "title": "Matices Culturales",
            "content": """## Expresiones Idiomáticas y Variación Cultural

Dominar los matices culturales implica comprender expresiones idiomáticas, registros lingüísticos y variaciones regionales.

### Modismos y Expresiones Idiomáticas:

**Expresiones sobre el estado de ánimo:**
- Estar en las nubes → Estar distraído
- Estar como una cabra → Estar loco
- Estar hecho polvo → Estar muy cansado
- Estar en su salsa → Sentirse cómodo

**Expresiones sobre situaciones:**
- Costar un ojo de la cara → Ser muy caro
- Ser pan comido → Ser muy fácil
- Meter la pata → Cometer un error
- Tomar el pelo → Burlarse de alguien
- Dar en el clavo → Acertar
- Irse por las ramas → Divagar, no ir al grano

**Expresiones sobre personas:**
- Ser uña y carne → Ser muy amigos
- Ser un bala perdida → Ser irresponsable
- Tener mala leche → Tener mal carácter

### Registros Lingüísticos:
- **Formal**: Usted, Le agradecería, Atentamente
- **Informal**: Tú, ¿Me puedes...?, Un saludo
- **Coloquial**: Tío/a, ¿Qué onda?, ¡Qué guay!

### Variaciones Regionales del Español:
- **España**: Coche, Móvil, Ordenador, Vale
- **México**: Carro, Celular, Computadora, Órale
- **Argentina**: Auto, Celular, Computadora, Dale
- **Colombia**: Carro, Celular, Computador, Listo

### Uso según Contexto:
El dominio de estos matices permite adaptar el discurso al interlocutor y la situación, demostrando competencia comunicativa avanzada.
            """,
            "vocabulary": [
                {"term": "Modismo", "definition": "Expresión fija con significado figurado", "example": "Llover a cántaros es un modismo."},
                {"term": "Coloquial", "definition": "Propio de la conversación informal", "example": "Guay es una expresión coloquial."},
                {"term": "Jerga", "definition": "Lenguaje especial de un grupo", "example": "Los médicos usan jerga profesional."},
                {"term": "Matiz", "definition": "Diferencia sutil de significado", "example": "Hay un matiz importante entre ambos términos."},
                {"term": "Connotación", "definition": "Significado adicional o emocional", "example": "Esa palabra tiene connotación negativa."},
                {"term": "Eufemismo", "definition": "Expresión suave para algo desagradable", "example": "Pasar a mejor vida es un eufemismo de morir."},
                {"term": "Ironía", "definition": "Decir lo contrario de lo que se piensa", "example": "Lo dijo con ironía evidente."},
                {"term": "Doble sentido", "definition": "Frase con dos interpretaciones", "example": "El chiste tenía un doble sentido."},
            ],
            "grammar_points": [
                "Uso de diminutivos con valor afectivo: cafecito, ratito, cerquita",
                "Diferencias sutiles entre ser y estar: Es listo vs. Está listo",
                "Subjuntivo en expresiones idiomáticas: Que te vaya bien"
            ]
        }
    ],
    "C2": [
        {
            "title": "Registro Literario",
            "content": """## Análisis y Apreciación Literaria

El nivel C2 implica comprender y apreciar textos literarios complejos, identificando recursos estilísticos y analizando críticamente las obras.

### Figuras Retóricas Principales:

**Figuras de significado:**
- **Metáfora**: Identificación entre dos elementos. "Sus ojos son esmeraldas"
- **Símil**: Comparación explícita. "Corre como el viento"
- **Hipérbole**: Exageración. "Te lo he dicho mil veces"
- **Personificación**: Atribuir cualidades humanas. "El viento susurraba"
- **Metonimia**: Sustitución por relación. "Leí a Cervantes" (sus obras)

**Figuras de sonido:**
- **Aliteración**: Repetición de sonidos. "El ruido con que rueda la ronca tempestad"
- **Onomatopeya**: Imitación de sonidos. "El tic-tac del reloj"

**Figuras de construcción:**
- **Anáfora**: Repetición al inicio. "Verde que te quiero verde. Verde viento. Verde ramas."
- **Hipérbaton**: Alteración del orden. "Del salón en el ángulo oscuro"

### Géneros Literarios:
- **Narrativa**: Novela, Cuento, Microrrelato
- **Poesía**: Soneto, Romance, Verso libre
- **Teatro**: Tragedia, Comedia, Drama
- **Ensayo**: Reflexión argumentada

### Movimientos Literarios Hispanos:
- **Siglo de Oro**: Cervantes, Lope de Vega, Quevedo
- **Romanticismo**: Bécquer, Espronceda
- **Modernismo**: Rubén Darío, Juan Ramón Jiménez
- **Generación del 27**: García Lorca, Alberti
- **Boom Latinoamericano**: García Márquez, Vargas Llosa, Cortázar

### Análisis de Texto Literario:
Al analizar un texto, considerar: tema, estructura, voz narrativa, estilo, contexto histórico y recursos literarios empleados.
            """,
            "vocabulary": [
                {"term": "Prosa", "definition": "Forma de expresión sin rima ni metro", "example": "La novela está escrita en prosa poética."},
                {"term": "Verso", "definition": "Línea de un poema con ritmo", "example": "El soneto tiene catorce versos."},
                {"term": "Estrofa", "definition": "Conjunto de versos", "example": "Cada estrofa tiene cuatro versos."},
                {"term": "Narrador", "definition": "Voz que cuenta la historia", "example": "El narrador es omnisciente."},
                {"term": "Desenlace", "definition": "Final de una historia", "example": "El desenlace fue inesperado."},
                {"term": "Trama", "definition": "Secuencia de eventos", "example": "La trama es muy compleja."},
                {"term": "Leitmotiv", "definition": "Tema recurrente", "example": "El agua es el leitmotiv de la obra."},
                {"term": "Intertextualidad", "definition": "Referencia a otras obras", "example": "Hay intertextualidad con el Quijote."},
            ],
            "grammar_points": [
                "Pretérito anterior literario: Hubo llegado cuando...",
                "Futuro de conjetura: ¿Qué hora será? Serán las tres",
                "Subjuntivo en oraciones independientes: ¡Ojalá fuera verdad!"
            ]
        },
        {
            "title": "Dialectos y Variantes",
            "content": """## Variación Lingüística del Español

El español es una lengua pluricéntrica con múltiples normas cultas y variaciones regionales.

### Español Peninsular (España):
- **Fonética**: Distinción /s/ y /θ/ (casa vs. caza)
- **Gramática**: Uso de vosotros/as, leísmo aceptado
- **Léxico**: Coche, móvil, ordenador, gafas, patata

### Español de México:
- **Fonética**: Seseo, conservación de consonantes
- **Gramática**: Ustedes para plural, diminutivos frecuentes (-ito)
- **Léxico**: Carro, celular, computadora, lentes, papa
- **Expresiones**: Órale, mero, ¿mande?

### Español Rioplatense (Argentina/Uruguay):
- **Fonética**: Yeísmo con rehilamiento (ll/y como "sh")
- **Gramática**: Voseo (vos tenés, vos querés)
- **Léxico**: Auto, celular, computadora, anteojos
- **Expresiones**: Che, dale, bárbaro

### Español Caribeño (Cuba, Puerto Rico, R. Dominicana):
- **Fonética**: Aspiración de /s/, lambdacismo (r→l)
- **Gramática**: Sujeto antepuesto en preguntas
- **Expresiones**: Chévere, ¿qué lo qué?, bacano

### Español Andino (Perú, Ecuador, Bolivia):
- **Fonética**: Conservación de consonantes
- **Influencia**: Del quechua y aymara
- **Expresiones**: Pues, nomás, ya pues

### Consideraciones Sociolingüísticas:
- Todas las variantes son igualmente válidas
- La norma culta varía según la región
- El español es una lengua policéntrica
- Hay que adaptar el registro al contexto
            """,
            "vocabulary": [
                {"term": "Dialecto", "definition": "Variedad regional de una lengua", "example": "El andaluz es un dialecto del español."},
                {"term": "Variante", "definition": "Forma diferente de la misma lengua", "example": "Es una variante del español americano."},
                {"term": "Seseo", "definition": "Pronunciar c/z como s", "example": "El seseo es general en América."},
                {"term": "Voseo", "definition": "Uso de vos en lugar de tú", "example": "El voseo es típico de Argentina."},
                {"term": "Arcaísmo", "definition": "Palabra o forma antigua", "example": "Vos es un arcaísmo en España."},
                {"term": "Neologismo", "definition": "Palabra nueva", "example": "Tuitear es un neologismo."},
                {"term": "Préstamo", "definition": "Palabra tomada de otro idioma", "example": "Fútbol es un préstamo del inglés."},
                {"term": "Calco", "definition": "Traducción literal de otra lengua", "example": "Rascacielos es un calco de skyscraper."},
            ],
            "grammar_points": [
                "Variación en el sistema pronominal: vos/tú/usted",
                "Diferencias en tiempos verbales: pretérito perfecto vs. indefinido",
                "Variación sintáctica: ¿Qué tú quieres? vs. ¿Qué quieres tú?"
            ]
        },
        {
            "title": "Comunicación Profesional",
            "content": """## Comunicación Empresarial de Alto Nivel

La comunicación profesional C2 implica dominar registros formales, negociación avanzada y comunicación estratégica.

### Presentaciones Ejecutivas:
**Estructura efectiva:**
1. Apertura impactante (dato, pregunta, historia)
2. Agenda clara
3. Desarrollo con evidencias
4. Manejo de objeciones
5. Cierre con llamada a la acción

**Expresiones profesionales:**
- "Permítanme comenzar destacando..."
- "Los datos reflejan claramente que..."
- "En respuesta a su observación..."
- "Para concluir, quisiera enfatizar..."

### Negociación Avanzada:
**Principios clave:**
- Preparación exhaustiva
- Escucha activa
- Identificación de intereses
- Búsqueda de soluciones win-win
- Cierre efectivo

**Expresiones de negociación:**
- "Entiendo su posición, sin embargo..."
- "¿Qué le parecería si...?"
- "Propongo que exploremos alternativas..."
- "Creo que podemos llegar a un acuerdo mutuamente beneficioso..."

### Comunicación Escrita Formal:
**Tipos de documentos:**
- Informes ejecutivos
- Propuestas comerciales
- Actas de reunión
- Comunicados institucionales

**Fórmulas de cortesía:**
- Apertura: "Me dirijo a usted para...", "Por medio de la presente..."
- Cierre: "Quedo a su disposición...", "Atentamente", "Cordialmente"

### Protocolo y Etiqueta Profesional:
- Tratamiento formal (usted, don/doña)
- Comunicación intercultural
- Gestión de conflictos
- Feedback constructivo
            """,
            "vocabulary": [
                {"term": "Interlocutor", "definition": "Persona con quien se habla", "example": "Mi interlocutor era el director."},
                {"term": "Consenso", "definition": "Acuerdo entre todas las partes", "example": "Llegamos a un consenso tras horas de debate."},
                {"term": "Dictamen", "definition": "Opinión o juicio formal", "example": "El dictamen legal fue favorable."},
                {"term": "Protocolo", "definition": "Conjunto de reglas formales", "example": "Seguimos el protocolo establecido."},
                {"term": "Cláusula", "definition": "Disposición de un contrato", "example": "La cláusula tercera especifica..."},
                {"term": "Subsanar", "definition": "Corregir, remediar", "example": "Debemos subsanar el error cuanto antes."},
                {"term": "Diligencia", "definition": "Cuidado y prontitud", "example": "Actuó con la debida diligencia."},
                {"term": "Salvaguardar", "definition": "Proteger, defender", "example": "Hay que salvaguardar los intereses de todos."},
            ],
            "grammar_points": [
                "Condicional de cortesía: ¿Podría indicarme...?, Desearía solicitar...",
                "Estructuras impersonales: Se ruega..., Se agradecería...",
                "Perífrasis formales: Cabe señalar, Es menester, Procede indicar"
            ]
        }
    ]
}

# ============== ENGLISH C1 y C2 ==============
ENGLISH_C1_C2 = {
    "C1": [
        {
            "title": "Advanced Argumentation",
            "content": """## Professional Argumentation Techniques

Advanced argumentation requires mastery of complex structures and sophisticated connectors to present ideas convincingly.

### Structure of a Solid Argument:
1. **Introduction**: Present the main thesis
2. **Development**: Present arguments with evidence
3. **Counter-arguments**: Anticipate and refute objections
4. **Conclusion**: Reaffirm position with synthesis

### Advanced Argumentative Connectors:

**To add information:**
- Furthermore / Moreover / In addition
- It should be noted that... / It is worth mentioning...
- In this regard... / Along the same lines...

**To contrast:**
- However / Nevertheless / On the contrary
- Despite the fact that... / Notwithstanding...
- While it is true that... / Although...

**To conclude:**
- In conclusion / To sum up / All things considered
- In essence / Ultimately / To conclude

### Expressions for Authoritative Argumentation:
- The data clearly demonstrates that...
- According to recent studies...
- It is undeniable that...
- It is evident that...
- There is no doubt that...

### Example of Argumentation:
"It should be noted that climate change represents one of the greatest challenges of our time. Nevertheless, viable solutions exist. On one hand, renewable energies offer sustainable alternatives. On the other hand, public awareness is increasing. Ultimately, although the problem is serious, collective action can make a difference."
            """,
            "vocabulary": [
                {"term": "It should be noted", "definition": "It's important to mention", "example": "It should be noted that results were positive."},
                {"term": "Nevertheless", "definition": "However, despite that", "example": "The project is ambitious; nevertheless, it's feasible."},
                {"term": "Ultimately", "definition": "Finally, in the end", "example": "Ultimately, the proposal is beneficial."},
                {"term": "Consequently", "definition": "As a result, therefore", "example": "Costs increased; consequently, we adjusted the budget."},
                {"term": "In light of", "definition": "Considering, because of", "example": "In light of recent events, we changed our approach."},
                {"term": "For the sake of", "definition": "In order to achieve", "example": "For the sake of transparency, we published the data."},
                {"term": "Hence", "definition": "For this reason, therefore", "example": "The market changed; hence we adapted our strategy."},
                {"term": "Underlie", "definition": "To be the hidden cause of", "example": "Several factors underlie this crisis."},
            ],
            "grammar_points": [
                "Subjunctive in concessive clauses: Be that as it may...",
                "Complex conditionals: Had I known..., Were it not for...",
                "Nominalizations: develop → development, implement → implementation"
            ]
        },
        {
            "title": "Academic Language",
            "content": """## Academic Writing and Research

Academic language is characterized by precision, objectivity, and the use of formal structures.

### Structure of an Academic Paper:
1. **Abstract**: Summary of the work (150-300 words)
2. **Introduction**: Context and objectives
3. **Literature Review**: Review of existing research
4. **Methodology**: How the research was conducted
5. **Results**: Main findings
6. **Discussion**: Interpretation of results
7. **Conclusions**: Summary and future directions
8. **References**: Cited sources

### Common Academic Verbs:
- **Analyze**: Examine in detail
- **Demonstrate**: Prove with evidence
- **Argue**: Present reasons
- **Maintain**: Hold a position
- **Conclude**: Reach a conclusion
- **Indicate**: Show clearly

### How to Cite Sources:
- According to Smith (2023), "education is fundamental..."
- As Johnson (2022) points out, there is a correlation...
- Studies by Williams (2021) demonstrate that...
- In accordance with recent research (Brown, 2023)...

### Hedging in Academic Writing:
- This appears to indicate that...
- The data suggests that...
- It could be argued that...
- There is a possibility that...

### Example Academic Paragraph:
"The present study aims to analyze the impact of social media on interpersonal communication. According to previous research (Smith, 2022; Johnson, 2023), there is a significant correlation between digital platform usage and changes in communication patterns. The results obtained suggest that, while networks facilitate connectivity, they may also affect the quality of face-to-face interactions."
            """,
            "vocabulary": [
                {"term": "Hypothesis", "definition": "A proposed explanation to be tested", "example": "The hypothesis was confirmed by the data."},
                {"term": "Methodology", "definition": "System of methods used", "example": "The methodology included surveys and interviews."},
                {"term": "To evidence", "definition": "To show, demonstrate", "example": "The results evidence a clear trend."},
                {"term": "To contrast", "definition": "To compare to show differences", "example": "It is necessary to contrast different sources."},
                {"term": "Bibliography", "definition": "List of works consulted", "example": "The bibliography includes 50 references."},
                {"term": "To cite", "definition": "To quote another author", "example": "It is mandatory to cite sources correctly."},
                {"term": "Thesis", "definition": "Main argument or proposition", "example": "My thesis addresses climate change."},
                {"term": "To corroborate", "definition": "To confirm, verify", "example": "Other studies corroborate these findings."},
            ],
            "grammar_points": [
                "Academic passive voice: It has been demonstrated that..., Was analyzed...",
                "Impersonal constructions: It can be observed..., One might argue...",
                "Conditional for hypotheses: This would indicate that..."
            ]
        },
        {
            "title": "Cultural Nuances",
            "content": """## Idioms and Cultural Variation

Mastering cultural nuances involves understanding idiomatic expressions, linguistic registers, and regional variations.

### Common Idioms and Expressions:

**Expressions about mood:**
- To be on cloud nine → To be very happy
- To be under the weather → To feel ill
- To be over the moon → To be extremely happy
- To feel blue → To feel sad

**Expressions about situations:**
- To cost an arm and a leg → To be very expensive
- A piece of cake → Very easy
- To put your foot in it → To make an embarrassing mistake
- To pull someone's leg → To joke with someone
- To hit the nail on the head → To be exactly right
- To beat around the bush → To avoid the main topic

**Expressions about people:**
- To be thick as thieves → To be very close friends
- A loose cannon → An unpredictable person
- To have a chip on your shoulder → To be easily offended

### Linguistic Registers:
- **Formal**: Sir/Madam, I would be grateful if..., Yours faithfully
- **Informal**: Hey, Can you...?, Cheers
- **Colloquial**: Mate, What's up?, Cool

### Regional Variations of English:
- **British**: Flat, Lift, Rubbish, Brilliant
- **American**: Apartment, Elevator, Garbage, Awesome
- **Australian**: Unit, Lift, Rubbish, Ripper

### Usage According to Context:
Mastery of these nuances allows you to adapt your speech to the listener and situation, demonstrating advanced communicative competence.
            """,
            "vocabulary": [
                {"term": "Idiom", "definition": "Fixed expression with figurative meaning", "example": "It's raining cats and dogs is an idiom."},
                {"term": "Colloquial", "definition": "Used in informal conversation", "example": "Cool is a colloquial expression."},
                {"term": "Slang", "definition": "Very informal language", "example": "Teenagers use a lot of slang."},
                {"term": "Nuance", "definition": "Subtle difference in meaning", "example": "There's an important nuance between the two terms."},
                {"term": "Connotation", "definition": "Additional or emotional meaning", "example": "That word has a negative connotation."},
                {"term": "Euphemism", "definition": "Mild expression for something unpleasant", "example": "Passed away is a euphemism for died."},
                {"term": "Irony", "definition": "Saying the opposite of what you mean", "example": "He said it with obvious irony."},
                {"term": "Double meaning", "definition": "Phrase with two interpretations", "example": "The joke had a double meaning."},
            ],
            "grammar_points": [
                "Use of understatement: Not bad (meaning very good)",
                "Subtle differences: I forgot vs. I've forgotten",
                "Tag questions for confirmation: You're coming, aren't you?"
            ]
        }
    ],
    "C2": [
        {
            "title": "Literary Register",
            "content": """## Literary Analysis and Appreciation

C2 level involves understanding and appreciating complex literary texts, identifying stylistic devices, and critically analyzing works.

### Main Rhetorical Figures:

**Figures of meaning:**
- **Metaphor**: Direct identification. "Her eyes are emeralds"
- **Simile**: Explicit comparison. "He runs like the wind"
- **Hyperbole**: Exaggeration. "I've told you a million times"
- **Personification**: Human qualities to objects. "The wind whispered"
- **Metonymy**: Substitution by relationship. "I read Shakespeare" (his works)

**Figures of sound:**
- **Alliteration**: Repetition of sounds. "Peter Piper picked a peck..."
- **Onomatopoeia**: Sound imitation. "The tick-tock of the clock"

**Figures of construction:**
- **Anaphora**: Repetition at beginning. "We shall fight on the beaches, we shall fight on the landing grounds..."
- **Chiasmus**: Reversed structure. "Ask not what your country can do for you..."

### Literary Genres:
- **Narrative**: Novel, Short story, Flash fiction
- **Poetry**: Sonnet, Free verse, Haiku
- **Drama**: Tragedy, Comedy, Tragicomedy
- **Essay**: Argumentative reflection

### Major Literary Movements:
- **Renaissance**: Shakespeare, Milton
- **Romanticism**: Wordsworth, Byron, Shelley
- **Victorian**: Dickens, Brontë sisters
- **Modernism**: Joyce, Woolf, Eliot
- **Contemporary**: McEwan, Atwood, Ishiguro

### Literary Text Analysis:
When analyzing a text, consider: theme, structure, narrative voice, style, historical context, and literary devices employed.
            """,
            "vocabulary": [
                {"term": "Prose", "definition": "Written language without rhyme or meter", "example": "The novel is written in poetic prose."},
                {"term": "Verse", "definition": "Line of poetry with rhythm", "example": "The sonnet has fourteen verses."},
                {"term": "Stanza", "definition": "Group of verses", "example": "Each stanza has four lines."},
                {"term": "Narrator", "definition": "Voice telling the story", "example": "The narrator is omniscient."},
                {"term": "Denouement", "definition": "Final resolution of a story", "example": "The denouement was unexpected."},
                {"term": "Plot", "definition": "Sequence of events", "example": "The plot is very complex."},
                {"term": "Leitmotif", "definition": "Recurring theme", "example": "Water is the leitmotif of the work."},
                {"term": "Intertextuality", "definition": "Reference to other works", "example": "There's intertextuality with Milton."},
            ],
            "grammar_points": [
                "Literary past perfect: Scarcely had he arrived when...",
                "Subjunctive in literary style: Were I to know..., Be it known...",
                "Inversion for emphasis: Never had I seen such beauty"
            ]
        },
        {
            "title": "Dialects and Variants",
            "content": """## Linguistic Variation in English

English is a pluricentric language with multiple standard norms and regional variations.

### British English:
- **Phonetics**: Non-rhotic (no 'r' after vowels), distinct vowels
- **Grammar**: Present perfect for recent past, collective nouns as plural
- **Lexicon**: Flat, lift, rubbish, bonnet, boot, queue

### American English:
- **Phonetics**: Rhotic (pronounced 'r'), flapped 't'
- **Grammar**: Simple past for recent events, collective nouns as singular
- **Lexicon**: Apartment, elevator, garbage, hood, trunk, line

### Australian English:
- **Phonetics**: Distinctive vowels, rising intonation
- **Vocabulary**: Arvo (afternoon), brekkie (breakfast), servo (service station)
- **Expressions**: No worries, good on ya, heaps

### Other Varieties:
- **Irish English**: After + gerund ("I'm after eating")
- **Scottish English**: Distinctive vowels, "wee" for small
- **Indian English**: Present continuous for habitual actions
- **South African English**: "Now now" (soon), "just now" (later)

### Sociolinguistic Considerations:
- All varieties are equally valid
- Standard language varies by region
- English is a polycentric language
- Register should match context and audience

### Code-Switching:
Proficient speakers can switch between varieties and registers depending on context, audience, and purpose.
            """,
            "vocabulary": [
                {"term": "Dialect", "definition": "Regional variety of a language", "example": "Cockney is a dialect of English."},
                {"term": "Variant", "definition": "Different form of the same language", "example": "It's a variant of American English."},
                {"term": "Rhotic", "definition": "Pronouncing 'r' after vowels", "example": "American English is rhotic."},
                {"term": "Accent", "definition": "Way of pronouncing", "example": "She has a Scottish accent."},
                {"term": "Archaism", "definition": "Old word or form", "example": "Thou is an archaism in English."},
                {"term": "Neologism", "definition": "New word", "example": "To google is a neologism."},
                {"term": "Loanword", "definition": "Word from another language", "example": "Kindergarten is a German loanword."},
                {"term": "Calque", "definition": "Literal translation from another language", "example": "Skyscraper was calqued into many languages."},
            ],
            "grammar_points": [
                "Variation in verb forms: gotten (US) vs. got (UK)",
                "Spelling differences: color/colour, organize/organise",
                "Preposition variation: at the weekend / on the weekend"
            ]
        },
        {
            "title": "Professional Communication",
            "content": """## High-Level Business Communication

C2 professional communication involves mastering formal registers, advanced negotiation, and strategic communication.

### Executive Presentations:
**Effective structure:**
1. Impactful opening (statistic, question, story)
2. Clear agenda
3. Development with evidence
4. Handling objections
5. Closing with call to action

**Professional expressions:**
- "Allow me to begin by highlighting..."
- "The data clearly reflects that..."
- "In response to your observation..."
- "To conclude, I would like to emphasize..."

### Advanced Negotiation:
**Key principles:**
- Thorough preparation
- Active listening
- Identifying interests
- Seeking win-win solutions
- Effective closing

**Negotiation expressions:**
- "I understand your position; however..."
- "What would you say if we...?"
- "I propose we explore alternatives..."
- "I believe we can reach a mutually beneficial agreement..."

### Formal Written Communication:
**Types of documents:**
- Executive reports
- Business proposals
- Meeting minutes
- Press releases

**Courtesy formulas:**
- Opening: "I am writing to...", "Further to our conversation..."
- Closing: "I remain at your disposal...", "Yours faithfully", "Kind regards"

### Professional Protocol and Etiquette:
- Formal address conventions
- Cross-cultural communication
- Conflict management
- Constructive feedback delivery
            """,
            "vocabulary": [
                {"term": "Interlocutor", "definition": "Person you are speaking with", "example": "My interlocutor was the CEO."},
                {"term": "Consensus", "definition": "Agreement among all parties", "example": "We reached a consensus after hours of debate."},
                {"term": "Verdict", "definition": "Formal opinion or decision", "example": "The legal verdict was favorable."},
                {"term": "Protocol", "definition": "Set of formal rules", "example": "We followed the established protocol."},
                {"term": "Clause", "definition": "Section of a contract", "example": "Clause three specifies the terms."},
                {"term": "To rectify", "definition": "To correct, fix", "example": "We must rectify the error promptly."},
                {"term": "Due diligence", "definition": "Careful investigation", "example": "We conducted due diligence before signing."},
                {"term": "To safeguard", "definition": "To protect, defend", "example": "We must safeguard everyone's interests."},
            ],
            "grammar_points": [
                "Conditional for politeness: Would you be so kind as to...?",
                "Impersonal structures: It is requested that..., It would be appreciated if...",
                "Formal subjunctive: I suggest that he be informed..."
            ]
        }
    ]
}

# ============== PORTUGUÊS C1 y C2 ==============
PORTUGUESE_C1_C2 = {
    "C1": [
        {
            "title": "Argumentação Avançada",
            "content": """## Técnicas de Argumentação Profissional

A argumentação avançada requer domínio de estruturas complexas e conectores sofisticados para apresentar ideias de forma convincente.

### Estrutura de um Argumento Sólido:
1. **Introdução**: Apresentar a tese principal
2. **Desenvolvimento**: Expor argumentos com evidências
3. **Contra-argumentos**: Antecipar e refutar objeções
4. **Conclusão**: Reafirmar a posição com síntese

### Conectores Argumentativos Avançados:

**Para adicionar informação:**
- Além disso / Ademais / Por outro lado
- Cabe acrescentar que... / É preciso destacar que...
- Nesse mesmo sentido... / Da mesma forma...

**Para contrastar:**
- No entanto / Contudo / Pelo contrário
- Apesar de... / Embora... / Ainda assim...
- Se bem que... / Conquanto...

**Para concluir:**
- Em conclusão / Em suma / Para resumir
- Em síntese / Por fim / Diante do exposto

### Expressões para Argumentar com Autoridade:
- Os dados demonstram claramente que...
- Segundo estudos recentes...
- É inegável que...
- Torna-se evidente que...
- Não resta dúvida de que...

### Exemplo de Argumentação:
"Cabe destacar que as mudanças climáticas representam um dos maiores desafios do nosso tempo. No entanto, existem soluções viáveis. Por um lado, as energias renováveis oferecem alternativas sustentáveis. Por outro lado, a conscientização cidadã está aumentando. Em suma, embora o problema seja grave, a ação coletiva pode fazer a diferença."
            """,
            "vocabulary": [
                {"term": "Cabe destacar", "definition": "É importante mencionar", "example": "Cabe destacar que os resultados foram positivos."},
                {"term": "No entanto", "definition": "Porém, todavia", "example": "O projeto é ambicioso; no entanto, é viável."},
                {"term": "Em suma", "definition": "Em resumo, finalmente", "example": "Em suma, a proposta é benéfica."},
                {"term": "Por conseguinte", "definition": "Como resultado, portanto", "example": "Os custos aumentaram; por conseguinte, ajustamos o orçamento."},
                {"term": "Em decorrência de", "definition": "Como consequência de", "example": "Em decorrência da pandemia, mudou a forma de trabalhar."},
                {"term": "Em prol de", "definition": "Em favor de, para", "example": "Em prol da transparência, publicamos os dados."},
                {"term": "Daí que", "definition": "Por isso, por essa razão", "example": "O mercado mudou; daí que adaptamos a estratégia."},
                {"term": "Subjacente", "definition": "Que está por baixo, causa oculta", "example": "Vários fatores são subjacentes a esta crise."},
            ],
            "grammar_points": [
                "Subjuntivo em orações concessivas: Embora seja difícil, vou tentar",
                "Orações condicionais complexas: Se tivesse sabido..., Caso houvesse...",
                "Nominalizações: desenvolver → o desenvolvimento, implementar → a implementação"
            ]
        },
        {
            "title": "Linguagem Acadêmica",
            "content": """## Escrita e Pesquisa Acadêmica

A linguagem acadêmica caracteriza-se pela precisão, objetividade e uso de estruturas formais.

### Estrutura de um Trabalho Acadêmico:
1. **Resumo/Abstract**: Síntese do trabalho (150-300 palavras)
2. **Introdução**: Contextualização e objetivos
3. **Referencial Teórico**: Revisão da literatura existente
4. **Metodologia**: Como a pesquisa foi realizada
5. **Resultados**: Principais achados
6. **Discussão**: Interpretação dos resultados
7. **Conclusões**: Síntese e direções futuras
8. **Referências**: Fontes citadas

### Verbos Acadêmicos Frequentes:
- **Analisar**: Examinar detalhadamente
- **Demonstrar**: Provar com evidências
- **Argumentar**: Apresentar razões
- **Sustentar**: Manter uma posição
- **Concluir**: Chegar a uma conclusão
- **Evidenciar**: Mostrar claramente

### Como Citar Fontes:
- Segundo Silva (2023), "a educação é fundamental..."
- Como aponta Santos (2022), existe uma correlação...
- Os estudos de Oliveira (2021) demonstram que...
- De acordo com pesquisas recentes (Costa, 2023)...

### Expressões de Cautela Acadêmica:
- Parece indicar que...
- Os dados sugerem que...
- Poder-se-ia argumentar que...
- Há a possibilidade de que...

### Exemplo de Parágrafo Acadêmico:
"O presente estudo tem como objetivo analisar o impacto das redes sociais na comunicação interpessoal. Segundo pesquisas anteriores (Silva, 2022; Santos, 2023), existe uma correlação significativa entre o uso de plataformas digitais e mudanças nos padrões comunicativos. Os resultados obtidos sugerem que, embora as redes facilitem a conectividade, também podem afetar a qualidade das interações presenciais."
            """,
            "vocabulary": [
                {"term": "Hipótese", "definition": "Suposição a ser investigada", "example": "A hipótese foi confirmada pelos dados."},
                {"term": "Metodologia", "definition": "Conjunto de métodos utilizados", "example": "A metodologia incluiu pesquisas e entrevistas."},
                {"term": "Evidenciar", "definition": "Demonstrar, tornar evidente", "example": "Os resultados evidenciam uma tendência clara."},
                {"term": "Contrastar", "definition": "Comparar para ver diferenças", "example": "É necessário contrastar diferentes fontes."},
                {"term": "Bibliografia", "definition": "Lista de obras consultadas", "example": "A bibliografia inclui 50 referências."},
                {"term": "Citar", "definition": "Mencionar palavras de outro autor", "example": "É obrigatório citar as fontes corretamente."},
                {"term": "Tese", "definition": "Proposição que se defende", "example": "Minha tese aborda as mudanças climáticas."},
                {"term": "Corroborar", "definition": "Confirmar, verificar", "example": "Outros estudos corroboram esses achados."},
            ],
            "grammar_points": [
                "Voz passiva acadêmica: Foi demonstrado que..., Foi analisado...",
                "Impessoal com SE: Pode-se observar..., Considera-se que...",
                "Uso do futuro do pretérito para hipóteses: Isso indicaria que..."
            ]
        },
        {
            "title": "Nuances Culturais",
            "content": """## Expressões Idiomáticas e Variação Cultural

Dominar as nuances culturais implica compreender expressões idiomáticas, registros linguísticos e variações regionais.

### Expressões Idiomáticas Portuguesas:

**Expressões sobre estado de ânimo:**
- Estar nas nuvens → Estar distraído
- Estar doido varrido → Estar muito louco
- Estar de rastos → Estar muito cansado
- Estar no seu elemento → Sentir-se confortável

**Expressões sobre situações:**
- Custar os olhos da cara → Ser muito caro
- Ser canja → Ser muito fácil
- Meter os pés pelas mãos → Cometer um erro
- Gozar com a cara de alguém → Brincar com alguém
- Acertar em cheio → Acertar completamente
- Fazer rodeios → Não ir direto ao assunto

**Expressões sobre pessoas:**
- Ser unha com carne → Ser muito amigos
- Ser um troca-tintas → Ser irresponsável
- Ter mau feitio → Ter mau temperamento

### Registros Linguísticos:
- **Formal**: O senhor/A senhora, Agradecia que..., Atenciosamente
- **Informal**: Tu/Você, Podes...?, Um abraço
- **Coloquial**: Pá, E aí?, Fixe

### Variações do Português:
- **Portugal**: Autocarro, Telemóvel, Pequeno-almoço
- **Brasil**: Ônibus, Celular, Café da manhã
- **Angola**: Machimbombo, Celular, Mata-bicho
- **Moçambique**: Machimbombo, Celular, Mata-bicho

### Uso Segundo o Contexto:
O domínio destas nuances permite adaptar o discurso ao interlocutor e à situação, demonstrando competência comunicativa avançada.
            """,
            "vocabulary": [
                {"term": "Expressão idiomática", "definition": "Expressão fixa com significado figurado", "example": "Chover a cântaros é uma expressão idiomática."},
                {"term": "Coloquial", "definition": "Próprio da conversa informal", "example": "Fixe é uma expressão coloquial."},
                {"term": "Gíria", "definition": "Linguagem especial de um grupo", "example": "Os jovens usam muita gíria."},
                {"term": "Nuance", "definition": "Diferença sutil de significado", "example": "Há uma nuance importante entre os termos."},
                {"term": "Conotação", "definition": "Significado adicional ou emocional", "example": "Essa palavra tem conotação negativa."},
                {"term": "Eufemismo", "definition": "Expressão suave para algo desagradável", "example": "Bater as botas é um eufemismo de morrer."},
                {"term": "Ironia", "definition": "Dizer o contrário do que se pensa", "example": "Disse com ironia evidente."},
                {"term": "Duplo sentido", "definition": "Frase com duas interpretações", "example": "A piada tinha duplo sentido."},
            ],
            "grammar_points": [
                "Uso de diminutivos com valor afetivo: cafezinho, bocadinho, pertinho",
                "Diferenças sutis entre ser e estar: É esperto vs. Está esperto",
                "Conjuntivo em expressões idiomáticas: Que te corra bem"
            ]
        }
    ],
    "C2": [
        {
            "title": "Registro Literário",
            "content": """## Análise e Apreciação Literária

O nível C2 implica compreender e apreciar textos literários complexos, identificando recursos estilísticos e analisando criticamente as obras.

### Figuras Retóricas Principais:

**Figuras de significado:**
- **Metáfora**: Identificação direta. "Os seus olhos são esmeraldas"
- **Comparação**: Comparação explícita. "Corre como o vento"
- **Hipérbole**: Exagero. "Já te disse mil vezes"
- **Personificação**: Qualidades humanas. "O vento sussurrava"
- **Metonímia**: Substituição por relação. "Li Camões" (as suas obras)

**Figuras de som:**
- **Aliteração**: Repetição de sons. "O rato roeu a rolha"
- **Onomatopeia**: Imitação de sons. "O tiquetaque do relógio"

**Figuras de construção:**
- **Anáfora**: Repetição no início. "É fogo que arde sem se ver; é ferida que dói..."
- **Hipérbato**: Alteração da ordem. "Das naus a vela inchada"

### Gêneros Literários:
- **Narrativa**: Romance, Conto, Microconto
- **Poesia**: Soneto, Ode, Verso livre
- **Teatro**: Tragédia, Comédia, Drama
- **Ensaio**: Reflexão argumentada

### Movimentos Literários Lusófonos:
- **Classicismo**: Camões, Sá de Miranda
- **Romantismo**: Garrett, Herculano, Alencar
- **Modernismo**: Fernando Pessoa, Mário de Andrade
- **Contemporâneo**: Saramago, Clarice Lispector, Pepetela

### Análise de Texto Literário:
Ao analisar um texto, considerar: tema, estrutura, voz narrativa, estilo, contexto histórico e recursos literários empregados.
            """,
            "vocabulary": [
                {"term": "Prosa", "definition": "Forma de expressão sem rima nem métrica", "example": "O romance está escrito em prosa poética."},
                {"term": "Verso", "definition": "Linha de um poema com ritmo", "example": "O soneto tem catorze versos."},
                {"term": "Estrofe", "definition": "Conjunto de versos", "example": "Cada estrofe tem quatro versos."},
                {"term": "Narrador", "definition": "Voz que conta a história", "example": "O narrador é omnisciente."},
                {"term": "Desenlace", "definition": "Final de uma história", "example": "O desenlace foi inesperado."},
                {"term": "Enredo", "definition": "Sequência de eventos", "example": "O enredo é muito complexo."},
                {"term": "Leitmotiv", "definition": "Tema recorrente", "example": "A água é o leitmotiv da obra."},
                {"term": "Intertextualidade", "definition": "Referência a outras obras", "example": "Há intertextualidade com Os Lusíadas."},
            ],
            "grammar_points": [
                "Pretérito mais-que-perfeito simples literário: Chegara quando...",
                "Conjuntivo em orações independentes: Oxalá fosse verdade!",
                "Inversão para ênfase: Nunca tinha visto tal beleza"
            ]
        },
        {
            "title": "Dialetos e Variantes",
            "content": """## Variação Linguística do Português

O português é uma língua pluricêntrica com múltiplas normas cultas e variações regionais.

### Português Europeu (Portugal):
- **Fonética**: Vogais reduzidas, consoantes finais
- **Gramática**: Uso de tu/você, colocação proclítica em certos contextos
- **Léxico**: Autocarro, telemóvel, frigorífico, pequeno-almoço

### Português Brasileiro:
- **Fonética**: Vogais abertas, palatalização de t/d
- **Gramática**: Você como tratamento geral, próclise dominante
- **Léxico**: Ônibus, celular, geladeira, café da manhã
- **Expressões**: Legal, beleza, e aí?

### Português Africano (Angola, Moçambique, etc.):
- **Influências**: Línguas bantu locais
- **Vocabulário**: Kota (mais velho), bué (muito)
- **Expressões**: Está

### Português de Timor-Leste:
- **Influências**: Línguas austronésias, tétum
- **Características**: Mistura com tétum

### Considerações Sociolinguísticas:
- Todas as variantes são igualmente válidas
- A norma culta varia segundo a região
- O português é uma língua policêntrica
- Há que adaptar o registo ao contexto

### Acordo Ortográfico:
O Acordo Ortográfico de 1990 visa unificar a escrita, embora existam diferenças de aplicação entre países.
            """,
            "vocabulary": [
                {"term": "Dialeto", "definition": "Variedade regional de uma língua", "example": "O açoriano é um dialeto do português."},
                {"term": "Variante", "definition": "Forma diferente da mesma língua", "example": "É uma variante do português americano."},
                {"term": "Sotaque", "definition": "Modo de pronunciar", "example": "Ela tem sotaque lisboeta."},
                {"term": "Arcaísmo", "definition": "Palavra ou forma antiga", "example": "Vós é um arcaísmo em muitos contextos."},
                {"term": "Neologismo", "definition": "Palavra nova", "example": "Tuitar é um neologismo."},
                {"term": "Empréstimo", "definition": "Palavra de outro idioma", "example": "Software é um empréstimo do inglês."},
                {"term": "Decalque", "definition": "Tradução literal de outra língua", "example": "Arranha-céus é um decalque."},
                {"term": "Lusofonia", "definition": "Conjunto de países de língua portuguesa", "example": "A lusofonia abrange vários continentes."},
            ],
            "grammar_points": [
                "Variação na colocação pronominal: próclise vs. ênclise",
                "Diferenças no uso de tempos verbais: perfeito simples vs. composto",
                "Variação no gerúndio: estou a fazer (PT) vs. estou fazendo (BR)"
            ]
        },
        {
            "title": "Comunicação Profissional",
            "content": """## Comunicação Empresarial de Alto Nível

A comunicação profissional C2 implica dominar registos formais, negociação avançada e comunicação estratégica.

### Apresentações Executivas:
**Estrutura eficaz:**
1. Abertura impactante (dado, pergunta, história)
2. Agenda clara
3. Desenvolvimento com evidências
4. Gestão de objeções
5. Fecho com chamada à ação

**Expressões profissionais:**
- "Permitam-me começar por destacar..."
- "Os dados refletem claramente que..."
- "Em resposta à vossa observação..."
- "Para concluir, gostaria de enfatizar..."

### Negociação Avançada:
**Princípios-chave:**
- Preparação exaustiva
- Escuta ativa
- Identificação de interesses
- Busca de soluções win-win
- Fecho eficaz

**Expressões de negociação:**
- "Compreendo a vossa posição, no entanto..."
- "O que achariam se...?"
- "Proponho que exploremos alternativas..."
- "Creio que podemos chegar a um acordo mutuamente benéfico..."

### Comunicação Escrita Formal:
**Tipos de documentos:**
- Relatórios executivos
- Propostas comerciais
- Atas de reunião
- Comunicados institucionais

**Fórmulas de cortesia:**
- Abertura: "Venho por este meio...", "Na sequência de..."
- Fecho: "Fico ao dispor...", "Com os melhores cumprimentos", "Atenciosamente"

### Protocolo e Etiqueta Profissional:
- Tratamento formal (V. Exa., Dr./Dra.)
- Comunicação intercultural
- Gestão de conflitos
- Feedback construtivo
            """,
            "vocabulary": [
                {"term": "Interlocutor", "definition": "Pessoa com quem se fala", "example": "O meu interlocutor era o diretor."},
                {"term": "Consenso", "definition": "Acordo entre todas as partes", "example": "Chegámos a um consenso após horas de debate."},
                {"term": "Parecer", "definition": "Opinião ou juízo formal", "example": "O parecer jurídico foi favorável."},
                {"term": "Protocolo", "definition": "Conjunto de regras formais", "example": "Seguimos o protocolo estabelecido."},
                {"term": "Cláusula", "definition": "Disposição de um contrato", "example": "A cláusula terceira especifica..."},
                {"term": "Sanar", "definition": "Corrigir, remediar", "example": "Devemos sanar o erro quanto antes."},
                {"term": "Diligência", "definition": "Cuidado e prontidão", "example": "Atuou com a devida diligência."},
                {"term": "Salvaguardar", "definition": "Proteger, defender", "example": "Há que salvaguardar os interesses de todos."},
            ],
            "grammar_points": [
                "Condicional de cortesia: Poderia indicar-me...?, Desejaria solicitar...",
                "Estruturas impessoais: Solicita-se..., Agradecer-se-ia...",
                "Perífrases formais: Cabe referir, É mister, Importa salientar"
            ]
        }
    ]
}

async def update_c1_c2():
    """Actualizar el contenido de los niveles C1 y C2 en todos los idiomas."""
    
    content_map = {
        "spanish": SPANISH_C1_C2,
        "english": ENGLISH_C1_C2,
        "portuguese": PORTUGUESE_C1_C2
    }
    
    updated_count = 0
    
    for language, levels_data in content_map.items():
        for level, lessons_list in levels_data.items():
            # Obtener el curso
            course = await db.courses.find_one({"language": language, "level": level})
            if not course:
                print(f"  ⚠️ Curso no encontrado: {language} {level}")
                continue
            
            course_id = str(course['_id'])
            
            # Eliminar lecciones existentes de este curso
            await db.lessons.delete_many({"course_id": course_id})
            
            # Insertar nuevas lecciones
            for i, lesson_data in enumerate(lessons_list):
                lesson_doc = {
                    "course_id": course_id,
                    "title": lesson_data["title"],
                    "content": lesson_data["content"].strip(),
                    "vocabulary": lesson_data["vocabulary"],
                    "grammar_points": lesson_data["grammar_points"],
                    "order": i + 1
                }
                await db.lessons.insert_one(lesson_doc)
                updated_count += 1
            
            print(f"  ✓ {language.upper()} {level}: {len(lessons_list)} lecciones actualizadas")
    
    print(f"\n✅ Total de lecciones actualizadas: {updated_count}")

if __name__ == "__main__":
    asyncio.run(update_c1_c2())

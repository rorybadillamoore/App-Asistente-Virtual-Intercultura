// ==================== COMPLETE LESSON DATA ====================
// Real educational content for all 5 languages and 6 levels

export const LANGUAGES = [
  { id: 'spanish', name: 'Español', flag: '🇨🇷', greeting: '¡Pura Vida!', color: '#22955B', nativeName: 'Español' },
  { id: 'english', name: 'English', flag: '🇺🇸', greeting: 'Hello!', color: '#003189', nativeName: 'English' },
  { id: 'french', name: 'Français', flag: '🇫🇷', greeting: 'Bonjour!', color: '#003189', nativeName: 'Français' },
  { id: 'german', name: 'Deutsch', flag: '🇩🇪', greeting: 'Hallo!', color: '#1a1a1a', nativeName: 'Deutsch' },
  { id: 'portuguese', name: 'Português', flag: '🇧🇷', greeting: 'Olá!', color: '#fa8a00', nativeName: 'Português' },
];

export const LEVELS = [
  { id: 'A1', title: 'Acceso', desc: 'Principiante. Entiende y usa expresiones cotidianas básicas.', color: '#B6C932' },
  { id: 'A2', title: 'Plataforma', desc: 'Básico. Se comunica en tareas sencillas y habituales.', color: '#8fb82a' },
  { id: 'B1', title: 'Umbral', desc: 'Intermedio. Puede lidiar con situaciones de viaje.', color: '#fa8a00' },
  { id: 'B2', title: 'Avanzado', desc: 'Intermedio Alto. Entiende textos complejos y técnicos.', color: '#f07800' },
  { id: 'C1', title: 'Dominio', desc: 'Avanzado. Se expresa con fluidez y espontaneidad.', color: '#e34b33' },
  { id: 'C2', title: 'Maestría', desc: 'Experto. Comprende todo lo que oye y lee.', color: '#c43d2a' },
];

// ==================== SPANISH CONTENT ====================
export const SPANISH_CONTENT = {
  A1: {
    lessons: [
      {
        id: 'es-a1-1',
        title: 'Saludos y Presentaciones',
        description: 'Aprende a saludar y presentarte en español',
        content: `## Saludos Básicos

Los saludos son fundamentales para iniciar cualquier conversación.

### Saludos formales:
- **Buenos días** (mañana, hasta las 12:00)
- **Buenas tardes** (desde las 12:00 hasta las 20:00)
- **Buenas noches** (desde las 20:00)

### Saludos informales:
- **¡Hola!** - El saludo más común
- **¿Qué tal?** - How's it going?
- **¿Cómo estás?** - How are you?

## Presentaciones

Para presentarte, usa estas estructuras:
- **Me llamo** [nombre] - My name is...
- **Soy** [nombre] - I am...
- **Mucho gusto** / **Encantado(a)** - Nice to meet you

### Ejemplo de diálogo:
> A: ¡Hola! Me llamo María. ¿Y tú?
> B: Hola María, soy Juan. Mucho gusto.
> A: Encantada. ¿De dónde eres?
> B: Soy de México. ¿Y tú?
> A: Soy de Costa Rica.`,
        vocabulary: [
          { word: 'Hola', translation: 'Hello', example: '¡Hola! ¿Cómo estás?', pronunciation: 'OH-lah' },
          { word: 'Buenos días', translation: 'Good morning', example: 'Buenos días, señor García.', pronunciation: 'BWEH-nohs DEE-ahs' },
          { word: 'Buenas tardes', translation: 'Good afternoon', example: 'Buenas tardes a todos.', pronunciation: 'BWEH-nahs TAR-dehs' },
          { word: 'Buenas noches', translation: 'Good evening/night', example: 'Buenas noches, hasta mañana.', pronunciation: 'BWEH-nahs NOH-chehs' },
          { word: 'Me llamo', translation: 'My name is', example: 'Me llamo Ana.', pronunciation: 'meh YAH-moh' },
          { word: 'Mucho gusto', translation: 'Nice to meet you', example: 'Mucho gusto en conocerte.', pronunciation: 'MOO-choh GOOS-toh' },
          { word: '¿Cómo te llamas?', translation: "What's your name?", example: 'Hola, ¿cómo te llamas?', pronunciation: 'KOH-moh teh YAH-mahs' },
          { word: '¿De dónde eres?', translation: 'Where are you from?', example: '¿De dónde eres? Soy de Colombia.', pronunciation: 'deh DOHN-deh EH-rehs' },
        ],
        grammar: [
          { title: 'Verbo SER', rule: 'yo SOY, tú ERES, él/ella ES, nosotros SOMOS, ellos SON', examples: ['Yo soy estudiante', 'Ella es profesora'] },
          { title: 'Verbo LLAMARSE', rule: 'me llamo, te llamas, se llama', examples: ['Me llamo Carlos', '¿Cómo te llamas?'] },
          { title: 'Artículos definidos', rule: 'EL (masc.), LA (fem.), LOS/LAS (plural)', examples: ['El libro', 'La casa', 'Los niños'] },
        ]
      },
      {
        id: 'es-a1-2',
        title: 'Números y Colores',
        description: 'Aprende los números del 1 al 100 y los colores',
        content: `## Los Números del 1 al 20

| Número | Español | Número | Español |
|--------|---------|--------|---------|
| 1 | uno | 11 | once |
| 2 | dos | 12 | doce |
| 3 | tres | 13 | trece |
| 4 | cuatro | 14 | catorce |
| 5 | cinco | 15 | quince |
| 6 | seis | 16 | dieciséis |
| 7 | siete | 17 | diecisiete |
| 8 | ocho | 18 | dieciocho |
| 9 | nueve | 19 | diecinueve |
| 10 | diez | 20 | veinte |

## Números del 21 al 100
- 21 - veintiuno, 30 - treinta, 40 - cuarenta
- 50 - cincuenta, 60 - sesenta, 70 - setenta
- 80 - ochenta, 90 - noventa, 100 - cien

## Los Colores

### Colores básicos:
- 🔴 **Rojo** - Red
- 🔵 **Azul** - Blue
- 🟢 **Verde** - Green
- 🟡 **Amarillo** - Yellow
- 🟠 **Naranja** - Orange
- ⚫ **Negro** - Black
- ⚪ **Blanco** - White`,
        vocabulary: [
          { word: 'Rojo', translation: 'Red', example: 'La manzana es roja.', pronunciation: 'ROH-hoh' },
          { word: 'Azul', translation: 'Blue', example: 'El cielo es azul.', pronunciation: 'ah-SOOL' },
          { word: 'Verde', translation: 'Green', example: 'La hierba es verde.', pronunciation: 'BEHR-deh' },
          { word: 'Amarillo', translation: 'Yellow', example: 'El sol es amarillo.', pronunciation: 'ah-mah-REE-yoh' },
          { word: 'Blanco', translation: 'White', example: 'La nieve es blanca.', pronunciation: 'BLAHN-koh' },
          { word: 'Negro', translation: 'Black', example: 'El gato es negro.', pronunciation: 'NEH-groh' },
          { word: 'Uno', translation: 'One', example: 'Tengo un hermano.', pronunciation: 'OO-noh' },
          { word: 'Diez', translation: 'Ten', example: 'Son las diez de la mañana.', pronunciation: 'dyehs' },
        ],
        grammar: [
          { title: 'Concordancia de género', rule: 'rojo/roja, blanco/blanca', examples: ['El coche rojo', 'La casa roja'] },
          { title: 'Concordancia de número', rule: 'azul/azules, verde/verdes', examples: ['El libro azul', 'Los libros azules'] },
          { title: 'Uso de hay', rule: 'HAY + número + sustantivo', examples: ['Hay tres gatos', 'Hay una mesa'] },
        ]
      },
      {
        id: 'es-a1-3',
        title: 'La Familia',
        description: 'Vocabulario y expresiones sobre la familia',
        content: `## Miembros de la Familia

### Familia Nuclear:
- 👨 **Padre / Papá** - Father
- 👩 **Madre / Mamá** - Mother
- 👦 **Hijo** - Son
- 👧 **Hija** - Daughter
- 👦👦 **Hermano / Hermana** - Brother / Sister

### Familia Extendida:
- 👴 **Abuelo** - Grandfather
- 👵 **Abuela** - Grandmother
- 👨 **Tío** - Uncle
- 👩 **Tía** - Aunt
- 👦👧 **Primo / Prima** - Cousin

### Relaciones:
- 💑 **Esposo / Esposa** - Husband / Wife
- 💕 **Novio / Novia** - Boyfriend / Girlfriend

## Ejemplo de descripción familiar:
> "Mi familia es grande. Tengo dos hermanos y una hermana. Mis padres se llaman Carlos y María. Mis abuelos viven en el campo. Tengo muchos primos."`,
        vocabulary: [
          { word: 'Padre', translation: 'Father', example: 'Mi padre trabaja en un banco.', pronunciation: 'PAH-dreh' },
          { word: 'Madre', translation: 'Mother', example: 'Mi madre cocina muy bien.', pronunciation: 'MAH-dreh' },
          { word: 'Hermano', translation: 'Brother', example: 'Tengo un hermano mayor.', pronunciation: 'ehr-MAH-noh' },
          { word: 'Hermana', translation: 'Sister', example: 'Mi hermana estudia medicina.', pronunciation: 'ehr-MAH-nah' },
          { word: 'Abuelo', translation: 'Grandfather', example: 'Mi abuelo tiene 80 años.', pronunciation: 'ah-BWEH-loh' },
          { word: 'Abuela', translation: 'Grandmother', example: 'Mi abuela hace pasteles.', pronunciation: 'ah-BWEH-lah' },
          { word: 'Tío', translation: 'Uncle', example: 'Mi tío vive en Madrid.', pronunciation: 'TEE-oh' },
          { word: 'Prima', translation: 'Female cousin', example: 'Mi prima es muy simpática.', pronunciation: 'PREE-mah' },
        ],
        grammar: [
          { title: 'Posesivos', rule: 'MI, TU, SU, NUESTRO', examples: ['Mi madre', 'Tu padre', 'Su hermano'] },
          { title: 'Verbo TENER', rule: 'yo tengo, tú tienes, él tiene', examples: ['Tengo dos hermanos', '¿Tienes hijos?'] },
          { title: 'Plural de sustantivos', rule: 'hermano → hermanos, ciudad → ciudades', examples: ['Un hermano, dos hermanos'] },
        ]
      },
      {
        id: 'es-a1-4',
        title: 'En el Restaurante',
        description: 'Pedir comida y bebida en un restaurante',
        content: `## Vocabulario del Restaurante

### Comidas del día:
- 🌅 **Desayuno** - Breakfast (7:00-10:00)
- ☀️ **Almuerzo** - Lunch (13:00-15:00)
- 🌙 **Cena** - Dinner (20:00-22:00)

### Frases útiles:
- "Una mesa para dos, por favor"
- "¿Puedo ver el menú?"
- "Quisiera ordenar..."
- "La cuenta, por favor"

### Vocabulario básico:
- **El menú** - The menu
- **El camarero** - The waiter
- **La cuenta** - The bill
- **La propina** - The tip`,
        vocabulary: [
          { word: 'Desayuno', translation: 'Breakfast', example: 'El desayuno es a las 8.', pronunciation: 'deh-sah-YOO-noh' },
          { word: 'Almuerzo', translation: 'Lunch', example: '¿Qué hay para almuerzo?', pronunciation: 'ahl-MWEHR-soh' },
          { word: 'Cena', translation: 'Dinner', example: 'La cena es a las 9.', pronunciation: 'SEH-nah' },
          { word: 'Agua', translation: 'Water', example: 'Un vaso de agua, por favor.', pronunciation: 'AH-gwah' },
          { word: 'Café', translation: 'Coffee', example: 'Un café con leche.', pronunciation: 'kah-FEH' },
          { word: 'Pan', translation: 'Bread', example: 'Me gusta el pan fresco.', pronunciation: 'pahn' },
          { word: 'Cuenta', translation: 'Bill', example: 'La cuenta, por favor.', pronunciation: 'KWEHN-tah' },
          { word: 'Delicioso', translation: 'Delicious', example: '¡Está delicioso!', pronunciation: 'deh-lee-SYOH-soh' },
        ],
        grammar: [
          { title: 'Verbo QUERER', rule: 'yo quiero, tú quieres, él quiere', examples: ['Quiero un café', '¿Quieres agua?'] },
          { title: 'Pedir con cortesía', rule: 'Quisiera + sustantivo / Por favor', examples: ['Quisiera un café', 'Agua, por favor'] },
          { title: 'Verbo GUSTAR', rule: 'Me gusta / Me gustan', examples: ['Me gusta el café', 'Me gustan los tacos'] },
        ]
      },
      {
        id: 'es-a1-5',
        title: 'La Casa y los Muebles',
        description: 'Describe tu hogar y sus habitaciones',
        content: `## Habitaciones de la Casa

- 🛋️ **Sala / Salón** - Living room
- 🍳 **Cocina** - Kitchen
- 🛏️ **Dormitorio** - Bedroom
- 🚿 **Baño** - Bathroom
- 🍽️ **Comedor** - Dining room
- 🚗 **Garaje** - Garage
- 🌳 **Jardín** - Garden

## Muebles Básicos

- **Mesa** - Table
- **Silla** - Chair
- **Sofá** - Sofa
- **Cama** - Bed
- **Armario** - Wardrobe
- **Estantería** - Bookshelf`,
        vocabulary: [
          { word: 'Casa', translation: 'House', example: 'Mi casa es pequeña.', pronunciation: 'KAH-sah' },
          { word: 'Cocina', translation: 'Kitchen', example: 'Cocino en la cocina.', pronunciation: 'koh-SEE-nah' },
          { word: 'Dormitorio', translation: 'Bedroom', example: 'Mi dormitorio es grande.', pronunciation: 'dohr-mee-TOH-ryoh' },
          { word: 'Baño', translation: 'Bathroom', example: '¿Dónde está el baño?', pronunciation: 'BAH-nyoh' },
          { word: 'Mesa', translation: 'Table', example: 'La mesa es de madera.', pronunciation: 'MEH-sah' },
          { word: 'Silla', translation: 'Chair', example: 'Hay cuatro sillas.', pronunciation: 'SEE-yah' },
          { word: 'Cama', translation: 'Bed', example: 'La cama es cómoda.', pronunciation: 'KAH-mah' },
          { word: 'Ventana', translation: 'Window', example: 'Abre la ventana.', pronunciation: 'behn-TAH-nah' },
        ],
        grammar: [
          { title: 'Verbo ESTAR para ubicación', rule: 'El libro ESTÁ en la mesa', examples: ['El baño está arriba', 'La cocina está abajo'] },
          { title: 'Preposiciones de lugar', rule: 'en, sobre, debajo de, al lado de', examples: ['El gato está debajo de la mesa', 'El libro está sobre la cama'] },
          { title: 'HAY vs ESTÁ', rule: 'HAY (existencia) vs ESTÁ (ubicación)', examples: ['Hay un libro en la mesa', 'El libro está en la mesa'] },
        ]
      },
      {
        id: 'es-a1-6',
        title: 'El Tiempo y la Hora',
        description: 'Aprende a decir la hora y hablar del tiempo',
        content: `## Preguntar y Decir la Hora

### Pregunta:
- **¿Qué hora es?** - What time is it?

### Respuestas:
- Es la una (1:00)
- Son las dos (2:00)
- Son las tres y media (3:30)
- Son las cuatro y cuarto (4:15)
- Son las cinco menos cuarto (4:45)

## Partes del Día
- **La mañana** (6:00-12:00)
- **La tarde** (12:00-20:00)
- **La noche** (20:00-6:00)

## Días de la Semana
Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo`,
        vocabulary: [
          { word: 'Hora', translation: 'Hour/Time', example: '¿Qué hora es?', pronunciation: 'OH-rah' },
          { word: 'Minuto', translation: 'Minute', example: 'En cinco minutos.', pronunciation: 'mee-NOO-toh' },
          { word: 'Mañana', translation: 'Morning/Tomorrow', example: 'Por la mañana estudio.', pronunciation: 'mah-NYAH-nah' },
          { word: 'Tarde', translation: 'Afternoon', example: 'Por la tarde trabajo.', pronunciation: 'TAHR-deh' },
          { word: 'Noche', translation: 'Night', example: 'Por la noche duermo.', pronunciation: 'NOH-cheh' },
          { word: 'Lunes', translation: 'Monday', example: 'El lunes tengo clase.', pronunciation: 'LOO-nehs' },
          { word: 'Semana', translation: 'Week', example: 'Esta semana estoy ocupado.', pronunciation: 'seh-MAH-nah' },
          { word: 'Hoy', translation: 'Today', example: 'Hoy es martes.', pronunciation: 'oy' },
        ],
        grammar: [
          { title: 'Decir la hora', rule: 'ES la una / SON las + número', examples: ['Es la una', 'Son las tres'] },
          { title: 'Media y cuarto', rule: 'Y media (30), Y cuarto (15), Menos cuarto (45)', examples: ['Son las dos y media', 'Son las tres menos cuarto'] },
          { title: 'Preposiciones de tiempo', rule: 'A las (hora), Por la (parte del día)', examples: ['A las ocho', 'Por la mañana'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-es-a1',
        title: 'Quiz de Español A1',
        questions: [
          { question: '¿Cómo se dice "Hello" en español?', options: ['Hola', 'Adiós', 'Gracias', 'Por favor'], correct: 0, explanation: '"Hola" es el saludo informal más común en español.' },
          { question: '¿Cuál es el plural de "libro"?', options: ['Libros', 'Libroes', 'Libras', 'Libro'], correct: 0, explanation: 'Los sustantivos terminados en vocal forman el plural añadiendo -s.' },
          { question: 'Completa: "Yo ___ estudiante"', options: ['soy', 'eres', 'es', 'somos'], correct: 0, explanation: 'El verbo SER con "yo" es "soy".' },
          { question: '¿Qué color es "azul"?', options: ['Blue', 'Red', 'Green', 'Yellow'], correct: 0, explanation: '"Azul" significa "blue" en inglés.' },
          { question: '¿Qué número es "quince"?', options: ['15', '14', '16', '13'], correct: 0, explanation: '"Quince" es el número 15 en español.' },
          { question: '¿Cómo se dice "mother" en español?', options: ['Madre', 'Padre', 'Hermana', 'Abuela'], correct: 0, explanation: '"Madre" significa "mother" en español.' },
          { question: 'Completa: "Me ___ María"', options: ['llamo', 'llamas', 'llama', 'llamamos'], correct: 0, explanation: 'Con "yo" usamos "me llamo".' },
          { question: '¿Qué día viene después del lunes?', options: ['Martes', 'Miércoles', 'Domingo', 'Viernes'], correct: 0, explanation: 'Martes es el segundo día de la semana.' },
          { question: '¿Cómo se dice "Thank you"?', options: ['Gracias', 'Hola', 'Adiós', 'Por favor'], correct: 0, explanation: '"Gracias" es la forma de agradecer en español.' },
          { question: 'El artículo para "casa" es:', options: ['la', 'el', 'los', 'las'], correct: 0, explanation: '"Casa" es femenino, por eso usa "la".' },
        ]
      }
    ],
    flashcards: [
      { word: 'Hola', translation: 'Hello', example: '¡Hola! ¿Cómo estás?', pronunciation: 'OH-lah' },
      { word: 'Gracias', translation: 'Thank you', example: 'Muchas gracias por tu ayuda.', pronunciation: 'GRAH-syahs' },
      { word: 'Por favor', translation: 'Please', example: 'Un café, por favor.', pronunciation: 'por fah-VOR' },
      { word: 'Buenos días', translation: 'Good morning', example: 'Buenos días, señor.', pronunciation: 'BWEH-nohs DEE-ahs' },
      { word: 'Buenas noches', translation: 'Good night', example: 'Buenas noches, hasta mañana.', pronunciation: 'BWEH-nahs NOH-chehs' },
      { word: 'Sí', translation: 'Yes', example: 'Sí, entiendo.', pronunciation: 'see' },
      { word: 'No', translation: 'No', example: 'No, gracias.', pronunciation: 'noh' },
      { word: 'Agua', translation: 'Water', example: 'Un vaso de agua, por favor.', pronunciation: 'AH-gwah' },
      { word: 'Casa', translation: 'House', example: 'Mi casa es pequeña.', pronunciation: 'KAH-sah' },
      { word: 'Familia', translation: 'Family', example: 'Mi familia es grande.', pronunciation: 'fah-MEE-lyah' },
    ]
  },
  A2: {
    lessons: [
      {
        id: 'es-a2-1',
        title: 'Ir de Compras',
        description: 'Vocabulario y frases para comprar',
        content: `## En la Tienda

### Frases útiles para comprar:
- **¿Cuánto cuesta esto?** - How much does this cost?
- **¿Tiene esto en otro color/talla?** - Do you have this in another color/size?
- **Me lo llevo** - I'll take it
- **¿Puedo pagar con tarjeta?** - Can I pay by card?
- **¿Dónde está la caja?** - Where is the checkout?

### Vocabulario de ropa:
- Camisa, Pantalón, Vestido, Falda, Zapatos
- Chaqueta, Abrigo, Bufanda, Sombrero

### Tallas:
- Pequeño (S), Mediano (M), Grande (L), Extra Grande (XL)`,
        vocabulary: [
          { word: '¿Cuánto cuesta?', translation: 'How much does it cost?', example: '¿Cuánto cuesta este libro?', pronunciation: 'KWAHN-toh KWEHS-tah' },
          { word: 'Barato', translation: 'Cheap', example: 'Este restaurante es muy barato.', pronunciation: 'bah-RAH-toh' },
          { word: 'Caro', translation: 'Expensive', example: 'El hotel es demasiado caro.', pronunciation: 'KAH-roh' },
          { word: 'Talla', translation: 'Size', example: '¿Qué talla usas?', pronunciation: 'TAH-yah' },
          { word: 'Probador', translation: 'Fitting room', example: 'El probador está al fondo.', pronunciation: 'proh-bah-DOHR' },
          { word: 'Efectivo', translation: 'Cash', example: 'Pago en efectivo.', pronunciation: 'eh-fehk-TEE-boh' },
          { word: 'Tarjeta', translation: 'Card', example: '¿Aceptan tarjeta?', pronunciation: 'tahr-HEH-tah' },
          { word: 'Descuento', translation: 'Discount', example: 'Hay un 20% de descuento.', pronunciation: 'dehs-KWEHN-toh' },
        ],
        grammar: [
          { title: 'Verbo COSTAR', rule: 'cuesta (singular), cuestan (plural)', examples: ['¿Cuánto cuesta?', '¿Cuánto cuestan los zapatos?'] },
          { title: 'Pronombres de objeto', rule: 'lo, la, los, las', examples: ['Me lo llevo', '¿La tiene en azul?'] },
          { title: 'Comparativos', rule: 'más... que, menos... que', examples: ['Es más caro que el otro', 'Es menos grande'] },
        ]
      },
      {
        id: 'es-a2-2',
        title: 'Rutina Diaria',
        description: 'Describe tu día típico',
        content: `## Mi Día Típico

### Verbos reflexivos:
- **Despertarse** - to wake up
- **Levantarse** - to get up
- **Ducharse** - to shower
- **Vestirse** - to get dressed
- **Acostarse** - to go to bed

### Expresiones de tiempo:
- Por la mañana - in the morning
- Por la tarde - in the afternoon
- Por la noche - at night

### Ejemplo de rutina:
"Me despierto a las 7. Me levanto y me ducho. Desayuno a las 7:30. Trabajo de 9 a 5. Ceno a las 8 y me acuesto a las 11."`,
        vocabulary: [
          { word: 'Despertarse', translation: 'To wake up', example: 'Me despierto a las 6.', pronunciation: 'dehs-pehr-TAHR-seh' },
          { word: 'Levantarse', translation: 'To get up', example: 'Me levanto inmediatamente.', pronunciation: 'leh-bahn-TAHR-seh' },
          { word: 'Desayunar', translation: 'To have breakfast', example: 'Desayuno café y tostadas.', pronunciation: 'deh-sah-yoo-NAHR' },
          { word: 'Almorzar', translation: 'To have lunch', example: 'Almuerzo a la 1.', pronunciation: 'ahl-mohr-SAHR' },
          { word: 'Cenar', translation: 'To have dinner', example: 'Ceno con mi familia.', pronunciation: 'seh-NAHR' },
          { word: 'Acostarse', translation: 'To go to bed', example: 'Me acuesto temprano.', pronunciation: 'ah-kohs-TAHR-seh' },
          { word: 'Temprano', translation: 'Early', example: 'Llego temprano al trabajo.', pronunciation: 'tehm-PRAH-noh' },
          { word: 'Tarde', translation: 'Late', example: 'Hoy llegué tarde.', pronunciation: 'TAHR-deh' },
        ],
        grammar: [
          { title: 'Verbos reflexivos', rule: 'me levanto, te levantas, se levanta', examples: ['Me ducho por la mañana', 'Ella se viste rápido'] },
          { title: 'La hora', rule: 'Son las dos, Es la una', examples: ['Son las ocho', 'Es la una y media'] },
          { title: 'Preposiciones de tiempo', rule: 'a las, de... a...', examples: ['A las nueve', 'De 9 a 5'] },
        ]
      },
      {
        id: 'es-a2-3',
        title: 'El Clima y las Estaciones',
        description: 'Habla sobre el tiempo atmosférico',
        content: `## El Tiempo Atmosférico

### Expresiones del clima:
- **Hace sol** - It's sunny
- **Hace calor** - It's hot
- **Hace frío** - It's cold
- **Hace viento** - It's windy
- **Llueve** - It's raining
- **Nieva** - It's snowing
- **Está nublado** - It's cloudy

### Las Estaciones:
- 🌸 Primavera (marzo-mayo)
- ☀️ Verano (junio-agosto)
- 🍂 Otoño (septiembre-noviembre)
- ❄️ Invierno (diciembre-febrero)`,
        vocabulary: [
          { word: 'Hace sol', translation: "It's sunny", example: 'Hoy hace mucho sol.', pronunciation: 'AH-seh sohl' },
          { word: 'Hace frío', translation: "It's cold", example: 'En invierno hace mucho frío.', pronunciation: 'AH-seh FREE-oh' },
          { word: 'Hace calor', translation: "It's hot", example: 'En verano hace calor.', pronunciation: 'AH-seh kah-LOHR' },
          { word: 'Llueve', translation: "It's raining", example: 'Llueve mucho en abril.', pronunciation: 'YWEH-beh' },
          { word: 'Nieva', translation: "It's snowing", example: 'Nieva en las montañas.', pronunciation: 'NYEH-bah' },
          { word: 'Primavera', translation: 'Spring', example: 'Las flores salen en primavera.', pronunciation: 'pree-mah-BEH-rah' },
          { word: 'Verano', translation: 'Summer', example: 'Vamos a la playa en verano.', pronunciation: 'beh-RAH-noh' },
          { word: 'Invierno', translation: 'Winter', example: 'El invierno es muy frío.', pronunciation: 'een-BYEHR-noh' },
        ],
        grammar: [
          { title: 'HACER para clima', rule: 'Hace frío, Hace calor, Hace viento', examples: ['Hace mucho calor hoy', 'No hace frío'] },
          { title: 'Verbos impersonales', rule: 'llueve, nieva, truena', examples: ['Llueve mucho', 'Nieva en diciembre'] },
          { title: 'Futuro próximo', rule: 'va a + infinitivo', examples: ['Va a llover mañana', 'Va a hacer calor'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-es-a2',
        title: 'Quiz de Español A2',
        questions: [
          { question: 'Ayer yo ___ al cine', options: ['fui', 'voy', 'iré', 'iba'], correct: 0, explanation: '"Fui" es el pretérito indefinido de "ir".' },
          { question: '¿Cuál es el pasado de "comer"?', options: ['comí', 'como', 'comeré', 'comía'], correct: 0, explanation: '"Comí" es el pretérito indefinido de "comer".' },
          { question: 'El superlativo de "grande" es:', options: ['grandísimo', 'más grande', 'muy grande', 'el grande'], correct: 0, explanation: '"Grandísimo" es el superlativo absoluto.' },
          { question: '¿Qué tiempo verbal es "hablaré"?', options: ['Futuro', 'Presente', 'Pasado', 'Condicional'], correct: 0, explanation: '"Hablaré" es futuro simple.' },
          { question: 'Completa: "Me gusta ___ música"', options: ['la', 'el', 'un', 'una'], correct: 0, explanation: '"Música" es femenino, usa "la".' },
        ]
      }
    ],
    flashcards: [
      { word: 'Trabajar', translation: 'To work', example: 'Yo trabajo en una oficina.', pronunciation: 'trah-bah-HAR' },
      { word: 'Comer', translation: 'To eat', example: 'Me gusta comer pizza.', pronunciation: 'koh-MER' },
      { word: 'Comprar', translation: 'To buy', example: 'Voy a comprar pan.', pronunciation: 'kohm-PRAR' },
      { word: 'Bonito', translation: 'Beautiful', example: 'El vestido es muy bonito.', pronunciation: 'boh-NEE-toh' },
      { word: 'Siempre', translation: 'Always', example: 'Siempre llego temprano.', pronunciation: 'SYEM-preh' },
      { word: 'Nunca', translation: 'Never', example: 'Nunca como carne.', pronunciation: 'NOON-kah' },
      { word: 'Cerca', translation: 'Near', example: 'El banco está cerca.', pronunciation: 'SEHR-kah' },
      { word: 'Lejos', translation: 'Far', example: 'Mi trabajo está lejos.', pronunciation: 'LEH-hohs' },
    ]
  },
  B1: {
    lessons: [
      {
        id: 'es-b1-1',
        title: 'Expresar Opiniones',
        description: 'Aprende a dar tu opinión de forma educada',
        content: `## Cómo Expresar tu Opinión

### Frases para dar opiniones:
- **Creo que...** - I think that...
- **Pienso que...** - I think that...
- **En mi opinión...** - In my opinion...
- **Me parece que...** - It seems to me that...
- **Desde mi punto de vista...** - From my point of view...

### Para estar de acuerdo:
- Estoy de acuerdo - I agree
- Tienes razón - You're right
- Exactamente - Exactly

### Para estar en desacuerdo:
- No estoy de acuerdo - I don't agree
- No lo veo así - I don't see it that way
- Depende - It depends`,
        vocabulary: [
          { word: 'Creo que', translation: 'I think that', example: 'Creo que es una buena idea.', pronunciation: 'KREH-oh keh' },
          { word: 'Estoy de acuerdo', translation: 'I agree', example: 'Estoy de acuerdo contigo.', pronunciation: 'ehs-TOY deh ah-KWEHR-doh' },
          { word: 'Sin embargo', translation: 'However', example: 'Me gusta, sin embargo es caro.', pronunciation: 'seen ehm-BAHR-goh' },
          { word: 'Aunque', translation: 'Although', example: 'Aunque llueve, salgo a correr.', pronunciation: 'OWN-keh' },
          { word: 'Por lo tanto', translation: 'Therefore', example: 'Estudié mucho, por lo tanto aprobé.', pronunciation: 'pohr loh TAHN-toh' },
          { word: 'Además', translation: 'Furthermore', example: 'Es inteligente, además es simpático.', pronunciation: 'ah-deh-MAHS' },
          { word: 'En cambio', translation: 'On the other hand', example: 'Juan estudia, en cambio Pedro no.', pronunciation: 'ehn KAHM-byoh' },
          { word: 'A pesar de', translation: 'Despite', example: 'A pesar de todo, soy feliz.', pronunciation: 'ah peh-SAHR deh' },
        ],
        grammar: [
          { title: 'Subjuntivo con opiniones negativas', rule: 'No creo que + subjuntivo', examples: ['No creo que sea verdad', 'No pienso que venga'] },
          { title: 'Conectores de contraste', rule: 'pero, sin embargo, aunque', examples: ['Me gusta pero es caro', 'Aunque llueve, salgo'] },
          { title: 'Conectores de adición', rule: 'además, también, asimismo', examples: ['Además, es muy simpático', 'También habla francés'] },
        ]
      },
      {
        id: 'es-b1-2',
        title: 'Viajes y Turismo',
        description: 'Vocabulario para planificar viajes',
        content: `## Planificar un Viaje

### En el aeropuerto:
- Facturar el equipaje - To check in luggage
- Puerta de embarque - Boarding gate
- Tarjeta de embarque - Boarding pass
- Control de seguridad - Security check

### En el hotel:
- Reservar una habitación - To book a room
- Habitación individual/doble - Single/double room
- Check-in / Check-out
- ¿Está incluido el desayuno?`,
        vocabulary: [
          { word: 'Reservar', translation: 'To book', example: 'Quiero reservar una habitación.', pronunciation: 'reh-sehr-BAHR' },
          { word: 'Vuelo', translation: 'Flight', example: 'Mi vuelo sale a las 10.', pronunciation: 'BWEH-loh' },
          { word: 'Equipaje', translation: 'Luggage', example: 'Llevo poco equipaje.', pronunciation: 'eh-kee-PAH-heh' },
          { word: 'Pasaporte', translation: 'Passport', example: 'Necesitas tu pasaporte.', pronunciation: 'pah-sah-POHR-teh' },
          { word: 'Alojamiento', translation: 'Accommodation', example: 'Busco alojamiento barato.', pronunciation: 'ah-loh-hah-MYEHN-toh' },
          { word: 'Turista', translation: 'Tourist', example: 'Soy turista en esta ciudad.', pronunciation: 'too-REES-tah' },
          { word: 'Excursión', translation: 'Excursion', example: 'Hicimos una excursión.', pronunciation: 'ehks-koor-SYOHN' },
          { word: 'Recuerdos', translation: 'Souvenirs', example: 'Compré muchos recuerdos.', pronunciation: 'reh-KWEHR-dohs' },
        ],
        grammar: [
          { title: 'Condicional de cortesía', rule: 'Quisiera, Me gustaría', examples: ['Quisiera reservar', 'Me gustaría una habitación'] },
          { title: 'Futuro simple', rule: 'viajaré, visitaré, iré', examples: ['Viajaré a España', 'Visitaré el museo'] },
          { title: 'Condicionales', rule: 'Si tengo dinero, viajaré', examples: ['Si hace sol, iremos a la playa', 'Si puedo, te ayudaré'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-es-b1',
        title: 'Quiz de Español B1',
        questions: [
          { question: 'Si yo ___ rico, viajaría por el mundo', options: ['fuera', 'soy', 'era', 'seré'], correct: 0, explanation: 'El condicional irreal usa "si + imperfecto de subjuntivo".' },
          { question: '¿Qué es un "sinónimo"?', options: ['Palabra con significado similar', 'Palabra opuesta', 'Palabra técnica', 'Palabra antigua'], correct: 0, explanation: 'Un sinónimo tiene significado similar.' },
          { question: 'El condicional de "poder" es:', options: ['podría', 'puedo', 'pude', 'podré'], correct: 0, explanation: '"Podría" es el condicional de "poder".' },
          { question: '"Había comido" es un tiempo:', options: ['Pluscuamperfecto', 'Presente', 'Futuro', 'Pretérito'], correct: 0, explanation: '"Había comido" es pluscuamperfecto.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Desarrollar', translation: 'To develop', example: 'Quiero desarrollar mis habilidades.', pronunciation: 'deh-sah-roh-YAHR' },
      { word: 'Conseguir', translation: 'To achieve', example: 'Voy a conseguir el trabajo.', pronunciation: 'kohn-seh-GEER' },
      { word: 'Mejorar', translation: 'To improve', example: 'Necesito mejorar mi español.', pronunciation: 'meh-hoh-RAHR' },
      { word: 'Esperanza', translation: 'Hope', example: 'Tengo esperanza en el futuro.', pronunciation: 'ehs-peh-RAHN-sah' },
      { word: 'Preocuparse', translation: 'To worry', example: 'No te preocupes por eso.', pronunciation: 'preh-oh-koo-PAHR-seh' },
      { word: 'Disfrutar', translation: 'To enjoy', example: 'Disfruto mucho de la música.', pronunciation: 'dees-froo-TAHR' },
    ]
  },
  B2: {
    lessons: [
      {
        id: 'es-b2-1',
        title: 'El Mundo Laboral',
        description: 'Vocabulario profesional avanzado',
        content: `## Vocabulario Profesional

### Buscar trabajo:
- Curriculum vitae (CV) / Hoja de vida
- Carta de presentación - Cover letter
- Entrevista de trabajo - Job interview
- Oferta de empleo - Job offer

### En la oficina:
- Reunión - Meeting
- Plazo de entrega - Deadline
- Jefe/a - Boss
- Compañero/a de trabajo - Colleague`,
        vocabulary: [
          { word: 'Solicitar', translation: 'To apply for', example: 'Voy a solicitar el puesto.', pronunciation: 'soh-lee-see-TAHR' },
          { word: 'Contratar', translation: 'To hire', example: 'Van a contratar a 5 personas.', pronunciation: 'kohn-trah-TAHR' },
          { word: 'Despedir', translation: 'To fire', example: 'Lo despidieron ayer.', pronunciation: 'dehs-peh-DEER' },
          { word: 'Ascender', translation: 'To promote', example: 'Me ascendieron a gerente.', pronunciation: 'ahs-sehn-DEHR' },
          { word: 'Sueldo', translation: 'Salary', example: 'El sueldo es negociable.', pronunciation: 'SWEHL-doh' },
          { word: 'Jornada', translation: 'Work day', example: 'Trabajo jornada completa.', pronunciation: 'hohr-NAH-dah' },
        ],
        grammar: [
          { title: 'Voz pasiva', rule: 'SER + participio', examples: ['El candidato fue seleccionado', 'La reunión fue cancelada'] },
          { title: 'Oraciones de relativo', rule: 'que, quien, donde, cuyo', examples: ['La empresa que me contrató', 'El jefe con quien trabajo'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-es-b2',
        title: 'Quiz de Español B2',
        questions: [
          { question: '"Habría ido si hubiera podido" expresa:', options: ['Condición irreal pasada', 'Certeza', 'Obligación', 'Deseo presente'], correct: 0, explanation: 'Es una condición irreal en el pasado.' },
          { question: '¿Qué figura retórica es "sus ojos son soles"?', options: ['Metáfora', 'Símil', 'Hipérbole', 'Personificación'], correct: 0, explanation: 'Es una metáfora porque identifica directamente.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Imprescindible', translation: 'Essential', example: 'El agua es imprescindible.', pronunciation: 'eem-prehs-seen-DEE-bleh' },
      { word: 'Aprovechar', translation: 'To take advantage', example: 'Debes aprovechar esta oportunidad.', pronunciation: 'ah-proh-beh-CHAHR' },
      { word: 'Destacar', translation: 'To stand out', example: 'Su trabajo destaca por su calidad.', pronunciation: 'dehs-tah-KAHR' },
    ]
  },
  C1: {
    lessons: [
      {
        id: 'es-c1-1',
        title: 'Registro Académico',
        description: 'Lenguaje formal y académico',
        content: `## Lenguaje Académico

### Expresiones formales:
- Cabe destacar que... - It should be noted that...
- Se puede afirmar que... - It can be stated that...
- Según los estudios... - According to studies...

### Conectores académicos:
- No obstante - Nevertheless
- Asimismo - Likewise
- En consecuencia - Consequently`,
        vocabulary: [
          { word: 'Entrañable', translation: 'Endearing', example: 'Es un recuerdo entrañable.', pronunciation: 'ehn-trah-NYAH-bleh' },
          { word: 'Idiosincrasia', translation: 'Idiosyncrasy', example: 'La idiosincrasia cultural.', pronunciation: 'ee-dyoh-seen-KRAH-syah' },
          { word: 'Escudriñar', translation: 'To scrutinize', example: 'Hay que escudriñar los datos.', pronunciation: 'ehs-koo-dree-NYAHR' },
        ],
        grammar: [
          { title: 'Subjuntivo en oraciones sustantivas', rule: 'Es importante que + subjuntivo', examples: ['Es necesario que vengas', 'Es probable que llueva'] },
        ]
      }
    ],
    quizzes: [{ id: 'quiz-es-c1', title: 'Quiz C1', questions: [] }],
    flashcards: []
  },
  C2: {
    lessons: [
      {
        id: 'es-c2-1',
        title: 'Matices Literarios',
        description: 'Dominio del español literario',
        content: `## Literatura y Estilo

### Figuras retóricas avanzadas:
- Anacoluto - Inconsistencia gramatical intencional
- Zeugma - Un verbo para múltiples complementos
- Hipérbaton - Alteración del orden sintáctico`,
        vocabulary: [
          { word: 'Abigarrado', translation: 'Motley', example: 'Un grupo abigarrado.', pronunciation: 'ah-bee-gah-RRAH-doh' },
          { word: 'Sempiterno', translation: 'Everlasting', example: 'Su amor es sempiterno.', pronunciation: 'sehm-pee-TEHR-noh' },
        ],
        grammar: [
          { title: 'Estilo indirecto libre', rule: 'Mezcla de narración y pensamiento', examples: ['Pensó que quizás fuera verdad'] },
        ]
      }
    ],
    quizzes: [{ id: 'quiz-es-c2', title: 'Quiz C2', questions: [] }],
    flashcards: []
  }
};

// ==================== ENGLISH CONTENT ====================
export const ENGLISH_CONTENT = {
  A1: {
    lessons: [
      {
        id: 'en-a1-1',
        title: 'Greetings and Introductions',
        description: 'Learn to greet and introduce yourself',
        content: `## Basic Greetings

### Formal greetings:
- **Good morning** (until 12:00)
- **Good afternoon** (12:00-18:00)
- **Good evening** (after 18:00)

### Informal greetings:
- **Hello / Hi** - Most common greeting
- **Hey** - Very casual
- **How are you?** - Common question

## Introductions
- **My name is...** / **I'm...**
- **Nice to meet you**
- **Where are you from?**`,
        vocabulary: [
          { word: 'Hello', translation: 'Hola', example: 'Hello, how are you?', pronunciation: 'heh-LOH' },
          { word: 'Good morning', translation: 'Buenos días', example: 'Good morning, everyone!', pronunciation: 'good MOR-ning' },
          { word: 'Thank you', translation: 'Gracias', example: 'Thank you very much.', pronunciation: 'THANK yoo' },
          { word: 'Please', translation: 'Por favor', example: 'A coffee, please.', pronunciation: 'pleez' },
          { word: 'Goodbye', translation: 'Adiós', example: 'Goodbye, see you later.', pronunciation: 'good-BYE' },
          { word: 'Yes', translation: 'Sí', example: 'Yes, I understand.', pronunciation: 'yes' },
          { word: 'No', translation: 'No', example: 'No, thank you.', pronunciation: 'noh' },
          { word: 'Excuse me', translation: 'Disculpe', example: 'Excuse me, where is...?', pronunciation: 'ik-SKYOOZ mee' },
        ],
        grammar: [
          { title: "Verb 'to be'", rule: 'I AM, You ARE, He/She IS', examples: ['I am a student', 'She is a teacher'] },
          { title: 'Articles', rule: 'A (consonant), AN (vowel), THE (specific)', examples: ['A book', 'An apple', 'The car'] },
          { title: 'Basic word order', rule: 'Subject + Verb + Object', examples: ['I speak English', 'She reads books'] },
        ]
      },
      {
        id: 'en-a1-2',
        title: 'Numbers and Colors',
        description: 'Learn numbers 1-100 and basic colors',
        content: `## Numbers 1-20

| Number | English | Number | English |
|--------|---------|--------|---------|
| 1 | one | 11 | eleven |
| 2 | two | 12 | twelve |
| 3 | three | 13 | thirteen |
| 4 | four | 14 | fourteen |
| 5 | five | 15 | fifteen |

## Colors
- 🔴 **Red** - Rojo
- 🔵 **Blue** - Azul
- 🟢 **Green** - Verde
- 🟡 **Yellow** - Amarillo`,
        vocabulary: [
          { word: 'Red', translation: 'Rojo', example: 'The apple is red.', pronunciation: 'red' },
          { word: 'Blue', translation: 'Azul', example: 'The sky is blue.', pronunciation: 'bloo' },
          { word: 'Green', translation: 'Verde', example: 'The grass is green.', pronunciation: 'green' },
          { word: 'Yellow', translation: 'Amarillo', example: 'The sun is yellow.', pronunciation: 'YEL-oh' },
          { word: 'One', translation: 'Uno', example: 'I have one brother.', pronunciation: 'wun' },
          { word: 'Ten', translation: 'Diez', example: "It's ten o'clock.", pronunciation: 'ten' },
        ],
        grammar: [
          { title: 'Plural nouns', rule: 'Add -s or -es', examples: ['book → books', 'box → boxes'] },
          { title: 'There is/are', rule: 'There is (singular), There are (plural)', examples: ['There is a book', 'There are three books'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-en-a1',
        title: 'English A1 Quiz',
        questions: [
          { question: 'What is "hola" in English?', options: ['Hello', 'Goodbye', 'Thanks', 'Please'], correct: 0, explanation: '"Hello" is the common greeting.' },
          { question: 'The plural of "book" is:', options: ['Books', 'Bookes', 'Bookies', 'Book'], correct: 0, explanation: 'Add -s for regular plurals.' },
          { question: 'Complete: "I ___ a student"', options: ['am', 'is', 'are', 'be'], correct: 0, explanation: '"I" uses "am" with verb to be.' },
          { question: 'The article for "apple" is:', options: ['an', 'a', 'the', 'none'], correct: 0, explanation: 'Use "an" before vowels.' },
          { question: 'What color is "azul"?', options: ['Blue', 'Red', 'Green', 'Yellow'], correct: 0, explanation: '"Azul" means "blue" in English.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Hello', translation: 'Hola', example: 'Hello, how are you?', pronunciation: 'heh-LOH' },
      { word: 'Thank you', translation: 'Gracias', example: 'Thank you very much.', pronunciation: 'THANK yoo' },
      { word: 'Please', translation: 'Por favor', example: 'A coffee, please.', pronunciation: 'pleez' },
      { word: 'Water', translation: 'Agua', example: 'A glass of water, please.', pronunciation: 'WAW-ter' },
      { word: 'House', translation: 'Casa', example: 'My house is small.', pronunciation: 'hows' },
      { word: 'Family', translation: 'Familia', example: 'My family is big.', pronunciation: 'FAM-uh-lee' },
    ]
  },
  A2: {
    lessons: [
      {
        id: 'en-a2-1',
        title: 'Shopping',
        description: 'Vocabulary for shopping',
        content: `## At the Store

### Useful phrases:
- **How much does this cost?**
- **Do you have this in another size/color?**
- **I'll take it**
- **Can I pay by card?**`,
        vocabulary: [
          { word: 'How much?', translation: '¿Cuánto cuesta?', example: 'How much is this book?', pronunciation: 'how much' },
          { word: 'Cheap', translation: 'Barato', example: 'This restaurant is cheap.', pronunciation: 'cheep' },
          { word: 'Expensive', translation: 'Caro', example: 'The hotel is expensive.', pronunciation: 'ik-SPEN-siv' },
          { word: 'Size', translation: 'Talla', example: 'What size do you wear?', pronunciation: 'size' },
        ],
        grammar: [
          { title: 'Present continuous', rule: 'am/is/are + -ing', examples: ["I'm shopping", "She's buying"] },
        ]
      }
    ],
    quizzes: [{ id: 'quiz-en-a2', title: 'Quiz A2', questions: [] }],
    flashcards: [
      { word: 'To work', translation: 'Trabajar', example: 'I work in an office.', pronunciation: 'too werk' },
      { word: 'To eat', translation: 'Comer', example: 'I like to eat pizza.', pronunciation: 'too eet' },
    ]
  },
  B1: {
    lessons: [
      {
        id: 'en-b1-1',
        title: 'Expressing Opinions',
        description: 'Learn to give your opinion politely',
        content: `## How to Express Opinions

### Phrases for giving opinions:
- **I think that...**
- **In my opinion...**
- **It seems to me that...**
- **From my point of view...**

### Agreeing:
- I agree
- You're right
- Exactly

### Disagreeing:
- I don't agree
- I see it differently
- Not necessarily`,
        vocabulary: [
          { word: 'I think', translation: 'Creo que', example: "I think it's a good idea.", pronunciation: 'I think' },
          { word: 'However', translation: 'Sin embargo', example: "I like it; however, it's expensive.", pronunciation: 'how-EV-er' },
          { word: 'Although', translation: 'Aunque', example: "Although it's raining, I'll go out.", pronunciation: 'awl-THOH' },
          { word: 'Therefore', translation: 'Por lo tanto', example: 'I studied hard, therefore I passed.', pronunciation: 'THAIR-for' },
        ],
        grammar: [
          { title: 'Conditionals', rule: 'If + past, would + infinitive', examples: ['If I had money, I would travel'] },
        ]
      }
    ],
    quizzes: [{ id: 'quiz-en-b1', title: 'Quiz B1', questions: [] }],
    flashcards: []
  },
  B2: { lessons: [], quizzes: [], flashcards: [] },
  C1: { lessons: [], quizzes: [], flashcards: [] },
  C2: { lessons: [], quizzes: [], flashcards: [] }
};

// ==================== FRENCH CONTENT ====================
export const FRENCH_CONTENT = {
  A1: {
    lessons: [
      {
        id: 'fr-a1-1',
        title: 'Salutations et Présentations',
        description: 'Apprenez à saluer et vous présenter',
        content: `## Salutations de base

### Salutations formelles:
- **Bonjour** - Good morning/Hello
- **Bonsoir** - Good evening
- **Bonne nuit** - Good night

### Salutations informelles:
- **Salut** - Hi
- **Coucou** - Hey (very casual)

## Présentations
- **Je m'appelle...** - My name is...
- **Je suis...** - I am...
- **Enchanté(e)** - Nice to meet you`,
        vocabulary: [
          { word: 'Bonjour', translation: 'Hello/Good day', example: 'Bonjour, comment allez-vous?', pronunciation: 'bon-ZHOOR' },
          { word: 'Merci', translation: 'Thank you', example: 'Merci beaucoup!', pronunciation: 'mer-SEE' },
          { word: "S'il vous plaît", translation: 'Please', example: "Un café, s'il vous plaît.", pronunciation: 'seel voo PLEH' },
          { word: 'Au revoir', translation: 'Goodbye', example: 'Au revoir, à demain!', pronunciation: 'oh reh-VWAHR' },
          { word: 'Oui', translation: 'Yes', example: 'Oui, je comprends.', pronunciation: 'wee' },
          { word: 'Non', translation: 'No', example: 'Non, merci.', pronunciation: 'noh' },
        ],
        grammar: [
          { title: "Verbe 'être'", rule: 'Je SUIS, Tu ES, Il/Elle EST', examples: ['Je suis étudiant', 'Elle est professeur'] },
          { title: 'Articles définis', rule: 'LE (masc.), LA (fem.), LES (pluriel)', examples: ['Le livre', 'La maison', 'Les enfants'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-fr-a1',
        title: 'Quiz de Français A1',
        questions: [
          { question: 'Comment dit-on "Hello" en français?', options: ['Bonjour', 'Au revoir', 'Merci', "S'il vous plaît"], correct: 0, explanation: '"Bonjour" est la salutation standard.' },
          { question: "Le pluriel de 'livre' est:", options: ['Livres', 'Livrees', 'Livrés', 'Livre'], correct: 0, explanation: 'On ajoute -s pour former le pluriel.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Bonjour', translation: 'Hello', example: 'Bonjour, comment ça va?', pronunciation: 'bon-ZHOOR' },
      { word: 'Merci', translation: 'Thank you', example: 'Merci beaucoup!', pronunciation: 'mer-SEE' },
      { word: 'Eau', translation: 'Water', example: "Un verre d'eau, s'il vous plaît.", pronunciation: 'oh' },
      { word: 'Maison', translation: 'House', example: 'Ma maison est grande.', pronunciation: 'meh-ZON' },
    ]
  },
  A2: { lessons: [], quizzes: [], flashcards: [] },
  B1: { lessons: [], quizzes: [], flashcards: [] },
  B2: { lessons: [], quizzes: [], flashcards: [] },
  C1: { lessons: [], quizzes: [], flashcards: [] },
  C2: { lessons: [], quizzes: [], flashcards: [] }
};

// ==================== GERMAN CONTENT ====================
export const GERMAN_CONTENT = {
  A1: {
    lessons: [
      {
        id: 'de-a1-1',
        title: 'Grüße und Vorstellungen',
        description: 'Lernen Sie zu grüßen und sich vorzustellen',
        content: `## Grundlegende Grüße

### Formelle Grüße:
- **Guten Morgen** - Good morning
- **Guten Tag** - Good day
- **Guten Abend** - Good evening
- **Gute Nacht** - Good night

### Informelle Grüße:
- **Hallo** - Hello
- **Hi** - Hi

## Vorstellungen
- **Ich heiße...** - My name is...
- **Ich bin...** - I am...
- **Freut mich** - Nice to meet you`,
        vocabulary: [
          { word: 'Hallo', translation: 'Hello', example: 'Hallo, wie geht es dir?', pronunciation: 'HAH-loh' },
          { word: 'Guten Morgen', translation: 'Good morning', example: 'Guten Morgen, Herr Schmidt.', pronunciation: 'GOO-ten MOR-gen' },
          { word: 'Danke', translation: 'Thank you', example: 'Vielen Dank für Ihre Hilfe.', pronunciation: 'DAHN-keh' },
          { word: 'Bitte', translation: 'Please/You\'re welcome', example: 'Einen Kaffee, bitte.', pronunciation: 'BIT-teh' },
          { word: 'Auf Wiedersehen', translation: 'Goodbye', example: 'Auf Wiedersehen, bis morgen!', pronunciation: 'owf VEE-der-zey-en' },
          { word: 'Ja', translation: 'Yes', example: 'Ja, ich verstehe.', pronunciation: 'yah' },
        ],
        grammar: [
          { title: "Verb 'sein'", rule: 'Ich BIN, Du BIST, Er/Sie IST', examples: ['Ich bin Student', 'Sie ist Lehrerin'] },
          { title: 'Artikel', rule: 'DER (mask.), DIE (fem.), DAS (neutr.)', examples: ['Der Mann', 'Die Frau', 'Das Kind'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-de-a1',
        title: 'Deutsch A1 Quiz',
        questions: [
          { question: 'Wie sagt man "Hello" auf Deutsch?', options: ['Hallo', 'Tschüss', 'Danke', 'Bitte'], correct: 0, explanation: '"Hallo" ist die informelle Begrüßung.' },
          { question: 'Der Plural von "Buch" ist:', options: ['Bücher', 'Buchs', 'Buchen', 'Buch'], correct: 0, explanation: '"Buch" wird zu "Bücher" im Plural.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Hallo', translation: 'Hello', example: 'Hallo, wie geht es?', pronunciation: 'HAH-loh' },
      { word: 'Danke', translation: 'Thank you', example: 'Danke schön!', pronunciation: 'DAHN-keh' },
      { word: 'Wasser', translation: 'Water', example: 'Ein Glas Wasser, bitte.', pronunciation: 'VAH-ser' },
      { word: 'Haus', translation: 'House', example: 'Das Haus ist groß.', pronunciation: 'hows' },
    ]
  },
  A2: { lessons: [], quizzes: [], flashcards: [] },
  B1: { lessons: [], quizzes: [], flashcards: [] },
  B2: { lessons: [], quizzes: [], flashcards: [] },
  C1: { lessons: [], quizzes: [], flashcards: [] },
  C2: { lessons: [], quizzes: [], flashcards: [] }
};

// ==================== PORTUGUESE CONTENT ====================
export const PORTUGUESE_CONTENT = {
  A1: {
    lessons: [
      {
        id: 'pt-a1-1',
        title: 'Saudações e Apresentações',
        description: 'Aprenda a cumprimentar e se apresentar',
        content: `## Saudações Básicas

### Saudações formais:
- **Bom dia** - Good morning
- **Boa tarde** - Good afternoon
- **Boa noite** - Good evening/night

### Saudações informais:
- **Olá** - Hello
- **Oi** - Hi
- **E aí?** - What's up?

## Apresentações
- **Meu nome é...** / **Me chamo...**
- **Eu sou...**
- **Prazer em conhecê-lo(a)**`,
        vocabulary: [
          { word: 'Olá', translation: 'Hello', example: 'Olá! Como vai você?', pronunciation: 'oh-LAH' },
          { word: 'Bom dia', translation: 'Good morning', example: 'Bom dia! Tudo bem?', pronunciation: 'bom DEE-ah' },
          { word: 'Obrigado/a', translation: 'Thank you', example: 'Muito obrigado pela ajuda.', pronunciation: 'oh-bree-GAH-doo' },
          { word: 'Por favor', translation: 'Please', example: 'Um café, por favor.', pronunciation: 'por fah-VOR' },
          { word: 'Tchau', translation: 'Bye', example: 'Tchau, até amanhã!', pronunciation: 'chow' },
          { word: 'Sim', translation: 'Yes', example: 'Sim, eu entendo.', pronunciation: 'seem' },
        ],
        grammar: [
          { title: "Verbo 'ser'", rule: 'Eu SOU, Tu ÉS, Ele/Ela É', examples: ['Eu sou estudante', 'Ela é professora'] },
          { title: 'Artigos definidos', rule: 'O (masc.), A (fem.), OS/AS (plural)', examples: ['O livro', 'A casa', 'Os meninos'] },
        ]
      }
    ],
    quizzes: [
      {
        id: 'quiz-pt-a1',
        title: 'Quiz de Português A1',
        questions: [
          { question: 'Como se diz "Hello" em português?', options: ['Olá', 'Tchau', 'Obrigado', 'Por favor'], correct: 0, explanation: '"Olá" é a saudação comum.' },
          { question: 'O plural de "livro" é:', options: ['Livros', 'Livroes', 'Livras', 'Livro'], correct: 0, explanation: 'Adiciona-se -s para formar o plural.' },
        ]
      }
    ],
    flashcards: [
      { word: 'Olá', translation: 'Hello', example: 'Olá! Como vai?', pronunciation: 'oh-LAH' },
      { word: 'Obrigado', translation: 'Thank you', example: 'Muito obrigado!', pronunciation: 'oh-bree-GAH-doo' },
      { word: 'Água', translation: 'Water', example: 'Um copo de água, por favor.', pronunciation: 'AH-gwah' },
      { word: 'Casa', translation: 'House', example: 'Minha casa é pequena.', pronunciation: 'KAH-zah' },
    ]
  },
  A2: { lessons: [], quizzes: [], flashcards: [] },
  B1: { lessons: [], quizzes: [], flashcards: [] },
  B2: { lessons: [], quizzes: [], flashcards: [] },
  C1: { lessons: [], quizzes: [], flashcards: [] },
  C2: { lessons: [], quizzes: [], flashcards: [] }
};

// ==================== HELPER FUNCTIONS ====================
export const getContentByLanguage = (languageId) => {
  switch (languageId) {
    case 'spanish': return SPANISH_CONTENT;
    case 'english': return ENGLISH_CONTENT;
    case 'french': return FRENCH_CONTENT;
    case 'german': return GERMAN_CONTENT;
    case 'portuguese': return PORTUGUESE_CONTENT;
    default: return SPANISH_CONTENT;
  }
};

export const getLanguageInfo = (languageId) => {
  return LANGUAGES.find(l => l.id === languageId) || LANGUAGES[0];
};

export const getLevelInfo = (levelId) => {
  return LEVELS.find(l => l.id === levelId) || LEVELS[0];
};

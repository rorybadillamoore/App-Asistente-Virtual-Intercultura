"""
Script para poblar la base de datos con contenido educativo completo.
Idiomas: Español, Inglés, Portugués
Niveles: A1, A2, B1, B2, C1, C2
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'polyglot_academy')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Definición de contenido por idioma y nivel
COURSE_CONTENT = {
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

# Flashcards por idioma y nivel (vocabulario esencial basado en metodología Cambridge)
FLASHCARDS = {
    "spanish": {
        "A1": [
            {"word": "Hola", "translation": "Hello", "example": "¡Hola! ¿Cómo estás?", "pronunciation": "OH-lah"},
            {"word": "Gracias", "translation": "Thank you", "example": "Muchas gracias por tu ayuda.", "pronunciation": "GRAH-syahs"},
            {"word": "Por favor", "translation": "Please", "example": "Un café, por favor.", "pronunciation": "por fah-VOR"},
            {"word": "Buenos días", "translation": "Good morning", "example": "Buenos días, señor.", "pronunciation": "BWEH-nohs DEE-ahs"},
            {"word": "Buenas noches", "translation": "Good night", "example": "Buenas noches, hasta mañana.", "pronunciation": "BWEH-nahs NOH-chehs"},
            {"word": "Sí", "translation": "Yes", "example": "Sí, entiendo.", "pronunciation": "see"},
            {"word": "No", "translation": "No", "example": "No, gracias.", "pronunciation": "noh"},
            {"word": "Agua", "translation": "Water", "example": "Un vaso de agua, por favor.", "pronunciation": "AH-gwah"},
            {"word": "Casa", "translation": "House", "example": "Mi casa es pequeña.", "pronunciation": "KAH-sah"},
            {"word": "Familia", "translation": "Family", "example": "Mi familia es grande.", "pronunciation": "fah-MEE-lyah"},
        ],
        "A2": [
            {"word": "Trabajar", "translation": "To work", "example": "Yo trabajo en una oficina.", "pronunciation": "trah-bah-HAR"},
            {"word": "Comer", "translation": "To eat", "example": "Me gusta comer pizza.", "pronunciation": "koh-MER"},
            {"word": "Comprar", "translation": "To buy", "example": "Voy a comprar pan.", "pronunciation": "kohm-PRAR"},
            {"word": "Bonito", "translation": "Beautiful", "example": "El vestido es muy bonito.", "pronunciation": "boh-NEE-toh"},
            {"word": "Barato", "translation": "Cheap", "example": "Este libro es barato.", "pronunciation": "bah-RAH-toh"},
            {"word": "Caro", "translation": "Expensive", "example": "El coche es muy caro.", "pronunciation": "KAH-roh"},
            {"word": "Siempre", "translation": "Always", "example": "Siempre llego temprano.", "pronunciation": "SYEM-preh"},
            {"word": "Nunca", "translation": "Never", "example": "Nunca como carne.", "pronunciation": "NOON-kah"},
            {"word": "Cerca", "translation": "Near", "example": "El banco está cerca.", "pronunciation": "SER-kah"},
            {"word": "Lejos", "translation": "Far", "example": "Mi trabajo está lejos.", "pronunciation": "LEH-hohs"},
        ],
        "B1": [
            {"word": "Desarrollar", "translation": "To develop", "example": "Quiero desarrollar mis habilidades.", "pronunciation": "deh-sah-roh-YAR"},
            {"word": "Conseguir", "translation": "To achieve/get", "example": "Voy a conseguir el trabajo.", "pronunciation": "kohn-seh-GEER"},
            {"word": "Mejorar", "translation": "To improve", "example": "Necesito mejorar mi español.", "pronunciation": "meh-hoh-RAR"},
            {"word": "Aunque", "translation": "Although", "example": "Aunque llueve, saldré.", "pronunciation": "OWN-keh"},
            {"word": "Sin embargo", "translation": "However", "example": "Me gusta; sin embargo, es caro.", "pronunciation": "seen em-BAR-goh"},
            {"word": "Mientras", "translation": "While", "example": "Estudio mientras trabajo.", "pronunciation": "MYEN-trahs"},
            {"word": "Esperanza", "translation": "Hope", "example": "Tengo esperanza en el futuro.", "pronunciation": "ehs-peh-RAN-sah"},
            {"word": "Preocuparse", "translation": "To worry", "example": "No te preocupes por eso.", "pronunciation": "preh-oh-koo-PAR-seh"},
            {"word": "Disfrutar", "translation": "To enjoy", "example": "Disfruto mucho de la música.", "pronunciation": "dees-froo-TAR"},
            {"word": "Realizar", "translation": "To accomplish", "example": "Voy a realizar mi sueño.", "pronunciation": "reh-ah-lee-SAR"},
        ],
        "B2": [
            {"word": "Imprescindible", "translation": "Essential", "example": "El agua es imprescindible para vivir.", "pronunciation": "eem-prehs-seen-DEE-bleh"},
            {"word": "Aprovechar", "translation": "To take advantage", "example": "Debes aprovechar esta oportunidad.", "pronunciation": "ah-proh-veh-CHAR"},
            {"word": "Destacar", "translation": "To stand out", "example": "Su trabajo destaca por su calidad.", "pronunciation": "dehs-tah-KAR"},
            {"word": "A pesar de", "translation": "Despite", "example": "A pesar de todo, soy feliz.", "pronunciation": "ah peh-SAR deh"},
            {"word": "Asimismo", "translation": "Likewise", "example": "Asimismo, debemos considerar otros factores.", "pronunciation": "ah-see-MEES-moh"},
            {"word": "Cuestionar", "translation": "To question", "example": "Es importante cuestionar las noticias.", "pronunciation": "kwehs-tyoh-NAR"},
            {"word": "Proporcionar", "translation": "To provide", "example": "Te proporcionaré toda la información.", "pronunciation": "proh-pohr-syoh-NAR"},
            {"word": "Sostener", "translation": "To sustain/hold", "example": "Sostengo mi opinión firmemente.", "pronunciation": "sohs-teh-NER"},
            {"word": "Abordar", "translation": "To address/tackle", "example": "Debemos abordar este problema.", "pronunciation": "ah-bohr-DAR"},
            {"word": "Vincular", "translation": "To link", "example": "Hay que vincular teoría y práctica.", "pronunciation": "been-koo-LAR"},
        ],
        "C1": [
            {"word": "Entrañable", "translation": "Endearing", "example": "Es un recuerdo entrañable de mi infancia.", "pronunciation": "ehn-trah-NYAH-bleh"},
            {"word": "Idiosincrasia", "translation": "Idiosyncrasy", "example": "Cada cultura tiene su propia idiosincrasia.", "pronunciation": "ee-dyoh-seen-KRAH-syah"},
            {"word": "Escudriñar", "translation": "To scrutinize", "example": "Hay que escudriñar los datos cuidadosamente.", "pronunciation": "ehs-koo-dree-NYAR"},
            {"word": "Subyacer", "translation": "To underlie", "example": "Varios factores subyacen a este fenómeno.", "pronunciation": "soob-yah-SER"},
            {"word": "Elucidar", "translation": "To elucidate", "example": "El profesor elucidó el concepto complejo.", "pronunciation": "eh-loo-see-DAR"},
            {"word": "Conllevar", "translation": "To entail", "example": "Este proyecto conlleva grandes responsabilidades.", "pronunciation": "kohn-yeh-VAR"},
            {"word": "Dilucidar", "translation": "To clarify", "example": "Intentaré dilucidar este misterio.", "pronunciation": "dee-loo-see-DAR"},
            {"word": "Desdeñar", "translation": "To disdain", "example": "No debemos desdeñar las opiniones ajenas.", "pronunciation": "dehs-deh-NYAR"},
            {"word": "Inherente", "translation": "Inherent", "example": "La creatividad es inherente al ser humano.", "pronunciation": "een-eh-REN-teh"},
            {"word": "Soslayar", "translation": "To sidestep", "example": "No podemos soslayar este problema.", "pronunciation": "sohs-lah-YAR"},
        ],
        "C2": [
            {"word": "Abigarrado", "translation": "Motley/variegated", "example": "Era un grupo abigarrado de personas.", "pronunciation": "ah-bee-gah-RAH-doh"},
            {"word": "Desabrido", "translation": "Bland/surly", "example": "Su respuesta fue desabrida.", "pronunciation": "deh-sah-BREE-doh"},
            {"word": "Acérrimo", "translation": "Staunch", "example": "Es un acérrimo defensor de los derechos.", "pronunciation": "ah-SEH-ree-moh"},
            {"word": "Recóndito", "translation": "Hidden/recondite", "example": "Exploramos lugares recónditos.", "pronunciation": "reh-KOHN-dee-toh"},
            {"word": "Sempiterno", "translation": "Everlasting", "example": "Su amor es sempiterno.", "pronunciation": "sehm-pee-TER-noh"},
            {"word": "Prístino", "translation": "Pristine", "example": "El bosque estaba en estado prístino.", "pronunciation": "PREES-tee-noh"},
            {"word": "Aquiescencia", "translation": "Acquiescence", "example": "Su aquiescencia sorprendió a todos.", "pronunciation": "ah-kyehs-SEN-syah"},
            {"word": "Consuetudinario", "translation": "Customary", "example": "Es un derecho consuetudinario.", "pronunciation": "kohn-sweh-too-dee-NAH-ryoh"},
            {"word": "Execrable", "translation": "Execrable", "example": "Su comportamiento fue execrable.", "pronunciation": "ehk-seh-KRAH-bleh"},
            {"word": "Resquemor", "translation": "Resentment", "example": "Aún guarda cierto resquemor.", "pronunciation": "rehs-keh-MOR"},
        ]
    },
    "english": {
        "A1": [
            {"word": "Hello", "translation": "Hola", "example": "Hello, how are you?", "pronunciation": "heh-LOH"},
            {"word": "Thank you", "translation": "Gracias", "example": "Thank you very much.", "pronunciation": "THANK yoo"},
            {"word": "Please", "translation": "Por favor", "example": "A coffee, please.", "pronunciation": "pleez"},
            {"word": "Good morning", "translation": "Buenos días", "example": "Good morning, everyone!", "pronunciation": "good MOR-ning"},
            {"word": "Goodbye", "translation": "Adiós", "example": "Goodbye, see you later.", "pronunciation": "good-BYE"},
            {"word": "Yes", "translation": "Sí", "example": "Yes, I understand.", "pronunciation": "yes"},
            {"word": "No", "translation": "No", "example": "No, thank you.", "pronunciation": "noh"},
            {"word": "Water", "translation": "Agua", "example": "A glass of water, please.", "pronunciation": "WAW-ter"},
            {"word": "House", "translation": "Casa", "example": "My house is small.", "pronunciation": "hows"},
            {"word": "Family", "translation": "Familia", "example": "My family is big.", "pronunciation": "FAM-uh-lee"},
        ],
        "A2": [
            {"word": "To work", "translation": "Trabajar", "example": "I work in an office.", "pronunciation": "too werk"},
            {"word": "To eat", "translation": "Comer", "example": "I like to eat pizza.", "pronunciation": "too eet"},
            {"word": "To buy", "translation": "Comprar", "example": "I'm going to buy bread.", "pronunciation": "too bye"},
            {"word": "Beautiful", "translation": "Bonito/Hermoso", "example": "The dress is very beautiful.", "pronunciation": "BYOO-tuh-ful"},
            {"word": "Cheap", "translation": "Barato", "example": "This book is cheap.", "pronunciation": "cheep"},
            {"word": "Expensive", "translation": "Caro", "example": "The car is very expensive.", "pronunciation": "ik-SPEN-siv"},
            {"word": "Always", "translation": "Siempre", "example": "I always arrive early.", "pronunciation": "AWL-weyz"},
            {"word": "Never", "translation": "Nunca", "example": "I never eat meat.", "pronunciation": "NEV-er"},
            {"word": "Near", "translation": "Cerca", "example": "The bank is near.", "pronunciation": "neer"},
            {"word": "Far", "translation": "Lejos", "example": "My job is far away.", "pronunciation": "fahr"},
        ],
        "B1": [
            {"word": "To develop", "translation": "Desarrollar", "example": "I want to develop my skills.", "pronunciation": "dih-VEL-uhp"},
            {"word": "To achieve", "translation": "Conseguir/Lograr", "example": "I will achieve my goals.", "pronunciation": "uh-CHEEV"},
            {"word": "To improve", "translation": "Mejorar", "example": "I need to improve my English.", "pronunciation": "im-PROOV"},
            {"word": "Although", "translation": "Aunque", "example": "Although it's raining, I'll go out.", "pronunciation": "awl-THOH"},
            {"word": "However", "translation": "Sin embargo", "example": "I like it; however, it's expensive.", "pronunciation": "how-EV-er"},
            {"word": "While", "translation": "Mientras", "example": "I study while I work.", "pronunciation": "wile"},
            {"word": "Hope", "translation": "Esperanza", "example": "I have hope for the future.", "pronunciation": "hohp"},
            {"word": "To worry", "translation": "Preocuparse", "example": "Don't worry about it.", "pronunciation": "WUR-ee"},
            {"word": "To enjoy", "translation": "Disfrutar", "example": "I really enjoy music.", "pronunciation": "en-JOY"},
            {"word": "To accomplish", "translation": "Realizar/Lograr", "example": "I will accomplish my dream.", "pronunciation": "uh-KOM-plish"},
        ],
        "B2": [
            {"word": "Essential", "translation": "Imprescindible", "example": "Water is essential for life.", "pronunciation": "ih-SEN-shul"},
            {"word": "To take advantage", "translation": "Aprovechar", "example": "You should take advantage of this opportunity.", "pronunciation": "teyk ad-VAN-tij"},
            {"word": "To stand out", "translation": "Destacar", "example": "His work stands out for its quality.", "pronunciation": "stand owt"},
            {"word": "Despite", "translation": "A pesar de", "example": "Despite everything, I am happy.", "pronunciation": "dih-SPITE"},
            {"word": "Likewise", "translation": "Asimismo", "example": "Likewise, we must consider other factors.", "pronunciation": "LIKE-wize"},
            {"word": "To question", "translation": "Cuestionar", "example": "It's important to question the news.", "pronunciation": "KWES-chun"},
            {"word": "To provide", "translation": "Proporcionar", "example": "I will provide you with all the information.", "pronunciation": "pruh-VIDE"},
            {"word": "To sustain", "translation": "Sostener", "example": "I sustain my opinion firmly.", "pronunciation": "suh-STEYN"},
            {"word": "To address", "translation": "Abordar", "example": "We must address this problem.", "pronunciation": "uh-DRES"},
            {"word": "To link", "translation": "Vincular", "example": "We need to link theory and practice.", "pronunciation": "lingk"},
        ],
        "C1": [
            {"word": "Endearing", "translation": "Entrañable", "example": "It's an endearing memory from my childhood.", "pronunciation": "en-DEER-ing"},
            {"word": "Idiosyncrasy", "translation": "Idiosincrasia", "example": "Every culture has its own idiosyncrasy.", "pronunciation": "id-ee-oh-SING-kruh-see"},
            {"word": "To scrutinize", "translation": "Escudriñar", "example": "We must scrutinize the data carefully.", "pronunciation": "SKROO-tuh-nize"},
            {"word": "To underlie", "translation": "Subyacer", "example": "Several factors underlie this phenomenon.", "pronunciation": "un-der-LIE"},
            {"word": "To elucidate", "translation": "Elucidar", "example": "The professor elucidated the complex concept.", "pronunciation": "ih-LOO-sih-deyt"},
            {"word": "To entail", "translation": "Conllevar", "example": "This project entails great responsibilities.", "pronunciation": "en-TEYL"},
            {"word": "To clarify", "translation": "Dilucidar/Aclarar", "example": "I will try to clarify this mystery.", "pronunciation": "KLAR-uh-fy"},
            {"word": "To disdain", "translation": "Desdeñar", "example": "We shouldn't disdain others' opinions.", "pronunciation": "dis-DEYN"},
            {"word": "Inherent", "translation": "Inherente", "example": "Creativity is inherent to human beings.", "pronunciation": "in-HEER-uhnt"},
            {"word": "To sidestep", "translation": "Soslayar", "example": "We cannot sidestep this problem.", "pronunciation": "SIDE-step"},
        ],
        "C2": [
            {"word": "Motley", "translation": "Abigarrado", "example": "It was a motley group of people.", "pronunciation": "MOT-lee"},
            {"word": "Surly", "translation": "Desabrido/Hosco", "example": "His response was surly.", "pronunciation": "SUR-lee"},
            {"word": "Staunch", "translation": "Acérrimo", "example": "He is a staunch defender of rights.", "pronunciation": "stawnch"},
            {"word": "Recondite", "translation": "Recóndito", "example": "We explored recondite places.", "pronunciation": "REK-uhn-dite"},
            {"word": "Everlasting", "translation": "Sempiterno", "example": "Their love is everlasting.", "pronunciation": "ev-er-LAS-ting"},
            {"word": "Pristine", "translation": "Prístino", "example": "The forest was in pristine condition.", "pronunciation": "PRIS-teen"},
            {"word": "Acquiescence", "translation": "Aquiescencia", "example": "His acquiescence surprised everyone.", "pronunciation": "ak-wee-ES-uhns"},
            {"word": "Customary", "translation": "Consuetudinario", "example": "It is a customary right.", "pronunciation": "KUS-tuh-mer-ee"},
            {"word": "Execrable", "translation": "Execrable", "example": "His behavior was execrable.", "pronunciation": "EK-sih-kruh-bul"},
            {"word": "Resentment", "translation": "Resquemor", "example": "He still holds some resentment.", "pronunciation": "rih-ZENT-muhnt"},
        ]
    },
    "portuguese": {
        "A1": [
            {"word": "Olá", "translation": "Hello/Hola", "example": "Olá! Como vai você?", "pronunciation": "oh-LAH"},
            {"word": "Obrigado/a", "translation": "Thank you/Gracias", "example": "Muito obrigado pela ajuda.", "pronunciation": "oh-bree-GAH-doo"},
            {"word": "Por favor", "translation": "Please/Por favor", "example": "Um café, por favor.", "pronunciation": "por fah-VOR"},
            {"word": "Bom dia", "translation": "Good morning/Buenos días", "example": "Bom dia! Tudo bem?", "pronunciation": "bom DEE-ah"},
            {"word": "Boa noite", "translation": "Good night/Buenas noches", "example": "Boa noite, até amanhã.", "pronunciation": "BOH-ah NOY-chee"},
            {"word": "Sim", "translation": "Yes/Sí", "example": "Sim, eu entendo.", "pronunciation": "seem"},
            {"word": "Não", "translation": "No/No", "example": "Não, obrigado.", "pronunciation": "nowng"},
            {"word": "Água", "translation": "Water/Agua", "example": "Um copo de água, por favor.", "pronunciation": "AH-gwah"},
            {"word": "Casa", "translation": "House/Casa", "example": "Minha casa é pequena.", "pronunciation": "KAH-zah"},
            {"word": "Família", "translation": "Family/Familia", "example": "Minha família é grande.", "pronunciation": "fah-MEE-lyah"},
        ],
        "A2": [
            {"word": "Trabalhar", "translation": "To work/Trabajar", "example": "Eu trabalho em um escritório.", "pronunciation": "trah-bah-LYAR"},
            {"word": "Comer", "translation": "To eat/Comer", "example": "Eu gosto de comer pizza.", "pronunciation": "koh-MER"},
            {"word": "Comprar", "translation": "To buy/Comprar", "example": "Vou comprar pão.", "pronunciation": "kohm-PRAR"},
            {"word": "Bonito", "translation": "Beautiful/Bonito", "example": "O vestido é muito bonito.", "pronunciation": "boh-NEE-too"},
            {"word": "Barato", "translation": "Cheap/Barato", "example": "Este livro é barato.", "pronunciation": "bah-RAH-too"},
            {"word": "Caro", "translation": "Expensive/Caro", "example": "O carro é muito caro.", "pronunciation": "KAH-roo"},
            {"word": "Sempre", "translation": "Always/Siempre", "example": "Sempre chego cedo.", "pronunciation": "SEM-pree"},
            {"word": "Nunca", "translation": "Never/Nunca", "example": "Nunca como carne.", "pronunciation": "NOON-kah"},
            {"word": "Perto", "translation": "Near/Cerca", "example": "O banco está perto.", "pronunciation": "PER-too"},
            {"word": "Longe", "translation": "Far/Lejos", "example": "Meu trabalho fica longe.", "pronunciation": "LON-zhee"},
        ],
        "B1": [
            {"word": "Desenvolver", "translation": "To develop/Desarrollar", "example": "Quero desenvolver minhas habilidades.", "pronunciation": "deh-zen-vol-VER"},
            {"word": "Conseguir", "translation": "To achieve/Conseguir", "example": "Vou conseguir o emprego.", "pronunciation": "kon-seh-GEER"},
            {"word": "Melhorar", "translation": "To improve/Mejorar", "example": "Preciso melhorar meu português.", "pronunciation": "mel-yo-RAR"},
            {"word": "Embora", "translation": "Although/Aunque", "example": "Embora chova, vou sair.", "pronunciation": "em-BOH-rah"},
            {"word": "Porém", "translation": "However/Sin embargo", "example": "Gosto; porém, é caro.", "pronunciation": "poh-REM"},
            {"word": "Enquanto", "translation": "While/Mientras", "example": "Estudo enquanto trabalho.", "pronunciation": "en-KWAN-too"},
            {"word": "Esperança", "translation": "Hope/Esperanza", "example": "Tenho esperança no futuro.", "pronunciation": "es-peh-RAN-sah"},
            {"word": "Preocupar-se", "translation": "To worry/Preocuparse", "example": "Não se preocupe com isso.", "pronunciation": "preh-oh-koo-PAR-see"},
            {"word": "Aproveitar", "translation": "To enjoy/Disfrutar", "example": "Aproveito muito a música.", "pronunciation": "ah-proh-vey-TAR"},
            {"word": "Realizar", "translation": "To accomplish/Realizar", "example": "Vou realizar meu sonho.", "pronunciation": "heh-ah-lee-ZAR"},
        ],
        "B2": [
            {"word": "Imprescindível", "translation": "Essential/Imprescindible", "example": "A água é imprescindível para viver.", "pronunciation": "eem-pres-seen-DEE-vel"},
            {"word": "Aproveitar", "translation": "To take advantage/Aprovechar", "example": "Deve aproveitar esta oportunidade.", "pronunciation": "ah-proh-vey-TAR"},
            {"word": "Destacar", "translation": "To stand out/Destacar", "example": "Seu trabalho destaca pela qualidade.", "pronunciation": "des-tah-KAR"},
            {"word": "Apesar de", "translation": "Despite/A pesar de", "example": "Apesar de tudo, sou feliz.", "pronunciation": "ah-peh-ZAR dee"},
            {"word": "Igualmente", "translation": "Likewise/Asimismo", "example": "Igualmente, devemos considerar outros fatores.", "pronunciation": "ee-gwal-MEN-tee"},
            {"word": "Questionar", "translation": "To question/Cuestionar", "example": "É importante questionar as notícias.", "pronunciation": "kes-tee-oh-NAR"},
            {"word": "Proporcionar", "translation": "To provide/Proporcionar", "example": "Vou proporcionar toda a informação.", "pronunciation": "proh-por-see-oh-NAR"},
            {"word": "Sustentar", "translation": "To sustain/Sostener", "example": "Sustento minha opinião firmemente.", "pronunciation": "soos-ten-TAR"},
            {"word": "Abordar", "translation": "To address/Abordar", "example": "Devemos abordar este problema.", "pronunciation": "ah-bor-DAR"},
            {"word": "Vincular", "translation": "To link/Vincular", "example": "Há que vincular teoria e prática.", "pronunciation": "veen-koo-LAR"},
        ],
        "C1": [
            {"word": "Entranhável", "translation": "Endearing/Entrañable", "example": "É uma lembrança entranhável da infância.", "pronunciation": "en-tran-YAH-vel"},
            {"word": "Idiossincrasia", "translation": "Idiosyncrasy/Idiosincrasia", "example": "Cada cultura tem sua própria idiossincrasia.", "pronunciation": "ee-dee-oh-seen-KRAH-zyah"},
            {"word": "Escrutinar", "translation": "To scrutinize/Escudriñar", "example": "Há que escrutinar os dados cuidadosamente.", "pronunciation": "es-kroo-tee-NAR"},
            {"word": "Subjacente", "translation": "Underlying/Subyacente", "example": "Vários fatores são subjacentes a este fenômeno.", "pronunciation": "soob-zhah-SEN-tee"},
            {"word": "Elucidar", "translation": "To elucidate/Elucidar", "example": "O professor elucidou o conceito complexo.", "pronunciation": "eh-loo-see-DAR"},
            {"word": "Acarretar", "translation": "To entail/Conllevar", "example": "Este projeto acarreta grandes responsabilidades.", "pronunciation": "ah-kah-heh-TAR"},
            {"word": "Dilucidar", "translation": "To clarify/Dilucidar", "example": "Tentarei dilucidar este mistério.", "pronunciation": "dee-loo-see-DAR"},
            {"word": "Desdenhar", "translation": "To disdain/Desdeñar", "example": "Não devemos desdenhar as opiniões alheias.", "pronunciation": "des-den-YAR"},
            {"word": "Inerente", "translation": "Inherent/Inherente", "example": "A criatividade é inerente ao ser humano.", "pronunciation": "ee-neh-REN-tee"},
            {"word": "Contornar", "translation": "To sidestep/Soslayar", "example": "Não podemos contornar este problema.", "pronunciation": "kon-tor-NAR"},
        ],
        "C2": [
            {"word": "Variegado", "translation": "Motley/Abigarrado", "example": "Era um grupo variegado de pessoas.", "pronunciation": "vah-ree-eh-GAH-doo"},
            {"word": "Desabrido", "translation": "Bland/Desabrido", "example": "Sua resposta foi desabrida.", "pronunciation": "deh-zah-BREE-doo"},
            {"word": "Acérrimo", "translation": "Staunch/Acérrimo", "example": "É um acérrimo defensor dos direitos.", "pronunciation": "ah-SEH-hee-moo"},
            {"word": "Recôndito", "translation": "Hidden/Recóndito", "example": "Exploramos lugares recônditos.", "pronunciation": "heh-KON-dee-too"},
            {"word": "Sempiterno", "translation": "Everlasting/Sempiterno", "example": "Seu amor é sempiterno.", "pronunciation": "sem-pee-TER-noo"},
            {"word": "Pristino", "translation": "Pristine/Prístino", "example": "A floresta estava em estado pristino.", "pronunciation": "PREES-tee-noo"},
            {"word": "Aquiescência", "translation": "Acquiescence/Aquiescencia", "example": "Sua aquiescência surpreendeu a todos.", "pronunciation": "ah-kee-es-SEN-syah"},
            {"word": "Consuetudinário", "translation": "Customary/Consuetudinario", "example": "É um direito consuetudinário.", "pronunciation": "kon-sweh-too-dee-NAH-ryoo"},
            {"word": "Execrável", "translation": "Execrable/Execrable", "example": "Seu comportamento foi execrável.", "pronunciation": "ek-seh-KRAH-vel"},
            {"word": "Ressentimento", "translation": "Resentment/Resquemor", "example": "Ainda guarda certo ressentimento.", "pronunciation": "heh-sen-tee-MEN-too"},
        ]
    }
}

# Lecciones básicas por nivel
LESSONS = {
    "A1": [
        {"title": "Saludos y Presentaciones", "content": "Aprende a saludar y presentarte. Vocabulario básico para conocer a nuevas personas."},
        {"title": "Números y Colores", "content": "Los números del 1 al 100 y los colores principales."},
        {"title": "La Familia", "content": "Vocabulario de la familia: madre, padre, hermano, hermana, abuelos."},
    ],
    "A2": [
        {"title": "Ir de Compras", "content": "Vocabulario y frases útiles para ir de compras."},
        {"title": "Rutina Diaria", "content": "Describir actividades cotidianas y horarios."},
        {"title": "El Clima y las Estaciones", "content": "Hablar sobre el tiempo y las estaciones del año."},
    ],
    "B1": [
        {"title": "Expresar Opiniones", "content": "Frases y estructuras para dar tu opinión."},
        {"title": "Viajes y Turismo", "content": "Vocabulario para planificar y hablar de viajes."},
        {"title": "Salud y Bienestar", "content": "Vocabulario médico básico y cómo describir síntomas."},
    ],
    "B2": [
        {"title": "El Mundo Laboral", "content": "Vocabulario profesional y comunicación en el trabajo."},
        {"title": "Actualidad y Noticias", "content": "Discutir eventos actuales y medios de comunicación."},
        {"title": "Cultura y Tradiciones", "content": "Explorar tradiciones culturales y festividades."},
    ],
    "C1": [
        {"title": "Argumentación Avanzada", "content": "Técnicas para construir argumentos sólidos."},
        {"title": "Lenguaje Académico", "content": "Vocabulario y estructuras para contextos académicos."},
        {"title": "Matices Culturales", "content": "Comprender sutilezas culturales y expresiones idiomáticas."},
    ],
    "C2": [
        {"title": "Registro Literario", "content": "Análisis de textos literarios y estilo avanzado."},
        {"title": "Dialectos y Variantes", "content": "Explorar variaciones regionales del idioma."},
        {"title": "Comunicación Profesional", "content": "Dominio del lenguaje en contextos de alto nivel."},
    ]
}

async def seed_database():
    """Poblar la base de datos con contenido educativo completo."""
    
    # Limpiar datos existentes
    await db.courses.delete_many({})
    await db.flashcards.delete_many({})
    await db.lessons.delete_many({})
    
    languages = ["spanish", "english", "portuguese"]
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    course_count = 0
    flashcard_count = 0
    lesson_count = 0
    
    for language in languages:
        for level in levels:
            # Crear curso
            course_info = COURSE_CONTENT[language][level]
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
            
            # Crear lecciones para el curso
            lesson_templates = LESSONS[level]
            for i, lesson_template in enumerate(lesson_templates):
                lesson_doc = {
                    "course_id": course_id,
                    "title": lesson_template["title"],
                    "content": lesson_template["content"],
                    "vocabulary": [],
                    "grammar_points": [],
                    "order": i + 1,
                    "created_at": datetime.utcnow()
                }
                await db.lessons.insert_one(lesson_doc)
                lesson_count += 1
            
            # Crear flashcards
            flashcards = FLASHCARDS[language][level]
            for card in flashcards:
                flashcard_doc = {
                    "language": language,
                    "level": level,
                    "word": card["word"],
                    "translation": card["translation"],
                    "example": card["example"],
                    "pronunciation": card["pronunciation"],
                    "created_by": "system",
                    "created_at": datetime.utcnow()
                }
                await db.flashcards.insert_one(flashcard_doc)
                flashcard_count += 1
    
    print(f"✅ Contenido creado exitosamente:")
    print(f"   - {course_count} cursos")
    print(f"   - {lesson_count} lecciones")
    print(f"   - {flashcard_count} flashcards")
    
    return {
        "courses": course_count,
        "lessons": lesson_count,
        "flashcards": flashcard_count
    }

if __name__ == "__main__":
    asyncio.run(seed_database())

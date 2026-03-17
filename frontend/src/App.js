import { useState } from "react";
import "@/App.css";
import { 
  BookOpen, 
  MessageCircle, 
  Mic, 
  Brain, 
  ChevronRight, 
  Globe, 
  GraduationCap,
  Sparkles,
  Volume2,
  CheckCircle,
  Target,
  Users,
  Award,
  ArrowRight,
  Play,
  Lightbulb,
  BookMarked
} from "lucide-react";

// ==================== DATA ====================

const LANGUAGES = [
  { id: 'spanish', name: 'Español', flag: '🇨🇷', greeting: '¡Pura Vida!', color: '#22955B' },
  { id: 'english', name: 'English', flag: '🇺🇸', greeting: 'Hello!', color: '#003189' },
  { id: 'french', name: 'Français', flag: '🇫🇷', greeting: 'Bonjour!', color: '#003189' },
  { id: 'german', name: 'Deutsch', flag: '🇩🇪', greeting: 'Hallo!', color: '#1a1a1a' },
  { id: 'portuguese', name: 'Português', flag: '🇧🇷', greeting: 'Olá!', color: '#fa8a00' },
];

const LEVELS = [
  { id: 'A1', title: 'Acceso (A1)', desc: 'Principiante. Entiende y usa expresiones cotidianas.', topics: ['Saludos', 'Presentación', 'Comidas'], color: '#B6C932' },
  { id: 'A2', title: 'Plataforma (A2)', desc: 'Básico. Se comunica en tareas sencillas y habituales.', topics: ['Familia', 'Compras', 'Trabajo'], color: '#8fb82a' },
  { id: 'B1', title: 'Umbral (B1)', desc: 'Intermedio. Puede lidiar con situaciones de viaje.', topics: ['Viajes', 'Opiniones', 'Eventos'], color: '#fa8a00' },
  { id: 'B2', title: 'Avanzado (B2)', desc: 'Intermedio Alto. Entiende textos complejos y técnicos.', topics: ['Debates', 'Cultura', 'Negocios'], color: '#f07800' },
  { id: 'C1', title: 'Dominio (C1)', desc: 'Avanzado. Se expresa con fluidez y espontaneidad.', topics: ['Académico', 'Profesional', 'Matices'], color: '#e34b33' },
  { id: 'C2', title: 'Maestría (C2)', desc: 'Experto. Comprende todo lo que oye y lee.', topics: ['Literatura', 'Ciencia', 'Nativo'], color: '#c43d2a' },
];

// Real lesson content from the app
const LESSONS_DATA = {
  spanish: {
    A1: {
      title: "Saludos y Presentaciones",
      content: "Aprende a saludar y presentarte en español. Estas son las expresiones más importantes que necesitarás para conocer a nuevas personas.",
      vocabulary: [
        { word: "Hola", translation: "Hello", example: "¡Hola! ¿Cómo estás?", pronunciation: "OH-lah" },
        { word: "Buenos días", translation: "Good morning", example: "Buenos días, señor.", pronunciation: "BWEH-nohs DEE-ahs" },
        { word: "Gracias", translation: "Thank you", example: "Muchas gracias por tu ayuda.", pronunciation: "GRAH-syahs" },
        { word: "Por favor", translation: "Please", example: "Un café, por favor.", pronunciation: "por fah-VOR" },
      ],
      grammar: [
        "El verbo 'ser' se usa para identidad: Yo SOY María, Tú ERES estudiante",
        "Los artículos: EL (masculino), LA (femenino), LOS/LAS (plural)",
        "Orden básico: Sujeto + Verbo + Objeto",
      ]
    },
    B1: {
      title: "Expresar Opiniones",
      content: "Aprende a dar tu opinión de forma educada y participar en conversaciones más complejas.",
      vocabulary: [
        { word: "Desarrollar", translation: "To develop", example: "Quiero desarrollar mis habilidades.", pronunciation: "deh-sah-roh-YAR" },
        { word: "Sin embargo", translation: "However", example: "Me gusta; sin embargo, es caro.", pronunciation: "seen em-BAR-goh" },
        { word: "Mejorar", translation: "To improve", example: "Necesito mejorar mi español.", pronunciation: "meh-hoh-RAR" },
        { word: "Aunque", translation: "Although", example: "Aunque llueve, saldré.", pronunciation: "OWN-keh" },
      ],
      grammar: [
        "Subjuntivo para expresar duda: Dudo que él VENGA",
        "Condicionales: Si yo TUVIERA dinero, viajaría",
        "Conectores de contraste: aunque, sin embargo, no obstante",
      ]
    }
  },
  english: {
    A1: {
      title: "Greetings and Introductions",
      content: "Learn to greet and introduce yourself in English. These are the most important expressions you'll need to meet new people.",
      vocabulary: [
        { word: "Hello", translation: "Hola", example: "Hello, how are you?", pronunciation: "heh-LOH" },
        { word: "Good morning", translation: "Buenos días", example: "Good morning, everyone!", pronunciation: "good MOR-ning" },
        { word: "Thank you", translation: "Gracias", example: "Thank you very much.", pronunciation: "THANK yoo" },
        { word: "Please", translation: "Por favor", example: "A coffee, please.", pronunciation: "pleez" },
      ],
      grammar: [
        "Verb 'to be': I AM, You ARE, He/She IS",
        "Articles: A (consonant), AN (vowel), THE (specific)",
        "Basic order: Subject + Verb + Object",
      ]
    },
    B1: {
      title: "Expressing Opinions",
      content: "Learn to give your opinion politely and participate in more complex conversations.",
      vocabulary: [
        { word: "To develop", translation: "Desarrollar", example: "I want to develop my skills.", pronunciation: "dih-VEL-uhp" },
        { word: "However", translation: "Sin embargo", example: "I like it; however, it's expensive.", pronunciation: "how-EV-er" },
        { word: "To improve", translation: "Mejorar", example: "I need to improve my English.", pronunciation: "im-PROOV" },
        { word: "Although", translation: "Aunque", example: "Although it's raining, I'll go out.", pronunciation: "awl-THOH" },
      ],
      grammar: [
        "Conditionals: If I HAD money, I would travel",
        "Present Perfect: I HAVE BEEN learning for 2 years",
        "Linking words: however, nevertheless, although",
      ]
    }
  },
  french: {
    A1: {
      title: "Salutations et Présentations",
      content: "Apprenez à saluer et à vous présenter en français. Ce sont les expressions les plus importantes pour rencontrer de nouvelles personnes.",
      vocabulary: [
        { word: "Bonjour", translation: "Hello/Good day", example: "Bonjour, comment allez-vous?", pronunciation: "bon-ZHOOR" },
        { word: "Merci", translation: "Thank you", example: "Merci beaucoup!", pronunciation: "mer-SEE" },
        { word: "S'il vous plaît", translation: "Please", example: "Un café, s'il vous plaît.", pronunciation: "seel voo PLEH" },
        { word: "Au revoir", translation: "Goodbye", example: "Au revoir, à demain!", pronunciation: "oh reh-VWAHR" },
      ],
      grammar: [
        "Le verbe 'être': Je SUIS, Tu ES, Il/Elle EST",
        "Les articles: LE (masc.), LA (fem.), LES (pluriel)",
        "Ordre basique: Sujet + Verbe + Objet",
      ]
    }
  },
  german: {
    A1: {
      title: "Grüße und Vorstellungen",
      content: "Lernen Sie, auf Deutsch zu grüßen und sich vorzustellen. Dies sind die wichtigsten Ausdrücke, um neue Leute kennenzulernen.",
      vocabulary: [
        { word: "Hallo", translation: "Hello", example: "Hallo, wie geht es dir?", pronunciation: "HAH-loh" },
        { word: "Guten Morgen", translation: "Good morning", example: "Guten Morgen, Herr Schmidt.", pronunciation: "GOO-ten MOR-gen" },
        { word: "Danke", translation: "Thank you", example: "Vielen Dank für Ihre Hilfe.", pronunciation: "DAHN-keh" },
        { word: "Bitte", translation: "Please", example: "Einen Kaffee, bitte.", pronunciation: "BIT-teh" },
      ],
      grammar: [
        "Das Verb 'sein': Ich BIN, Du BIST, Er/Sie IST",
        "Die Artikel: DER (mask.), DIE (fem.), DAS (neutr.)",
        "Grundlegende Wortstellung: Subjekt + Verb + Objekt",
      ]
    }
  },
  portuguese: {
    A1: {
      title: "Saudações e Apresentações",
      content: "Aprenda a cumprimentar e se apresentar em português. Estas são as expressões mais importantes para conhecer novas pessoas.",
      vocabulary: [
        { word: "Olá", translation: "Hello", example: "Olá! Como vai você?", pronunciation: "oh-LAH" },
        { word: "Bom dia", translation: "Good morning", example: "Bom dia! Tudo bem?", pronunciation: "bom DEE-ah" },
        { word: "Obrigado/a", translation: "Thank you", example: "Muito obrigado pela ajuda.", pronunciation: "oh-bree-GAH-doo" },
        { word: "Por favor", translation: "Please", example: "Um café, por favor.", pronunciation: "por fah-VOR" },
      ],
      grammar: [
        "O verbo 'ser': Eu SOU, Tu ÉS, Ele/Ela É",
        "Os artigos: O (masc.), A (fem.), OS/AS (plural)",
        "Ordem básica: Sujeito + Verbo + Objeto",
      ]
    }
  }
};

const FLASHCARDS_DATA = [
  { word: "Hola", translation: "Hello", language: "spanish", level: "A1" },
  { word: "Gracias", translation: "Thank you", language: "spanish", level: "A1" },
  { word: "Hello", translation: "Hola", language: "english", level: "A1" },
  { word: "Bonjour", translation: "Hello", language: "french", level: "A1" },
  { word: "Hallo", translation: "Hello", language: "german", level: "A1" },
];

const FEATURES = [
  {
    icon: Brain,
    title: "Ejercicios con IA",
    description: "Ejercicios generativos personalizados con GPT-4 que se adaptan a tu nivel.",
    color: "#22955B",
    large: true
  },
  {
    icon: Volume2,
    title: "Pronunciación TTS",
    description: "Audio de alta calidad con ElevenLabs para una pronunciación perfecta.",
    color: "#fa8a00"
  },
  {
    icon: Target,
    title: "Quizzes Interactivos",
    description: "Evalúa tu progreso con tests dinámicos por nivel.",
    color: "#003189"
  }
];

// ==================== COMPONENTS ====================

const Navigation = () => (
  <nav className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #22955B 0%, #B6C932 100%)' }}>
            <Globe className="w-5 h-5 text-white" />
          </div>
          <span className="font-serif text-xl font-bold text-gray-900">Intercultura</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8">
          <a href="#idiomas" className="nav-link">Idiomas</a>
          <a href="#niveles" className="nav-link">Niveles</a>
          <a href="#lecciones" className="nav-link">Lecciones</a>
          <a href="#caracteristicas" className="nav-link">Características</a>
        </div>
        
        <button className="btn-primary text-sm" data-testid="cta-descargar-nav">
          <Play className="w-4 h-4" />
          Comenzar
        </button>
      </div>
    </div>
  </nav>
);

const CodePhone = ({ selectedLanguage, selectedLevel }) => {
  const [activeTab, setActiveTab] = useState('vocab');
  const lesson = LESSONS_DATA[selectedLanguage]?.[selectedLevel] || LESSONS_DATA.spanish.A1;
  
  return (
    <div className="relative animate-float">
      {/* Floating bubbles */}
      <div className="chat-bubble spanish">
        <span className="mr-2">🇨🇷</span> ¡Hola!
      </div>
      <div className="chat-bubble english">
        <span className="mr-2">🇺🇸</span> Hello!
      </div>
      <div className="chat-bubble french">
        <span className="mr-2">🇫🇷</span> Bonjour!
      </div>
      <div className="chat-bubble german">
        <span className="mr-2">🇩🇪</span> Hallo!
      </div>
      <div className="chat-bubble portuguese">
        <span className="mr-2">🇧🇷</span> Olá!
      </div>
      
      {/* Phone */}
      <div className="code-phone" data-testid="code-phone">
        <div className="code-phone-screen">
          {/* App Header */}
          <div className="px-4 py-3 bg-gradient-to-r from-[#22955B] to-[#B6C932]">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-white" />
              <span className="text-white font-semibold text-sm">{lesson.title}</span>
            </div>
          </div>
          
          {/* Tabs */}
          <div className="flex border-b border-gray-100">
            <button 
              className={`tab-button flex-1 text-xs ${activeTab === 'vocab' ? 'active' : ''}`}
              onClick={() => setActiveTab('vocab')}
              data-testid="tab-vocab"
            >
              Vocabulario
            </button>
            <button 
              className={`tab-button flex-1 text-xs ${activeTab === 'grammar' ? 'active' : ''}`}
              onClick={() => setActiveTab('grammar')}
              data-testid="tab-grammar"
            >
              Gramática
            </button>
          </div>
          
          {/* Content */}
          <div className="p-4 overflow-y-auto" style={{ maxHeight: '380px' }}>
            {activeTab === 'vocab' && (
              <div className="space-y-3">
                {lesson.vocabulary.map((item, index) => (
                  <div key={index} className="bg-gray-50 rounded-xl p-3 hover:bg-gray-100 transition-colors">
                    <div className="flex justify-between items-start mb-1">
                      <span className="font-bold text-gray-900 text-sm">{item.word}</span>
                      <button className="text-[#22955B] hover:text-[#1a7346]">
                        <Volume2 className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-gray-500 text-xs">{item.translation}</p>
                    <p className="text-gray-400 text-xs italic mt-1">"{item.example}"</p>
                  </div>
                ))}
              </div>
            )}
            
            {activeTab === 'grammar' && (
              <div className="space-y-3">
                {lesson.grammar.map((point, index) => (
                  <div key={index} className="flex gap-3 bg-gradient-to-r from-[#22955B]/5 to-[#B6C932]/5 rounded-xl p-3">
                    <div className="w-6 h-6 rounded-full bg-[#22955B] flex items-center justify-center flex-shrink-0">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                    <p className="text-gray-700 text-xs leading-relaxed">{point}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {/* Bottom Button */}
          <div className="absolute bottom-4 left-4 right-4">
            <button className="w-full py-3 bg-[#22955B] text-white rounded-xl font-semibold text-sm flex items-center justify-center gap-2">
              <CheckCircle className="w-4 h-4" />
              Completar Lección
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const HeroSection = ({ selectedLanguage, setSelectedLanguage, selectedLevel, setSelectedLevel }) => (
  <section className="hero-section pt-24" data-testid="hero-section">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-16 items-center min-h-[calc(100vh-6rem)]">
        {/* Left Content */}
        <div className="animate-fade-in-up">
          <span className="section-label mb-4 block">Intercultura Asistente Virtual</span>
          <h1 className="section-title mb-6">
            Hable el mundo.<br />
            <span className="text-[#22955B]">5 idiomas.</span><br />
            <span className="text-[#B6C932]">6 niveles.</span>
          </h1>
          <p className="text-lg text-gray-600 mb-8 leading-relaxed max-w-lg">
            Aprende Español, Inglés, Francés, Alemán y Portugués con lecciones reales siguiendo el Marco Común Europeo de Referencia (MCER) de A1 a C2.
          </p>
          
          <div className="flex flex-wrap gap-4 mb-12">
            <button className="btn-primary" data-testid="cta-comenzar-hero">
              Comenzar Gratis
              <ArrowRight className="w-4 h-4" />
            </button>
            <button className="btn-secondary" data-testid="cta-ver-lecciones">
              Ver Lecciones
            </button>
          </div>
          
          {/* Stats */}
          <div className="grid grid-cols-3 gap-8">
            <div>
              <p className="font-serif text-3xl font-bold text-gray-900">5</p>
              <p className="text-sm text-gray-500">Idiomas</p>
            </div>
            <div>
              <p className="font-serif text-3xl font-bold text-gray-900">180+</p>
              <p className="text-sm text-gray-500">Lecciones</p>
            </div>
            <div>
              <p className="font-serif text-3xl font-bold text-gray-900">300+</p>
              <p className="text-sm text-gray-500">Flashcards</p>
            </div>
          </div>
        </div>
        
        {/* Right - Phone */}
        <div className="flex justify-center lg:justify-end">
          <CodePhone 
            selectedLanguage={selectedLanguage} 
            selectedLevel={selectedLevel}
          />
        </div>
      </div>
    </div>
  </section>
);

const LanguageSection = ({ selectedLanguage, setSelectedLanguage }) => (
  <section id="idiomas" className="py-24 bg-white" data-testid="languages-section">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16">
        <span className="section-label mb-4 block">Idiomas Disponibles</span>
        <h2 className="section-title">Elige tu próximo idioma</h2>
        <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
          Cada idioma incluye 6 niveles completos (A1-C2) con lecciones, vocabulario, gramática y ejercicios prácticos.
        </p>
      </div>
      
      <div className="flex flex-wrap justify-center gap-6">
        {LANGUAGES.map((lang) => (
          <div
            key={lang.id}
            className={`ticket-card text-center ${selectedLanguage === lang.id ? 'active' : ''}`}
            onClick={() => setSelectedLanguage(lang.id)}
            data-testid={`language-card-${lang.id}`}
          >
            <span className="text-4xl mb-3 block">{lang.flag}</span>
            <h3 className="font-bold text-gray-900 mb-1">{lang.name}</h3>
            <p className="text-sm" style={{ color: lang.color }}>{lang.greeting}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const LevelsSection = ({ selectedLevel, setSelectedLevel }) => (
  <section id="niveles" className="py-24 bg-blob-primary" data-testid="levels-section">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-16 items-start">
        {/* Left Content */}
        <div>
          <span className="section-label mb-4 block">Marco Común Europeo</span>
          <h2 className="section-title mb-6">Del principiante al experto</h2>
          <p className="text-gray-600 mb-8 leading-relaxed">
            Nuestras lecciones siguen el estándar internacional MCER utilizado por Cambridge y otras instituciones de renombre mundial.
          </p>
          
          <div className="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm">
            <div className="w-12 h-12 rounded-full bg-[#22955B]/10 flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-[#22955B]" />
            </div>
            <div>
              <p className="font-bold text-gray-900">Metodología Cambridge</p>
              <p className="text-sm text-gray-500">Contenido certificado y estructurado</p>
            </div>
          </div>
        </div>
        
        {/* Right - Metro Line */}
        <div className="metro-line">
          {LEVELS.map((level) => (
            <div 
              key={level.id} 
              className={`metro-station level-${level.id.toLowerCase()} cursor-pointer`}
              onClick={() => setSelectedLevel(level.id)}
              data-testid={`level-station-${level.id}`}
            >
              <div className={`bg-white rounded-xl p-5 shadow-sm transition-all ${selectedLevel === level.id ? 'ring-2 ring-[#22955B] shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-2">
                  <span 
                    className="text-xs font-bold px-2 py-1 rounded-full text-white"
                    style={{ backgroundColor: level.color }}
                  >
                    {level.id}
                  </span>
                  <h3 className="font-bold text-gray-900">{level.title}</h3>
                </div>
                <p className="text-sm text-gray-600 mb-3">{level.desc}</p>
                <div className="flex flex-wrap gap-2">
                  {level.topics.map((topic, i) => (
                    <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

const LessonsSection = ({ selectedLanguage, selectedLevel }) => {
  const lesson = LESSONS_DATA[selectedLanguage]?.[selectedLevel] || LESSONS_DATA.spanish.A1;
  const langInfo = LANGUAGES.find(l => l.id === selectedLanguage) || LANGUAGES[0];
  
  return (
    <section id="lecciones" className="py-24 bg-white" data-testid="lessons-section">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="section-label mb-4 block">Contenido Real</span>
          <h2 className="section-title">
            Lecciones de {langInfo.name} - Nivel {selectedLevel}
          </h2>
          <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
            Explora una muestra del contenido educativo real que encontrarás en nuestra aplicación.
          </p>
        </div>
        
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Lesson Card */}
          <div className="lesson-card" data-testid="lesson-preview-card">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: langInfo.color + '20' }}>
                <BookOpen className="w-5 h-5" style={{ color: langInfo.color }} />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">{lesson.title}</h3>
                <p className="text-sm text-gray-500">{langInfo.flag} {langInfo.name} • {selectedLevel}</p>
              </div>
            </div>
            
            <p className="text-gray-600 mb-6">{lesson.content}</p>
            
            <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
              <BookMarked className="w-4 h-4 text-[#22955B]" />
              Vocabulario
            </h4>
            
            <div className="space-y-3">
              {lesson.vocabulary.map((item, index) => (
                <div key={index} className="vocab-item" data-testid={`vocab-item-${index}`}>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900">{item.word}</span>
                      <span className="text-xs text-gray-400">[{item.pronunciation}]</span>
                    </div>
                    <p className="text-sm text-gray-500">{item.translation}</p>
                    <p className="text-sm text-gray-400 italic">"{item.example}"</p>
                  </div>
                  <button className="text-[#22955B] hover:text-[#1a7346] p-2">
                    <Volume2 className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
          
          {/* Grammar Card */}
          <div>
            <div className="grammar-box mb-6" data-testid="grammar-box">
              <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-[#fa8a00]" />
                Puntos Gramaticales
              </h4>
              
              <div className="space-y-4">
                {lesson.grammar.map((point, index) => (
                  <div key={index} className="flex gap-3">
                    <div className="w-6 h-6 rounded-full bg-[#B6C932] flex items-center justify-center flex-shrink-0">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                    <p className="text-gray-700">{point}</p>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Quick Quiz Preview */}
            <div className="bg-gradient-to-br from-[#22955B] to-[#B6C932] rounded-2xl p-6 text-white">
              <h4 className="font-bold mb-2 flex items-center gap-2">
                <Sparkles className="w-5 h-5" />
                Quiz Rápido
              </h4>
              <p className="text-white/80 text-sm mb-4">
                Pon a prueba tu conocimiento con preguntas interactivas después de cada lección.
              </p>
              <div className="bg-white/20 rounded-xl p-4">
                <p className="font-medium mb-3">¿Cómo se dice "Hello" en español?</p>
                <div className="grid grid-cols-2 gap-2">
                  {['Hola', 'Gracias', 'Adiós', 'Por favor'].map((opt, i) => (
                    <button key={i} className="bg-white/20 hover:bg-white/30 rounded-lg py-2 text-sm transition-colors">
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const FlashcardsSection = () => {
  const [currentCard, setCurrentCard] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  
  const card = FLASHCARDS_DATA[currentCard];
  const langInfo = LANGUAGES.find(l => l.id === card.language);
  
  const nextCard = () => {
    setIsFlipped(false);
    setTimeout(() => {
      setCurrentCard((prev) => (prev + 1) % FLASHCARDS_DATA.length);
    }, 150);
  };
  
  return (
    <section className="py-24 bg-blob-accent" data-testid="flashcards-section">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="section-label mb-4 block">Flashcards</span>
          <h2 className="section-title">Aprende con repetición espaciada</h2>
          <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
            Más de 300 flashcards con pronunciación de audio para memorizar vocabulario de forma efectiva.
          </p>
        </div>
        
        <div className="flex flex-col items-center">
          <div className="flashcard-container mb-8">
            <div 
              className={`flashcard ${isFlipped ? 'flipped' : ''}`}
              onClick={() => setIsFlipped(!isFlipped)}
              data-testid="flashcard"
            >
              <div className="flashcard-face flashcard-front">
                <span className="text-4xl mb-2">{langInfo?.flag}</span>
                <span className="text-3xl font-bold">{card.word}</span>
                <span className="text-white/70 text-sm mt-2">Toca para voltear</span>
              </div>
              <div className="flashcard-face flashcard-back">
                <span className="text-2xl font-bold text-gray-900">{card.translation}</span>
                <span className="text-[#22955B] text-sm mt-2">{card.level} • {langInfo?.name}</span>
              </div>
            </div>
          </div>
          
          <div className="flex gap-4">
            <button 
              className="px-6 py-3 bg-[#fa8a00] text-white rounded-xl font-semibold hover:bg-[#e07b00] transition-colors"
              onClick={nextCard}
              data-testid="flashcard-next"
            >
              Estudiar de nuevo
            </button>
            <button 
              className="px-6 py-3 bg-[#22955B] text-white rounded-xl font-semibold hover:bg-[#1a7346] transition-colors"
              onClick={nextCard}
              data-testid="flashcard-know"
            >
              Lo sé ✓
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

const FeaturesSection = () => (
  <section id="caracteristicas" className="py-24 bg-white" data-testid="features-section">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16">
        <span className="section-label mb-4 block">Características</span>
        <h2 className="section-title">Tecnología al servicio del aprendizaje</h2>
      </div>
      
      <div className="bento-grid">
        {FEATURES.map((feature, index) => (
          <div 
            key={index} 
            className={`bento-item ${feature.large ? 'large' : ''}`}
            data-testid={`feature-card-${index}`}
          >
            <div 
              className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
              style={{ backgroundColor: feature.color + '15' }}
            >
              <feature.icon className="w-7 h-7" style={{ color: feature.color }} />
            </div>
            <h3 className="font-bold text-xl text-gray-900 mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.description}</p>
            
            {feature.large && (
              <div className="mt-6 p-4 bg-gray-50 rounded-xl">
                <div className="flex items-start gap-3">
                  <MessageCircle className="w-5 h-5 text-[#22955B] mt-1" />
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Ejemplo de ejercicio generado:</p>
                    <p className="text-gray-900 font-medium">"Completa la oración: Yo ___ estudiante de español."</p>
                    <div className="flex gap-2 mt-3">
                      <span className="text-xs bg-[#22955B]/10 text-[#22955B] px-3 py-1 rounded-full">soy ✓</span>
                      <span className="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full">eres</span>
                      <span className="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full">es</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  </section>
);

const Footer = () => (
  <footer className="footer" data-testid="footer">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid md:grid-cols-4 gap-12 mb-12">
        {/* Brand */}
        <div className="md:col-span-2">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #22955B 0%, #B6C932 100%)' }}>
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="font-serif text-xl font-bold text-white">Intercultura</span>
          </div>
          <p className="text-gray-400 mb-6 max-w-md">
            Asistente Virtual para aprender idiomas siguiendo la metodología Cambridge. 
            Aprende Español, Inglés, Francés, Alemán y Portugués.
          </p>
          <div className="flex gap-3">
            {LANGUAGES.map((lang) => (
              <span key={lang.id} className="text-2xl" title={lang.name}>{lang.flag}</span>
            ))}
          </div>
        </div>
        
        {/* Links */}
        <div>
          <h4 className="font-bold text-white mb-4">Idiomas</h4>
          <ul className="space-y-2">
            {LANGUAGES.map((lang) => (
              <li key={lang.id}>
                <a href={`#idiomas`} className="text-gray-400 hover:text-[#B6C932] transition-colors">
                  {lang.flag} {lang.name}
                </a>
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h4 className="font-bold text-white mb-4">Niveles</h4>
          <ul className="space-y-2">
            {LEVELS.map((level) => (
              <li key={level.id}>
                <a href={`#niveles`} className="text-gray-400 hover:text-[#B6C932] transition-colors">
                  {level.id} - {level.title.split(' ')[0]}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p className="text-gray-500 text-sm">
          © 2026 Intercultura - Escuela de Idiomas, Costa Rica. Todos los derechos reservados.
        </p>
        <div className="flex items-center gap-2">
          <span className="text-gray-500 text-sm">Versión 1.0.0</span>
          <span className="text-gray-600">•</span>
          <span className="text-xs bg-[#22955B]/20 text-[#22955B] px-2 py-1 rounded-full">
            Metodología Cambridge
          </span>
        </div>
      </div>
    </div>
  </footer>
);

// ==================== MAIN APP ====================

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState('spanish');
  const [selectedLevel, setSelectedLevel] = useState('A1');
  
  return (
    <div className="App">
      <Navigation />
      
      <HeroSection 
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
        selectedLevel={selectedLevel}
        setSelectedLevel={setSelectedLevel}
      />
      
      <LanguageSection 
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
      />
      
      <LevelsSection 
        selectedLevel={selectedLevel}
        setSelectedLevel={setSelectedLevel}
      />
      
      <LessonsSection 
        selectedLanguage={selectedLanguage}
        selectedLevel={selectedLevel}
      />
      
      <FlashcardsSection />
      
      <FeaturesSection />
      
      <Footer />
    </div>
  );
}

export default App;

import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Link, useParams, useNavigate } from "react-router-dom";
import { 
  BookOpen, MessageCircle, Mic, Brain, ChevronRight, Globe, GraduationCap,
  Sparkles, Volume2, CheckCircle, Target, Users, Award, ArrowRight, Play,
  Lightbulb, BookMarked, ArrowLeft, Home, Layers, FileText, HelpCircle,
  RotateCcw, ChevronDown, Menu, X
} from "lucide-react";
import {
  LANGUAGES, LEVELS, getContentByLanguage, getLanguageInfo, getLevelInfo,
  SPANISH_CONTENT, ENGLISH_CONTENT, FRENCH_CONTENT, GERMAN_CONTENT, PORTUGUESE_CONTENT
} from "./data/courseData";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// ==================== AUDIO TTS HOOK ====================
const useAudio = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentWord, setCurrentWord] = useState(null);

  const playAudio = async (text, language = 'spanish') => {
    if (isPlaying) return;
    
    setIsPlaying(true);
    setCurrentWord(text);
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/tts/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language })
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.audio_base64) {
          const audio = new Audio(`data:audio/${data.format};base64,${data.audio_base64}`);
          audio.onended = () => {
            setIsPlaying(false);
            setCurrentWord(null);
          };
          await audio.play();
        }
      }
    } catch (error) {
      console.log('TTS not available, using browser speech');
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language === 'spanish' ? 'es-ES' : 
                       language === 'english' ? 'en-US' :
                       language === 'french' ? 'fr-FR' :
                       language === 'german' ? 'de-DE' : 'pt-BR';
      utterance.onend = () => {
        setIsPlaying(false);
        setCurrentWord(null);
      };
      speechSynthesis.speak(utterance);
    }
  };

  return { playAudio, isPlaying, currentWord };
};

// ==================== NAVIGATION ====================
const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center gradient-primary">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="font-serif text-xl font-bold text-gray-900">Intercultura</span>
          </Link>
          
          <div className="hidden md:flex items-center gap-6">
            <Link to="/" className="nav-link">Inicio</Link>
            <Link to="/languages" className="nav-link">Idiomas</Link>
            {LANGUAGES.slice(0, 3).map(lang => (
              <Link key={lang.id} to={`/${lang.id}`} className="nav-link flex items-center gap-1">
                <span>{lang.flag}</span>
                <span className="hidden lg:inline">{lang.name}</span>
              </Link>
            ))}
          </div>
          
          <div className="flex items-center gap-4">
            <Link to="/languages" className="btn-primary text-sm hidden sm:flex" data-testid="cta-comenzar-nav">
              <Play className="w-4 h-4" />
              Comenzar
            </Link>
            <button 
              className="md:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
        
        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <div className="flex flex-col gap-2">
              <Link to="/" className="nav-link py-2" onClick={() => setIsMenuOpen(false)}>Inicio</Link>
              <Link to="/languages" className="nav-link py-2" onClick={() => setIsMenuOpen(false)}>Todos los Idiomas</Link>
              {LANGUAGES.map(lang => (
                <Link key={lang.id} to={`/${lang.id}`} className="nav-link py-2 flex items-center gap-2" onClick={() => setIsMenuOpen(false)}>
                  <span>{lang.flag}</span> {lang.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

// ==================== HOME PAGE ====================
const HomePage = () => {
  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="hero-section" data-testid="hero-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center min-h-[calc(100vh-6rem)] py-12">
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
                <Link to="/languages" className="btn-primary" data-testid="cta-comenzar-hero">
                  Comenzar Gratis
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link to="/spanish/A1" className="btn-secondary" data-testid="cta-ver-lecciones">
                  Ver Lecciones
                </Link>
              </div>
              
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
            
            <div className="flex justify-center lg:justify-end">
              <div className="grid grid-cols-2 gap-4 max-w-md">
                {LANGUAGES.map((lang, i) => (
                  <Link 
                    key={lang.id} 
                    to={`/${lang.id}`}
                    className={`ticket-card text-center hover:scale-105 transition-transform ${i === 4 ? 'col-span-2 justify-self-center w-1/2' : ''}`}
                    data-testid={`home-lang-${lang.id}`}
                  >
                    <span className="text-3xl mb-2 block">{lang.flag}</span>
                    <h3 className="font-bold text-gray-900">{lang.name}</h3>
                    <p className="text-sm" style={{ color: lang.color }}>{lang.greeting}</p>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Languages Section */}
      <section className="py-20 bg-white" data-testid="languages-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="section-label mb-4 block">Idiomas Disponibles</span>
            <h2 className="section-title">Elige tu próximo idioma</h2>
          </div>
          
          <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-6">
            {LANGUAGES.map((lang) => (
              <Link
                key={lang.id}
                to={`/${lang.id}`}
                className="ticket-card text-center group"
                data-testid={`language-card-${lang.id}`}
              >
                <span className="text-5xl mb-4 block group-hover:scale-110 transition-transform">{lang.flag}</span>
                <h3 className="font-bold text-gray-900 mb-1">{lang.name}</h3>
                <p className="text-sm text-gray-500 mb-3">{lang.nativeName}</p>
                <span className="text-sm font-medium" style={{ color: lang.color }}>
                  6 niveles →
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Levels Section */}
      <section className="py-20 bg-blob-primary" data-testid="levels-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="section-label mb-4 block">Marco Común Europeo</span>
            <h2 className="section-title">Del principiante al experto</h2>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {LEVELS.map((level) => (
              <div 
                key={level.id} 
                className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow"
                data-testid={`level-card-${level.id}`}
              >
                <div className="flex items-center gap-3 mb-3">
                  <span 
                    className="text-sm font-bold px-3 py-1 rounded-full text-white"
                    style={{ backgroundColor: level.color }}
                  >
                    {level.id}
                  </span>
                  <h3 className="font-bold text-gray-900">{level.title}</h3>
                </div>
                <p className="text-sm text-gray-600">{level.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white" data-testid="features-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="section-label mb-4 block">Características</span>
            <h2 className="section-title">Tecnología al servicio del aprendizaje</h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bento-item">
              <div className="w-14 h-14 rounded-2xl bg-[#22955B]/10 flex items-center justify-center mb-4">
                <Brain className="w-7 h-7 text-[#22955B]" />
              </div>
              <h3 className="font-bold text-xl text-gray-900 mb-2">Ejercicios con IA</h3>
              <p className="text-gray-600">Ejercicios generativos personalizados con GPT-4.</p>
            </div>
            <div className="bento-item">
              <div className="w-14 h-14 rounded-2xl bg-[#fa8a00]/10 flex items-center justify-center mb-4">
                <Volume2 className="w-7 h-7 text-[#fa8a00]" />
              </div>
              <h3 className="font-bold text-xl text-gray-900 mb-2">Audio TTS</h3>
              <p className="text-gray-600">Pronunciación con ElevenLabs de alta calidad.</p>
            </div>
            <div className="bento-item">
              <div className="w-14 h-14 rounded-2xl bg-[#003189]/10 flex items-center justify-center mb-4">
                <Target className="w-7 h-7 text-[#003189]" />
              </div>
              <h3 className="font-bold text-xl text-gray-900 mb-2">Quizzes</h3>
              <p className="text-gray-600">Evalúa tu progreso con tests interactivos.</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

// ==================== LANGUAGES LIST PAGE ====================
const LanguagesPage = () => {
  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link to="/" className="text-[#22955B] hover:underline flex items-center gap-1 mb-4">
            <ArrowLeft className="w-4 h-4" /> Volver al inicio
          </Link>
          <h1 className="section-title">Todos los Idiomas</h1>
          <p className="text-gray-600 mt-2">Selecciona un idioma para ver todos los niveles y lecciones disponibles.</p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {LANGUAGES.map((lang) => {
            const content = getContentByLanguage(lang.id);
            const totalLessons = Object.values(content).reduce((acc, level) => acc + (level.lessons?.length || 0), 0);
            
            return (
              <Link
                key={lang.id}
                to={`/${lang.id}`}
                className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-lg transition-all group border-l-4"
                style={{ borderLeftColor: lang.color }}
                data-testid={`lang-page-${lang.id}`}
              >
                <span className="text-6xl mb-4 block group-hover:scale-110 transition-transform">{lang.flag}</span>
                <h2 className="font-serif text-2xl font-bold text-gray-900 mb-2">{lang.name}</h2>
                <p className="text-gray-500 mb-4">{lang.nativeName}</p>
                
                <div className="flex gap-4 text-sm text-gray-600 mb-4">
                  <span className="flex items-center gap-1">
                    <Layers className="w-4 h-4" /> 6 niveles
                  </span>
                  <span className="flex items-center gap-1">
                    <FileText className="w-4 h-4" /> {totalLessons}+ lecciones
                  </span>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  {LEVELS.map(level => (
                    <span 
                      key={level.id}
                      className="text-xs px-2 py-1 rounded-full text-white"
                      style={{ backgroundColor: level.color }}
                    >
                      {level.id}
                    </span>
                  ))}
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ==================== LANGUAGE PAGE (shows all levels) ====================
const LanguagePage = () => {
  const { languageId } = useParams();
  const langInfo = getLanguageInfo(languageId);
  const content = getContentByLanguage(languageId);
  
  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link to="/languages" className="text-[#22955B] hover:underline flex items-center gap-1 mb-4">
            <ArrowLeft className="w-4 h-4" /> Todos los idiomas
          </Link>
          
          <div className="flex items-center gap-4 mb-4">
            <span className="text-6xl">{langInfo.flag}</span>
            <div>
              <h1 className="section-title">{langInfo.name}</h1>
              <p className="text-gray-600">{langInfo.greeting}</p>
            </div>
          </div>
        </div>
        
        {/* Levels Grid */}
        <div className="grid gap-8">
          {LEVELS.map((level) => {
            const levelContent = content[level.id];
            const lessons = levelContent?.lessons || [];
            const flashcards = levelContent?.flashcards || [];
            const quizzes = levelContent?.quizzes || [];
            
            return (
              <div 
                key={level.id} 
                className="bg-white rounded-2xl p-6 shadow-sm"
                data-testid={`level-section-${level.id}`}
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
                  <div className="flex items-center gap-3">
                    <span 
                      className="text-lg font-bold px-4 py-2 rounded-xl text-white"
                      style={{ backgroundColor: level.color }}
                    >
                      {level.id}
                    </span>
                    <div>
                      <h2 className="font-bold text-xl text-gray-900">{level.title}</h2>
                      <p className="text-sm text-gray-500">{level.desc}</p>
                    </div>
                  </div>
                  
                  <Link 
                    to={`/${languageId}/${level.id}`}
                    className="btn-primary text-sm"
                    data-testid={`go-to-${languageId}-${level.id}`}
                  >
                    Ver todo el contenido
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
                
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen className="w-5 h-5 text-[#22955B]" />
                      <span className="font-semibold">{lessons.length} Lecciones</span>
                    </div>
                    {lessons.slice(0, 2).map((lesson, i) => (
                      <p key={i} className="text-sm text-gray-600 truncate">• {lesson.title}</p>
                    ))}
                    {lessons.length > 2 && <p className="text-sm text-gray-400">+ {lessons.length - 2} más</p>}
                  </div>
                  
                  <div className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Layers className="w-5 h-5 text-[#fa8a00]" />
                      <span className="font-semibold">{flashcards.length} Flashcards</span>
                    </div>
                    {flashcards.slice(0, 2).map((card, i) => (
                      <p key={i} className="text-sm text-gray-600 truncate">• {card.word}</p>
                    ))}
                  </div>
                  
                  <div className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <HelpCircle className="w-5 h-5 text-[#003189]" />
                      <span className="font-semibold">{quizzes.length} Quiz{quizzes.length !== 1 ? 'zes' : ''}</span>
                    </div>
                    {quizzes.map((quiz, i) => (
                      <p key={i} className="text-sm text-gray-600 truncate">• {quiz.questions?.length || 0} preguntas</p>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ==================== LEVEL PAGE (full content for a level) ====================
const LevelPage = () => {
  const { languageId, levelId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('lessons');
  const { playAudio, isPlaying, currentWord } = useAudio();
  
  const langInfo = getLanguageInfo(languageId);
  const levelInfo = getLevelInfo(levelId);
  const content = getContentByLanguage(languageId);
  const levelContent = content[levelId] || { lessons: [], quizzes: [], flashcards: [] };
  
  const { lessons, quizzes, flashcards } = levelContent;
  
  // Flashcard state
  const [currentFlashcard, setCurrentFlashcard] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  
  // Quiz state
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [quizComplete, setQuizComplete] = useState(false);
  
  const currentQuiz = quizzes[0];
  
  const handleFlashcardNext = () => {
    setIsFlipped(false);
    setTimeout(() => {
      setCurrentFlashcard((prev) => (prev + 1) % flashcards.length);
    }, 150);
  };
  
  const handleAnswerSelect = (index) => {
    if (selectedAnswer !== null) return;
    setSelectedAnswer(index);
    if (index === currentQuiz.questions[currentQuestion].correct) {
      setScore(score + 1);
    }
  };
  
  const handleNextQuestion = () => {
    if (currentQuestion < currentQuiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
    } else {
      setQuizComplete(true);
    }
  };
  
  const resetQuiz = () => {
    setQuizStarted(false);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setScore(0);
    setQuizComplete(false);
  };
  
  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link to={`/${languageId}`} className="text-[#22955B] hover:underline flex items-center gap-1 mb-4">
            <ArrowLeft className="w-4 h-4" /> Volver a {langInfo.name}
          </Link>
          
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">{langInfo.flag}</span>
            <span 
              className="text-lg font-bold px-4 py-2 rounded-xl text-white"
              style={{ backgroundColor: levelInfo.color }}
            >
              {levelInfo.id}
            </span>
            <div>
              <h1 className="font-serif text-3xl font-bold text-gray-900">
                {langInfo.name} - {levelInfo.title}
              </h1>
              <p className="text-gray-600">{levelInfo.desc}</p>
            </div>
          </div>
        </div>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {[
            { id: 'lessons', label: 'Lecciones', icon: BookOpen, count: lessons.length },
            { id: 'flashcards', label: 'Flashcards', icon: Layers, count: flashcards.length },
            { id: 'quiz', label: 'Quiz', icon: HelpCircle, count: currentQuiz?.questions?.length || 0 },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all whitespace-nowrap ${
                activeTab === tab.id 
                  ? 'bg-[#22955B] text-white' 
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
              data-testid={`tab-${tab.id}`}
            >
              <tab.icon className="w-5 h-5" />
              {tab.label}
              <span className={`text-xs px-2 py-0.5 rounded-full ${
                activeTab === tab.id ? 'bg-white/20' : 'bg-gray-100'
              }`}>
                {tab.count}
              </span>
            </button>
          ))}
        </div>
        
        {/* Tab Content */}
        {activeTab === 'lessons' && (
          <div className="space-y-8" data-testid="lessons-content">
            {lessons.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl">
                <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Las lecciones para este nivel están en desarrollo.</p>
              </div>
            ) : (
              lessons.map((lesson, lessonIndex) => (
                <div key={lesson.id} className="bg-white rounded-2xl shadow-sm overflow-hidden" data-testid={`lesson-${lessonIndex}`}>
                  <div className="p-6 border-b border-gray-100">
                    <div className="flex items-center gap-3">
                      <span className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold" style={{ backgroundColor: levelInfo.color }}>
                        {lessonIndex + 1}
                      </span>
                      <div>
                        <h2 className="font-bold text-xl text-gray-900">{lesson.title}</h2>
                        <p className="text-sm text-gray-500">{lesson.description}</p>
                      </div>
                    </div>
                  </div>
                  
                  {/* Lesson Content */}
                  <div className="p-6">
                    <div className="prose prose-sm max-w-none mb-8">
                      <div className="bg-gray-50 rounded-xl p-6 whitespace-pre-wrap text-gray-700 leading-relaxed">
                        {lesson.content}
                      </div>
                    </div>
                    
                    {/* Vocabulary */}
                    {lesson.vocabulary && lesson.vocabulary.length > 0 && (
                      <div className="mb-8">
                        <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                          <BookMarked className="w-5 h-5 text-[#22955B]" />
                          Vocabulario
                        </h3>
                        <div className="grid md:grid-cols-2 gap-3">
                          {lesson.vocabulary.map((item, i) => (
                            <div key={i} className="vocab-item" data-testid={`vocab-${lessonIndex}-${i}`}>
                              <div className="flex-1">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <span className="font-bold text-gray-900">{item.word}</span>
                                  <span className="text-xs text-gray-400">[{item.pronunciation}]</span>
                                </div>
                                <p className="text-sm text-gray-500">{item.translation}</p>
                                <p className="text-sm text-gray-400 italic">"{item.example}"</p>
                              </div>
                              <button 
                                onClick={() => playAudio(item.word, languageId)}
                                className={`text-[#22955B] hover:text-[#1a7346] p-2 rounded-lg hover:bg-[#22955B]/10 transition-colors ${
                                  isPlaying && currentWord === item.word ? 'animate-pulse bg-[#22955B]/10' : ''
                                }`}
                                data-testid={`audio-btn-${i}`}
                              >
                                <Volume2 className="w-5 h-5" />
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Grammar */}
                    {lesson.grammar && lesson.grammar.length > 0 && (
                      <div>
                        <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                          <Lightbulb className="w-5 h-5 text-[#fa8a00]" />
                          Puntos Gramaticales
                        </h3>
                        <div className="space-y-4">
                          {lesson.grammar.map((point, i) => (
                            <div key={i} className="grammar-box" data-testid={`grammar-${lessonIndex}-${i}`}>
                              <h4 className="font-bold text-gray-900 mb-2">{point.title}</h4>
                              <p className="text-gray-700 mb-2 font-mono text-sm bg-white/50 rounded px-2 py-1 inline-block">
                                {point.rule}
                              </p>
                              <div className="flex flex-wrap gap-2 mt-2">
                                {point.examples.map((ex, j) => (
                                  <span key={j} className="text-sm text-gray-600 bg-white rounded-lg px-3 py-1">
                                    "{ex}"
                                  </span>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
        
        {activeTab === 'flashcards' && (
          <div className="flex flex-col items-center" data-testid="flashcards-content">
            {flashcards.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl w-full">
                <Layers className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Las flashcards para este nivel están en desarrollo.</p>
              </div>
            ) : (
              <>
                <p className="text-gray-500 mb-6">
                  Flashcard {currentFlashcard + 1} de {flashcards.length}
                </p>
                
                <div className="flashcard-container mb-8">
                  <div 
                    className={`flashcard ${isFlipped ? 'flipped' : ''}`}
                    onClick={() => setIsFlipped(!isFlipped)}
                    data-testid="flashcard"
                  >
                    <div className="flashcard-face flashcard-front" style={{ background: `linear-gradient(135deg, ${levelInfo.color} 0%, ${langInfo.color} 100%)` }}>
                      <span className="text-4xl mb-2">{langInfo.flag}</span>
                      <span className="text-3xl font-bold">{flashcards[currentFlashcard].word}</span>
                      <span className="text-white/70 text-sm mt-2">Toca para voltear</span>
                    </div>
                    <div className="flashcard-face flashcard-back">
                      <span className="text-2xl font-bold text-gray-900">{flashcards[currentFlashcard].translation}</span>
                      <span className="text-sm text-gray-500 mt-2">[{flashcards[currentFlashcard].pronunciation}]</span>
                      <span className="text-sm text-gray-400 italic mt-2">"{flashcards[currentFlashcard].example}"</span>
                      <button 
                        onClick={(e) => { e.stopPropagation(); playAudio(flashcards[currentFlashcard].word, languageId); }}
                        className="mt-4 flex items-center gap-2 text-[#22955B] hover:text-[#1a7346]"
                      >
                        <Volume2 className="w-5 h-5" /> Escuchar
                      </button>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-4">
                  <button 
                    className="px-6 py-3 bg-[#fa8a00] text-white rounded-xl font-semibold hover:bg-[#e07b00] transition-colors"
                    onClick={handleFlashcardNext}
                    data-testid="flashcard-next"
                  >
                    <RotateCcw className="w-5 h-5 inline mr-2" />
                    Estudiar de nuevo
                  </button>
                  <button 
                    className="px-6 py-3 bg-[#22955B] text-white rounded-xl font-semibold hover:bg-[#1a7346] transition-colors"
                    onClick={handleFlashcardNext}
                    data-testid="flashcard-know"
                  >
                    <CheckCircle className="w-5 h-5 inline mr-2" />
                    Lo sé
                  </button>
                </div>
              </>
            )}
          </div>
        )}
        
        {activeTab === 'quiz' && (
          <div data-testid="quiz-content">
            {!currentQuiz || currentQuiz.questions?.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl">
                <HelpCircle className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">El quiz para este nivel está en desarrollo.</p>
              </div>
            ) : !quizStarted ? (
              <div className="bg-white rounded-2xl p-8 text-center max-w-lg mx-auto">
                <div className="w-20 h-20 rounded-full mx-auto mb-6 flex items-center justify-center" style={{ backgroundColor: levelInfo.color + '20' }}>
                  <Target className="w-10 h-10" style={{ color: levelInfo.color }} />
                </div>
                <h2 className="font-bold text-2xl text-gray-900 mb-2">{currentQuiz.title}</h2>
                <p className="text-gray-500 mb-6">{currentQuiz.questions.length} preguntas</p>
                <button 
                  onClick={() => setQuizStarted(true)}
                  className="btn-primary"
                  data-testid="start-quiz"
                >
                  <Play className="w-5 h-5" />
                  Comenzar Quiz
                </button>
              </div>
            ) : quizComplete ? (
              <div className="bg-white rounded-2xl p-8 text-center max-w-lg mx-auto">
                <div className="w-20 h-20 rounded-full mx-auto mb-6 flex items-center justify-center bg-[#22955B]/10">
                  <Award className="w-10 h-10 text-[#22955B]" />
                </div>
                <h2 className="font-bold text-2xl text-gray-900 mb-2">¡Quiz Completado!</h2>
                <p className="text-4xl font-bold mb-2" style={{ color: score >= currentQuiz.questions.length / 2 ? '#22955B' : '#e34b33' }}>
                  {score} / {currentQuiz.questions.length}
                </p>
                <p className="text-gray-500 mb-6">
                  {score >= currentQuiz.questions.length * 0.8 ? '¡Excelente trabajo!' :
                   score >= currentQuiz.questions.length * 0.5 ? '¡Buen intento!' :
                   'Sigue practicando'}
                </p>
                <button onClick={resetQuiz} className="btn-primary" data-testid="restart-quiz">
                  <RotateCcw className="w-5 h-5" />
                  Intentar de nuevo
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-2xl p-8 max-w-2xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                  <span className="text-sm text-gray-500">
                    Pregunta {currentQuestion + 1} de {currentQuiz.questions.length}
                  </span>
                  <span className="text-sm font-semibold" style={{ color: levelInfo.color }}>
                    Puntos: {score}
                  </span>
                </div>
                
                <div className="w-full bg-gray-100 rounded-full h-2 mb-8">
                  <div 
                    className="h-2 rounded-full transition-all"
                    style={{ 
                      width: `${((currentQuestion + 1) / currentQuiz.questions.length) * 100}%`,
                      backgroundColor: levelInfo.color
                    }}
                  />
                </div>
                
                <h3 className="font-bold text-xl text-gray-900 mb-6">
                  {currentQuiz.questions[currentQuestion].question}
                </h3>
                
                <div className="space-y-3 mb-6">
                  {currentQuiz.questions[currentQuestion].options.map((option, i) => {
                    const isCorrect = i === currentQuiz.questions[currentQuestion].correct;
                    const isSelected = i === selectedAnswer;
                    
                    return (
                      <button
                        key={i}
                        onClick={() => handleAnswerSelect(i)}
                        disabled={selectedAnswer !== null}
                        className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                          selectedAnswer === null 
                            ? 'border-gray-200 hover:border-[#22955B] hover:bg-[#22955B]/5' 
                            : isCorrect 
                              ? 'border-[#22955B] bg-[#22955B]/10' 
                              : isSelected 
                                ? 'border-[#e34b33] bg-[#e34b33]/10' 
                                : 'border-gray-200 opacity-50'
                        }`}
                        data-testid={`quiz-option-${i}`}
                      >
                        <span className="flex items-center gap-3">
                          <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                            selectedAnswer === null 
                              ? 'bg-gray-100' 
                              : isCorrect 
                                ? 'bg-[#22955B] text-white' 
                                : isSelected 
                                  ? 'bg-[#e34b33] text-white' 
                                  : 'bg-gray-100'
                          }`}>
                            {String.fromCharCode(65 + i)}
                          </span>
                          {option}
                        </span>
                      </button>
                    );
                  })}
                </div>
                
                {selectedAnswer !== null && (
                  <div className={`p-4 rounded-xl mb-6 ${
                    selectedAnswer === currentQuiz.questions[currentQuestion].correct 
                      ? 'bg-[#22955B]/10 text-[#22955B]' 
                      : 'bg-[#e34b33]/10 text-[#e34b33]'
                  }`}>
                    <p className="font-semibold mb-1">
                      {selectedAnswer === currentQuiz.questions[currentQuestion].correct ? '✓ ¡Correcto!' : '✗ Incorrecto'}
                    </p>
                    <p className="text-sm opacity-80">
                      {currentQuiz.questions[currentQuestion].explanation}
                    </p>
                  </div>
                )}
                
                {selectedAnswer !== null && (
                  <button onClick={handleNextQuestion} className="btn-primary w-full" data-testid="next-question">
                    {currentQuestion < currentQuiz.questions.length - 1 ? 'Siguiente Pregunta' : 'Ver Resultados'}
                    <ArrowRight className="w-5 h-5" />
                  </button>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// ==================== FOOTER ====================
const Footer = () => (
  <footer className="footer" data-testid="footer">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid md:grid-cols-4 gap-12 mb-12">
        <div className="md:col-span-2">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center gradient-primary">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="font-serif text-xl font-bold text-white">Intercultura</span>
          </div>
          <p className="text-gray-400 mb-6 max-w-md">
            Asistente Virtual para aprender idiomas siguiendo la metodología Cambridge.
          </p>
          <div className="flex gap-3">
            {LANGUAGES.map((lang) => (
              <Link key={lang.id} to={`/${lang.id}`} className="text-2xl hover:scale-110 transition-transform" title={lang.name}>
                {lang.flag}
              </Link>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="font-bold text-white mb-4">Idiomas</h4>
          <ul className="space-y-2">
            {LANGUAGES.map((lang) => (
              <li key={lang.id}>
                <Link to={`/${lang.id}`} className="text-gray-400 hover:text-[#B6C932] transition-colors">
                  {lang.flag} {lang.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h4 className="font-bold text-white mb-4">Niveles</h4>
          <ul className="space-y-2">
            {LEVELS.map((level) => (
              <li key={level.id}>
                <span className="text-gray-400">{level.id} - {level.title}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p className="text-gray-500 text-sm">
          © 2026 Intercultura - Escuela de Idiomas, Costa Rica.
        </p>
        <div className="flex items-center gap-2">
          <span className="text-gray-500 text-sm">Versión 2.0.0</span>
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
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/languages" element={<LanguagesPage />} />
        <Route path="/:languageId" element={<LanguagePage />} />
        <Route path="/:languageId/:levelId" element={<LevelPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

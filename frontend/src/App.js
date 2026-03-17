import { useState, useEffect, createContext, useContext } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Link, useParams, useNavigate } from "react-router-dom";
import { 
  BookOpen, MessageCircle, Mic, Brain, ChevronRight, Globe, GraduationCap,
  Sparkles, Volume2, CheckCircle, Target, Users, Award, ArrowRight, Play,
  Lightbulb, BookMarked, ArrowLeft, Home, Layers, FileText, HelpCircle,
  RotateCcw, ChevronDown, Menu, X, User, LogOut, LogIn, UserPlus, Loader2
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// ==================== AUTH CONTEXT ====================
const AuthContext = createContext(null);

const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        logout();
      }
    } catch (e) {
      console.error('Auth error:', e);
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      return { success: true };
    }
    return { success: false, error: 'Credenciales inválidas' };
  };

  const register = async (name, email, password) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, role: 'student' })
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      return { success: true };
    }
    const err = await res.json();
    return { success: false, error: err.detail || 'Error al registrar' };
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// ==================== CONSTANTS ====================
const LANGUAGES = [
  { id: 'spanish', name: 'Español', flag: '🇨🇷', greeting: '¡Pura Vida!', color: '#22955B' },
  { id: 'english', name: 'English', flag: '🇺🇸', greeting: 'Hello!', color: '#003189' },
  { id: 'french', name: 'Français', flag: '🇫🇷', greeting: 'Bonjour!', color: '#003189' },
  { id: 'german', name: 'Deutsch', flag: '🇩🇪', greeting: 'Hallo!', color: '#1a1a1a' },
  { id: 'portuguese', name: 'Português', flag: '🇧🇷', greeting: 'Olá!', color: '#fa8a00' },
];

const LEVELS = [
  { id: 'A1', title: 'Acceso', desc: 'Principiante', color: '#B6C932' },
  { id: 'A2', title: 'Plataforma', desc: 'Básico', color: '#8fb82a' },
  { id: 'B1', title: 'Umbral', desc: 'Intermedio', color: '#fa8a00' },
  { id: 'B2', title: 'Avanzado', desc: 'Intermedio Alto', color: '#f07800' },
  { id: 'C1', title: 'Dominio', desc: 'Avanzado', color: '#e34b33' },
  { id: 'C2', title: 'Maestría', desc: 'Experto', color: '#c43d2a' },
];

const getLangInfo = (id) => LANGUAGES.find(l => l.id === id) || LANGUAGES[0];
const getLevelInfo = (id) => LEVELS.find(l => l.id === id) || LEVELS[0];

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
          audio.onended = () => { setIsPlaying(false); setCurrentWord(null); };
          await audio.play();
          return;
        }
      }
    } catch (error) {
      console.log('Using browser TTS fallback');
    }
    
    // Fallback to browser TTS
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'spanish' ? 'es-ES' : language === 'english' ? 'en-US' :
                     language === 'french' ? 'fr-FR' : language === 'german' ? 'de-DE' : 'pt-BR';
    utterance.onend = () => { setIsPlaying(false); setCurrentWord(null); };
    speechSynthesis.speak(utterance);
  };

  return { playAudio, isPlaying, currentWord };
};

// ==================== NAVIGATION ====================
const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  
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
            <Link to="/courses" className="nav-link">Cursos</Link>
            {user && <Link to="/progress" className="nav-link">Mi Progreso</Link>}
          </div>
          
          <div className="flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <span className="text-sm text-gray-600 hidden sm:block">{user.name}</span>
                <button onClick={logout} className="p-2 text-gray-500 hover:text-gray-700" data-testid="logout-btn">
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login" className="btn-secondary text-sm py-2 px-4" data-testid="login-link">
                  <LogIn className="w-4 h-4" /> Entrar
                </Link>
                <Link to="/register" className="btn-primary text-sm py-2 px-4 hidden sm:flex" data-testid="register-link">
                  <UserPlus className="w-4 h-4" /> Registrarse
                </Link>
              </div>
            )}
            <button className="md:hidden p-2" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
        
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <div className="flex flex-col gap-2">
              <Link to="/" className="nav-link py-2" onClick={() => setIsMenuOpen(false)}>Inicio</Link>
              <Link to="/courses" className="nav-link py-2" onClick={() => setIsMenuOpen(false)}>Cursos</Link>
              {user && <Link to="/progress" className="nav-link py-2" onClick={() => setIsMenuOpen(false)}>Mi Progreso</Link>}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

// ==================== AUTH PAGES ====================
const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const result = await login(email, password);
    setLoading(false);
    if (result.success) {
      navigate('/courses');
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="pt-20 min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl p-8 shadow-sm max-w-md w-full">
        <h1 className="font-serif text-2xl font-bold text-center mb-6">Iniciar Sesión</h1>
        
        {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#22955B]"
              required
              data-testid="login-email"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#22955B]"
              required
              data-testid="login-password"
            />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading} data-testid="login-submit">
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Entrar'}
          </button>
        </form>
        
        <p className="text-center text-sm text-gray-500 mt-6">
          ¿No tienes cuenta? <Link to="/register" className="text-[#22955B] font-medium">Regístrate</Link>
        </p>
      </div>
    </div>
  );
};

const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const result = await register(name, email, password);
    setLoading(false);
    if (result.success) {
      navigate('/courses');
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="pt-20 min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl p-8 shadow-sm max-w-md w-full">
        <h1 className="font-serif text-2xl font-bold text-center mb-6">Crear Cuenta</h1>
        
        {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#22955B]"
              required
              data-testid="register-name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#22955B]"
              required
              data-testid="register-email"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#22955B]"
              required
              minLength={6}
              data-testid="register-password"
            />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading} data-testid="register-submit">
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Registrarse'}
          </button>
        </form>
        
        <p className="text-center text-sm text-gray-500 mt-6">
          ¿Ya tienes cuenta? <Link to="/login" className="text-[#22955B] font-medium">Inicia sesión</Link>
        </p>
      </div>
    </div>
  );
};

// ==================== HOME PAGE ====================
const HomePage = () => {
  return (
    <div className="pt-16">
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
                Aprende Español, Inglés, Francés, Alemán y Portugués con lecciones, quizzes, flashcards y ejercicios de IA.
              </p>
              
              <div className="flex flex-wrap gap-4 mb-12">
                <Link to="/courses" className="btn-primary" data-testid="cta-comenzar-hero">
                  Comenzar Gratis <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
              
              <div className="grid grid-cols-3 gap-8">
                <div><p className="font-serif text-3xl font-bold text-gray-900">5</p><p className="text-sm text-gray-500">Idiomas</p></div>
                <div><p className="font-serif text-3xl font-bold text-gray-900">54+</p><p className="text-sm text-gray-500">Lecciones</p></div>
                <div><p className="font-serif text-3xl font-bold text-gray-900">180+</p><p className="text-sm text-gray-500">Flashcards</p></div>
              </div>
            </div>
            
            <div className="flex justify-center lg:justify-end">
              <div className="grid grid-cols-2 gap-4 max-w-md">
                {LANGUAGES.map((lang, i) => (
                  <Link key={lang.id} to={`/courses/${lang.id}`}
                    className={`ticket-card text-center hover:scale-105 transition-transform ${i === 4 ? 'col-span-2 justify-self-center w-1/2' : ''}`}>
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

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="section-label mb-4 block">Características</span>
            <h2 className="section-title">Tecnología al servicio del aprendizaje</h2>
          </div>
          
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { icon: Brain, title: 'Ejercicios IA', desc: 'Generados con GPT-4', color: '#22955B' },
              { icon: Volume2, title: 'Audio TTS', desc: 'ElevenLabs HD', color: '#fa8a00' },
              { icon: Target, title: 'Quizzes', desc: 'Tests interactivos', color: '#003189' },
              { icon: Layers, title: 'Flashcards', desc: 'Repetición espaciada', color: '#e34b33' },
            ].map((f, i) => (
              <div key={i} className="bento-item text-center">
                <div className="w-14 h-14 rounded-2xl mx-auto mb-4 flex items-center justify-center" style={{ backgroundColor: f.color + '15' }}>
                  <f.icon className="w-7 h-7" style={{ color: f.color }} />
                </div>
                <h3 className="font-bold text-gray-900 mb-1">{f.title}</h3>
                <p className="text-sm text-gray-500">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  );
};

// ==================== COURSES PAGE ====================
const CoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/courses`)
      .then(r => r.json())
      .then(data => { setCourses(data); setLoading(false); })
      .catch(e => { console.error(e); setLoading(false); });
  }, []);

  const grouped = LANGUAGES.map(lang => ({
    ...lang,
    courses: courses.filter(c => c.language === lang.id)
  }));

  if (loading) return <div className="pt-20 min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#22955B]" /></div>;

  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="section-title mb-8">Todos los Cursos</h1>
        
        <div className="space-y-12">
          {grouped.map(lang => (
            <div key={lang.id} data-testid={`courses-${lang.id}`}>
              <div className="flex items-center gap-3 mb-4">
                <span className="text-4xl">{lang.flag}</span>
                <h2 className="font-serif text-2xl font-bold">{lang.name}</h2>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {lang.courses.map(course => {
                  const levelInfo = getLevelInfo(course.level);
                  return (
                    <Link key={course.id} to={`/course/${course.id}`}
                      className="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all border-l-4"
                      style={{ borderLeftColor: levelInfo.color }}
                      data-testid={`course-card-${course.id}`}>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs font-bold px-2 py-1 rounded-full text-white" style={{ backgroundColor: levelInfo.color }}>
                          {course.level}
                        </span>
                        <span className="text-xs text-gray-500">{course.lesson_count} lecciones</span>
                      </div>
                      <h3 className="font-bold text-gray-900">{course.title}</h3>
                      <p className="text-sm text-gray-500 mt-1">{course.description}</p>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ==================== COURSE DETAIL PAGE ====================
const CourseDetailPage = () => {
  const { courseId } = useParams();
  const { token } = useAuth();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [flashcards, setFlashcards] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [activeTab, setActiveTab] = useState('lessons');
  const [loading, setLoading] = useState(true);
  const { playAudio, isPlaying, currentWord } = useAudio();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [courseRes, lessonsRes, quizzesRes] = await Promise.all([
          fetch(`${BACKEND_URL}/api/courses/${courseId}`),
          fetch(`${BACKEND_URL}/api/courses/${courseId}/lessons`),
          fetch(`${BACKEND_URL}/api/courses/${courseId}/quizzes`),
        ]);
        
        const courseData = await courseRes.json();
        const lessonsData = await lessonsRes.json();
        const quizzesData = await quizzesRes.json();
        
        setCourse(courseData);
        setLessons(lessonsData);
        setQuizzes(quizzesData);
        
        // Fetch flashcards for this language/level
        const flashRes = await fetch(`${BACKEND_URL}/api/flashcards?language=${courseData.language}&level=${courseData.level}&limit=50`);
        const flashData = await flashRes.json();
        setFlashcards(flashData);
      } catch (e) {
        console.error(e);
      }
      setLoading(false);
    };
    fetchData();
  }, [courseId]);

  // Flashcard state
  const [currentFlashcard, setCurrentFlashcard] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  
  // Quiz state
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [quizComplete, setQuizComplete] = useState(false);
  const [aiExercise, setAiExercise] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  if (loading) return <div className="pt-20 min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#22955B]" /></div>;
  if (!course) return <div className="pt-20 min-h-screen flex items-center justify-center">Curso no encontrado</div>;

  const langInfo = getLangInfo(course.language);
  const levelInfo = getLevelInfo(course.level);
  const currentQuiz = quizzes[0];

  const completeLesson = async (lessonId) => {
    if (!token) return;
    await fetch(`${BACKEND_URL}/api/lessons/${lessonId}/complete`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });
  };

  const generateAIExercise = async () => {
    setAiLoading(true);
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = `Bearer ${token}`;
      
      const res = await fetch(`${BACKEND_URL}/api/ai/generate-exercise`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          language: course.language,
          level: course.level,
          topic: lessons[0]?.title || 'general',
          exercise_type: 'grammar'
        })
      });
      const data = await res.json();
      if (data.success) setAiExercise(data.exercise);
    } catch (e) {
      console.error(e);
    }
    setAiLoading(false);
  };

  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link to="/courses" className="text-[#22955B] hover:underline flex items-center gap-1 mb-4">
            <ArrowLeft className="w-4 h-4" /> Volver a cursos
          </Link>
          
          <div className="flex items-center gap-4">
            <span className="text-4xl">{langInfo.flag}</span>
            <span className="text-lg font-bold px-4 py-2 rounded-xl text-white" style={{ backgroundColor: levelInfo.color }}>{course.level}</span>
            <div>
              <h1 className="font-serif text-2xl font-bold text-gray-900">{course.title}</h1>
              <p className="text-gray-500">{course.description}</p>
            </div>
          </div>
        </div>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {[
            { id: 'lessons', label: 'Lecciones', icon: BookOpen, count: lessons.length },
            { id: 'flashcards', label: 'Flashcards', icon: Layers, count: flashcards.length },
            { id: 'quiz', label: 'Quiz', icon: HelpCircle, count: currentQuiz?.questions?.length || 0 },
            { id: 'ai', label: 'Ejercicios IA', icon: Brain, count: null },
          ].map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all whitespace-nowrap ${
                activeTab === tab.id ? 'bg-[#22955B] text-white' : 'bg-white text-gray-600 hover:bg-gray-100'}`}
              data-testid={`tab-${tab.id}`}>
              <tab.icon className="w-5 h-5" />
              {tab.label}
              {tab.count !== null && <span className={`text-xs px-2 py-0.5 rounded-full ${activeTab === tab.id ? 'bg-white/20' : 'bg-gray-100'}`}>{tab.count}</span>}
            </button>
          ))}
        </div>
        
        {/* Lessons Tab */}
        {activeTab === 'lessons' && (
          <div className="space-y-6">
            {lessons.map((lesson, i) => (
              <div key={lesson.id} className="bg-white rounded-2xl shadow-sm overflow-hidden">
                <div className="p-6 border-b border-gray-100">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold" style={{ backgroundColor: levelInfo.color }}>{i + 1}</span>
                      <h2 className="font-bold text-xl text-gray-900">{lesson.title}</h2>
                    </div>
                    {token && (
                      <button onClick={() => completeLesson(lesson.id)} className="btn-secondary text-sm py-2 px-4">
                        <CheckCircle className="w-4 h-4" /> Completar
                      </button>
                    )}
                  </div>
                </div>
                
                <div className="p-6">
                  <div className="bg-gray-50 rounded-xl p-6 mb-6 whitespace-pre-wrap text-gray-700">{lesson.content}</div>
                  
                  {lesson.vocabulary?.length > 0 && (
                    <div className="mb-6">
                      <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                        <BookMarked className="w-5 h-5 text-[#22955B]" /> Vocabulario
                      </h3>
                      <div className="grid md:grid-cols-2 gap-3">
                        {lesson.vocabulary.map((v, j) => (
                          <div key={j} className="vocab-item">
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <span className="font-bold text-gray-900">{v.word}</span>
                                {v.pronunciation && <span className="text-xs text-gray-400">[{v.pronunciation}]</span>}
                              </div>
                              <p className="text-sm text-gray-500">{v.translation}</p>
                              {v.example && <p className="text-sm text-gray-400 italic">"{v.example}"</p>}
                            </div>
                            <button onClick={() => playAudio(v.word, course.language)}
                              className={`p-2 rounded-lg hover:bg-[#22955B]/10 ${isPlaying && currentWord === v.word ? 'animate-pulse bg-[#22955B]/10' : ''}`}>
                              <Volume2 className="w-5 h-5 text-[#22955B]" />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {lesson.grammar_points?.length > 0 && (
                    <div>
                      <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                        <Lightbulb className="w-5 h-5 text-[#fa8a00]" /> Puntos Gramaticales
                      </h3>
                      <div className="space-y-2">
                        {lesson.grammar_points.map((g, j) => (
                          <div key={j} className="grammar-box flex gap-3">
                            <CheckCircle className="w-5 h-5 text-[#22955B] flex-shrink-0 mt-0.5" />
                            <p className="text-gray-700">{g}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Flashcards Tab */}
        {activeTab === 'flashcards' && flashcards.length > 0 && (
          <div className="flex flex-col items-center">
            <p className="text-gray-500 mb-6">Flashcard {currentFlashcard + 1} de {flashcards.length}</p>
            
            <div className="flashcard-container mb-8">
              <div className={`flashcard ${isFlipped ? 'flipped' : ''}`} onClick={() => setIsFlipped(!isFlipped)}>
                <div className="flashcard-face flashcard-front" style={{ background: `linear-gradient(135deg, ${levelInfo.color} 0%, ${langInfo.color} 100%)` }}>
                  <span className="text-4xl mb-2">{langInfo.flag}</span>
                  <span className="text-3xl font-bold">{flashcards[currentFlashcard].word}</span>
                  <span className="text-white/70 text-sm mt-2">Toca para voltear</span>
                </div>
                <div className="flashcard-face flashcard-back">
                  <span className="text-2xl font-bold text-gray-900">{flashcards[currentFlashcard].translation}</span>
                  {flashcards[currentFlashcard].pronunciation && <span className="text-sm text-gray-500 mt-2">[{flashcards[currentFlashcard].pronunciation}]</span>}
                  {flashcards[currentFlashcard].example && <span className="text-sm text-gray-400 italic mt-2">"{flashcards[currentFlashcard].example}"</span>}
                  <button onClick={(e) => { e.stopPropagation(); playAudio(flashcards[currentFlashcard].word, course.language); }}
                    className="mt-4 flex items-center gap-2 text-[#22955B]">
                    <Volume2 className="w-5 h-5" /> Escuchar
                  </button>
                </div>
              </div>
            </div>
            
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-[#fa8a00] text-white rounded-xl font-semibold"
                onClick={() => { setIsFlipped(false); setTimeout(() => setCurrentFlashcard((p) => (p + 1) % flashcards.length), 150); }}>
                <RotateCcw className="w-5 h-5 inline mr-2" /> Estudiar de nuevo
              </button>
              <button className="px-6 py-3 bg-[#22955B] text-white rounded-xl font-semibold"
                onClick={() => { setIsFlipped(false); setTimeout(() => setCurrentFlashcard((p) => (p + 1) % flashcards.length), 150); }}>
                <CheckCircle className="w-5 h-5 inline mr-2" /> Lo sé
              </button>
            </div>
          </div>
        )}
        
        {/* Quiz Tab */}
        {activeTab === 'quiz' && currentQuiz && (
          <div>
            {!quizStarted ? (
              <div className="bg-white rounded-2xl p-8 text-center max-w-lg mx-auto">
                <Target className="w-16 h-16 mx-auto mb-4" style={{ color: levelInfo.color }} />
                <h2 className="font-bold text-2xl mb-2">{currentQuiz.title}</h2>
                <p className="text-gray-500 mb-6">{currentQuiz.questions.length} preguntas</p>
                <button onClick={() => setQuizStarted(true)} className="btn-primary">
                  <Play className="w-5 h-5" /> Comenzar Quiz
                </button>
              </div>
            ) : quizComplete ? (
              <div className="bg-white rounded-2xl p-8 text-center max-w-lg mx-auto">
                <Award className="w-16 h-16 mx-auto mb-4 text-[#22955B]" />
                <h2 className="font-bold text-2xl mb-2">¡Quiz Completado!</h2>
                <p className="text-4xl font-bold mb-2" style={{ color: score >= currentQuiz.questions.length / 2 ? '#22955B' : '#e34b33' }}>
                  {score} / {currentQuiz.questions.length}
                </p>
                <button onClick={() => { setQuizStarted(false); setCurrentQuestion(0); setSelectedAnswer(null); setScore(0); setQuizComplete(false); }}
                  className="btn-primary mt-4">
                  <RotateCcw className="w-5 h-5" /> Intentar de nuevo
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-2xl p-8 max-w-2xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                  <span className="text-sm text-gray-500">Pregunta {currentQuestion + 1} de {currentQuiz.questions.length}</span>
                  <span className="text-sm font-semibold" style={{ color: levelInfo.color }}>Puntos: {score}</span>
                </div>
                
                <div className="w-full bg-gray-100 rounded-full h-2 mb-8">
                  <div className="h-2 rounded-full transition-all" style={{ width: `${((currentQuestion + 1) / currentQuiz.questions.length) * 100}%`, backgroundColor: levelInfo.color }} />
                </div>
                
                <h3 className="font-bold text-xl mb-6">{currentQuiz.questions[currentQuestion].question}</h3>
                
                <div className="space-y-3 mb-6">
                  {currentQuiz.questions[currentQuestion].options.map((opt, i) => {
                    const isCorrect = i === currentQuiz.questions[currentQuestion].correct_answer;
                    const isSelected = i === selectedAnswer;
                    return (
                      <button key={i}
                        onClick={() => { if (selectedAnswer === null) { setSelectedAnswer(i); if (isCorrect) setScore(s => s + 1); } }}
                        disabled={selectedAnswer !== null}
                        className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                          selectedAnswer === null ? 'border-gray-200 hover:border-[#22955B]' :
                          isCorrect ? 'border-[#22955B] bg-[#22955B]/10' :
                          isSelected ? 'border-[#e34b33] bg-[#e34b33]/10' : 'border-gray-200 opacity-50'}`}>
                        <span className="flex items-center gap-3">
                          <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                            selectedAnswer === null ? 'bg-gray-100' :
                            isCorrect ? 'bg-[#22955B] text-white' :
                            isSelected ? 'bg-[#e34b33] text-white' : 'bg-gray-100'}`}>
                            {String.fromCharCode(65 + i)}
                          </span>
                          {opt}
                        </span>
                      </button>
                    );
                  })}
                </div>
                
                {selectedAnswer !== null && (
                  <>
                    <div className={`p-4 rounded-xl mb-6 ${selectedAnswer === currentQuiz.questions[currentQuestion].correct_answer ? 'bg-[#22955B]/10 text-[#22955B]' : 'bg-[#e34b33]/10 text-[#e34b33]'}`}>
                      <p className="font-semibold">{selectedAnswer === currentQuiz.questions[currentQuestion].correct_answer ? '✓ ¡Correcto!' : '✗ Incorrecto'}</p>
                      {currentQuiz.questions[currentQuestion].explanation && <p className="text-sm opacity-80 mt-1">{currentQuiz.questions[currentQuestion].explanation}</p>}
                    </div>
                    <button onClick={() => { if (currentQuestion < currentQuiz.questions.length - 1) { setCurrentQuestion(q => q + 1); setSelectedAnswer(null); } else { setQuizComplete(true); } }}
                      className="btn-primary w-full">
                      {currentQuestion < currentQuiz.questions.length - 1 ? 'Siguiente Pregunta' : 'Ver Resultados'} <ArrowRight className="w-5 h-5" />
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        )}
        
        {/* AI Exercises Tab */}
        {activeTab === 'ai' && (
          <div className="max-w-2xl mx-auto">
            {!aiExercise ? (
              <div className="bg-white rounded-2xl p-8 text-center">
                <Brain className="w-16 h-16 mx-auto mb-4 text-[#22955B]" />
                <h2 className="font-bold text-2xl mb-2">Ejercicios con Inteligencia Artificial</h2>
                <p className="text-gray-500 mb-6">Genera ejercicios personalizados para tu nivel con GPT-4</p>
                <button onClick={generateAIExercise} className="btn-primary" disabled={aiLoading}>
                  {aiLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                  {aiLoading ? 'Generando...' : 'Generar Ejercicio'}
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-2xl p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="font-bold text-xl text-gray-900">{aiExercise.title}</h2>
                    <p className="text-gray-500">{aiExercise.description}</p>
                  </div>
                  <button onClick={() => { setAiExercise(null); generateAIExercise(); }} className="btn-secondary text-sm py-2 px-4">
                    <RotateCcw className="w-4 h-4" /> Nuevo
                  </button>
                </div>
                
                {aiExercise.instructions && <p className="bg-gray-50 p-4 rounded-xl mb-6 text-gray-700">{aiExercise.instructions}</p>}
                
                {aiExercise.questions?.map((q, i) => (
                  <div key={i} className="mb-6 p-4 bg-gray-50 rounded-xl">
                    <p className="font-semibold mb-3">{i + 1}. {q.question}</p>
                    <div className="grid grid-cols-2 gap-2">
                      {q.options?.map((opt, j) => (
                        <button key={j} className={`p-3 rounded-lg border text-left text-sm ${j === q.correct_answer ? 'border-[#22955B] bg-[#22955B]/10' : 'border-gray-200'}`}>
                          {String.fromCharCode(65 + j)}) {opt}
                        </button>
                      ))}
                    </div>
                    {q.explanation && <p className="text-sm text-gray-500 mt-2 italic">{q.explanation}</p>}
                  </div>
                ))}
                
                {aiExercise.vocabulary?.length > 0 && (
                  <div className="mt-6">
                    <h3 className="font-bold mb-3">Vocabulario</h3>
                    <div className="grid md:grid-cols-2 gap-2">
                      {aiExercise.vocabulary.map((v, i) => (
                        <div key={i} className="p-3 bg-gray-50 rounded-lg">
                          <span className="font-semibold">{v.word}</span> - {v.translation}
                          {v.example && <p className="text-sm text-gray-400 italic">"{v.example}"</p>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {aiExercise.grammar_tip && (
                  <div className="mt-6 grammar-box">
                    <Lightbulb className="w-5 h-5 text-[#fa8a00] inline mr-2" />
                    <span className="font-semibold">Tip:</span> {aiExercise.grammar_tip}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// ==================== PROGRESS PAGE ====================
const ProgressPage = () => {
  const { token, user } = useAuth();
  const [progress, setProgress] = useState(null);
  const [langProgress, setLangProgress] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { setLoading(false); return; }
    Promise.all([
      fetch(`${BACKEND_URL}/api/progress`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
      fetch(`${BACKEND_URL}/api/progress/by-language`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
    ]).then(([p, lp]) => { setProgress(p); setLangProgress(lp); setLoading(false); })
    .catch(e => { console.error(e); setLoading(false); });
  }, [token]);

  if (!token) return <div className="pt-20 min-h-screen flex items-center justify-center"><p>Inicia sesión para ver tu progreso</p></div>;
  if (loading) return <div className="pt-20 min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#22955B]" /></div>;

  return (
    <div className="pt-20 pb-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="section-title mb-8">Mi Progreso</h1>
        
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Cursos Iniciados', value: progress?.courses_started || 0, icon: BookOpen, color: '#22955B' },
            { label: 'Lecciones Completadas', value: progress?.lessons_completed || 0, icon: CheckCircle, color: '#B6C932' },
            { label: 'Quizzes Tomados', value: progress?.quizzes_taken || 0, icon: Target, color: '#fa8a00' },
            { label: 'Promedio', value: `${progress?.average_score || 0}%`, icon: Award, color: '#003189' },
          ].map((stat, i) => (
            <div key={i} className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: stat.color + '15' }}>
                  <stat.icon className="w-5 h-5" style={{ color: stat.color }} />
                </div>
              </div>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-sm text-gray-500">{stat.label}</p>
            </div>
          ))}
        </div>
        
        <h2 className="font-bold text-xl mb-4">Progreso por Idioma</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {langProgress.map(lp => {
            const lang = getLangInfo(lp.language);
            return (
              <div key={lp.language} className="bg-white rounded-xl p-6 shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-3xl">{lang.flag}</span>
                  <h3 className="font-bold text-lg">{lang.name}</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between"><span className="text-gray-500">Lecciones:</span><span className="font-semibold">{lp.lessons_completed}</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Quizzes:</span><span className="font-semibold">{lp.quizzes_taken}</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Flashcards:</span><span className="font-semibold">{lp.flashcards_reviewed}</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Promedio:</span><span className="font-semibold">{lp.average_score}%</span></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ==================== FOOTER ====================
const Footer = () => (
  <footer className="footer">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid md:grid-cols-3 gap-12 mb-12">
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center gradient-primary">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <span className="font-serif text-xl font-bold text-white">Intercultura</span>
          </div>
          <p className="text-gray-400">Asistente Virtual para aprender idiomas con IA.</p>
        </div>
        
        <div>
          <h4 className="font-bold text-white mb-4">Idiomas</h4>
          <ul className="space-y-2">
            {LANGUAGES.map(l => <li key={l.id}><Link to={`/courses/${l.id}`} className="text-gray-400 hover:text-[#B6C932]">{l.flag} {l.name}</Link></li>)}
          </ul>
        </div>
        
        <div>
          <h4 className="font-bold text-white mb-4">Niveles</h4>
          <ul className="space-y-2">
            {LEVELS.map(l => <li key={l.id}><span className="text-gray-400">{l.id} - {l.title}</span></li>)}
          </ul>
        </div>
      </div>
      
      <div className="border-t border-gray-800 pt-8 text-center">
        <p className="text-gray-500 text-sm">© 2026 Intercultura - Costa Rica</p>
      </div>
    </div>
  </footer>
);

// ==================== MAIN APP ====================
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/courses/:languageId" element={<CoursesPage />} />
          <Route path="/course/:courseId" element={<CourseDetailPage />} />
          <Route path="/progress" element={<ProgressPage />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

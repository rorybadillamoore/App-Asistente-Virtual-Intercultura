import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, LANGUAGES, LEVELS, SHADOWS, getLanguageColor } from '../../src/constants/theme';
import { quizAPI, progressAPI } from '../../src/api/client';
import { Button } from '../../src/components/Button';

interface Quiz {
  id: string;
  title: string;
  course_id: string;
  language: string;
  level: string;
  question_count: number;
  time_limit_minutes: number;
}

interface LanguageProgress {
  language: string;
  quizzes_taken: number;
  average_score: number;
}

export default function QuizzesScreen() {
  const router = useRouter();
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [progress, setProgress] = useState<LanguageProgress[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      // Seed quizzes if needed
      await quizAPI.seed().catch(() => {});
      
      const [quizzesRes, progressRes] = await Promise.all([
        quizAPI.getAll(selectedLanguage || undefined, selectedLevel || undefined),
        progressAPI.byLanguage().catch(() => ({ data: [] }))
      ]);
      setQuizzes(quizzesRes.data);
      setProgress(progressRes.data || []);
    } catch (error) {
      console.log('Error fetching quizzes:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [selectedLanguage, selectedLevel]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const getLanguageStats = (lang: string) => {
    const p = progress.find(p => p.language === lang);
    return p || { quizzes_taken: 0, average_score: 0 };
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Progress Overview */}
        <Text style={styles.sectionTitle}>Tu Promedio de Quizzes Completados</Text>
        <View style={styles.progressGrid}>
          {LANGUAGES.map((lang) => {
            const stats = getLanguageStats(lang.id);
            return (
              <View key={lang.id} style={[styles.progressCard, { borderLeftColor: lang.color }]}>
                <Text style={styles.progressFlag}>{lang.flag}</Text>
                <Text style={styles.progressLang}>{lang.name}</Text>
                <Text style={[styles.progressScore, { color: stats.average_score >= 70 ? COLORS.success : stats.average_score >= 50 ? COLORS.warning : COLORS.gray500 }]}>
                  {stats.average_score > 0 ? `${stats.average_score}%` : '-'}
                </Text>
                <Text style={styles.progressCount}>{stats.quizzes_taken} quizzes</Text>
              </View>
            );
          })}
        </View>

        {/* Filters */}
        <Text style={styles.filterLabel}>Filtrar por Idioma</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, !selectedLanguage && styles.filterChipActive]}
            onPress={() => setSelectedLanguage(null)}
          >
            <Text style={[styles.filterChipText, !selectedLanguage && styles.filterChipTextActive]}>
              Todos
            </Text>
          </TouchableOpacity>
          {LANGUAGES.map((lang) => (
            <TouchableOpacity
              key={lang.id}
              style={[
                styles.filterChip,
                selectedLanguage === lang.id && styles.filterChipActive,
                selectedLanguage === lang.id && { backgroundColor: lang.color },
              ]}
              onPress={() => setSelectedLanguage(lang.id)}
            >
              <Text style={styles.filterChipFlag}>{lang.flag}</Text>
              <Text style={[styles.filterChipText, selectedLanguage === lang.id && styles.filterChipTextActive]}>
                {lang.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        <Text style={styles.filterLabel}>Filtrar por Nivel</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, !selectedLevel && styles.filterChipActive]}
            onPress={() => setSelectedLevel(null)}
          >
            <Text style={[styles.filterChipText, !selectedLevel && styles.filterChipTextActive]}>
              Todos
            </Text>
          </TouchableOpacity>
          {LEVELS.map((level) => (
            <TouchableOpacity
              key={level.id}
              style={[
                styles.filterChip,
                selectedLevel === level.id && styles.filterChipActive,
                selectedLevel === level.id && { backgroundColor: level.color },
              ]}
              onPress={() => setSelectedLevel(level.id)}
            >
              <Text style={[styles.filterChipText, selectedLevel === level.id && styles.filterChipTextActive]}>
                {level.id}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Quizzes List */}
        <Text style={styles.sectionTitle}>
          {quizzes.length} Quiz{quizzes.length !== 1 ? 'zes' : ''} Disponible{quizzes.length !== 1 ? 's' : ''}
        </Text>

        {loading ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Cargando quizzes...</Text>
          </View>
        ) : quizzes.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="help-circle-outline" size={48} color={COLORS.gray300} />
            <Text style={styles.emptyText}>No hay quizzes disponibles</Text>
          </View>
        ) : (
          quizzes.map((quiz) => (
            <TouchableOpacity
              key={quiz.id}
              style={[styles.quizCard, { borderLeftColor: getLanguageColor(quiz.language) }]}
              onPress={() => router.push(`/quiz/${quiz.id}`)}
            >
              <View style={styles.quizHeader}>
                <View style={[styles.levelBadge, { backgroundColor: getLanguageColor(quiz.language) }]}>
                  <Text style={styles.levelBadgeText}>{quiz.level}</Text>
                </View>
                <Text style={styles.quizLanguage}>{quiz.language.toUpperCase()}</Text>
              </View>
              <Text style={styles.quizTitle}>{quiz.title}</Text>
              <View style={styles.quizMeta}>
                <View style={styles.quizMetaItem}>
                  <Ionicons name="help-circle" size={16} color={COLORS.gray500} />
                  <Text style={styles.quizMetaText}>{quiz.question_count} preguntas</Text>
                </View>
                <View style={styles.quizMetaItem}>
                  <Ionicons name="time" size={16} color={COLORS.gray500} />
                  <Text style={styles.quizMetaText}>{quiz.time_limit_minutes} min</Text>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} style={styles.quizArrow} />
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: SPACING.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
    marginTop: SPACING.sm,
  },
  progressGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  progressCard: {
    width: '48%',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderLeftWidth: 4,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  progressFlag: {
    fontSize: 24,
    marginBottom: SPACING.xs,
  },
  progressLang: {
    fontSize: 12,
    color: COLORS.gray600,
    marginBottom: SPACING.xs,
  },
  progressScore: {
    fontSize: 24,
    fontWeight: '700',
  },
  progressCount: {
    fontSize: 10,
    color: COLORS.gray400,
  },
  filterLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray600,
    marginBottom: SPACING.sm,
  },
  filterScroll: {
    marginBottom: SPACING.md,
  },
  filterChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 20,
    marginRight: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.gray200,
  },
  filterChipActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  filterChipFlag: {
    fontSize: 16,
    marginRight: SPACING.xs,
  },
  filterChipText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.gray600,
  },
  filterChipTextActive: {
    color: COLORS.white,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: SPACING.xxl,
  },
  emptyText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray500,
    marginTop: SPACING.md,
  },
  quizCard: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    marginBottom: SPACING.sm,
    borderLeftWidth: 4,
    position: 'relative',
    ...SHADOWS.sm,
  },
  quizHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.sm,
    marginBottom: SPACING.xs,
  },
  levelBadge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 4,
  },
  levelBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.white,
  },
  quizLanguage: {
    fontSize: 10,
    fontWeight: '600',
    color: COLORS.gray500,
  },
  quizTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray900,
    marginBottom: SPACING.sm,
  },
  quizMeta: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  quizMetaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  quizMetaText: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  quizArrow: {
    position: 'absolute',
    right: SPACING.md,
    top: '50%',
  },
});

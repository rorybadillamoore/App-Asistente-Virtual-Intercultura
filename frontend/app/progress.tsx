import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../src/constants/theme';
import { progressAPI } from '../src/api/client';

interface ProgressData {
  user_id: string;
  courses_started: number;
  lessons_completed: number;
  flashcards_reviewed: number;
  quizzes_taken: number;
  average_score: number;
}

interface LanguageProgress {
  language: string;
  lessons_completed: number;
  quizzes_taken: number;
  average_score: number;
  flashcards_reviewed: number;
}

const languageInfo: Record<string, { name: string; flag: string; color: string }> = {
  spanish: { name: 'Español', flag: '🇪🇸', color: COLORS.spanish },
  english: { name: 'English', flag: '🇬🇧', color: COLORS.english },
  portuguese: { name: 'Português', flag: '🇧🇷', color: COLORS.portuguese },
  german: { name: 'Deutsch', flag: '🇩🇪', color: '#1a1a1a' },
  french: { name: 'Français', flag: '🇫🇷', color: '#003189' },
};

export default function ProgressScreen() {
  const router = useRouter();
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [langProgress, setLangProgress] = useState<LanguageProgress[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const [overallRes, langRes] = await Promise.all([
          progressAPI.get(),
          progressAPI.byLanguage(),
        ]);
        setProgress(overallRes.data);
        setLangProgress(langRes.data);
      } catch (e) {
        console.log('Error fetching progress:', e);
      } finally {
        setLoading(false);
      }
    };
    fetchProgress();
  }, []);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn} data-testid="progress-back-btn">
          <Ionicons name="arrow-back" size={24} color={COLORS.gray900} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Mi Progreso</Text>
        <View style={styles.backBtn} />
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
          {/* Stats Overview */}
          <View style={styles.statsGrid} data-testid="progress-stats">
            {[
              { icon: 'book-outline', label: 'Lecciones', value: progress?.lessons_completed ?? 0, color: COLORS.primary },
              { icon: 'flash-outline', label: 'Flashcards', value: progress?.flashcards_reviewed ?? 0, color: COLORS.accentOrange },
              { icon: 'school-outline', label: 'Quizzes', value: progress?.quizzes_taken ?? 0, color: COLORS.secondary },
              { icon: 'trophy-outline', label: 'Promedio', value: `${progress?.average_score ?? 0}%`, color: COLORS.accent },
            ].map((stat, i) => (
              <View key={i} style={styles.statCard}>
                <Ionicons name={stat.icon as any} size={28} color={stat.color} />
                <Text style={styles.statValue}>{stat.value}</Text>
                <Text style={styles.statLabel}>{stat.label}</Text>
              </View>
            ))}
          </View>

          {/* Language Breakdown */}
          <Text style={styles.sectionTitle}>Progreso por Idioma</Text>
          {langProgress.map((lp) => {
            const info = languageInfo[lp.language];
            if (!info) return null;
            return (
              <View key={lp.language} style={[styles.langCard, { borderLeftColor: info.color }]} data-testid={`lang-progress-${lp.language}`}>
                <View style={styles.langHeader}>
                  <Text style={styles.langFlag}>{info.flag}</Text>
                  <View style={styles.langInfo}>
                    <Text style={styles.langName}>{info.name}</Text>
                    {lp.quizzes_taken > 0 && (
                      <Text style={styles.langScore}>Promedio: {lp.average_score}%</Text>
                    )}
                  </View>
                </View>
                <View style={styles.langStats}>
                  <View style={styles.langStatItem}>
                    <Ionicons name="book-outline" size={16} color={COLORS.gray500} />
                    <Text style={styles.langStatText}>{lp.lessons_completed} lecciones</Text>
                  </View>
                  <View style={styles.langStatItem}>
                    <Ionicons name="school-outline" size={16} color={COLORS.gray500} />
                    <Text style={styles.langStatText}>{lp.quizzes_taken} quizzes</Text>
                  </View>
                  <View style={styles.langStatItem}>
                    <Ionicons name="flash-outline" size={16} color={COLORS.gray500} />
                    <Text style={styles.langStatText}>{lp.flashcards_reviewed} flashcards</Text>
                  </View>
                </View>
              </View>
            );
          })}

          {langProgress.every(lp => lp.lessons_completed === 0 && lp.quizzes_taken === 0) && (
            <View style={styles.emptyState}>
              <Ionicons name="trending-up-outline" size={48} color={COLORS.gray300} />
              <Text style={styles.emptyText}>¡Comienza tu primera lección para ver tu progreso aquí!</Text>
            </View>
          )}
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  backBtn: { width: 40, height: 40, justifyContent: 'center', alignItems: 'center' },
  headerTitle: { fontSize: 18, fontWeight: '700', color: COLORS.gray900 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  content: { padding: SPACING.md },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: SPACING.sm, marginBottom: SPACING.lg },
  statCard: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  statValue: { fontSize: 24, fontWeight: '700', color: COLORS.gray900, marginTop: SPACING.xs },
  statLabel: { fontSize: 12, color: COLORS.gray500, marginTop: 2 },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: COLORS.gray900, marginBottom: SPACING.sm },
  langCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderLeftWidth: 4,
    ...SHADOWS.sm,
  },
  langHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: SPACING.sm },
  langFlag: { fontSize: 28, marginRight: SPACING.sm },
  langInfo: { flex: 1 },
  langName: { fontSize: 16, fontWeight: '700', color: COLORS.gray900 },
  langScore: { fontSize: 12, color: COLORS.gray500 },
  langStats: { flexDirection: 'row', justifyContent: 'space-around' },
  langStatItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  langStatText: { fontSize: 12, color: COLORS.gray600 },
  emptyState: { alignItems: 'center', paddingVertical: SPACING.xl },
  emptyText: { fontSize: 14, color: COLORS.gray500, textAlign: 'center', marginTop: SPACING.md },
});

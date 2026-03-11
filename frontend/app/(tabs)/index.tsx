import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS, LANGUAGES } from '../../src/constants/theme';
import { useAuthStore } from '../../src/store/authStore';
import { progressAPI, coursesAPI } from '../../src/api/client';
import { Card } from '../../src/components/Card';

interface Progress {
  courses_started: number;
  lessons_completed: number;
  flashcards_reviewed: number;
  quizzes_taken: number;
  average_score: number;
}

export default function HomeScreen() {
  const router = useRouter();
  // Use selector to avoid re-renders when other auth state changes
  const user = useAuthStore((state) => state.user);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchProgress = async () => {
    try {
      const response = await progressAPI.get();
      setProgress(response.data);
    } catch (error) {
      console.log('Error fetching progress:', error);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchProgress();
    setRefreshing(false);
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Buenos días';
    if (hour < 18) return 'Buenas tardes';
    return 'Buenas noches';
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>{getGreeting()},</Text>
            <Text style={styles.userName}>{user?.name || 'Estudiante'}</Text>
          </View>
          <View style={styles.roleBadge}>
            <Ionicons
              name={user?.role === 'teacher' ? 'school' : 'person'}
              size={16}
              color={COLORS.primary}
            />
            <Text style={styles.roleText}>
              {user?.role === 'teacher' ? 'Profesor' : 'Estudiante'}
            </Text>
          </View>
        </View>

        {/* Progress Card */}
        <Card style={styles.progressCard}>
          <Text style={styles.sectionTitle}>Tu Progreso</Text>
          <View style={styles.statsGrid}>
            <View style={styles.statItem}>
              <View style={[styles.statIcon, { backgroundColor: COLORS.primaryLight + '20' }]}>
                <Ionicons name="book" size={20} color={COLORS.primary} />
              </View>
              <Text style={styles.statValue}>{progress?.lessons_completed || 0}</Text>
              <Text style={styles.statLabel}>Lecciones</Text>
            </View>
            <View style={styles.statItem}>
              <View style={[styles.statIcon, { backgroundColor: COLORS.secondary + '20' }]}>
                <Ionicons name="flash" size={20} color={COLORS.secondary} />
              </View>
              <Text style={styles.statValue}>{progress?.flashcards_reviewed || 0}</Text>
              <Text style={styles.statLabel}>Flashcards</Text>
            </View>
            <View style={styles.statItem}>
              <View style={[styles.statIcon, { backgroundColor: COLORS.warning + '20' }]}>
                <Ionicons name="checkmark-circle" size={20} color={COLORS.warning} />
              </View>
              <Text style={styles.statValue}>{progress?.quizzes_taken || 0}</Text>
              <Text style={styles.statLabel}>Quizzes</Text>
            </View>
            <View style={styles.statItem}>
              <View style={[styles.statIcon, { backgroundColor: COLORS.info + '20' }]}>
                <Ionicons name="trending-up" size={20} color={COLORS.info} />
              </View>
              <Text style={styles.statValue}>{progress?.average_score?.toFixed(0) || 0}%</Text>
              <Text style={styles.statLabel}>Promedio</Text>
            </View>
          </View>
        </Card>

        {/* Languages Section */}
        <Text style={styles.sectionTitle}>Idiomas Disponibles</Text>
        <View style={styles.languagesGrid}>
          {LANGUAGES.map((lang) => (
            <TouchableOpacity
              key={lang.id}
              style={[styles.languageCard, { borderLeftColor: lang.color }]}
              onPress={() => router.push({ pathname: '/(tabs)/courses', params: { language: lang.id } })}
            >
              <Text style={styles.languageFlag}>{lang.flag}</Text>
              <Text style={styles.languageName}>{lang.name}</Text>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Actions */}
        <Text style={styles.sectionTitle}>Acciones Rápidas</Text>
        <View style={styles.actionsGrid}>
          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/(tabs)/flashcards')}
          >
            <View style={[styles.actionIcon, { backgroundColor: COLORS.secondary + '20' }]}>
              <Ionicons name="flash" size={24} color={COLORS.secondary} />
            </View>
            <Text style={styles.actionText}>Practicar Flashcards</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/(tabs)/ai-tools')}
          >
            <View style={[styles.actionIcon, { backgroundColor: COLORS.primary + '20' }]}>
              <Ionicons name="sparkles" size={24} color={COLORS.primary} />
            </View>
            <Text style={styles.actionText}>Ejercicios con IA</Text>
          </TouchableOpacity>
        </View>
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
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  greeting: {
    fontSize: 16,
    color: COLORS.gray500,
  },
  userName: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  roleBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.xs,
    backgroundColor: COLORS.primaryLight + '20',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 20,
  },
  roleText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.primary,
  },
  progressCard: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.md,
    marginTop: SPACING.md,
  },
  statItem: {
    flex: 1,
    minWidth: '40%',
    alignItems: 'center',
  },
  statIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  statValue: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  languagesGrid: {
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  languageCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderLeftWidth: 4,
    ...SHADOWS.sm,
  },
  languageFlag: {
    fontSize: 24,
    marginRight: SPACING.md,
  },
  languageName: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray800,
  },
  actionsGrid: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  actionCard: {
    flex: 1,
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  actionIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  actionText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray700,
    textAlign: 'center',
  },
});

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../../src/constants/theme';
import { teacherAPI } from '../../src/api/client';
import { useAuthStore } from '../../src/store/authStore';
import { useRouter } from 'expo-router';

interface Student {
  user_id: string;
  name: string;
  email: string;
  lessons_completed: number;
  quizzes_taken: number;
  average_score: number;
  flashcards_reviewed: number;
}

interface Stats {
  total_students: number;
  total_courses: number;
  total_quizzes: number;
  average_score: number;
  quizzes_completed: number;
}

export default function TeacherScreen() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [students, setStudents] = useState<Student[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  // Redirect if not teacher
  if (user?.role !== 'teacher') {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.accessDenied}>
          <Ionicons name="lock-closed" size={64} color={COLORS.gray300} />
          <Text style={styles.accessDeniedTitle}>Acceso Restringido</Text>
          <Text style={styles.accessDeniedText}>
            Esta sección es solo para profesores.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  const fetchData = async () => {
    try {
      const [studentsRes, statsRes] = await Promise.all([
        teacherAPI.getStudents(),
        teacherAPI.getStats()
      ]);
      setStudents(studentsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.log('Error fetching teacher data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return COLORS.success;
    if (score >= 60) return COLORS.warning;
    if (score > 0) return COLORS.error;
    return COLORS.gray400;
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
          <View style={styles.headerIcon}>
            <Ionicons name="school" size={32} color={COLORS.white} />
          </View>
          <Text style={styles.headerTitle}>Panel del Profesor</Text>
          <Text style={styles.headerSubtitle}>Gestiona tus estudiantes</Text>
        </View>

        {/* Stats Overview */}
        {stats && (
          <View style={styles.statsContainer}>
            <View style={styles.statCard}>
              <Ionicons name="people" size={24} color={COLORS.primary} />
              <Text style={styles.statValue}>{stats.total_students}</Text>
              <Text style={styles.statLabel}>Estudiantes</Text>
            </View>
            <View style={styles.statCard}>
              <Ionicons name="book" size={24} color={COLORS.secondary} />
              <Text style={styles.statValue}>{stats.total_courses}</Text>
              <Text style={styles.statLabel}>Cursos</Text>
            </View>
            <View style={styles.statCard}>
              <Ionicons name="checkmark-circle" size={24} color={COLORS.info} />
              <Text style={styles.statValue}>{stats.quizzes_completed}</Text>
              <Text style={styles.statLabel}>Quizzes</Text>
            </View>
            <View style={styles.statCard}>
              <Ionicons name="trending-up" size={24} color={COLORS.warning} />
              <Text style={styles.statValue}>{stats.average_score}%</Text>
              <Text style={styles.statLabel}>Promedio</Text>
            </View>
          </View>
        )}

        {/* Students List */}
        <Text style={styles.sectionTitle}>
          Estudiantes ({students.length})
        </Text>

        {loading ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Cargando estudiantes...</Text>
          </View>
        ) : students.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="people-outline" size={48} color={COLORS.gray300} />
            <Text style={styles.emptyText}>No hay estudiantes registrados</Text>
          </View>
        ) : (
          students.map((student) => (
            <View key={student.user_id} style={styles.studentCard}>
              <View style={styles.studentAvatar}>
                <Text style={styles.studentAvatarText}>
                  {student.name.charAt(0).toUpperCase()}
                </Text>
              </View>
              <View style={styles.studentInfo}>
                <Text style={styles.studentName}>{student.name}</Text>
                <Text style={styles.studentEmail}>{student.email}</Text>
                <View style={styles.studentStats}>
                  <View style={styles.studentStatItem}>
                    <Ionicons name="book" size={12} color={COLORS.gray400} />
                    <Text style={styles.studentStatText}>{student.lessons_completed} lecciones</Text>
                  </View>
                  <View style={styles.studentStatItem}>
                    <Ionicons name="flash" size={12} color={COLORS.gray400} />
                    <Text style={styles.studentStatText}>{student.flashcards_reviewed} flashcards</Text>
                  </View>
                </View>
              </View>
              <View style={styles.studentScore}>
                <Text style={[styles.scoreValue, { color: getScoreColor(student.average_score) }]}>
                  {student.average_score > 0 ? `${student.average_score}%` : '-'}
                </Text>
                <Text style={styles.scoreLabel}>{student.quizzes_taken} quizzes</Text>
              </View>
            </View>
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
  accessDenied: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  accessDeniedTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.gray900,
    marginTop: SPACING.md,
  },
  accessDeniedText: {
    fontSize: 14,
    color: COLORS.gray500,
    textAlign: 'center',
    marginTop: SPACING.sm,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  headerIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: COLORS.secondary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  headerSubtitle: {
    fontSize: 14,
    color: COLORS.gray500,
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  statCard: {
    width: '48%',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
    marginTop: SPACING.xs,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
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
  studentCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    marginBottom: SPACING.sm,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  studentAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  studentAvatarText: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.white,
  },
  studentInfo: {
    flex: 1,
  },
  studentName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray900,
  },
  studentEmail: {
    fontSize: 12,
    color: COLORS.gray500,
    marginBottom: SPACING.xs,
  },
  studentStats: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  studentStatItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  studentStatText: {
    fontSize: 10,
    color: COLORS.gray400,
  },
  studentScore: {
    alignItems: 'center',
  },
  scoreValue: {
    fontSize: 20,
    fontWeight: '700',
  },
  scoreLabel: {
    fontSize: 10,
    color: COLORS.gray400,
  },
});

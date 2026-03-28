import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS, getLanguageColor, getLevelColor } from '../../src/constants/theme';
import { coursesAPI } from '../../src/api/client';
import { Card } from '../../src/components/Card';

interface Course {
  id: string;
  language: string;
  level: string;
  title: string;
  description: string;
  lesson_count: number;
}

interface Lesson {
  id: string;
  title: string;
  order: number;
}

interface Quiz {
  id: string;
  title: string;
}

export default function CourseDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [course, setCourse] = useState<Course | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourseData();
  }, [id]);

  const fetchCourseData = async () => {
    if (!id) return;
    try {
      const [courseRes, lessonsRes, quizzesRes] = await Promise.all([
        coursesAPI.getOne(id),
        coursesAPI.getLessons(id),
        coursesAPI.getQuizzes(id),
      ]);
      setCourse(courseRes.data);
      setLessons(lessonsRes.data);
      setQuizzes(quizzesRes.data);
    } catch (error) {
      console.log('Error fetching course:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  if (!course) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Curso no encontrado</Text>
      </View>
    );
  }

  const languageColor = getLanguageColor(course.language);
  const levelColor = getLevelColor(course.level);

  return (
    <>
      <Stack.Screen
        options={{
          title: course.title,
          headerStyle: { backgroundColor: COLORS.white },
          headerTintColor: COLORS.gray900,
          headerRight: () => (
            <TouchableOpacity onPress={() => router.replace('/(tabs)')} style={{ marginRight: 8 }}>
              <Ionicons name="home-outline" size={24} color={COLORS.primary} />
            </TouchableOpacity>
          ),
        }}
      />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Course Header */}
          <View style={[styles.headerCard, { borderTopColor: languageColor }]}>
            <View style={styles.badgeRow}>
              <View style={[styles.badge, { backgroundColor: languageColor }]}>
                <Text style={styles.badgeText}>{course.language.toUpperCase()}</Text>
              </View>
              <View style={[styles.badge, { backgroundColor: levelColor }]}>
                <Text style={styles.badgeText}>{course.level}</Text>
              </View>
            </View>
            <Text style={styles.courseTitle}>{course.title}</Text>
            <Text style={styles.courseDescription}>{course.description}</Text>
          </View>

          {/* Lessons Section */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              <Ionicons name="book" size={20} color={COLORS.gray900} /> Lecciones ({lessons.length})
            </Text>
            {lessons.length === 0 ? (
              <View style={styles.emptyCard}>
                <Ionicons name="book-outline" size={40} color={COLORS.gray300} />
                <Text style={styles.emptyText}>No hay lecciones disponibles</Text>
              </View>
            ) : (
              lessons.map((lesson, index) => (
                <TouchableOpacity
                  key={lesson.id}
                  style={styles.lessonCard}
                  onPress={() => router.push(`/lesson/${lesson.id}`)}
                >
                  <View style={styles.lessonNumber}>
                    <Text style={styles.lessonNumberText}>{index + 1}</Text>
                  </View>
                  <Text style={styles.lessonTitle}>{lesson.title}</Text>
                  <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
                </TouchableOpacity>
              ))
            )}
          </View>

          {/* Quizzes Section */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              <Ionicons name="checkmark-circle" size={20} color={COLORS.gray900} /> Quizzes ({quizzes.length})
            </Text>
            {quizzes.length === 0 ? (
              <View style={styles.emptyCard}>
                <Ionicons name="help-circle-outline" size={40} color={COLORS.gray300} />
                <Text style={styles.emptyText}>No hay quizzes disponibles</Text>
              </View>
            ) : (
              quizzes.map((quiz) => (
                <TouchableOpacity
                  key={quiz.id}
                  style={styles.quizCard}
                  onPress={() => router.push(`/quiz/${quiz.id}`)}
                >
                  <View style={styles.quizIcon}>
                    <Ionicons name="help-circle" size={24} color={COLORS.warning} />
                  </View>
                  <Text style={styles.quizTitle}>{quiz.title}</Text>
                  <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
                </TouchableOpacity>
              ))
            )}
          </View>
        </ScrollView>
      </SafeAreaView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  errorText: {
    fontSize: 16,
    color: COLORS.gray500,
  },
  scrollContent: {
    padding: SPACING.md,
  },
  headerCard: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderTopWidth: 4,
    ...SHADOWS.md,
  },
  badgeRow: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
  },
  badge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 6,
  },
  badgeText: {
    color: COLORS.white,
    fontSize: 12,
    fontWeight: '700',
  },
  courseTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.sm,
  },
  courseDescription: {
    fontSize: 16,
    color: COLORS.gray600,
    lineHeight: 24,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  emptyCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.xl,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  emptyText: {
    fontSize: 14,
    color: COLORS.gray400,
    marginTop: SPACING.sm,
  },
  lessonCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  lessonNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  lessonNumberText: {
    color: COLORS.white,
    fontSize: 14,
    fontWeight: '700',
  },
  lessonTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray800,
  },
  quizCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  quizIcon: {
    marginRight: SPACING.md,
  },
  quizTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray800,
  },
});

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, LANGUAGES, LEVELS, getLanguageColor } from '../../src/constants/theme';
import { coursesAPI } from '../../src/api/client';
import { CourseCard } from '../../src/components/Card';

interface Course {
  id: string;
  language: string;
  level: string;
  title: string;
  description: string;
  lesson_count: number;
}

export default function CoursesScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ language?: string }>();
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(params.language || null);
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchCourses = async () => {
    try {
      const response = await coursesAPI.getAll(
        selectedLanguage || undefined,
        selectedLevel || undefined
      );
      setCourses(response.data);
    } catch (error) {
      console.log('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, [selectedLanguage, selectedLevel]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchCourses();
    setRefreshing(false);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Language Filter */}
        <Text style={styles.filterLabel}>Idioma</Text>
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
              <Text
                style={[
                  styles.filterChipText,
                  selectedLanguage === lang.id && styles.filterChipTextActive,
                ]}
              >
                {lang.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Level Filter */}
        <Text style={styles.filterLabel}>Nivel</Text>
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
              <Text
                style={[
                  styles.filterChipText,
                  selectedLevel === level.id && styles.filterChipTextActive,
                ]}
              >
                {level.id}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Courses List */}
        <Text style={styles.sectionTitle}>
          {courses.length} Curso{courses.length !== 1 ? 's' : ''} Disponible{courses.length !== 1 ? 's' : ''}
        </Text>

        {loading ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Cargando cursos...</Text>
          </View>
        ) : courses.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="book-outline" size={48} color={COLORS.gray300} />
            <Text style={styles.emptyText}>No hay cursos disponibles</Text>
            <Text style={styles.emptySubtext}>Intenta cambiar los filtros</Text>
          </View>
        ) : (
          courses.map((course) => (
            <CourseCard
              key={course.id}
              title={course.title}
              language={course.language}
              level={course.level}
              description={course.description}
              lessonCount={course.lesson_count}
              languageColor={getLanguageColor(course.language)}
              onPress={() => router.push(`/course/${course.id}`)}
            />
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
    marginTop: SPACING.sm,
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
  emptySubtext: {
    fontSize: 14,
    color: COLORS.gray400,
    marginTop: SPACING.xs,
  },
});

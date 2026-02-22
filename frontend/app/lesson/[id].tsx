import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../../src/constants/theme';
import { lessonsAPI } from '../../src/api/client';
import { Button } from '../../src/components/Button';

interface Lesson {
  id: string;
  course_id: string;
  title: string;
  content: string;
  vocabulary: Array<{ word: string; translation: string; example?: string }>;
  grammar_points: string[];
}

export default function LessonDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    fetchLesson();
  }, [id]);

  const fetchLesson = async () => {
    if (!id) return;
    try {
      const response = await lessonsAPI.getOne(id);
      setLesson(response.data);
    } catch (error) {
      console.log('Error fetching lesson:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    if (!id) return;
    setCompleting(true);
    try {
      await lessonsAPI.complete(id);
      router.back();
    } catch (error) {
      console.log('Error completing lesson:', error);
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  if (!lesson) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Lección no encontrada</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: lesson.title,
          headerStyle: { backgroundColor: COLORS.white },
          headerTintColor: COLORS.gray900,
        }}
      />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Lesson Content */}
          <View style={styles.contentCard}>
            <Text style={styles.lessonTitle}>{lesson.title}</Text>
            <Text style={styles.lessonContent}>{lesson.content}</Text>
          </View>

          {/* Vocabulary Section */}
          {lesson.vocabulary && lesson.vocabulary.length > 0 && (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="book" size={20} color={COLORS.secondary} />
                <Text style={styles.sectionTitle}>Vocabulario</Text>
              </View>
              {lesson.vocabulary.map((item, index) => (
                <View key={index} style={styles.vocabCard}>
                  <Text style={styles.vocabWord}>{item.word}</Text>
                  <Text style={styles.vocabTranslation}>{item.translation}</Text>
                  {item.example && (
                    <Text style={styles.vocabExample}>"{item.example}"</Text>
                  )}
                </View>
              ))}
            </View>
          )}

          {/* Grammar Points Section */}
          {lesson.grammar_points && lesson.grammar_points.length > 0 && (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="bulb" size={20} color={COLORS.warning} />
                <Text style={styles.sectionTitle}>Puntos Gramaticales</Text>
              </View>
              {lesson.grammar_points.map((point, index) => (
                <View key={index} style={styles.grammarCard}>
                  <View style={styles.grammarBullet}>
                    <Ionicons name="checkmark" size={16} color={COLORS.white} />
                  </View>
                  <Text style={styles.grammarText}>{point}</Text>
                </View>
              ))}
            </View>
          )}

          {/* Complete Button */}
          <Button
            title="Marcar como Completada"
            onPress={handleComplete}
            loading={completing}
            variant="primary"
            size="lg"
            style={styles.completeButton}
            icon={<Ionicons name="checkmark-circle" size={20} color={COLORS.white} />}
          />
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
  contentCard: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    ...SHADOWS.md,
  },
  lessonTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  lessonContent: {
    fontSize: 16,
    color: COLORS.gray700,
    lineHeight: 26,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  vocabCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  vocabWord: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  vocabTranslation: {
    fontSize: 14,
    color: COLORS.gray600,
    marginTop: SPACING.xs,
  },
  vocabExample: {
    fontSize: 14,
    color: COLORS.gray500,
    fontStyle: 'italic',
    marginTop: SPACING.xs,
  },
  grammarCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  grammarBullet: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: COLORS.secondary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.sm,
  },
  grammarText: {
    flex: 1,
    fontSize: 15,
    color: COLORS.gray700,
    lineHeight: 22,
  },
  completeButton: {
    marginTop: SPACING.md,
  },
});

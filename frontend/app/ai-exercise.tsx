import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS, getLanguageColor, getLevelColor } from '../src/constants/theme';
import { aiAPI } from '../src/api/client';
import { Button } from '../src/components/Button';

interface Exercise {
  title: string;
  instructions: string;
  questions: Array<{
    question: string;
    options: string[];
    correct_answer: number;
    explanation: string;
  }>;
  vocabulary?: Array<{
    word: string;
    translation: string;
    example?: string;
  }>;
  grammar_tip?: string;
}

export default function AIExerciseScreen() {
  const { language, level, exercise_type, topic } = useLocalSearchParams<{
    language: string;
    level: string;
    exercise_type: string;
    topic: string;
  }>();
  const router = useRouter();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<number[]>([]);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    generateExercise();
  }, []);

  const generateExercise = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await aiAPI.generateExercise({
        language: language || 'spanish',
        level: level || 'A1',
        topic: topic || 'general',
        exercise_type: exercise_type || 'grammar',
      });
      
      if (response.data.success && response.data.exercise) {
        setExercise(response.data.exercise);
        setSelectedAnswers(new Array(response.data.exercise.questions?.length || 0).fill(-1));
      } else {
        setError('No se pudo generar el ejercicio');
      }
    } catch (err: any) {
      console.log('Error generating exercise:', err);
      setError(err.response?.data?.detail || 'Error al generar el ejercicio');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (index: number) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[currentQuestion] = index;
    setSelectedAnswers(newAnswers);
  };

  const handleNext = () => {
    if (exercise && currentQuestion < exercise.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleFinish = () => {
    setShowResults(true);
  };

  const calculateScore = () => {
    if (!exercise) return { correct: 0, total: 0, percentage: 0 };
    let correct = 0;
    exercise.questions.forEach((q, i) => {
      if (selectedAnswers[i] === q.correct_answer) correct++;
    });
    return {
      correct,
      total: exercise.questions.length,
      percentage: Math.round((correct / exercise.questions.length) * 100),
    };
  };

  const languageColor = getLanguageColor(language || 'spanish');
  const levelColor = getLevelColor(level || 'A1');

  if (loading) {
    return (
      <>
        <Stack.Screen options={{ title: 'Generando Ejercicio' }} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={styles.loadingText}>Generando ejercicio con IA...</Text>
          <Text style={styles.loadingSubtext}>Esto puede tomar unos segundos</Text>
        </View>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Stack.Screen options={{ title: 'Error' }} />
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={64} color={COLORS.error} />
          <Text style={styles.errorText}>{error}</Text>
          <Button
            title="Reintentar"
            onPress={generateExercise}
            variant="primary"
            style={styles.retryButton}
          />
          <Button
            title="Volver"
            onPress={() => router.back()}
            variant="outline"
            style={styles.retryButton}
          />
        </View>
      </>
    );
  }

  if (!exercise || !exercise.questions) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>No se pudo cargar el ejercicio</Text>
        <Button title="Volver" onPress={() => router.back()} variant="outline" />
      </View>
    );
  }

  // Results Screen
  if (showResults) {
    const score = calculateScore();
    return (
      <>
        <Stack.Screen options={{ title: 'Resultados' }} />
        <SafeAreaView style={styles.container} edges={['bottom']}>
          <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
            <View style={styles.resultHeader}>
              <View style={[
                styles.resultIcon,
                { backgroundColor: score.percentage >= 70 ? COLORS.success + '20' : COLORS.warning + '20' }
              ]}>
                <Ionicons
                  name={score.percentage >= 70 ? 'sparkles' : 'bulb'}
                  size={48}
                  color={score.percentage >= 70 ? COLORS.success : COLORS.warning}
                />
              </View>
              <Text style={styles.resultTitle}>
                {score.percentage >= 70 ? '¡Muy bien!' : 'Sigue Practicando'}
              </Text>
              <Text style={styles.resultScore}>
                {score.correct} / {score.total}
              </Text>
              <Text style={styles.resultPercentage}>{score.percentage}%</Text>
            </View>

            {/* Vocabulary Section */}
            {exercise.vocabulary && exercise.vocabulary.length > 0 && (
              <View style={styles.vocabSection}>
                <Text style={styles.vocabTitle}>Vocabulario Aprendido</Text>
                {exercise.vocabulary.map((item, index) => (
                  <View key={index} style={styles.vocabCard}>
                    <Text style={styles.vocabWord}>{item.word}</Text>
                    <Text style={styles.vocabTranslation}>{item.translation}</Text>
                  </View>
                ))}
              </View>
            )}

            {/* Grammar Tip */}
            {exercise.grammar_tip && (
              <View style={styles.tipCard}>
                <Ionicons name="bulb" size={24} color={COLORS.warning} />
                <View style={styles.tipContent}>
                  <Text style={styles.tipTitle}>Consejo Gramatical</Text>
                  <Text style={styles.tipText}>{exercise.grammar_tip}</Text>
                </View>
              </View>
            )}

            <View style={styles.actionButtons}>
              <Button
                title="Nuevo Ejercicio"
                onPress={() => {
                  setShowResults(false);
                  setCurrentQuestion(0);
                  generateExercise();
                }}
                variant="primary"
                style={styles.actionButton}
              />
              <Button
                title="Volver"
                onPress={() => router.back()}
                variant="outline"
                style={styles.actionButton}
              />
            </View>
          </ScrollView>
        </SafeAreaView>
      </>
    );
  }

  const question = exercise.questions[currentQuestion];
  const allAnswered = selectedAnswers.every((a) => a >= 0);

  return (
    <>
      <Stack.Screen options={{ title: exercise.title || 'Ejercicio IA' }} />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Header Badges */}
          <View style={styles.badgeRow}>
            <View style={[styles.badge, { backgroundColor: languageColor }]}>
              <Text style={styles.badgeText}>{(language || 'spanish').toUpperCase()}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: levelColor }]}>
              <Text style={styles.badgeText}>{level || 'A1'}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: COLORS.primary }]}>
              <Ionicons name="sparkles" size={12} color={COLORS.white} />
              <Text style={styles.badgeText}> IA</Text>
            </View>
          </View>

          {/* Instructions */}
          {exercise.instructions && (
            <View style={styles.instructionsCard}>
              <Ionicons name="information-circle" size={20} color={COLORS.info} />
              <Text style={styles.instructionsText}>{exercise.instructions}</Text>
            </View>
          )}

          {/* Progress */}
          <View style={styles.progressContainer}>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFill,
                  { width: `${((currentQuestion + 1) / exercise.questions.length) * 100}%` },
                ]}
              />
            </View>
            <Text style={styles.progressText}>
              Pregunta {currentQuestion + 1} de {exercise.questions.length}
            </Text>
          </View>

          {/* Question */}
          <View style={styles.questionCard}>
            <Text style={styles.questionText}>{question.question}</Text>
          </View>

          {/* Options */}
          {question.options.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.optionCard,
                selectedAnswers[currentQuestion] === index && styles.optionCardSelected,
              ]}
              onPress={() => handleSelectAnswer(index)}
            >
              <View style={[
                styles.optionLetter,
                selectedAnswers[currentQuestion] === index && styles.optionLetterSelected,
              ]}>
                <Text style={[
                  styles.optionLetterText,
                  selectedAnswers[currentQuestion] === index && styles.optionLetterTextSelected,
                ]}>
                  {String.fromCharCode(65 + index)}
                </Text>
              </View>
              <Text style={[
                styles.optionText,
                selectedAnswers[currentQuestion] === index && styles.optionTextSelected,
              ]}>
                {option}
              </Text>
            </TouchableOpacity>
          ))}

          {/* Navigation */}
          <View style={styles.navigationContainer}>
            <Button
              title="Anterior"
              onPress={handlePrevious}
              variant="outline"
              disabled={currentQuestion === 0}
              style={styles.navButton}
            />
            {currentQuestion < exercise.questions.length - 1 ? (
              <Button
                title="Siguiente"
                onPress={handleNext}
                variant="primary"
                disabled={selectedAnswers[currentQuestion] < 0}
                style={styles.navButton}
              />
            ) : (
              <Button
                title="Finalizar"
                onPress={handleFinish}
                variant="primary"
                disabled={!allAnswered}
                style={styles.navButton}
              />
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
    padding: SPACING.lg,
  },
  loadingText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.gray700,
    marginTop: SPACING.md,
  },
  loadingSubtext: {
    fontSize: 14,
    color: COLORS.gray500,
    marginTop: SPACING.xs,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
    padding: SPACING.lg,
  },
  errorText: {
    fontSize: 16,
    color: COLORS.gray600,
    textAlign: 'center',
    marginTop: SPACING.md,
    marginBottom: SPACING.lg,
  },
  retryButton: {
    marginTop: SPACING.sm,
    minWidth: 150,
  },
  scrollContent: {
    padding: SPACING.md,
  },
  badgeRow: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 6,
  },
  badgeText: {
    color: COLORS.white,
    fontSize: 12,
    fontWeight: '700',
  },
  instructionsCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: COLORS.info + '15',
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    gap: SPACING.sm,
  },
  instructionsText: {
    flex: 1,
    fontSize: 14,
    color: COLORS.gray700,
    lineHeight: 20,
  },
  progressContainer: {
    marginBottom: SPACING.md,
  },
  progressBar: {
    height: 8,
    backgroundColor: COLORS.gray200,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  progressText: {
    textAlign: 'center',
    marginTop: SPACING.sm,
    fontSize: 14,
    color: COLORS.gray500,
  },
  questionCard: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    ...SHADOWS.md,
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.gray900,
    lineHeight: 26,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 2,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  optionCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primaryLight + '10',
  },
  optionLetter: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.gray100,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  optionLetterSelected: {
    backgroundColor: COLORS.primary,
  },
  optionLetterText: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.gray600,
  },
  optionLetterTextSelected: {
    color: COLORS.white,
  },
  optionText: {
    flex: 1,
    fontSize: 16,
    color: COLORS.gray700,
  },
  optionTextSelected: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  navigationContainer: {
    flexDirection: 'row',
    gap: SPACING.md,
    marginTop: SPACING.lg,
  },
  navButton: {
    flex: 1,
  },
  resultHeader: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  resultIcon: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  resultTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  resultScore: {
    fontSize: 48,
    fontWeight: '800',
    color: COLORS.primary,
    marginTop: SPACING.sm,
  },
  resultPercentage: {
    fontSize: 18,
    color: COLORS.gray500,
  },
  vocabSection: {
    marginBottom: SPACING.lg,
  },
  vocabTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  vocabCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  vocabWord: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  vocabTranslation: {
    fontSize: 14,
    color: COLORS.gray600,
  },
  tipCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.warning + '15',
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    gap: SPACING.sm,
  },
  tipContent: {
    flex: 1,
  },
  tipTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.warning,
    marginBottom: SPACING.xs,
  },
  tipText: {
    fontSize: 14,
    color: COLORS.gray700,
    lineHeight: 20,
  },
  actionButtons: {
    gap: SPACING.sm,
  },
  actionButton: {
    width: '100%',
  },
});

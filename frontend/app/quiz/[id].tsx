import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../src/constants/theme';
import { quizAPI } from '../src/api/client';
import { Button } from '../src/components/Button';

interface Quiz {
  id: string;
  title: string;
  questions: Array<{
    question: string;
    options: string[];
    correct_answer: number;
    explanation: string;
  }>;
  time_limit_minutes: number;
}

interface QuizResult {
  quiz_id: string;
  score: number;
  total: number;
  percentage: number;
  results: Array<{
    question: string;
    your_answer: number;
    correct_answer: number;
    is_correct: boolean;
    explanation: string;
  }>;
}

export default function QuizScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<QuizResult | null>(null);

  useEffect(() => {
    fetchQuiz();
  }, [id]);

  const fetchQuiz = async () => {
    if (!id) return;
    try {
      const response = await quizAPI.getOne(id);
      setQuiz(response.data);
      setAnswers(new Array(response.data.questions.length).fill(-1));
    } catch (error) {
      console.log('Error fetching quiz:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (index: number) => {
    setSelectedAnswer(index);
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = index;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (quiz && currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(answers[currentQuestion + 1] >= 0 ? answers[currentQuestion + 1] : null);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
      setSelectedAnswer(answers[currentQuestion - 1] >= 0 ? answers[currentQuestion - 1] : null);
    }
  };

  const handleSubmit = async () => {
    if (!id || !quiz) return;
    setSubmitting(true);
    try {
      const response = await quizAPI.submit(id, answers);
      setResult(response.data);
    } catch (error) {
      console.log('Error submitting quiz:', error);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  if (!quiz) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Quiz no encontrado</Text>
      </View>
    );
  }

  // Results Screen
  if (result) {
    return (
      <>
        <Stack.Screen options={{ title: 'Resultados' }} />
        <SafeAreaView style={styles.container} edges={['bottom']}>
          <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
            <View style={styles.resultHeader}>
              <View style={[
                styles.resultIcon,
                { backgroundColor: result.percentage >= 70 ? COLORS.success + '20' : COLORS.warning + '20' }
              ]}>
                <Ionicons
                  name={result.percentage >= 70 ? 'trophy' : 'ribbon'}
                  size={48}
                  color={result.percentage >= 70 ? COLORS.success : COLORS.warning}
                />
              </View>
              <Text style={styles.resultTitle}>
                {result.percentage >= 70 ? '¡Excelente!' : 'Sigue Practicando'}
              </Text>
              <Text style={styles.resultScore}>
                {result.score} / {result.total}
              </Text>
              <Text style={styles.resultPercentage}>{result.percentage.toFixed(0)}%</Text>
            </View>

            <Text style={styles.reviewTitle}>Revisión de Respuestas</Text>
            {result.results.map((item, index) => (
              <View
                key={index}
                style={[
                  styles.reviewCard,
                  { borderLeftColor: item.is_correct ? COLORS.success : COLORS.error }
                ]}
              >
                <View style={styles.reviewHeader}>
                  <Ionicons
                    name={item.is_correct ? 'checkmark-circle' : 'close-circle'}
                    size={24}
                    color={item.is_correct ? COLORS.success : COLORS.error}
                  />
                  <Text style={styles.reviewQuestion}>{item.question}</Text>
                </View>
                {!item.is_correct && item.explanation && (
                  <Text style={styles.reviewExplanation}>{item.explanation}</Text>
                )}
              </View>
            ))}

            <Button
              title="Volver al Curso"
              onPress={() => router.back()}
              variant="primary"
              style={styles.backButton}
            />
          </ScrollView>
        </SafeAreaView>
      </>
    );
  }

  const question = quiz.questions[currentQuestion];
  const allAnswered = answers.every((a) => a >= 0);

  return (
    <>
      <Stack.Screen options={{ title: quiz.title }} />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Progress */}
          <View style={styles.progressContainer}>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFill,
                  { width: `${((currentQuestion + 1) / quiz.questions.length) * 100}%` },
                ]}
              />
            </View>
            <Text style={styles.progressText}>
              Pregunta {currentQuestion + 1} de {quiz.questions.length}
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
                selectedAnswer === index && styles.optionCardSelected,
              ]}
              onPress={() => handleSelectAnswer(index)}
            >
              <View style={[
                styles.optionLetter,
                selectedAnswer === index && styles.optionLetterSelected,
              ]}>
                <Text style={[
                  styles.optionLetterText,
                  selectedAnswer === index && styles.optionLetterTextSelected,
                ]}>
                  {String.fromCharCode(65 + index)}
                </Text>
              </View>
              <Text style={[
                styles.optionText,
                selectedAnswer === index && styles.optionTextSelected,
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
            {currentQuestion < quiz.questions.length - 1 ? (
              <Button
                title="Siguiente"
                onPress={handleNext}
                variant="primary"
                disabled={selectedAnswer === null}
                style={styles.navButton}
              />
            ) : (
              <Button
                title="Enviar Quiz"
                onPress={handleSubmit}
                variant="primary"
                disabled={!allAnswered}
                loading={submitting}
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
  },
  errorText: {
    fontSize: 16,
    color: COLORS.gray500,
  },
  scrollContent: {
    padding: SPACING.md,
  },
  progressContainer: {
    marginBottom: SPACING.lg,
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
  reviewTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  reviewCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderLeftWidth: 4,
    ...SHADOWS.sm,
  },
  reviewHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: SPACING.sm,
  },
  reviewQuestion: {
    flex: 1,
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.gray800,
  },
  reviewExplanation: {
    fontSize: 14,
    color: COLORS.gray600,
    marginTop: SPACING.sm,
    marginLeft: 32,
    fontStyle: 'italic',
  },
  backButton: {
    marginTop: SPACING.lg,
  },
});

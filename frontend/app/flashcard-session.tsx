import React, { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Animated, Platform, ActivityIndicator, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS, getLanguageColor } from '../src/constants/theme';
import { flashcardsAPI, ttsAPI } from '../src/api/client';
import { Button } from '../src/components/Button';

interface Flashcard {
  id: string;
  language: string;
  level: string;
  word: string;
  translation: string;
  example: string;
  pronunciation: string;
}

export default function FlashcardSessionScreen() {
  const { language, level } = useLocalSearchParams<{ language: string; level: string }>();
  const router = useRouter();
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [flipAnim] = useState(new Animated.Value(0));
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    fetchFlashcards();
  }, [language, level]);

  const fetchFlashcards = async () => {
    try {
      const response = await flashcardsAPI.getAll(language, level, 20);
      setFlashcards(response.data);
    } catch (error) {
      console.log('Error fetching flashcards:', error);
    }
  };

  const flipCard = () => {
    Animated.spring(flipAnim, {
      toValue: isFlipped ? 0 : 1,
      friction: 8,
      tension: 10,
      useNativeDriver: true,
    }).start();
    setIsFlipped(!isFlipped);
  };

  const handleAnswer = async (correct: boolean) => {
    const currentCard = flashcards[currentIndex];
    
    try {
      await flashcardsAPI.review(currentCard.id, correct);
    } catch (error) {
      console.log('Error recording review:', error);
    }

    if (correct) {
      setCorrectCount(correctCount + 1);
    }

    // Reset flip and move to next card
    setIsFlipped(false);
    flipAnim.setValue(0);

    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setSessionComplete(true);
    }
  };

  const restartSession = () => {
    setCurrentIndex(0);
    setCorrectCount(0);
    setIsFlipped(false);
    setSessionComplete(false);
    flipAnim.setValue(0);
  };

  const playPronunciation = async (text: string) => {
    if (isPlayingAudio) return;
    
    setIsPlayingAudio(true);
    try {
      const response = await ttsAPI.generate(text, language || 'spanish');
      const { audio_base64 } = response.data;
      
      if (Platform.OS === 'web') {
        // Web audio playback
        if (audioRef.current) {
          audioRef.current.pause();
        }
        const audio = new Audio(`data:audio/mp3;base64,${audio_base64}`);
        audioRef.current = audio;
        audio.onended = () => setIsPlayingAudio(false);
        audio.onerror = () => setIsPlayingAudio(false);
        await audio.play();
      } else {
        // For native, we would use expo-av
        // This is a simplified web-first implementation
        setIsPlayingAudio(false);
      }
    } catch (error) {
      console.log('Error playing pronunciation:', error);
      setIsPlayingAudio(false);
    }
  };

  if (flashcards.length === 0) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Cargando tarjetas...</Text>
      </View>
    );
  }

  if (sessionComplete) {
    const percentage = Math.round((correctCount / flashcards.length) * 100);
    return (
      <>
        <Stack.Screen options={{ title: 'Resultados' }} />
        <SafeAreaView style={styles.container} edges={['bottom']}>
          <View style={styles.resultsContainer}>
            <View style={styles.resultsIcon}>
              <Ionicons
                name={percentage >= 70 ? 'trophy' : 'ribbon'}
                size={60}
                color={percentage >= 70 ? COLORS.warning : COLORS.primary}
              />
            </View>
            <Text style={styles.resultsTitle}>
              ¡Sesión Completada!
            </Text>
            <Text style={styles.resultsScore}>
              {correctCount} / {flashcards.length}
            </Text>
            <Text style={styles.resultsPercentage}>{percentage}% correcto</Text>
            <View style={styles.resultsButtons}>
              <Button
                title="Repetir Sesión"
                onPress={restartSession}
                variant="outline"
                style={styles.resultButton}
              />
              <Button
                title="Volver"
                onPress={() => router.back()}
                variant="primary"
                style={styles.resultButton}
              />
            </View>
          </View>
        </SafeAreaView>
      </>
    );
  }

  const currentCard = flashcards[currentIndex];
  const languageColor = getLanguageColor(currentCard.language);

  const frontInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '180deg'],
  });

  const backInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['180deg', '360deg'],
  });

  return (
    <>
      <Stack.Screen options={{ title: `Flashcards ${level}`, headerRight: () => (
            <TouchableOpacity onPress={() => router.replace('/(tabs)')} style={{ marginRight: 8 }}>
              <Ionicons name="home-outline" size={24} color={COLORS.primary} />
            </TouchableOpacity>
          ) }} />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Progress */}
        <View style={styles.progressContainer}>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressFill,
                {
                  width: `${((currentIndex + 1) / flashcards.length) * 100}%`,
                  backgroundColor: languageColor,
                },
              ]}
            />
          </View>
          <Text style={styles.progressText}>
            {currentIndex + 1} / {flashcards.length}
          </Text>
        </View>

        {/* Flashcard */}
        <TouchableOpacity style={styles.cardContainer} onPress={flipCard} activeOpacity={0.9}>
          <Animated.View
            style={[
              styles.card,
              styles.cardFront,
              { borderTopColor: languageColor },
              { transform: [{ rotateY: frontInterpolate }] },
            ]}
          >
            <Text style={styles.cardInstruction}>Toca para voltear</Text>
            <Text style={styles.cardWord}>{currentCard.word}</Text>
            {currentCard.pronunciation && (
              <Text style={styles.cardPronunciation}>{currentCard.pronunciation}</Text>
            )}
          </Animated.View>

          <Animated.View
            style={[
              styles.card,
              styles.cardBack,
              { borderTopColor: languageColor },
              { transform: [{ rotateY: backInterpolate }] },
            ]}
          >
            <Text style={styles.cardInstruction}>Traducción</Text>
            <Text style={styles.cardTranslation}>{currentCard.translation}</Text>
            {currentCard.example && (
              <Text style={styles.cardExample}>"{currentCard.example}"</Text>
            )}
          </Animated.View>
        </TouchableOpacity>

        {/* Bottom Controls */}
        <View style={styles.controlsContainer}>
          {/* Audio Button */}
          <TouchableOpacity
            style={[styles.audioButton, isPlayingAudio && styles.audioButtonPlaying]}
            onPress={() => playPronunciation(currentCard.word)}
            disabled={isPlayingAudio}
          >
            {isPlayingAudio ? (
              <ActivityIndicator size="small" color={COLORS.white} />
            ) : (
              <Ionicons name="volume-high" size={28} color={COLORS.white} />
            )}
          </TouchableOpacity>
          
          {/* Answer Buttons */}
          <TouchableOpacity
            style={[styles.answerButton, styles.wrongButton]}
            onPress={() => handleAnswer(false)}
          >
            <Ionicons name="close" size={28} color={COLORS.white} />
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.answerButton, styles.correctButton]}
            onPress={() => handleAnswer(true)}
          >
            <Ionicons name="checkmark" size={28} color={COLORS.white} />
          </TouchableOpacity>
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
  scrollContent: {
    padding: SPACING.md,
    paddingBottom: SPACING.xl,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  loadingText: {
    fontSize: 16,
    color: COLORS.gray500,
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
    borderRadius: 4,
  },
  progressText: {
    textAlign: 'center',
    marginTop: SPACING.sm,
    fontSize: 14,
    color: COLORS.gray500,
  },
  cardContainer: {
    height: 320,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  card: {
    position: 'absolute',
    width: '100%',
    height: 300,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: SPACING.xl,
    justifyContent: 'center',
    alignItems: 'center',
    backfaceVisibility: 'hidden',
    borderTopWidth: 6,
    overflow: 'visible',
    ...SHADOWS.lg,
  },
  cardFront: {},
  cardBack: {},
  cardInstruction: {
    position: 'absolute',
    top: SPACING.md,
    fontSize: 12,
    color: COLORS.gray400,
  },
  cardWord: {
    fontSize: 36,
    fontWeight: '700',
    color: COLORS.gray900,
    textAlign: 'center',
  },
  cardPronunciation: {
    fontSize: 16,
    color: COLORS.gray500,
    fontStyle: 'italic',
    marginTop: SPACING.sm,
  },
  cardTranslation: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.primary,
    textAlign: 'center',
  },
  cardExample: {
    fontSize: 14,
    color: COLORS.gray500,
    fontStyle: 'italic',
    marginTop: SPACING.md,
    textAlign: 'center',
  },
  answerContainer: {
    flexDirection: 'row',
    gap: SPACING.md,
    marginTop: SPACING.lg,
  },
  controlsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: SPACING.md,
    marginTop: SPACING.lg,
    paddingHorizontal: SPACING.md,
  },
  answerButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: SPACING.sm,
    paddingVertical: SPACING.lg,
    borderRadius: 16,
  },
  wrongButton: {
    backgroundColor: COLORS.error,
  },
  correctButton: {
    backgroundColor: COLORS.success,
  },
  answerButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.white,
  },
  resultsContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.lg,
  },
  resultsIcon: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: COLORS.gray100,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  resultsTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.md,
  },
  resultsScore: {
    fontSize: 48,
    fontWeight: '800',
    color: COLORS.primary,
  },
  resultsPercentage: {
    fontSize: 18,
    color: COLORS.gray500,
    marginBottom: SPACING.xl,
  },
  resultsButtons: {
    flexDirection: 'row',
    gap: SPACING.md,
    width: '100%',
  },
  resultButton: {
    flex: 1,
  },
  audioButton: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.md,
  },
  audioButtonPlaying: {
    backgroundColor: COLORS.secondary,
  },
  audioHint: {
    marginTop: SPACING.xs,
    fontSize: 12,
    color: COLORS.gray400,
  },
  audioContainer: {
    alignItems: 'center',
    paddingVertical: SPACING.lg,
    backgroundColor: COLORS.gray100,
    borderRadius: 12,
    marginHorizontal: SPACING.md,
  },
});

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, LANGUAGES, LEVELS, SHADOWS } from '../../src/constants/theme';
import { flashcardsAPI } from '../../src/api/client';
import { Button } from '../../src/components/Button';

interface Flashcard {
  id: string;
  language: string;
  level: string;
  word: string;
  translation: string;
  example: string;
  pronunciation: string;
}

export default function FlashcardsScreen() {
  const router = useRouter();
  const [selectedLanguage, setSelectedLanguage] = useState<string>('spanish');
  const [selectedLevel, setSelectedLevel] = useState<string>('A1');
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchFlashcards = async () => {
    try {
      const response = await flashcardsAPI.getAll(selectedLanguage, selectedLevel, 50);
      setFlashcards(response.data);
    } catch (error) {
      console.log('Error fetching flashcards:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFlashcards();
  }, [selectedLanguage, selectedLevel]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchFlashcards();
    setRefreshing(false);
  };

  const startSession = () => {
    if (flashcards.length > 0) {
      router.push({
        pathname: '/flashcard-session',
        params: { language: selectedLanguage, level: selectedLevel },
      });
    }
  };

  const selectedLangData = LANGUAGES.find((l) => l.id === selectedLanguage);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Language Selection */}
        <Text style={styles.filterLabel}>Selecciona el Idioma</Text>
        <View style={styles.languageGrid}>
          {LANGUAGES.map((lang) => (
            <TouchableOpacity
              key={lang.id}
              style={[
                styles.languageCard,
                selectedLanguage === lang.id && styles.languageCardActive,
                selectedLanguage === lang.id && { borderColor: lang.color },
              ]}
              onPress={() => setSelectedLanguage(lang.id)}
            >
              <Text style={styles.languageFlag}>{lang.flag}</Text>
              <Text
                style={[
                  styles.languageName,
                  selectedLanguage === lang.id && { color: lang.color },
                ]}
              >
                {lang.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Level Selection */}
        <Text style={styles.filterLabel}>Selecciona el Nivel</Text>
        <View style={styles.levelGrid}>
          {LEVELS.map((level) => (
            <TouchableOpacity
              key={level.id}
              style={[
                styles.levelCard,
                selectedLevel === level.id && styles.levelCardActive,
                selectedLevel === level.id && { backgroundColor: level.color },
              ]}
              onPress={() => setSelectedLevel(level.id)}
            >
              <Text
                style={[
                  styles.levelText,
                  selectedLevel === level.id && styles.levelTextActive,
                ]}
              >
                {level.id}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Summary Card */}
        <View style={[styles.summaryCard, { borderLeftColor: selectedLangData?.color }]}>
          <View style={styles.summaryHeader}>
            <Text style={styles.summaryFlag}>{selectedLangData?.flag}</Text>
            <View>
              <Text style={styles.summaryTitle}>{selectedLangData?.name}</Text>
              <Text style={styles.summaryLevel}>Nivel {selectedLevel}</Text>
            </View>
          </View>
          <View style={styles.summaryStats}>
            <View style={styles.summaryStatItem}>
              <Ionicons name="flash" size={20} color={COLORS.primary} />
              <Text style={styles.summaryStatValue}>{flashcards.length}</Text>
              <Text style={styles.summaryStatLabel}>Tarjetas</Text>
            </View>
          </View>
        </View>

        {/* Start Button */}
        <Button
          title={flashcards.length > 0 ? 'Comenzar Sesión' : 'Sin tarjetas disponibles'}
          onPress={startSession}
          disabled={flashcards.length === 0}
          size="lg"
          style={styles.startButton}
        />

        {/* Preview Cards */}
        {flashcards.length > 0 && (
          <>
            <Text style={styles.previewTitle}>Vista Previa</Text>
            {flashcards.slice(0, 3).map((card) => (
              <View key={card.id} style={styles.previewCard}>
                <Text style={styles.previewWord}>{card.word}</Text>
                <Text style={styles.previewTranslation}>{card.translation}</Text>
                {card.pronunciation && (
                  <Text style={styles.previewPronunciation}>{card.pronunciation}</Text>
                )}
              </View>
            ))}
            {flashcards.length > 3 && (
              <Text style={styles.moreText}>+{flashcards.length - 3} más...</Text>
            )}
          </>
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
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray700,
    marginBottom: SPACING.sm,
  },
  languageGrid: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  languageCard: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.gray200,
  },
  languageCardActive: {
    borderWidth: 2,
  },
  languageFlag: {
    fontSize: 32,
    marginBottom: SPACING.xs,
  },
  languageName: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.gray600,
  },
  levelGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  levelCard: {
    width: '30%',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    paddingVertical: SPACING.md,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: COLORS.gray200,
  },
  levelCardActive: {
    borderColor: 'transparent',
  },
  levelText: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.gray600,
  },
  levelTextActive: {
    color: COLORS.white,
  },
  summaryCard: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderLeftWidth: 4,
    marginBottom: SPACING.md,
    ...SHADOWS.md,
  },
  summaryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  summaryFlag: {
    fontSize: 40,
    marginRight: SPACING.md,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  summaryLevel: {
    fontSize: 14,
    color: COLORS.gray500,
  },
  summaryStats: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  summaryStatItem: {
    alignItems: 'center',
  },
  summaryStatValue: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  summaryStatLabel: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  startButton: {
    marginBottom: SPACING.lg,
  },
  previewTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray700,
    marginBottom: SPACING.sm,
  },
  previewCard: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  previewWord: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  previewTranslation: {
    fontSize: 14,
    color: COLORS.gray600,
  },
  previewPronunciation: {
    fontSize: 12,
    color: COLORS.gray400,
    fontStyle: 'italic',
    marginTop: SPACING.xs,
  },
  moreText: {
    fontSize: 14,
    color: COLORS.gray400,
    textAlign: 'center',
    marginTop: SPACING.sm,
  },
});

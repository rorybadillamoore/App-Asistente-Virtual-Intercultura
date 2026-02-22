import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, LANGUAGES, LEVELS, SHADOWS } from '../../src/constants/theme';
import { Button } from '../../src/components/Button';
import { Input } from '../../src/components/Input';

const EXERCISE_TYPES = [
  { id: 'grammar', name: 'Gramática', icon: 'book-outline' as const, color: COLORS.primary },
  { id: 'vocabulary', name: 'Vocabulario', icon: 'text-outline' as const, color: COLORS.secondary },
  { id: 'reading', name: 'Lectura', icon: 'reader-outline' as const, color: COLORS.info },
  { id: 'writing', name: 'Escritura', icon: 'create-outline' as const, color: COLORS.warning },
];

export default function AIToolsScreen() {
  const router = useRouter();
  const [selectedLanguage, setSelectedLanguage] = useState<string>('spanish');
  const [selectedLevel, setSelectedLevel] = useState<string>('A1');
  const [selectedType, setSelectedType] = useState<string>('grammar');
  const [topic, setTopic] = useState('');

  const handleGenerateExercise = () => {
    router.push({
      pathname: '/ai-exercise',
      params: {
        language: selectedLanguage,
        level: selectedLevel,
        exercise_type: selectedType,
        topic: topic || 'general',
      },
    });
  };

  const selectedLangData = LANGUAGES.find((l) => l.id === selectedLanguage);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.aiIconContainer}>
            <Ionicons name="sparkles" size={32} color={COLORS.white} />
          </View>
          <Text style={styles.headerTitle}>Ejercicios con IA</Text>
          <Text style={styles.headerSubtitle}>
            Genera ejercicios personalizados con inteligencia artificial
          </Text>
        </View>

        {/* Language Selection */}
        <Text style={styles.filterLabel}>Idioma</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
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

        {/* Level Selection */}
        <Text style={styles.filterLabel}>Nivel</Text>
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

        {/* Exercise Type Selection */}
        <Text style={styles.filterLabel}>Tipo de Ejercicio</Text>
        <View style={styles.typeGrid}>
          {EXERCISE_TYPES.map((type) => (
            <TouchableOpacity
              key={type.id}
              style={[
                styles.typeCard,
                selectedType === type.id && styles.typeCardActive,
                selectedType === type.id && { borderColor: type.color },
              ]}
              onPress={() => setSelectedType(type.id)}
            >
              <View
                style={[
                  styles.typeIconContainer,
                  selectedType === type.id && { backgroundColor: type.color },
                ]}
              >
                <Ionicons
                  name={type.icon}
                  size={24}
                  color={selectedType === type.id ? COLORS.white : type.color}
                />
              </View>
              <Text
                style={[
                  styles.typeName,
                  selectedType === type.id && { color: type.color },
                ]}
              >
                {type.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Topic Input */}
        <Input
          label="Tema (opcional)"
          placeholder="Ej: verbos irregulares, familia, viajes..."
          value={topic}
          onChangeText={setTopic}
          leftIcon="bulb-outline"
        />

        {/* Generate Button */}
        <Button
          title="Generar Ejercicio"
          onPress={handleGenerateExercise}
          size="lg"
          style={styles.generateButton}
          icon={<Ionicons name="sparkles" size={20} color={COLORS.white} />}
        />

        {/* Info Card */}
        <View style={styles.infoCard}>
          <Ionicons name="information-circle" size={24} color={COLORS.info} />
          <View style={styles.infoContent}>
            <Text style={styles.infoTitle}>Metodología Cambridge</Text>
            <Text style={styles.infoText}>
              Nuestros ejercicios siguen los estándares del Marco Común Europeo de Referencia para las Lenguas (MCER).
            </Text>
          </View>
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
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  aiIconContainer: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.xs,
  },
  headerSubtitle: {
    fontSize: 14,
    color: COLORS.gray500,
    textAlign: 'center',
  },
  filterLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray700,
    marginBottom: SPACING.sm,
  },
  filterScroll: {
    marginBottom: SPACING.lg,
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
    borderColor: 'transparent',
  },
  filterChipFlag: {
    fontSize: 18,
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
  typeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  typeCard: {
    width: '47%',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.gray200,
  },
  typeCardActive: {
    borderWidth: 2,
  },
  typeIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.gray100,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  typeName: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray600,
  },
  generateButton: {
    marginTop: SPACING.md,
    marginBottom: SPACING.lg,
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.info + '15',
    padding: SPACING.md,
    borderRadius: 12,
    gap: SPACING.sm,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.info,
    marginBottom: SPACING.xs,
  },
  infoText: {
    fontSize: 12,
    color: COLORS.gray600,
    lineHeight: 18,
  },
});

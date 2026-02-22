import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Button } from '../src/components/Button';
import { COLORS, SPACING } from '../src/constants/theme';
import { useAuthStore } from '../src/store/authStore';
import { seedData } from '../src/api/client';

export default function WelcomeScreen() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      router.replace('/(tabs)');
    }
    // Seed data on first load
    seedData().catch(() => {});
  }, [isAuthenticated]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <View style={styles.iconCircle}>
            <Ionicons name="language" size={60} color={COLORS.white} />
          </View>
          <Text style={styles.title}>Polyglot Academy</Text>
          <Text style={styles.subtitle}>Aprende Español, Inglés y Portugués</Text>
        </View>

        <View style={styles.featuresContainer}>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <Ionicons name="book" size={28} color={COLORS.spanish} />
              <Text style={styles.featureText}>Lecciones</Text>
            </View>
            <View style={styles.feature}>
              <Ionicons name="flash" size={28} color={COLORS.english} />
              <Text style={styles.featureText}>Flashcards</Text>
            </View>
          </View>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <Ionicons name="checkmark-circle" size={28} color={COLORS.portuguese} />
              <Text style={styles.featureText}>Quizzes</Text>
            </View>
            <View style={styles.feature}>
              <Ionicons name="sparkles" size={28} color={COLORS.primary} />
              <Text style={styles.featureText}>IA Asistente</Text>
            </View>
          </View>
        </View>

        <View style={styles.levelsContainer}>
          <Text style={styles.levelsTitle}>Niveles A1 - C2</Text>
          <Text style={styles.levelsSubtitle}>Metodología Cambridge</Text>
        </View>

        <View style={styles.buttonContainer}>
          <Button
            title="Iniciar Sesión"
            onPress={() => router.push('/login')}
            variant="primary"
            size="lg"
            style={styles.button}
          />
          <Button
            title="Crear Cuenta"
            onPress={() => router.push('/register')}
            variant="outline"
            size="lg"
            style={styles.button}
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    padding: SPACING.lg,
    justifyContent: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  iconCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.gray900,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.gray500,
    textAlign: 'center',
  },
  featuresContainer: {
    marginBottom: SPACING.xl,
  },
  featureRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: SPACING.xl,
    marginBottom: SPACING.md,
  },
  feature: {
    alignItems: 'center',
    width: 100,
  },
  featureText: {
    fontSize: 14,
    color: COLORS.gray600,
    marginTop: SPACING.xs,
  },
  levelsContainer: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
  },
  levelsTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  levelsSubtitle: {
    fontSize: 14,
    color: COLORS.gray500,
  },
  buttonContainer: {
    gap: SPACING.md,
  },
  button: {
    width: '100%',
  },
});

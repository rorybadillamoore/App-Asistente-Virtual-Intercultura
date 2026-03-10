import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Button } from '../src/components/Button';
import { COLORS, SPACING, APP_NAME, APP_TAGLINE } from '../src/constants/theme';
import { useAuthStore } from '../src/store/authStore';
import { seedData } from '../src/api/client';

const Logo = require('../assets/images/logo.png');

export default function WelcomeScreen() {
  const router = useRouter();
  const { isAuthenticated, _hasHydrated } = useAuthStore();

  useEffect(() => {
    if (_hasHydrated && isAuthenticated) {
      router.replace('/(tabs)');
    }
    seedData().catch(() => {});
  }, [isAuthenticated, _hasHydrated]);

  // Show loading while hydrating
  if (!_hasHydrated) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <Image source={Logo} style={styles.logo} resizeMode="contain" />
          <Text style={styles.title}>{APP_NAME}</Text>
          <Text style={styles.tagline}>{APP_TAGLINE}</Text>
        </View>

        <View style={styles.featuresContainer}>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <View style={[styles.featureIcon, { backgroundColor: COLORS.spanish + '20' }]}>
                <Ionicons name="book" size={24} color={COLORS.spanish} />
              </View>
              <Text style={styles.featureText}>Lecciones</Text>
            </View>
            <View style={styles.feature}>
              <View style={[styles.featureIcon, { backgroundColor: COLORS.english + '20' }]}>
                <Ionicons name="flash" size={24} color={COLORS.english} />
              </View>
              <Text style={styles.featureText}>Flashcards</Text>
            </View>
          </View>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <View style={[styles.featureIcon, { backgroundColor: COLORS.portuguese + '20' }]}>
                <Ionicons name="checkmark-circle" size={24} color={COLORS.portuguese} />
              </View>
              <Text style={styles.featureText}>Quizzes</Text>
            </View>
            <View style={styles.feature}>
              <View style={[styles.featureIcon, { backgroundColor: COLORS.primaryLight + '20' }]}>
                <Ionicons name="sparkles" size={24} color={COLORS.primary} />
              </View>
              <Text style={styles.featureText}>IA Asistente</Text>
            </View>
          </View>
        </View>

        <View style={styles.levelsContainer}>
          <Text style={styles.levelsTitle}>Niveles A1 - C2</Text>
          <Text style={styles.levelsSubtitle}>Metodología Cambridge</Text>
          <Text style={styles.established}>Est. 1993 • Pura Vida</Text>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
  logo: {
    width: 180,
    height: 180,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: 36,
    fontWeight: '800',
    color: COLORS.primary,
    marginBottom: SPACING.xs,
  },
  tagline: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.primaryLight,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: 14,
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
  featureIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  featureText: {
    fontSize: 14,
    color: COLORS.gray600,
  },
  levelsContainer: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary,
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
  established: {
    fontSize: 12,
    color: COLORS.primaryLight,
    fontWeight: '600',
    marginTop: SPACING.xs,
  },
  buttonContainer: {
    gap: SPACING.md,
  },
  button: {
    width: '100%',
  },
});

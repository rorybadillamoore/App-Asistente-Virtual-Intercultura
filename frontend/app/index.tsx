import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator } from 'react-native';
import { Redirect, useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Button } from '../src/components/Button';
import { COLORS, SPACING, APP_NAME, APP_TAGLINE } from '../src/constants/theme';
import { useAuthStore } from '../src/store/authStore';
import { seedData } from '../src/api/client';

const Logo = require('../assets/images/logo.png');

export default function WelcomeScreen() {
  const router = useRouter();
  const { isAuthenticated, isLoading, initializeAuth } = useAuthStore();

  useEffect(() => {
    initializeAuth();
    seedData().catch(() => {});
  }, []);

  // Show loading while checking auth
  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Image source={Logo} style={styles.loadingLogo} resizeMode="contain" />
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      </SafeAreaView>
    );
  }

  // Redirect to dashboard if authenticated
  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
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
              <View style={[styles.featureIcon, { backgroundColor: COLORS.warning + '20' }]}>
                <Ionicons name="checkmark-circle" size={24} color={COLORS.warning} />
              </View>
              <Text style={styles.featureText}>Quizzes</Text>
            </View>
            <View style={styles.feature}>
              <View style={[styles.featureIcon, { backgroundColor: COLORS.success + '20' }]}>
                <Ionicons name="sparkles" size={24} color={COLORS.success} />
              </View>
              <Text style={styles.featureText}>IA Asistente</Text>
            </View>
          </View>
        </View>

        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>Niveles A1 - C2</Text>
          <Text style={styles.infoText}>Metodología Cambridge</Text>
          <Text style={styles.infoSubtext}>Est. 1993 • Pura Vida</Text>
        </View>

        <View style={styles.buttonContainer}>
          <Button 
            title="Iniciar Sesión" 
            onPress={() => router.push('/login')}
            style={styles.primaryButton}
          />
          <Button 
            title="Crear Cuenta" 
            onPress={() => router.push('/register')}
            variant="outline"
            style={styles.secondaryButton}
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
  loadingLogo: {
    width: 100,
    height: 100,
    marginBottom: SPACING.lg,
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
    width: 120,
    height: 120,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.primary,
    textAlign: 'center',
  },
  tagline: {
    fontSize: 16,
    color: COLORS.secondary,
    textAlign: 'center',
    marginTop: SPACING.xs,
  },
  featuresContainer: {
    marginBottom: SPACING.lg,
  },
  featureRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: SPACING.xl,
    marginBottom: SPACING.md,
  },
  feature: {
    alignItems: 'center',
  },
  featureIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  featureText: {
    fontSize: 12,
    fontWeight: '500',
    color: COLORS.gray600,
  },
  infoCard: {
    backgroundColor: COLORS.white,
    padding: SPACING.lg,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: SPACING.xl,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
  },
  infoText: {
    fontSize: 14,
    color: COLORS.gray600,
    marginTop: SPACING.xs,
  },
  infoSubtext: {
    fontSize: 12,
    color: COLORS.secondary,
    marginTop: SPACING.xs,
  },
  buttonContainer: {
    gap: SPACING.md,
  },
  primaryButton: {
    width: '100%',
  },
  secondaryButton: {
    width: '100%',
  },
});

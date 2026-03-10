import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../src/store/authStore';
import { COLORS } from '../src/constants/theme';

function LoadingScreen() {
  return (
    <View style={styles.loading}>
      <ActivityIndicator size="large" color={COLORS.primary} />
    </View>
  );
}

export default function RootLayout() {
  const hasHydrated = useAuthStore((state) => state._hasHydrated);
  
  if (!hasHydrated) {
    return <LoadingScreen />;
  }

  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="login" />
        <Stack.Screen name="register" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="course/[id]" options={{ headerShown: true, title: 'Curso' }} />
        <Stack.Screen name="lesson/[id]" options={{ headerShown: true, title: 'Lección' }} />
        <Stack.Screen name="quiz/[id]" options={{ headerShown: true, title: 'Quiz' }} />
        <Stack.Screen name="flashcard-session" options={{ headerShown: true, title: 'Flashcards' }} />
        <Stack.Screen name="ai-exercise" options={{ headerShown: true, title: 'Ejercicio IA' }} />
      </Stack>
    </>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
});

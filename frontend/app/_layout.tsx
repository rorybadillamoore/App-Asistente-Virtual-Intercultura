import React, { useEffect } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { useAuthStore } from '../src/store/authStore';
import { COLORS } from '../src/constants/theme';

export default function RootLayout() {
  const { isAuthenticated } = useAuthStore();
  const [isLoading, setIsLoading] = React.useState(true);

  useEffect(() => {
    // Small delay to let zustand hydrate
    const timer = setTimeout(() => setIsLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <>
            <Stack.Screen name="index" />
            <Stack.Screen name="login" />
            <Stack.Screen name="register" />
          </>
        ) : (
          <>
            <Stack.Screen name="(tabs)" />
            <Stack.Screen name="course/[id]" options={{ headerShown: true, title: 'Curso' }} />
            <Stack.Screen name="lesson/[id]" options={{ headerShown: true, title: 'Lección' }} />
            <Stack.Screen name="quiz/[id]" options={{ headerShown: true, title: 'Quiz' }} />
            <Stack.Screen name="flashcard-session" options={{ headerShown: true, title: 'Flashcards' }} />
            <Stack.Screen name="ai-exercise" options={{ headerShown: true, title: 'Ejercicio IA' }} />
          </>
        )}
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

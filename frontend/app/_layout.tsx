import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
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

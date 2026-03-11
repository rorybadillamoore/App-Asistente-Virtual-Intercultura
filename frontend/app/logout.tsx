import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { COLORS, SPACING } from '../src/constants/theme';

export default function LogoutScreen() {
  useEffect(() => {
    // Clear localStorage and redirect
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      localStorage.removeItem('auth-storage');
      // Redirect to home after a brief moment
      const timer = setTimeout(() => {
        window.location.href = '/';
      }, 500);
      return () => clearTimeout(timer);
    }
  }, []);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={COLORS.primary} />
      <Text style={styles.text}>Cerrando sesión...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
  },
  text: {
    marginTop: SPACING.md,
    fontSize: 16,
    color: '#6B7280',
  },
});

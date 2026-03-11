import React from 'react';
import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { Link } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, APP_NAME } from '../../src/constants/theme';
import { useAuthStore } from '../../src/store/authStore';

export default function ProfileScreen() {
  const { user, clearAuth } = useAuthStore();

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Profile Header */}
        <View style={styles.profileHeader}>
          <View style={styles.avatarContainer}>
            <View style={styles.avatar}>
              <Text style={styles.avatarText}>
                {user?.name?.charAt(0).toUpperCase() || 'U'}
              </Text>
            </View>
            <View style={[styles.roleBadge, { backgroundColor: user?.role === 'teacher' ? COLORS.secondary : COLORS.primary }]}>
              <Ionicons name={user?.role === 'teacher' ? 'school' : 'person'} size={12} color={COLORS.white} />
            </View>
          </View>
          <Text style={styles.userName}>{user?.name || 'Usuario'}</Text>
          <Text style={styles.userEmail}>{user?.email}</Text>
          <View style={styles.roleContainer}>
            <Text style={styles.roleText}>{user?.role === 'teacher' ? 'Profesor' : 'Estudiante'}</Text>
          </View>
        </View>

        {/* Stats Card */}
        <View style={styles.statsCard}>
          <View style={styles.statItem}>
            <Ionicons name="book" size={24} color={COLORS.spanish} />
            <Text style={styles.statValue}>4</Text>
            <Text style={styles.statLabel}>Idiomas</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Ionicons name="school" size={24} color={COLORS.english} />
            <Text style={styles.statValue}>6</Text>
            <Text style={styles.statLabel}>Niveles</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Ionicons name="sparkles" size={24} color={COLORS.portuguese} />
            <Text style={styles.statValue}>IA</Text>
            <Text style={styles.statLabel}>Asistente</Text>
          </View>
        </View>

        {/* Menu Items */}
        <View style={styles.menuContainer}>
          <Link href="/(tabs)" asChild>
            <Pressable style={styles.menuItem}>
              <View style={styles.menuIconContainer}>
                <Ionicons name="stats-chart-outline" size={22} color={COLORS.primary} />
              </View>
              <View style={styles.menuContent}>
                <Text style={styles.menuTitle}>Mi Progreso</Text>
                <Text style={styles.menuSubtitle}>Ver estadísticas de aprendizaje</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </Pressable>
          </Link>

          <Link href="/(tabs)/courses" asChild>
            <Pressable style={styles.menuItem}>
              <View style={styles.menuIconContainer}>
                <Ionicons name="book-outline" size={22} color={COLORS.primary} />
              </View>
              <View style={styles.menuContent}>
                <Text style={styles.menuTitle}>Mis Cursos</Text>
                <Text style={styles.menuSubtitle}>Ver todos los cursos</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </Pressable>
          </Link>

          <Link href="/(tabs)/quizzes" asChild>
            <Pressable style={styles.menuItem}>
              <View style={styles.menuIconContainer}>
                <Ionicons name="help-circle-outline" size={22} color={COLORS.primary} />
              </View>
              <View style={styles.menuContent}>
                <Text style={styles.menuTitle}>Mis Quizzes</Text>
                <Text style={styles.menuSubtitle}>Practicar con quizzes</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </Pressable>
          </Link>
        </View>

        {/* Logout Button */}
        <Pressable style={styles.logoutButton} onPress={clearAuth}>
          <Ionicons name="log-out-outline" size={20} color={COLORS.error} />
          <Text style={styles.logoutButtonText}>Cerrar Sesión</Text>
        </Pressable>

        {/* Footer */}
        <Text style={styles.footerText}>{APP_NAME} v1.0{"\n"}© 2025 Metodología Cambridge</Text>
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
    paddingBottom: 100,
  },
  profileHeader: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  avatarContainer: {
    marginBottom: SPACING.md,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 40,
    fontWeight: '700',
    color: COLORS.white,
  },
  roleBadge: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: COLORS.background,
  },
  userName: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.xs,
  },
  userEmail: {
    fontSize: 14,
    color: COLORS.gray500,
    marginBottom: SPACING.sm,
  },
  roleContainer: {
    backgroundColor: COLORS.primaryLight + '20',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: 20,
  },
  roleText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.primary,
  },
  statsCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statDivider: {
    width: 1,
    backgroundColor: COLORS.gray200,
  },
  statValue: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.gray900,
    marginTop: SPACING.xs,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  menuContainer: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    marginBottom: SPACING.lg,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  menuIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.primaryLight + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  menuContent: {
    flex: 1,
  },
  menuTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray900,
  },
  menuSubtitle: {
    fontSize: 12,
    color: COLORS.gray500,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    marginBottom: SPACING.lg,
    gap: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.error,
  },
  logoutButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.error,
  },
  footerText: {
    textAlign: 'center',
    fontSize: 12,
    color: COLORS.gray400,
    lineHeight: 18,
  },
});

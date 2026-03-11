import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../../src/constants/theme';
import { useAuthStore } from '../../src/store/authStore';
import { Button } from '../../src/components/Button';

export default function ProfileScreen() {
  const router = useRouter();
  const { user, clearAuth } = useAuthStore();

  const handleLogout = () => {
    // For web: navigate using the full absolute URL to bypass expo-router
    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem('auth-storage');
      } catch (e) {}
      // Use full absolute URL to ensure browser treats this as a fresh page load
      const origin = window.location.origin;
      window.location.assign(origin);
      return;
    }
    
    // For native apps, use the traditional approach with Alert
    Alert.alert(
      'Cerrar Sesión',
      '¿Estás seguro de que quieres cerrar sesión?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Cerrar Sesión',
          style: 'destructive',
          onPress: () => {
            clearAuth();
            router.replace('/');
          },
        },
      ]
    );
  };

  const menuItems = [
    {
      icon: 'stats-chart-outline' as const,
      title: 'Mi Progreso',
      subtitle: 'Ver estadísticas de aprendizaje',
      onPress: () => router.push('/(tabs)'),
    },
    {
      icon: 'settings-outline' as const,
      title: 'Configuración',
      subtitle: 'Preferencias de la app',
      onPress: () => {},
    },
    {
      icon: 'help-circle-outline' as const,
      title: 'Ayuda',
      subtitle: 'Preguntas frecuentes',
      onPress: () => {},
    },
    {
      icon: 'information-circle-outline' as const,
      title: 'Acerca de',
      subtitle: 'Polyglot Academy v1.0',
      onPress: () => {},
    },
  ];

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
            <View
              style={[
                styles.roleBadge,
                { backgroundColor: user?.role === 'teacher' ? COLORS.secondary : COLORS.primary },
              ]}
            >
              <Ionicons
                name={user?.role === 'teacher' ? 'school' : 'person'}
                size={12}
                color={COLORS.white}
              />
            </View>
          </View>
          <Text style={styles.userName}>{user?.name || 'Usuario'}</Text>
          <Text style={styles.userEmail}>{user?.email}</Text>
          <View style={styles.roleContainer}>
            <Text style={styles.roleText}>
              {user?.role === 'teacher' ? 'Profesor' : 'Estudiante'}
            </Text>
          </View>
        </View>

        {/* Stats Card */}
        <View style={styles.statsCard}>
          <View style={styles.statItem}>
            <Ionicons name="book" size={24} color={COLORS.spanish} />
            <Text style={styles.statValue}>3</Text>
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
          {menuItems.map((item, index) => (
            <TouchableOpacity
              key={index}
              style={styles.menuItem}
              onPress={item.onPress}
              activeOpacity={0.7}
            >
              <View style={styles.menuIconContainer}>
                <Ionicons name={item.icon} size={22} color={COLORS.primary} />
              </View>
              <View style={styles.menuContent}>
                <Text style={styles.menuTitle}>{item.title}</Text>
                <Text style={styles.menuSubtitle}>{item.subtitle}</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </TouchableOpacity>
          ))}
        </View>

        {/* Logout Button */}
        <Button
          title="Cerrar Sesión"
          onPress={handleLogout}
          variant="outline"
          style={styles.logoutButton}
          icon={<Ionicons name="log-out-outline" size={20} color={COLORS.primary} />}
        />

        {/* Footer */}
        <Text style={styles.footerText}>
          Polyglot Academy © 2025{"\n"}Metodología Cambridge
        </Text>
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
  profileHeader: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  avatarContainer: {
    position: 'relative',
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
    ...SHADOWS.md,
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
    ...SHADOWS.sm,
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
    marginBottom: SPACING.lg,
  },
  footerText: {
    textAlign: 'center',
    fontSize: 12,
    color: COLORS.gray400,
    lineHeight: 18,
  },
});

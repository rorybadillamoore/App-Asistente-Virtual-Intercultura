import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Switch } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../src/constants/theme';

export default function SettingsScreen() {
  const router = useRouter();
  const [notifications, setNotifications] = useState(true);
  const [soundEffects, setSoundEffects] = useState(true);
  const [autoPlay, setAutoPlay] = useState(false);

  const sections = [
    {
      title: 'Aprendizaje',
      items: [
        {
          icon: 'notifications-outline' as const,
          label: 'Notificaciones de práctica',
          subtitle: 'Recordatorios diarios de estudio',
          toggle: true,
          value: notifications,
          onToggle: setNotifications,
        },
        {
          icon: 'volume-high-outline' as const,
          label: 'Efectos de sonido',
          subtitle: 'Sonidos al responder correctamente',
          toggle: true,
          value: soundEffects,
          onToggle: setSoundEffects,
        },
        {
          icon: 'play-circle-outline' as const,
          label: 'Reproducción automática',
          subtitle: 'Reproducir audio al ver flashcards',
          toggle: true,
          value: autoPlay,
          onToggle: setAutoPlay,
        },
      ],
    },
    {
      title: 'Cuenta',
      items: [
        {
          icon: 'person-outline' as const,
          label: 'Editar perfil',
          subtitle: 'Nombre y foto de perfil',
          toggle: false,
          chevron: true,
        },
        {
          icon: 'lock-closed-outline' as const,
          label: 'Cambiar contraseña',
          subtitle: 'Actualiza tu contraseña',
          toggle: false,
          chevron: true,
        },
      ],
    },
    {
      title: 'Privacidad',
      items: [
        {
          icon: 'shield-checkmark-outline' as const,
          label: 'Política de privacidad',
          subtitle: 'Cómo usamos tus datos',
          toggle: false,
          chevron: true,
        },
        {
          icon: 'document-text-outline' as const,
          label: 'Términos de servicio',
          subtitle: 'Condiciones de uso',
          toggle: false,
          chevron: true,
        },
      ],
    },
  ];

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn} data-testid="settings-back-btn">
          <Ionicons name="arrow-back" size={24} color={COLORS.gray900} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Configuración</Text>
        <View style={styles.backBtn} />
      </View>

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        {sections.map((section, si) => (
          <View key={si} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            <View style={styles.sectionCard}>
              {section.items.map((item, ii) => (
                <View
                  key={ii}
                  style={[styles.settingRow, ii < section.items.length - 1 && styles.rowBorder]}
                >
                  <View style={styles.settingIcon}>
                    <Ionicons name={item.icon} size={20} color={COLORS.primary} />
                  </View>
                  <View style={styles.settingInfo}>
                    <Text style={styles.settingLabel}>{item.label}</Text>
                    <Text style={styles.settingSubtitle}>{item.subtitle}</Text>
                  </View>
                  {item.toggle ? (
                    <Switch
                      value={item.value as boolean}
                      onValueChange={item.onToggle as (val: boolean) => void}
                      trackColor={{ false: COLORS.gray200, true: COLORS.primary }}
                      thumbColor={COLORS.white}
                    />
                  ) : item.chevron ? (
                    <Ionicons name="chevron-forward" size={18} color={COLORS.gray400} />
                  ) : null}
                </View>
              ))}
            </View>
          </View>
        ))}

        <View style={styles.versionInfo}>
          <Text style={styles.versionText}>Intercultura Costa Rica v1.0.0</Text>
          <Text style={styles.versionText}>Metodología Cambridge</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  backBtn: { width: 40, height: 40, justifyContent: 'center', alignItems: 'center' },
  headerTitle: { fontSize: 18, fontWeight: '700', color: COLORS.gray900 },
  content: { padding: SPACING.md },
  section: { marginBottom: SPACING.lg },
  sectionTitle: { fontSize: 13, fontWeight: '600', color: COLORS.gray500, textTransform: 'uppercase', marginBottom: SPACING.xs, paddingHorizontal: SPACING.xs },
  sectionCard: { backgroundColor: COLORS.white, borderRadius: 12, ...SHADOWS.sm },
  settingRow: { flexDirection: 'row', alignItems: 'center', padding: SPACING.md },
  rowBorder: { borderBottomWidth: 1, borderBottomColor: COLORS.gray100 },
  settingIcon: {
    width: 36, height: 36, borderRadius: 18,
    backgroundColor: COLORS.primary + '15',
    justifyContent: 'center', alignItems: 'center',
    marginRight: SPACING.md,
  },
  settingInfo: { flex: 1 },
  settingLabel: { fontSize: 15, fontWeight: '500', color: COLORS.gray900 },
  settingSubtitle: { fontSize: 12, color: COLORS.gray500, marginTop: 2 },
  versionInfo: { alignItems: 'center', paddingVertical: SPACING.lg },
  versionText: { fontSize: 12, color: COLORS.gray400, lineHeight: 20 },
});

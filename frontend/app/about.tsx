import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../src/constants/theme';

export default function AboutScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn} data-testid="about-back-btn">
          <Ionicons name="arrow-back" size={24} color={COLORS.gray900} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Acerca de</Text>
        <View style={styles.backBtn} />
      </View>

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        {/* Logo & Brand */}
        <View style={styles.brandSection}>
          <Image
            source={require('../assets/images/logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />
          <Text style={styles.appName}>Intercultura</Text>
          <Text style={styles.appTagline}>Asistente Virtual de Idiomas</Text>
          <View style={styles.versionBadge}>
            <Text style={styles.versionText}>Versión 1.0.0</Text>
          </View>
        </View>

        {/* Description */}
        <View style={styles.descCard}>
          <Text style={styles.descText}>
            Intercultura Costa Rica es una plataforma de aprendizaje de idiomas que combina metodología
            Cambridge con tecnología de inteligencia artificial para ofrecerte una experiencia de aprendizaje
            personalizada y efectiva.
          </Text>
        </View>

        {/* Features */}
        <Text style={styles.sectionTitle}>Características</Text>
        {[
          { icon: 'language-outline', label: '5 idiomas', desc: 'Español, Inglés, Portugués, Alemán y Francés' },
          { icon: 'layers-outline', label: '6 niveles Cambridge', desc: 'Desde A1 (principiante) hasta C2 (maestría)' },
          { icon: 'flash-outline', label: 'Flashcards con audio', desc: 'Pronunciación nativa con tecnología ElevenLabs' },
          { icon: 'sparkles-outline', label: 'IA Generativa', desc: 'Ejercicios personalizados con GPT-4' },
          { icon: 'bar-chart-outline', label: 'Seguimiento de progreso', desc: 'Panel detallado de tu avance' },
          { icon: 'school-outline', label: 'Panel para profesores', desc: 'Herramientas para seguimiento estudiantil' },
        ].map((feat, i) => (
          <View key={i} style={styles.featCard}>
            <View style={styles.featIcon}>
              <Ionicons name={feat.icon as any} size={22} color={COLORS.primary} />
            </View>
            <View style={styles.featInfo}>
              <Text style={styles.featLabel}>{feat.label}</Text>
              <Text style={styles.featDesc}>{feat.desc}</Text>
            </View>
          </View>
        ))}

        {/* Company */}
        <Text style={styles.sectionTitle}>La Empresa</Text>
        <View style={styles.companyCard}>
          <Text style={styles.companyText}>
            Recently named one of the "7 Best Spanish Schools in the World", Intercultura Costa Rica has a variety of Spanish programs for all ages and learners.{'\n\n'}You can learn Spanish in Costa Rica with our internationally recognized Spanish programs, offered year-round at both city and beachfront campuses. Each Spanish course is designed for full immersion in real-life contexts and social interactions.
          </Text>
          <View style={styles.contactRow}>
            <Ionicons name="globe-outline" size={16} color={COLORS.primary} />
            <Text style={styles.contactLink}>www.interculturacostarica.com</Text>
          </View>
          <View style={styles.contactRow}>
            <Ionicons name="mail-outline" size={16} color={COLORS.primary} />
            <Text style={styles.contactLink}>info@interculturacostarica.com</Text>
          </View>
        </View>

        <Text style={styles.copyright}>
          © 2025 Intercultura Costa Rica{'\n'}Todos los derechos reservados
        </Text>
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
  brandSection: { alignItems: 'center', paddingVertical: SPACING.xl },
  logo: { width: 100, height: 100, marginBottom: SPACING.md },
  appName: { fontSize: 28, fontWeight: '800', color: COLORS.primary, marginBottom: SPACING.xs },
  appTagline: { fontSize: 14, color: COLORS.gray500, marginBottom: SPACING.md },
  versionBadge: {
    backgroundColor: COLORS.primary + '15',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: 20,
  },
  versionText: { fontSize: 12, color: COLORS.primary, fontWeight: '600' },
  descCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    ...SHADOWS.sm,
  },
  descText: { fontSize: 14, color: COLORS.gray700, lineHeight: 22 },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: COLORS.gray900, marginBottom: SPACING.sm },
  featCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  featIcon: {
    width: 44, height: 44, borderRadius: 22,
    backgroundColor: COLORS.primary + '15',
    justifyContent: 'center', alignItems: 'center',
    marginRight: SPACING.md,
  },
  featInfo: { flex: 1 },
  featLabel: { fontSize: 14, fontWeight: '700', color: COLORS.gray900 },
  featDesc: { fontSize: 12, color: COLORS.gray500, marginTop: 2 },
  companyCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    ...SHADOWS.sm,
  },
  companyText: { fontSize: 14, color: COLORS.gray700, lineHeight: 22, marginBottom: SPACING.md },
  contactRow: { flexDirection: 'row', alignItems: 'center', gap: SPACING.xs, marginBottom: SPACING.xs },
  contactLink: { fontSize: 14, color: COLORS.primary, fontWeight: '500' },
  copyright: { textAlign: 'center', fontSize: 12, color: COLORS.gray400, lineHeight: 18, marginBottom: SPACING.lg },
});

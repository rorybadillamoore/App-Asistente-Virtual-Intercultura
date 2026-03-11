import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../src/constants/theme';

const faqs = [
  {
    q: '¿Cómo funciona el sistema de niveles?',
    a: 'Usamos el Marco Común Europeo de Referencia (MCER): A1 (principiante), A2 (elemental), B1 (intermedio), B2 (intermedio alto), C1 (avanzado) y C2 (maestría).',
  },
  {
    q: '¿Cómo uso los flashcards?',
    a: 'En la sección "Flashcards", selecciona el idioma y nivel. Toca el botón de audio para escuchar la pronunciación. Marca si la conoces o no para seguir tu progreso.',
  },
  {
    q: '¿Cómo funcionan los quizzes de IA?',
    a: 'La sección "IA" genera ejercicios personalizados usando inteligencia artificial. Selecciona idioma, nivel y tipo de ejercicio (gramática, vocabulario, lectura o escritura).',
  },
  {
    q: '¿Puedo estudiar varios idiomas a la vez?',
    a: '¡Sí! Puedes cambiar de idioma en cualquier sección. Tu progreso se guarda por separado para cada idioma.',
  },
  {
    q: '¿Los profesores pueden ver mi progreso?',
    a: 'Sí, los profesores tienen acceso a un panel donde pueden ver el progreso de todos sus estudiantes.',
  },
  {
    q: '¿Cómo registro mi progreso en lecciones?',
    a: 'Al completar una lección, toca el botón "Marcar como completada". Tu progreso se guarda automáticamente.',
  },
];

export default function HelpScreen() {
  const router = useRouter();
  const [expanded, setExpanded] = useState<number | null>(null);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn} data-testid="help-back-btn">
          <Ionicons name="arrow-back" size={24} color={COLORS.gray900} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Ayuda</Text>
        <View style={styles.backBtn} />
      </View>

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        {/* Contact Card */}
        <View style={styles.contactCard}>
          <Ionicons name="mail-outline" size={32} color={COLORS.primary} />
          <View style={styles.contactInfo}>
            <Text style={styles.contactTitle}>Soporte Intercultura</Text>
            <Text style={styles.contactEmail}>info@intercultura.cr</Text>
            <Text style={styles.contactHours}>Lunes a Viernes: 8:00 am – 5:00 pm</Text>
          </View>
        </View>

        {/* FAQ */}
        <Text style={styles.sectionTitle}>Preguntas Frecuentes</Text>
        {faqs.map((faq, i) => (
          <TouchableOpacity
            key={i}
            style={styles.faqItem}
            onPress={() => setExpanded(expanded === i ? null : i)}
            data-testid={`faq-item-${i}`}
          >
            <View style={styles.faqQuestion}>
              <Text style={styles.faqText}>{faq.q}</Text>
              <Ionicons
                name={expanded === i ? 'chevron-up' : 'chevron-down'}
                size={18}
                color={COLORS.gray500}
              />
            </View>
            {expanded === i && (
              <Text style={styles.faqAnswer}>{faq.a}</Text>
            )}
          </TouchableOpacity>
        ))}

        {/* Quick Tips */}
        <Text style={styles.sectionTitle}>Consejos de Uso</Text>
        {[
          { icon: 'time-outline', tip: 'Estudia 15-20 minutos al día para mejores resultados.' },
          { icon: 'headset-outline', tip: 'Usa auriculares para practicar la pronunciación con los audios.' },
          { icon: 'repeat-outline', tip: 'Repasa los flashcards que marcaste incorrectamente.' },
          { icon: 'star-outline', tip: 'Completa los quizzes de IA para practicar de forma interactiva.' },
        ].map((tip, i) => (
          <View key={i} style={styles.tipCard}>
            <Ionicons name={tip.icon as any} size={20} color={COLORS.primary} style={styles.tipIcon} />
            <Text style={styles.tipText}>{tip.tip}</Text>
          </View>
        ))}
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
  contactCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary + '10',
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.primary + '30',
  },
  contactInfo: { marginLeft: SPACING.md },
  contactTitle: { fontSize: 16, fontWeight: '700', color: COLORS.gray900 },
  contactEmail: { fontSize: 14, color: COLORS.primary, fontWeight: '500', marginTop: 2 },
  contactHours: { fontSize: 12, color: COLORS.gray500, marginTop: 2 },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: COLORS.gray900, marginBottom: SPACING.sm, marginTop: SPACING.md },
  faqItem: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  faqQuestion: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  faqText: { flex: 1, fontSize: 14, fontWeight: '600', color: COLORS.gray900, marginRight: SPACING.sm },
  faqAnswer: { fontSize: 14, color: COLORS.gray600, marginTop: SPACING.sm, lineHeight: 20 },
  tipCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  tipIcon: { marginRight: SPACING.sm, marginTop: 2 },
  tipText: { flex: 1, fontSize: 14, color: COLORS.gray700, lineHeight: 20 },
});

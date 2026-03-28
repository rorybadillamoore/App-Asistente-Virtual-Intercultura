import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert, TextInput, Linking, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, SHADOWS } from '../../src/constants/theme';
import { useAuthStore } from '../../src/store/authStore';
import { progressAPI, authAPI } from '../../src/api/client';
import { Button } from '../../src/components/Button';

type ActiveSection = null | 'settings' | 'help' | 'about';

export default function ProfileScreen() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [activeSection, setActiveSection] = useState<ActiveSection>(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [changingPassword, setChangingPassword] = useState(false);
  const [passwordMsg, setPasswordMsg] = useState('');

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      const confirmed = window.confirm('¿Estas seguro de que quieres cerrar sesion?');
      if (confirmed) {
        try { localStorage.removeItem('auth-storage'); } catch (e) {}
        window.location.href = '/';
      }
    } else {
      Alert.alert('Cerrar Sesion', '¿Estas seguro?', [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Cerrar Sesion', style: 'destructive', onPress: async () => {
          const { clearAuth } = useAuthStore.getState();
          await clearAuth();
          router.replace('/');
        }},
      ]);
    }
  };

  const showAlert = (title: string, message: string) => {
    if (typeof window !== 'undefined') {
      window.alert(`${title}\n\n${message}`);
    } else {
      Alert.alert(title, message);
    }
  };

  const handleChangePassword = async () => {
    setPasswordMsg('');
    if (!currentPassword || !newPassword || !confirmPassword) {
      setPasswordMsg('Completa todos los campos');
      return;
    }
    if (newPassword.length < 6) {
      setPasswordMsg('La nueva contrasena debe tener al menos 6 caracteres');
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordMsg('Las contrasenas no coinciden');
      return;
    }
    setChangingPassword(true);
    try {
      await authAPI.changePassword({ current_password: currentPassword, new_password: newPassword });
      setPasswordMsg('Contrasena actualizada exitosamente');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Error al cambiar contrasena';
      setPasswordMsg(msg);
    } finally {
      setChangingPassword(false);
    }
  };

  const openLink = (url: string) => {
    if (typeof window !== 'undefined') {
      window.open(url, '_blank');
    } else {
      Linking.openURL(url);
    }
  };

  const toggleSection = (section: ActiveSection) => {
    setActiveSection(activeSection === section ? null : section);
    setPasswordMsg('');
  };

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
            <Text style={styles.statValue}>5</Text>
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
          {/* Mi Progreso */}
          <TouchableOpacity
            style={styles.menuItem}
            data-testid="profile-progress-btn"
            onPress={async () => {
              try {
                const response = await progressAPI.get();
                const p = response.data;
                const msg = `Lecciones completadas: ${p.lessons_completed || 0}\nFlashcards revisados: ${p.flashcards_reviewed || 0}\nQuizzes realizados: ${p.quizzes_taken || 0}\nPromedio: ${p.average_score?.toFixed(0) || 0}%\nCursos iniciados: ${p.courses_started || 0}`;
                showAlert('Mi Progreso', msg);
              } catch {
                showAlert('Mi Progreso', 'No se pudo cargar el progreso.');
              }
            }}
            activeOpacity={0.7}
          >
            <View style={styles.menuIconContainer}>
              <Ionicons name="stats-chart-outline" size={22} color={COLORS.primary} />
            </View>
            <View style={styles.menuContent}>
              <Text style={styles.menuTitle}>Mi Progreso</Text>
              <Text style={styles.menuSubtitle}>Ver estadisticas de aprendizaje</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
          </TouchableOpacity>

          {/* Configuracion */}
          <TouchableOpacity
            style={styles.menuItem}
            data-testid="profile-settings-btn"
            onPress={() => toggleSection('settings')}
            activeOpacity={0.7}
          >
            <View style={styles.menuIconContainer}>
              <Ionicons name="settings-outline" size={22} color={COLORS.primary} />
            </View>
            <View style={styles.menuContent}>
              <Text style={styles.menuTitle}>Configuracion</Text>
              <Text style={styles.menuSubtitle}>Cambiar contrasena</Text>
            </View>
            <Ionicons name={activeSection === 'settings' ? 'chevron-down' : 'chevron-forward'} size={20} color={COLORS.gray400} />
          </TouchableOpacity>

          {activeSection === 'settings' && (
            <View style={styles.expandedSection} data-testid="settings-section">
              <Text style={styles.sectionTitle}>Cambiar Contrasena</Text>
              <TextInput
                style={styles.input}
                placeholder="Contrasena actual"
                secureTextEntry
                value={currentPassword}
                onChangeText={setCurrentPassword}
                data-testid="current-password-input"
                placeholderTextColor={COLORS.gray400}
              />
              <TextInput
                style={styles.input}
                placeholder="Nueva contrasena (min. 6 caracteres)"
                secureTextEntry
                value={newPassword}
                onChangeText={setNewPassword}
                data-testid="new-password-input"
                placeholderTextColor={COLORS.gray400}
              />
              <TextInput
                style={styles.input}
                placeholder="Confirmar nueva contrasena"
                secureTextEntry
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                data-testid="confirm-password-input"
                placeholderTextColor={COLORS.gray400}
              />
              {passwordMsg ? (
                <Text style={[styles.passwordMsg, passwordMsg.includes('exitosamente') ? styles.successMsg : styles.errorMsg]}>
                  {passwordMsg}
                </Text>
              ) : null}
              <TouchableOpacity
                style={[styles.changePassBtn, changingPassword && styles.disabledBtn]}
                onPress={handleChangePassword}
                disabled={changingPassword}
                data-testid="change-password-btn"
              >
                <Text style={styles.changePassBtnText}>
                  {changingPassword ? 'Guardando...' : 'Actualizar Contrasena'}
                </Text>
              </TouchableOpacity>
            </View>
          )}

          {/* Ayuda */}
          <TouchableOpacity
            style={styles.menuItem}
            data-testid="profile-help-btn"
            onPress={() => toggleSection('help')}
            activeOpacity={0.7}
          >
            <View style={styles.menuIconContainer}>
              <Ionicons name="help-circle-outline" size={22} color={COLORS.primary} />
            </View>
            <View style={styles.menuContent}>
              <Text style={styles.menuTitle}>Ayuda</Text>
              <Text style={styles.menuSubtitle}>Contacto y soporte</Text>
            </View>
            <Ionicons name={activeSection === 'help' ? 'chevron-down' : 'chevron-forward'} size={20} color={COLORS.gray400} />
          </TouchableOpacity>

          {activeSection === 'help' && (
            <View style={styles.expandedSection} data-testid="help-section">
              <Text style={styles.sectionTitle}>Contacto - Intercultura Costa Rica</Text>

              <TouchableOpacity style={styles.contactRow} onPress={() => openLink('tel:+50626563000')}>
                <Ionicons name="call-outline" size={20} color={COLORS.primary} />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>Telefono</Text>
                  <Text style={styles.contactValue}>+(506) 2656-3000</Text>
                </View>
              </TouchableOpacity>

              <TouchableOpacity style={styles.contactRow} onPress={() => openLink('https://wa.me/50683303555')}>
                <Ionicons name="logo-whatsapp" size={20} color="#25D366" />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>WhatsApp</Text>
                  <Text style={styles.contactValue}>+(506) 8330-3555</Text>
                </View>
              </TouchableOpacity>

              <TouchableOpacity style={styles.contactRow} onPress={() => openLink('mailto:info@interculturacostarica.com')}>
                <Ionicons name="mail-outline" size={20} color={COLORS.primary} />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>Email</Text>
                  <Text style={styles.contactValue}>info@interculturacostarica.com</Text>
                </View>
              </TouchableOpacity>

              <TouchableOpacity style={styles.contactRow} onPress={() => openLink('https://interculturacostarica.com')}>
                <Ionicons name="globe-outline" size={20} color={COLORS.primary} />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>Sitio Web</Text>
                  <Text style={styles.contactValue}>interculturacostarica.com</Text>
                </View>
              </TouchableOpacity>

              <View style={styles.divider} />
              <Text style={styles.sectionTitle}>Sedes</Text>

              <View style={styles.contactRow}>
                <Ionicons name="location-outline" size={20} color={COLORS.primary} />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>Campus Heredia</Text>
                  <Text style={styles.contactValue}>Ciudad colonial historica, Heredia, Costa Rica</Text>
                </View>
              </View>

              <View style={styles.contactRow}>
                <Ionicons name="location-outline" size={20} color={COLORS.primary} />
                <View style={styles.contactInfo}>
                  <Text style={styles.contactLabel}>Campus Playa Samara</Text>
                  <Text style={styles.contactValue}>Frente a la playa, Samara, Guanacaste, Costa Rica</Text>
                </View>
              </View>

              <View style={styles.divider} />
              <Text style={styles.sectionTitle}>Preguntas Frecuentes</Text>

              <View style={styles.faqItem}>
                <Text style={styles.faqQuestion}>¿Como inicio una leccion?</Text>
                <Text style={styles.faqAnswer}>Ve a Cursos, selecciona tu idioma y nivel, y haz clic en cualquier leccion para comenzar.</Text>
              </View>
              <View style={styles.faqItem}>
                <Text style={styles.faqQuestion}>¿Como funcionan las flashcards?</Text>
                <Text style={styles.faqAnswer}>Selecciona un idioma y nivel en la seccion Flashcards. Toca la tarjeta para ver la traduccion y usa los botones para marcar si la sabias.</Text>
              </View>
              <View style={styles.faqItem}>
                <Text style={styles.faqQuestion}>¿Los ejercicios de IA usan creditos?</Text>
                <Text style={styles.faqAnswer}>Si, los ejercicios generados por IA consumen creditos. Usa las lecciones y flashcards para practicar sin costo adicional.</Text>
              </View>
            </View>
          )}

          {/* Acerca de */}
          <TouchableOpacity
            style={[styles.menuItem, { borderBottomWidth: 0 }]}
            data-testid="profile-about-btn"
            onPress={() => toggleSection('about')}
            activeOpacity={0.7}
          >
            <View style={styles.menuIconContainer}>
              <Ionicons name="information-circle-outline" size={22} color={COLORS.primary} />
            </View>
            <View style={styles.menuContent}>
              <Text style={styles.menuTitle}>Acerca de</Text>
              <Text style={styles.menuSubtitle}>Intercultura Costa Rica v1.0</Text>
            </View>
            <Ionicons name={activeSection === 'about' ? 'chevron-down' : 'chevron-forward'} size={20} color={COLORS.gray400} />
          </TouchableOpacity>

          {activeSection === 'about' && (
            <View style={styles.expandedSection} data-testid="about-section">
              <Text style={styles.sectionTitle}>Intercultura Costa Rica</Text>
              <Text style={styles.aboutText}>
                Fundada en 1993, Intercultura Costa Rica es una escuela de inmersion linguistica con dos campus: uno en la ciudad historica de Heredia y otro frente a la playa en Samara, Guanacaste.
              </Text>
              <Text style={styles.aboutText}>
                Ofrecemos programas de inmersion en espanol para estudiantes internacionales, asi como clases de ingles, portugues, aleman y frances para estudiantes locales. Nuestra metodologia combina ensenanza comunicativa con inmersion cultural.
              </Text>
              <Text style={styles.aboutText}>
                Actividades gratuitas diarias incluyen: baile latino, cocina costarricense, conversacion con locales, yoga y excursiones culturales semanales.
              </Text>
              <View style={styles.divider} />
              <Text style={styles.aboutSmall}>Version 1.0 - Asistente Virtual</Text>
              <Text style={styles.aboutSmall}>Metodologia Cambridge - Niveles A1 a C2</Text>
              <Text style={styles.aboutSmall}>Est. 1993 - Pura Vida</Text>
              <Text style={[styles.aboutSmall, { marginTop: 8 }]}>© 2025 Intercultura Costa Rica</Text>
              <Text style={styles.aboutSmall}>Todos los derechos reservados</Text>
            </View>
          )}
        </View>

        {/* Logout Button */}
        <Button
          title="Cerrar Sesion"
          onPress={handleLogout}
          variant="outline"
          style={styles.logoutButton}
          icon={<Ionicons name="log-out-outline" size={20} color={COLORS.primary} />}
        />

        <Text style={styles.footerText}>
          Intercultura Costa Rica © 2025{"\n"}Metodologia Cambridge
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  scrollContent: { padding: SPACING.md },
  profileHeader: { alignItems: 'center', marginBottom: SPACING.lg },
  avatarContainer: { position: 'relative', marginBottom: SPACING.md },
  avatar: { width: 100, height: 100, borderRadius: 50, backgroundColor: COLORS.primary, justifyContent: 'center', alignItems: 'center' },
  avatarText: { fontSize: 40, fontWeight: '700', color: COLORS.white },
  roleBadge: { position: 'absolute', bottom: 0, right: 0, width: 28, height: 28, borderRadius: 14, justifyContent: 'center', alignItems: 'center', borderWidth: 3, borderColor: COLORS.background },
  userName: { fontSize: 24, fontWeight: '700', color: COLORS.gray900, marginBottom: SPACING.xs },
  userEmail: { fontSize: 14, color: COLORS.gray500, marginBottom: SPACING.sm },
  roleContainer: { backgroundColor: COLORS.primaryLight + '20', paddingHorizontal: SPACING.md, paddingVertical: SPACING.xs, borderRadius: 20 },
  roleText: { fontSize: 12, fontWeight: '600', color: COLORS.primary },
  statsCard: { flexDirection: 'row', backgroundColor: COLORS.white, borderRadius: 16, padding: SPACING.lg, marginBottom: SPACING.lg, ...SHADOWS.md },
  statItem: { flex: 1, alignItems: 'center' },
  statDivider: { width: 1, backgroundColor: COLORS.gray200 },
  statValue: { fontSize: 20, fontWeight: '700', color: COLORS.gray900, marginTop: SPACING.xs },
  statLabel: { fontSize: 12, color: COLORS.gray500 },
  menuContainer: { backgroundColor: COLORS.white, borderRadius: 16, marginBottom: SPACING.lg, ...SHADOWS.sm },
  menuItem: { flexDirection: 'row', alignItems: 'center', padding: SPACING.md, borderBottomWidth: 1, borderBottomColor: COLORS.gray100 },
  menuIconContainer: { width: 40, height: 40, borderRadius: 20, backgroundColor: COLORS.primaryLight + '20', justifyContent: 'center', alignItems: 'center', marginRight: SPACING.md },
  menuContent: { flex: 1 },
  menuTitle: { fontSize: 16, fontWeight: '600', color: COLORS.gray900 },
  menuSubtitle: { fontSize: 12, color: COLORS.gray500 },
  logoutButton: { marginBottom: SPACING.lg },
  footerText: { textAlign: 'center', fontSize: 12, color: COLORS.gray400, lineHeight: 18 },
  // Expanded sections
  expandedSection: { padding: SPACING.md, paddingTop: 0, borderBottomWidth: 1, borderBottomColor: COLORS.gray100 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: COLORS.gray900, marginBottom: SPACING.sm, marginTop: SPACING.xs },
  // Settings
  input: { backgroundColor: COLORS.gray100, borderRadius: 10, padding: 12, fontSize: 14, color: COLORS.gray900, marginBottom: 10, borderWidth: 1, borderColor: COLORS.gray200 },
  passwordMsg: { fontSize: 13, marginBottom: 10, textAlign: 'center' },
  successMsg: { color: COLORS.primary },
  errorMsg: { color: '#E53935' },
  changePassBtn: { backgroundColor: COLORS.primary, borderRadius: 10, paddingVertical: 12, alignItems: 'center' },
  changePassBtnText: { color: COLORS.white, fontWeight: '600', fontSize: 14 },
  disabledBtn: { opacity: 0.6 },
  // Help
  contactRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 10, gap: 12 },
  contactInfo: { flex: 1 },
  contactLabel: { fontSize: 12, color: COLORS.gray500 },
  contactValue: { fontSize: 14, color: COLORS.gray900, fontWeight: '500' },
  divider: { height: 1, backgroundColor: COLORS.gray200, marginVertical: 10 },
  faqItem: { marginBottom: 12 },
  faqQuestion: { fontSize: 14, fontWeight: '600', color: COLORS.gray900, marginBottom: 2 },
  faqAnswer: { fontSize: 13, color: COLORS.gray500, lineHeight: 18 },
  // About
  aboutText: { fontSize: 14, color: COLORS.gray600 || COLORS.gray500, lineHeight: 20, marginBottom: 10 },
  aboutSmall: { fontSize: 12, color: COLORS.gray400, textAlign: 'center' },
});

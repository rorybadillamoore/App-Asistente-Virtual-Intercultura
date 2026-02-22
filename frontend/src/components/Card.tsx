import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, BORDER_RADIUS, SPACING, SHADOWS } from '../constants/theme';

interface CardProps {
  children: React.ReactNode;
  onPress?: () => void;
  style?: ViewStyle;
  variant?: 'default' | 'elevated' | 'outlined';
}

export const Card: React.FC<CardProps> = ({ children, onPress, style, variant = 'elevated' }) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'default':
        return {};
      case 'elevated':
        return SHADOWS.md;
      case 'outlined':
        return { borderWidth: 1, borderColor: COLORS.gray200 };
      default:
        return SHADOWS.md;
    }
  };

  if (onPress) {
    return (
      <TouchableOpacity
        style={[styles.card, getVariantStyles(), style]}
        onPress={onPress}
        activeOpacity={0.8}
      >
        {children}
      </TouchableOpacity>
    );
  }

  return <View style={[styles.card, getVariantStyles(), style]}>{children}</View>;
};

interface CourseCardProps {
  title: string;
  language: string;
  level: string;
  description: string;
  lessonCount: number;
  languageColor: string;
  onPress: () => void;
}

export const CourseCard: React.FC<CourseCardProps> = ({
  title,
  language,
  level,
  description,
  lessonCount,
  languageColor,
  onPress,
}) => {
  return (
    <Card onPress={onPress} style={styles.courseCard}>
      <View style={[styles.languageBadge, { backgroundColor: languageColor }]}>
        <Text style={styles.languageText}>{language.toUpperCase()}</Text>
      </View>
      <View style={styles.levelBadge}>
        <Text style={styles.levelText}>{level}</Text>
      </View>
      <Text style={styles.courseTitle}>{title}</Text>
      <Text style={styles.courseDescription} numberOfLines={2}>
        {description}
      </Text>
      <View style={styles.courseFooter}>
        <View style={styles.lessonCount}>
          <Ionicons name="book-outline" size={16} color={COLORS.gray500} />
          <Text style={styles.lessonCountText}>{lessonCount} lecciones</Text>
        </View>
        <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
  },
  courseCard: {
    marginBottom: SPACING.md,
  },
  languageBadge: {
    position: 'absolute',
    top: SPACING.md,
    right: SPACING.md,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  languageText: {
    color: COLORS.white,
    fontSize: 10,
    fontWeight: '700',
  },
  levelBadge: {
    alignSelf: 'flex-start',
    backgroundColor: COLORS.gray100,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
    marginBottom: SPACING.sm,
  },
  levelText: {
    color: COLORS.gray700,
    fontSize: 12,
    fontWeight: '600',
  },
  courseTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.gray900,
    marginBottom: SPACING.xs,
  },
  courseDescription: {
    fontSize: 14,
    color: COLORS.gray500,
    marginBottom: SPACING.md,
    lineHeight: 20,
  },
  courseFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  lessonCount: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.xs,
  },
  lessonCountText: {
    fontSize: 14,
    color: COLORS.gray500,
  },
});

import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator, ViewStyle, TextStyle } from 'react-native';
import { COLORS, BORDER_RADIUS, SPACING } from '../constants/theme';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  icon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  style,
  textStyle,
  icon,
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          button: { backgroundColor: COLORS.primary },
          text: { color: COLORS.white },
        };
      case 'secondary':
        return {
          button: { backgroundColor: COLORS.secondary },
          text: { color: COLORS.white },
        };
      case 'outline':
        return {
          button: { backgroundColor: 'transparent', borderWidth: 2, borderColor: COLORS.primary },
          text: { color: COLORS.primary },
        };
      case 'ghost':
        return {
          button: { backgroundColor: 'transparent' },
          text: { color: COLORS.primary },
        };
      default:
        return {
          button: { backgroundColor: COLORS.primary },
          text: { color: COLORS.white },
        };
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'sm':
        return {
          button: { paddingVertical: SPACING.sm, paddingHorizontal: SPACING.md },
          text: { fontSize: 14 },
        };
      case 'md':
        return {
          button: { paddingVertical: SPACING.md, paddingHorizontal: SPACING.lg },
          text: { fontSize: 16 },
        };
      case 'lg':
        return {
          button: { paddingVertical: SPACING.lg, paddingHorizontal: SPACING.xl },
          text: { fontSize: 18 },
        };
      default:
        return {
          button: { paddingVertical: SPACING.md, paddingHorizontal: SPACING.lg },
          text: { fontSize: 16 },
        };
    }
  };

  const variantStyles = getVariantStyles();
  const sizeStyles = getSizeStyles();

  return (
    <TouchableOpacity
      style={[
        styles.button,
        variantStyles.button,
        sizeStyles.button,
        disabled && styles.disabled,
        style,
      ]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.8}
    >
      {loading ? (
        <ActivityIndicator color={variantStyles.text.color} />
      ) : (
        <>
          {icon}
          <Text style={[styles.text, variantStyles.text, sizeStyles.text, textStyle]}>
            {title}
          </Text>
        </>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: BORDER_RADIUS.lg,
    gap: SPACING.sm,
  },
  text: {
    fontWeight: '600',
  },
  disabled: {
    opacity: 0.5,
  },
});

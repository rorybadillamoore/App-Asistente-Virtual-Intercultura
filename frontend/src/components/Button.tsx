import React from 'react';
import { TouchableOpacity, Pressable, Text, StyleSheet, ActivityIndicator, ViewStyle, TextStyle, Platform } from 'react-native';
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

  // Use TouchableOpacity for mobile, Pressable for web
  const Touchable = Platform.OS === 'web' ? Pressable : TouchableOpacity;

  return (
    <Touchable
      style={[
        styles.button,
        variantStyles.button,
        sizeStyles.button,
        disabled && styles.disabled,
        style,
      ]}
      onPress={() => {
        console.log('Button pressed!');
        if (!disabled && !loading) {
          onPress();
        }
      }}
      disabled={disabled || loading}
      // @ts-ignore
      accessibilityRole="button"
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
    </Touchable>
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

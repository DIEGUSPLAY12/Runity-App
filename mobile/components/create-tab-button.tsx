import { BottomTabBarButtonProps } from '@react-navigation/bottom-tabs';
import { PlatformPressable } from '@react-navigation/elements';
import * as Haptics from 'expo-haptics';
import { StyleSheet, View } from 'react-native';

const ACTIVE_BG = '#004f5d';
const INACTIVE_BG = '#004f5d';

export function CreateTabButton(props: BottomTabBarButtonProps) {
  const isSelected = Boolean(props.accessibilityState?.selected);

  return (
    <PlatformPressable
      {...props}
      onPressIn={(ev) => {
        if (process.env.EXPO_OS === 'ios') {
          Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        }
        props.onPressIn?.(ev);
      }}
      style={[props.style, styles.wrapper]}>
      <View style={[styles.fab, { backgroundColor: isSelected ? ACTIVE_BG : INACTIVE_BG }]}>
        {props.children}
      </View>
    </PlatformPressable>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  fab: {
    width: 62,
    height: 62,
    borderRadius: 31,
    top: -16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
  },
});


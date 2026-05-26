import { StyleSheet } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';

export default function WorkoutScreen() {
  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title">Workout</ThemedText>
      <ThemedText>Tu plan de entrenamientos.</ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
});


import { StyleSheet, ScrollView, TouchableOpacity, TextInput, View, Image } from 'react-native';
import { useState } from 'react';
import { MaterialIcons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useThemeColor } from '@/hooks/use-theme-color';
import {router} from "expo-router";

export default function ProfileScreen() {
  const fixedAccent = '#004f5d';
  const errorColor = '#d9534f';
  const [displayName, setDisplayName] = useState('Alex Johnson');
  const [weight, setWeight] = useState('72');
  const [height, setHeight] = useState('180');
  const [weightError, setWeightError] = useState('');
  const [heightError, setHeightError] = useState('');
  const [fitnessGoal, setFitnessGoal] = useState<'build' | 'loss' | 'endurance'>('build');

  const backgroundColor = useThemeColor({}, 'background');
  const textColor = useThemeColor({}, 'text');
  const tintColor = useThemeColor({}, 'tint');

  const isNumericValue = (value: string) => /^\d+$/.test(value);

  const handleWeightChange = (value: string) => {
    const cleanedValue = value.replace(/[^0-9]/g, '');
    setWeight(cleanedValue);
    setWeightError(value !== cleanedValue ? 'Solo se permiten numeros' : '');
  };

  const handleHeightChange = (value: string) => {
    const cleanedValue = value.replace(/[^0-9]/g, '');
    setHeight(cleanedValue);
    setHeightError(value !== cleanedValue ? 'Solo se permiten numeros' : '');
  };

  const handleSaveChanges = () => {
    const isWeightValid = isNumericValue(weight);
    const isHeightValid = isNumericValue(height);

    setWeightError(isWeightValid ? '' : 'El peso debe ser numerico');
    setHeightError(isHeightValid ? '' : 'La altura debe ser numerica');

    if (!isWeightValid || !isHeightValid) {
      return;
    }

    // TODO: Implement save changes logic
    console.log('Changes saved:', { displayName, weight, height, fitnessGoal });
  };

  const getCheckboxStyle = (goalType: 'build' | 'loss' | 'endurance') => {
    const isSelected = fitnessGoal === goalType;
    return {
      backgroundColor: isSelected ? fixedAccent : 'transparent',
      borderColor: fixedAccent,
    };
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <ThemedView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.headerSideButton}>
          <MaterialIcons name="arrow-back" size={24} color={textColor} />
        </TouchableOpacity>
        <ThemedText numberOfLines={1} style={styles.headerTitle}>Profile Settings</ThemedText>
        <TouchableOpacity style={[styles.headerSideButton, styles.settingsButton]}>
          <MaterialIcons name="settings" size={24} color={fixedAccent} />
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Profile Avatar Section */}
        <View style={styles.avatarSection}>
          <View style={[styles.avatarContainer, { backgroundColor: '#4a7c6b' }]}>
            <Image
              source={{ uri: 'https://imgs.search.brave.com/9Fc1cwuibC-1qrk6PYwGjUSAibY8kGRCwA2_IVS_wQA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzhlLzA4/LzlhLzhlMDg5YWZm/YjQxZjU5ZDhhOGVi/NjM0ZjQ4ZWQ4YjFh/LmpwZw' }}
              style={styles.avatar}
            />
            <View style={[styles.editBadge, { backgroundColor: tintColor }]}>
              <MaterialIcons name="edit" size={14} color="white" />
            </View>
          </View>
          <ThemedText type="title" style={styles.userName}>Alex Johnson</ThemedText>
          <ThemedText style={[styles.userRole, { color: tintColor }]}>Computer Science Student</ThemedText>
        </View>

        {/* Stats Section */}
        <View style={styles.statsSection}>
          <View style={[styles.statCard, { backgroundColor, borderColor: '#e0e0e0', borderWidth: 1 }]}>
            <ThemedText type="defaultSemiBold" style={styles.statNumber}>124</ThemedText>
            <ThemedText style={styles.statLabel}>WORKOUTS</ThemedText>
          </View>
          <View style={[styles.statCard, { backgroundColor, borderColor: '#e0e0e0', borderWidth: 1 }]}>
            <ThemedText type="defaultSemiBold" style={styles.statNumber}>45</ThemedText>
            <ThemedText style={styles.statLabel}>DAY STREAK</ThemedText>
          </View>
          <View style={[styles.statCard, { backgroundColor, borderColor: '#e0e0e0', borderWidth: 1 }]}>
            <ThemedText type="defaultSemiBold" style={styles.statNumber}>12k</ThemedText>
            <ThemedText style={styles.statLabel}>CALORIES</ThemedText>
          </View>
        </View>

        {/* Personal Information Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <MaterialIcons name="person" size={24} color={textColor} />
            <ThemedText type="defaultSemiBold" style={styles.sectionTitle}>Personal Information</ThemedText>
          </View>

          <View style={styles.inputGroup}>
            <ThemedText style={styles.label}>Display Name</ThemedText>
            <TextInput
              style={[styles.input, { color: textColor, borderColor: '#e0e0e0' }]}
              placeholder="Display Name"
              placeholderTextColor="#999"
              value={displayName}
              onChangeText={setDisplayName}
            />
          </View>

          <View style={styles.rowInputs}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <ThemedText style={styles.label}>Weight (kg)</ThemedText>
              <TextInput
                style={[
                  styles.input,
                  { color: textColor, borderColor: weightError ? errorColor : '#e0e0e0' },
                ]}
                placeholder="Weight"
                placeholderTextColor="#999"
                value={weight}
                onChangeText={handleWeightChange}
                keyboardType="numeric"
              />
              {weightError ? <ThemedText style={[styles.inputErrorText, { color: errorColor }]}>{weightError}</ThemedText> : null}
            </View>
            <View style={[styles.inputGroup, { flex: 1, marginLeft: 12 }]}>
              <ThemedText style={styles.label}>Height (cm)</ThemedText>
              <TextInput
                style={[
                  styles.input,
                  { color: textColor, borderColor: heightError ? errorColor : '#e0e0e0' },
                ]}
                placeholder="Height"
                placeholderTextColor="#999"
                value={height}
                onChangeText={handleHeightChange}
                keyboardType="numeric"
              />
              {heightError ? <ThemedText style={[styles.inputErrorText, { color: errorColor }]}>{heightError}</ThemedText> : null}
            </View>
          </View>
        </View>

        {/* Fitness Goals Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <MaterialIcons name="fitness-center" size={24} color={textColor} />
            <ThemedText type="defaultSemiBold" style={styles.sectionTitle}>Fitness Goals</ThemedText>
          </View>

          <TouchableOpacity
            style={styles.goalOption}
            onPress={() => setFitnessGoal('build')}
            activeOpacity={1}
          >
            <View style={[styles.checkbox, getCheckboxStyle('build')]}>
              {fitnessGoal === 'build' && <View style={styles.checkboxInner} />}
            </View>
            <ThemedText style={styles.goalText}>Build Muscle</ThemedText>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.goalOption}
            onPress={() => setFitnessGoal('loss')}
            activeOpacity={1}
          >
            <View style={[styles.checkbox, getCheckboxStyle('loss')]}>
              {fitnessGoal === 'loss' && <View style={styles.checkboxInner} />}
            </View>
            <ThemedText style={styles.goalText}>Weight Loss</ThemedText>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.goalOption}
            onPress={() => setFitnessGoal('endurance')}
            activeOpacity={1}
          >
            <View style={[styles.checkbox, getCheckboxStyle('endurance')]}>
              {fitnessGoal === 'endurance' && <View style={styles.checkboxInner} />}
            </View>
            <ThemedText style={styles.goalText}>Endurance Training</ThemedText>
          </TouchableOpacity>
        </View>

        {/* Save Changes Button */}
        <TouchableOpacity
          style={[styles.saveButton, { backgroundColor: '#004f5d' }]}
          onPress={handleSaveChanges}
        >
          <MaterialIcons name="check" size={20} color="white" />
          <ThemedText style={styles.saveButtonText}>Save Changes</ThemedText>
        </TouchableOpacity>

        {/* Last Updated Text */}
        <ThemedText style={styles.lastUpdated}>Last updated: 2 hours ago</ThemedText>
      </ScrollView>
      </ThemedView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  headerSideButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: {
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 8,
    fontSize: 20,
    fontWeight: '600',
  },
  settingsButton: {
    backgroundColor: '#e0e0e0',
  },
  scrollContent: {
    paddingHorizontal: 16,
    paddingBottom: 24,
  },
  avatarSection: {
    alignItems: 'center',
    marginVertical: 24,
  },
  avatarContainer: {
    position: 'relative',
    width: 120,
    height: 120,
    borderRadius: 60,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
  },
  editBadge: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'white',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  userRole: {
    fontSize: 14,
  },
  statsSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 24,
    gap: 12,
  },
  statCard: {
    flex: 1,
    borderRadius: 16,
    paddingVertical: 24,
    paddingHorizontal: 12,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 28,
    fontWeight: '600',
    marginBottom: 8,
  },
  statLabel: {
    fontSize: 13,
    fontWeight: '500',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 18,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
  },
  inputErrorText: {
    fontSize: 12,
    marginTop: 6,
  },
  rowInputs: {
    flexDirection: 'row',
  },
  goalOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginBottom: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 50,
    borderWidth: 2,
    borderColor: '#ccc',
    backgroundColor: 'transparent',
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxInner: {
    width: 8,
    height: 8,
    borderRadius: 50,
    backgroundColor: 'white',
  },
  goalText: {
    fontSize: 16,
  },
  saveButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 16,
    borderRadius: 28,
    marginTop: 24,
    marginBottom: 16,
    gap: 8,
  },
  saveButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  lastUpdated: {
    textAlign: 'center',
    fontSize: 12,
    marginTop: 8,
    opacity: 0.6,
  },
});

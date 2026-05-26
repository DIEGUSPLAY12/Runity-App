import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { router } from 'expo-router';
import { useEffect, useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

type ActivityType = 'running' | 'cycling' | 'walking';

const ACTIVITIES: { key: ActivityType; label: string; icon: keyof typeof MaterialIcons.glyphMap }[] = [
  { key: 'running', label: 'Running', icon: 'directions-run' },
  { key: 'cycling', label: 'Cycling', icon: 'directions-bike' },
  { key: 'walking', label: 'Walking', icon: 'directions-walk' },
];

const FRIENDS = [
  { id: '1', initials: 'LA', color: '#f0ddd3' },
  { id: '2', initials: 'MR', color: '#edcfb8' },
  { id: '3', initials: 'AN', color: '#e8d3c0' },
];

const KM_PER_SECOND: Record<ActivityType, number> = {
  running: 0.0026,
  cycling: 0.0054,
  walking: 0.0014,
};

const MET_BY_ACTIVITY: Record<ActivityType, number> = {
  running: 9.8,
  cycling: 7.5,
  walking: 3.8,
};

export default function CreateScreen() {
  const [activity, setActivity] = useState<ActivityType>('running');
  const [hasStarted, setHasStarted] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [targetDistance, setTargetDistance] = useState('');
  const [weightInput, setWeightInput] = useState('70');

  const handleStartSession = () => {
  setHasStarted(true);
  setIsRunning(true);
  };

  const handleTogglePause = () => {
  setIsRunning((prev) => !prev);
  };

  const handleResetSession = () => {
  setIsRunning(false);
  setHasStarted(false);
  setSeconds(0);
  };

  const handleWeightChange = (value: string) => {
	const normalized = value.replace(',', '.').replace(/[^0-9.]/g, '');
	const [integerPart, ...decimalParts] = normalized.split('.');
	const nextValue = decimalParts.length
	  ? `${integerPart}.${decimalParts.join('')}`
	  : integerPart;

	setWeightInput(nextValue);
  };

  useEffect(() => {
	if (!isRunning) {
	  return;
	}

	const timer = setInterval(() => {
	  setSeconds((prev) => prev + 1);
	}, 1000);

	return () => clearInterval(timer);
  }, [isRunning]);

  const weightKg = useMemo(() => {
	const parsed = Number.parseFloat(weightInput);

	if (!Number.isFinite(parsed) || parsed <= 0) {
	  return 70;
	}

	return Math.min(250, Math.max(30, parsed));
  }, [weightInput]);

  const distanceKm = useMemo(() => seconds * KM_PER_SECOND[activity], [activity, seconds]);
  const kcal = useMemo(() => {
	const minutes = seconds / 60;
	const met = MET_BY_ACTIVITY[activity];

	// kcal/min = (MET * 3.5 * kg) / 200
	return Math.round(((met * 3.5 * weightKg) / 200) * minutes);
  }, [activity, seconds, weightKg]);
  const bpm = isRunning ? 118 + Math.round(Math.min(seconds / 18, 22)) : null;

  const hours = Math.floor(seconds / 3600)
	.toString()
	.padStart(2, '0');
  const minutes = Math.floor((seconds % 3600) / 60)
	.toString()
	.padStart(2, '0');
  const secs = (seconds % 60).toString().padStart(2, '0');

  return (
	<SafeAreaView style={styles.safeArea}>
	  <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
		<View style={styles.headerRow}>
		  <Pressable onPress={() => router.back()} style={styles.roundIconButton}>
			<MaterialIcons name="arrow-back-ios-new" size={20} color="#075166" />
		  </Pressable>
		  <Text style={styles.headerTitle}>ACTIVE SESSION</Text>
		</View>

		<View style={styles.activityBar}>
		  {ACTIVITIES.map((item) => {
			const active = activity === item.key;
			return (
			  <Pressable
				key={item.key}
				onPress={() => setActivity(item.key)}
				style={[styles.activityItem, active && styles.activityItemActive]}>
				<MaterialIcons
				  name={item.icon}
				  size={20}
				  color={active ? '#0a5568' : '#73839c'}
				/>
				<Text style={[styles.activityText, active && styles.activityTextActive]}>{item.label}</Text>
			  </Pressable>
			);
		  })}
		</View>

		<Text style={styles.durationLabel}>DURATION</Text>

		<Text style={styles.timerText}>
		  <Text style={styles.timerDark}>{hours}:</Text>
		  <Text style={styles.timerAccent}>{minutes}</Text>
		  <Text style={styles.timerDark}>:{secs}</Text>
		</Text>

		<View style={styles.metricsRow}>
		  <View style={styles.metricCell}>
			<Text style={styles.metricValue}>{distanceKm.toFixed(2)}</Text>
			<Text style={styles.metricLabel}>KM</Text>
		  </View>

		  <View style={styles.metricDivider} />

		  <View style={styles.metricCell}>
			<Text style={styles.metricValue}>{kcal}</Text>
			<Text style={styles.metricLabel}>KCAL</Text>
		  </View>

		  <View style={styles.metricDivider} />

		  <View style={styles.metricCell}>
			<Text style={styles.metricValue}>{bpm ? bpm : '--'}</Text>
			<Text style={styles.metricLabel}>BPM</Text>
		  </View>
		</View>

		<View style={styles.weightCard}>
		  <Text style={styles.weightLabel}>Weight for Kcal</Text>
		  <View style={styles.weightInputWrap}>
			<TextInput
			  style={styles.weightInput}
			  keyboardType="decimal-pad"
			  value={weightInput}
			  onChangeText={handleWeightChange}
			  placeholder="70"
			  placeholderTextColor="#b4c1cf"
			/>
			<Text style={styles.weightUnit}>kg</Text>
		  </View>
		</View>

		<Text style={styles.targetLabel}>Set Target Distance (Optional)</Text>
		<View style={styles.targetCard}>
		  <MaterialIcons name="straighten" size={20} color="#0a5568" />
		  <TextInput
			style={styles.targetInput}
			keyboardType="decimal-pad"
			value={targetDistance}
			onChangeText={setTargetDistance}
			placeholder="0.00"
			placeholderTextColor="#b4c1cf"
		  />
		  <Text style={styles.targetUnit}>KM</Text>
		</View>

		{!hasStarted ? (
		  <Pressable onPress={handleStartSession} style={styles.startButton}>
			<View style={styles.playIconBadge}>
			  <MaterialIcons name="play-arrow" size={18} color="#fd8a39" />
			</View>
			<Text style={styles.startButtonText}>Start Session</Text>
		  </Pressable>
		) : (
		  <View style={styles.sessionControlsRow}>
			<Pressable onPress={handleTogglePause} style={[styles.controlButton, styles.pauseButton]}>
			  <View style={styles.controlIconBadge}>
				<MaterialIcons
				  name={isRunning ? 'pause' : 'play-arrow'}
				  size={18}
				  color={isRunning ? '#fd8a39' : '#0a5568'}
				/>
			  </View>
			  <Text style={styles.pauseButtonText}>{isRunning ? 'Pausar' : 'Reanudar'}</Text>
			</Pressable>

			<Pressable onPress={handleResetSession} style={[styles.controlButton, styles.resetButton]}>
			  <View style={styles.controlIconBadge}>
				<MaterialIcons name="replay" size={16} color="#7a8799" />
			  </View>
			  <Text style={styles.resetButtonText}>Reset</Text>
			</Pressable>
		  </View>
		)}

		<View style={styles.nearbyHeader}>
		  <Text style={styles.nearbyTitle}>NEARBY NOW</Text>
		  <Text style={styles.activeFriendsText}>• 12 Friends Active</Text>
		</View>

		<View style={styles.avatarRow}>
		  {FRIENDS.map((friend) => (
			<View key={friend.id} style={[styles.avatarWrap, { backgroundColor: friend.color }]}> 
			  <Text style={styles.avatarText}>{friend.initials}</Text>
			</View>
		  ))}
		  <View style={styles.plusAvatar}>
			<Text style={styles.plusAvatarText}>+9</Text>
		  </View>
		</View>
	  </ScrollView>
	</SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
	flex: 1,
	backgroundColor: '#eff2f4',
  },
  content: {
	paddingHorizontal: 18,
	paddingTop: 8,
	paddingBottom: 28,
  },
  headerRow: {
	flexDirection: 'row',
	alignItems: 'center',
	gap: 80,
  },
  roundIconButton: {
	height: 48,
	width: 48,
	borderRadius: 24,
	backgroundColor: '#dbe3e8',
	alignItems: 'center',
	justifyContent: 'center',
  },
  headerTitle: {
	fontSize: 20,
	color: '#065367',
	fontWeight: '700',
	letterSpacing: 0.6,
  },
  activityBar: {
	marginTop: 18,
	borderRadius: 34,
	backgroundColor: '#dbe3e8',
	padding: 6,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'space-between',
	gap: 6,
  },
  activityItem: {
	flex: 1,
	borderRadius: 28,
	minHeight: 58,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'center',
	gap: 6,
  },
  activityItemActive: {
	backgroundColor: '#ffffff',
	shadowColor: '#2b4a63',
	shadowOffset: { width: 0, height: 4 },
	shadowOpacity: 0.15,
	shadowRadius: 8,
	elevation: 3,
  },
  activityText: {
	fontSize: 12,
	fontWeight: '500',
	color: '#6d7d96',
  },
  activityTextActive: {
	color: '#075166',
	fontWeight: '700',
  },
  durationLabel: {
	marginTop: 42,
	textAlign: 'center',
	color: '#648d9c',
	fontSize: 12,
	fontWeight: '700',
	letterSpacing: 2,
  },
  timerText: {
	marginTop: 10,
	textAlign: 'center',
	fontSize: 68,
	fontWeight: '700',
	letterSpacing: 1,
  },
  timerDark: {
	color: '#0b1637',
  },
  timerAccent: {
	color: '#0a5568',
  },
  metricsRow: {
	marginTop: 10,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'space-between',
  },
  metricCell: {
	flex: 1,
	alignItems: 'center',
	gap: 4,
  },
  metricValue: {
	fontSize: 42,
	color: '#0b1637',
	fontWeight: '700',
  },
  metricLabel: {
	fontSize: 12,
	color: '#9baabd',
	fontWeight: '700',
	letterSpacing: 1,
  },
  metricDivider: {
	width: 1,
	height: 54,
	backgroundColor: '#d8dee4',
  },
  weightCard: {
	marginTop: 16,
	borderRadius: 18,
	backgroundColor: '#ffffff',
	paddingHorizontal: 14,
	paddingVertical: 10,
	shadowColor: '#6f8ca1',
	shadowOffset: { width: 0, height: 4 },
	shadowOpacity: 0.14,
	shadowRadius: 8,
	elevation: 3,
  },
  weightLabel: {
	fontSize: 12,
	fontWeight: '600',
	color: '#5e7592',
	marginBottom: 8,
  },
  weightInputWrap: {
	borderRadius: 12,
	backgroundColor: '#f4f7f9',
	paddingHorizontal: 10,
	minHeight: 42,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'space-between',
  },
  weightInput: {
	flex: 1,
	fontSize: 16,
	fontWeight: '700',
	color: '#0b1637',
	paddingVertical: 0,
  },
  weightUnit: {
	fontSize: 14,
	fontWeight: '700',
	color: '#075166',
	marginLeft: 8,
  },
  targetLabel: {
	marginTop: 24,
	fontSize: 16,
	fontWeight: '600',
	color: '#5e7592',
  },
  targetCard: {
	marginTop: 12,
	borderRadius: 24,
	backgroundColor: '#ffffff',
	minHeight: 76,
	paddingHorizontal: 18,
	flexDirection: 'row',
	alignItems: 'center',
	shadowColor: '#6f8ca1',
	shadowOffset: { width: 0, height: 6 },
	shadowOpacity: 0.2,
	shadowRadius: 10,
	elevation: 4,
  },
  targetInput: {
	flex: 1,
	marginLeft: 12,
	fontSize: 22,
	color: '#b8c6d6',
	fontWeight: '700',
	paddingVertical: 0,
  },
  targetUnit: {
	fontSize: 18,
	color: '#075166',
	fontWeight: '700',
  },
  startButton: {
	marginTop: 18,
	borderRadius: 24,
	backgroundColor: '#fd8a39',
	minHeight: 78,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'center',
	gap: 12,
	shadowColor: '#ab6a33',
	shadowOffset: { width: 0, height: 6 },
	shadowOpacity: 0.2,
	shadowRadius: 12,
	elevation: 5,
  },
  sessionControlsRow: {
	marginTop: 18,
	flexDirection: 'row',
	gap: 10,
  },
  controlButton: {
	flex: 1,
	minHeight: 72,
	borderRadius: 20,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'center',
	gap: 10,
	shadowOffset: { width: 0, height: 6 },
	shadowOpacity: 0.16,
	shadowRadius: 10,
	elevation: 4,
  },
  pauseButton: {
	backgroundColor: '#fd8a39',
	shadowColor: '#ab6a33',
  },
  resetButton: {
	backgroundColor: '#ffffff',
	shadowColor: '#6f8ca1',
  },
  controlIconBadge: {
	height: 28,
	width: 28,
	borderRadius: 14,
	backgroundColor: '#ffffff',
	alignItems: 'center',
	justifyContent: 'center',
  },
  pauseButtonText: {
	fontSize: 18,
	color: '#fff7f0',
	fontWeight: '700',
  },
  resetButtonText: {
	fontSize: 18,
	color: '#7a8799',
	fontWeight: '700',
  },
  playIconBadge: {
	height: 30,
	width: 30,
	borderRadius: 15,
	backgroundColor: '#fff',
	alignItems: 'center',
	justifyContent: 'center',
  },
  startButtonText: {
	fontSize: 20,
	color: '#fff7f0',
	fontWeight: '700',
  },
  nearbyHeader: {
	marginTop: 26,
	flexDirection: 'row',
	alignItems: 'center',
	justifyContent: 'space-between',
  },
  nearbyTitle: {
	fontSize: 16,
	color: '#121a31',
	fontWeight: '700',
	letterSpacing: 1,
  },
  activeFriendsText: {
	fontSize: 13,
	color: '#1ab65d',
	fontWeight: '600',
  },
  avatarRow: {
	marginTop: 12,
	flexDirection: 'row',
	alignItems: 'center',
  },
  avatarWrap: {
	height: 42,
	width: 42,
	borderRadius: 21,
	marginRight: -8,
	borderWidth: 2,
	borderColor: '#eff2f4',
	alignItems: 'center',
	justifyContent: 'center',
  },
  avatarText: {
	color: '#425970',
	fontWeight: '700',
	fontSize: 11,
  },
  plusAvatar: {
	marginLeft: 2,
	height: 42,
	width: 42,
	borderRadius: 21,
	backgroundColor: '#075166',
	alignItems: 'center',
	justifyContent: 'center',
  },
  plusAvatarText: {
	color: '#ffffff',
	fontSize: 14,
	fontWeight: '700',
  },
});


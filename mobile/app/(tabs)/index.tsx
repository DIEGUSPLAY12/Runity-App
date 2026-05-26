import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import {push} from "expo-router/build/global-state/routing";

const friends = [
  { name: 'Alex', initials: 'A', color: '#EACDB8' },
  { name: 'Jordan', initials: 'J', color: '#CFD9C6' },
  { name: 'Sam', initials: 'S', color: '#EBCFB9' },
  { name: 'Riley', initials: 'R', color: '#E9C5B2' },
  { name: 'Casey', initials: 'C', color: '#DDD1BA' },
];

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.headerRow}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>HS</Text>
          </View>
          <Text style={styles.feedTitle}>Feed</Text>
          <Pressable style={styles.notificationButton}>
            <MaterialIcons name="notifications" size={22} color="#004f5d" />
          </Pressable>
        </View>

        <View style={styles.heroCard}>
          <View style={styles.statusBadge}>
            <Text style={styles.statusBadgeText}>CURRENT STATUS</Text>
          </View>
          <Text style={styles.mainTitle}>Not Training</Text>
          <Text style={styles.mainSubtitle}>
            Ready to break a sweat? Start your session and track your progress.
          </Text>
          <Pressable style={styles.startButton}>
            <MaterialIcons name="play-circle-filled" size={26} color="#004f5d" />
            <Text style={styles.startButtonText}>Start Training</Text>
          </Pressable>
        </View>

        <View style={styles.sectionHeaderRow}>
          <Text style={styles.sectionHeader}>Friends Training Now</Text>
          <Pressable onPress={() => push("/(tabs)/comunity")} hitSlop={8}>
            <Text style={styles.viewAllButton}>View all</Text>
          </Pressable>
        </View>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.friendsRow}>
          {friends.map((friend) => (
            <View key={friend.name} style={styles.friendItem}>
              <View style={styles.friendAvatar}>
                <View
                  style={[styles.friendAvatarInner, { backgroundColor: friend.color }]}>
                  <Text style={styles.friendAvatarText}>{friend.initials}</Text>
                </View>
                <View style={styles.friendOnlineDot} />
              </View>
              <Text style={styles.friendName}>{friend.name}</Text>
            </View>
          ))}
        </ScrollView>

        <Text style={[styles.sectionHeader, { marginTop: 32 }]}>Daily Summary</Text>

        <View style={styles.summaryRow}>
          <View style={[styles.summaryCard, styles.summaryCardShadow]}>
            <View style={styles.summaryCardHeader}>
              <MaterialIcons name="access-time-filled" size={18} color="#00586a" />
              <Text style={styles.summaryCardLabel}>ACTIVE TIME</Text>
            </View>
            <View style={styles.summaryCardValueRow}>
              <Text style={styles.bigNumber}>45</Text>
              <Text style={styles.summaryUnit}>min</Text>
            </View>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: '64%', backgroundColor: '#00586a' }]} />
            </View>
          </View>

          <View style={[styles.summaryCard, styles.summaryCardShadow]}>
            <View style={styles.summaryCardHeader}>
              <MaterialIcons name="local-fire-department" size={18} color="#1ec4b9" />
              <Text style={styles.summaryCardLabel}>CALORIES</Text>
            </View>
            <View style={styles.summaryCardValueRow}>
              <Text style={styles.bigNumber}>320</Text>
              <Text style={styles.summaryUnit}>kcal</Text>
            </View>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: '40%', backgroundColor: '#1ec4b9' }]} />
            </View>
          </View>
        </View>

        <Text style={styles.communityHighlightsTitle}>Community Highlights</Text>

        <View style={[styles.highlightCard, styles.summaryCardShadow]}>
          <View style={styles.highlightIcon}>
            <MaterialIcons name="fitness-center" size={24} color="#00586a" />
          </View>
          <View style={styles.highlightContent}>
            <Text style={styles.highlightText}>
              <Text style={{ fontWeight: '600' }}>Leo</Text> completed a{' '}
              <Text style={{ fontWeight: '600', color: '#00586a' }}>High Intensity</Text> workout.
            </Text>
            <Text style={styles.highlightSubtext}>24m ago - Campus Gym</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    paddingHorizontal: 16,
    paddingTop: 14,
    paddingBottom: 26,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  avatar: {
    height: 48,
    width: 48,
    borderRadius: 24,
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#726e71',
  },
  feedTitle: {
    fontSize: 32,
    fontWeight: '600',
    color: '#262626',
  },
  notificationButton: {
    height: 48,
    width: 48,
    borderRadius: 24,
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
  },
  heroCard: {
    marginTop: 20,
    borderRadius: 38,
    backgroundColor: '#00586a',
    paddingHorizontal: 18,
    paddingVertical: 20,
    shadowColor: '#0b2b36',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.22,
    shadowRadius: 16,
    elevation: 8,
  },
  statusBadge: {
    alignSelf: 'center',
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  statusBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  mainTitle: {
    marginTop: 24,
    fontSize: 34,
    fontWeight: '700',
    color: 'white',
    textAlign: 'center',
  },
  mainSubtitle: {
    marginTop: 12,
    paddingHorizontal: 16,
    fontSize: 16,
    textAlign: 'center',
    color: 'rgba(255, 255, 255, 0.75)',
  },
  startButton: {
    marginTop: 32,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 25,
    backgroundColor: '#2fd0cc',
    paddingVertical: 16,
  },
  startButtonText: {
    marginLeft: 12,
    fontSize: 22,
    fontWeight: '700',
    color: '#004f5d',
  },
  sectionHeader: {
    fontSize: 30,
    fontWeight: '600',
    color: '#262626',
    lineHeight: 36,
  },
  sectionHeaderRow: {
    marginTop: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  viewAllButton: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10bfb5',
    lineHeight: 36,
  },
  friendsRow: {
    gap: 16,
    paddingTop: 10,
    paddingBottom: 2,
  },
  friendItem: {
    alignItems: 'center',
  },
  friendAvatar: {
    height: 76,
    width: 76,
    borderRadius: 38,
    borderWidth: 2,
    borderColor: '#1ac8c1',
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
  },
  friendAvatarInner: {
    height: 64,
    width: 64,
    borderRadius: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  friendAvatarText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#5f5f5f',
  },
  friendOnlineDot: {
    position: 'absolute',
    bottom: 4,
    right: 4,
    height: 16,
    width: 16,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: 'white',
    backgroundColor: '#1ac8c1',
  },
  friendName: {
    marginTop: 8,
    fontSize: 16,
    color: '#5f5f5f',
  },
  summaryRow: {
    marginTop: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  summaryCard: {
    width: '48%',
    borderRadius: 30,
    backgroundColor: 'white',
    padding: 20,
  },
  summaryCardShadow: {
    shadowColor: '#8ca0ac',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.14,
    shadowRadius: 14,
    elevation: 4,
  },
  summaryCardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  summaryCardLabel: {
    marginLeft: 8,
    fontSize: 16,
    fontWeight: '600',
    color: '#5f748d',
  },
  summaryCardValueRow: {
    marginTop: 16,
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  bigNumber: {
    fontSize: 32,
    fontWeight: '700',
    color: '#262626',
  },
  summaryUnit: {
    marginBottom: 4,
    marginLeft: 8,
    fontSize: 20,
    color: '#90a1b2',
  },
  progressBar: {
    marginTop: 16,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#dfe7eb',
  },
  progressFill: {
    height: 8,
    borderRadius: 4,
  },
  communityHighlightsTitle: {
    marginTop: 32,
    fontSize: 28,
    fontWeight: '600',
    color: '#262626',
  },
  highlightCard: {
    marginTop: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 26,
    backgroundColor: 'white',
    padding: 16,
  },
  highlightIcon: {
    height: 64,
    width: 64,
    borderRadius: 32,
    backgroundColor: '#ecf1f4',
    alignItems: 'center',
    justifyContent: 'center',
  },
  highlightContent: {
    marginLeft: 16,
    flex: 1,
  },
  highlightText: {
    fontSize: 18,
    color: '#262626',
  },
  highlightSubtext: {
    marginTop: 4,
    fontSize: 16,
    color: '#8da1b4',
  },
});

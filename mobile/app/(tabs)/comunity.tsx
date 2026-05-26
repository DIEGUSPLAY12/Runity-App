import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { router } from 'expo-router';
import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '../../components/themed-text';
import { ThemedView } from '../../components/themed-view';

type CommunityTab = 'friends' | 'suggested';

type Friend = {
  id: string;
  name: string;
  handle: string;
  initials: string;
  avatarColor: string;
  isFollowing: boolean;
  isOnline: boolean;
};

const FRIENDS: Friend[] = [
  {
    id: 'alex',
    name: 'Alex J.',
    handle: '@alex_run',
    initials: 'AJ',
    avatarColor: '#E8C9AC',
    isFollowing: true,
    isOnline: true,
  },
  {
    id: 'sarah',
    name: 'Sarah W.',
    handle: '@sarah_lift',
    initials: 'SW',
    avatarColor: '#D5E3DD',
    isFollowing: false,
    isOnline: true,
  },
  {
    id: 'mike',
    name: 'Mike T.',
    handle: '@mike_strength',
    initials: 'MT',
    avatarColor: '#C8D5D8',
    isFollowing: true,
    isOnline: true,
  },
  {
    id: 'elena',
    name: 'Elena K.',
    handle: '@elena_train',
    initials: 'EK',
    avatarColor: '#D4DDBE',
    isFollowing: true,
    isOnline: true,
  },
  {
    id: 'david',
    name: 'David Miller',
    handle: '@david_run_fast',
    initials: 'DM',
    avatarColor: '#E9CEB3',
    isFollowing: true,
    isOnline: false,
  },
  {
    id: 'chloe',
    name: 'Chloe Simmons',
    handle: '@chloe_yoga',
    initials: 'CS',
    avatarColor: '#CEB08D',
    isFollowing: false,
    isOnline: false,
  },
  {
    id: 'jordan',
    name: 'Jordan Lee',
    handle: '@jordan_lift',
    initials: 'JL',
    avatarColor: '#EAE7DF',
    isFollowing: true,
    isOnline: false,
  },
  {
    id: 'maya',
    name: 'Maya Thompson',
    handle: '@maya_cycles',
    initials: 'MT',
    avatarColor: '#E4DED5',
    isFollowing: true,
    isOnline: false,
  },
  {
    id: 'chris',
    name: 'Chris Evans',
    handle: '@captain_training',
    initials: 'CE',
    avatarColor: '#E9E9E5',
    isFollowing: false,
    isOnline: false,
  },
];

const SUGGESTED: Friend[] = [
  {
    id: 'nina',
    name: 'Nina Lopez',
    handle: '@nina_mobility',
    initials: 'NL',
    avatarColor: '#D7E5EA',
    isFollowing: false,
    isOnline: true,
  },
  {
    id: 'omar',
    name: 'Omar Khan',
    handle: '@omar_hiit',
    initials: 'OK',
    avatarColor: '#E8DCC9',
    isFollowing: false,
    isOnline: false,
  },
  {
    id: 'val',
    name: 'Val Gomez',
    handle: '@val_swim',
    initials: 'VG',
    avatarColor: '#DCE7D7',
    isFollowing: false,
    isOnline: true,
  },
];

export default function CommunityScreen() {
  const [activeTab, setActiveTab] = useState<CommunityTab>('friends');
  const [searchValue, setSearchValue] = useState('');
  const [followState, setFollowState] = useState<Record<string, boolean>>(() => {
    return [...FRIENDS, ...SUGGESTED].reduce<Record<string, boolean>>((acc, friend) => {
      acc[friend.id] = friend.isFollowing;
      return acc;
    }, {});
  });

  const activeNow = useMemo(() => FRIENDS.filter((friend) => friend.isOnline).slice(0, 4), []);

  const listData = useMemo(() => {
    const source = activeTab === 'friends' ? FRIENDS : SUGGESTED;
    const normalizedSearch = searchValue.trim().toLowerCase();
    if (!normalizedSearch) {
      return source;
    }

    return source.filter(
      (friend) =>
        friend.name.toLowerCase().includes(normalizedSearch) ||
        friend.handle.toLowerCase().includes(normalizedSearch)
    );
  }, [activeTab, searchValue]);

  const toggleFollow = (friendId: string) => {
    setFollowState((prev) => ({ ...prev, [friendId]: !prev[friendId] }));
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <ThemedView style={styles.container} lightColor="#f2f4f5" darkColor="#0f172a">
        <View style={styles.headerRow}>
          <Pressable style={styles.iconButton} onPress={() => router.back()}>
            <MaterialIcons name="arrow-back" size={22} color="#0b4a5a" />
          </Pressable>
          <ThemedText style={styles.title}>Community</ThemedText>
          <Pressable style={[styles.iconButton, styles.addButton]}>
            <MaterialIcons name="person-add" size={21} color="#0b4a5a" />
          </Pressable>
        </View>

        <View style={styles.searchBar}>
          <MaterialIcons name="search" size={22} color="#6f9299" />
          <TextInput
            value={searchValue}
            onChangeText={setSearchValue}
            style={styles.searchInput}
            placeholder="Search students or sports clubs"
            placeholderTextColor="#7c9ba2"
          />
        </View>

        <View style={styles.tabRow}>
          <Pressable onPress={() => setActiveTab('friends')} style={styles.tabButton}>
            <ThemedText
              style={[styles.tabText, activeTab === 'friends' && styles.tabTextActive]}>
              Friends
            </ThemedText>
            {activeTab === 'friends' ? <View style={styles.activeTabLine} /> : null}
          </Pressable>

          <Pressable onPress={() => setActiveTab('suggested')} style={styles.tabButton}>
            <ThemedText
              style={[styles.tabText, activeTab === 'suggested' && styles.tabTextActive]}>
              Suggested
            </ThemedText>
            {activeTab === 'suggested' ? <View style={styles.activeTabLine} /> : null}
          </Pressable>
        </View>

        <ScrollView
          style={styles.scroll}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}>
          <ThemedText style={styles.sectionLabel}>ACTIVE NOW</ThemedText>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.activeNowRow}>
            {activeNow.map((friend) => (
              <View key={friend.id} style={styles.activeNowItem}>
                <View style={styles.activeAvatarFrame}>
                  <View style={[styles.avatarInner, { backgroundColor: friend.avatarColor }]}> 
                    <ThemedText style={styles.avatarInitials}>{friend.initials}</ThemedText>
                  </View>
                  <View style={styles.onlineDot} />
                </View>
                <ThemedText style={styles.activeNowName}>{friend.name}</ThemedText>
              </View>
            ))}
          </ScrollView>

          <ThemedText style={styles.sectionLabel}>
            {activeTab === 'friends' ? 'ALL FRIENDS' : 'ALL SUGGESTIONS'}
          </ThemedText>

          {listData.map((friend) => {
            const isFollowing = followState[friend.id];
            return (
              <View key={friend.id} style={styles.friendRow}>
                <View style={[styles.friendAvatar, { backgroundColor: friend.avatarColor }]}>
                  <ThemedText style={styles.friendInitials}>{friend.initials}</ThemedText>
                </View>

                <View style={styles.friendMeta}>
                  <ThemedText style={styles.friendName}>{friend.name}</ThemedText>
                  <ThemedText style={styles.friendHandle}>{friend.handle}</ThemedText>
                </View>

                <Pressable
                  onPress={() => toggleFollow(friend.id)}
                  style={[
                    styles.followButton,
                    isFollowing ? styles.followingButton : styles.followActionButton,
                  ]}>
                  <ThemedText
                    style={[
                      styles.followText,
                      isFollowing ? styles.followingText : styles.followActionText,
                    ]}>
                    {isFollowing ? 'Following' : 'Follow'}
                  </ThemedText>
                </Pressable>
              </View>
            );
          })}
        </ScrollView>
      </ThemedView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f2f4f5',
  },
  container: {
    flex: 1,
    paddingHorizontal: 14,
  },
  headerRow: {
    marginTop: 4,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  iconButton: {
    height: 40,
    width: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addButton: {
    backgroundColor: '#deebec',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#111827',
    letterSpacing: 0.2,
  },
  searchBar: {
    marginTop: 16,
    borderRadius: 22,
    backgroundColor: '#dce3e6',
    minHeight: 52,
    paddingHorizontal: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#4a6369',
    paddingVertical: 10,
  },
  tabRow: {
    marginTop: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#d2d9dc',
    flexDirection: 'row',
    gap: 28,
  },
  tabButton: {
    paddingBottom: 10,
  },
  tabText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#87a4aa',
  },
  tabTextActive: {
    color: '#0b4a5a',
  },
  activeTabLine: {
    marginTop: 8,
    height: 3,
    borderRadius: 2,
    backgroundColor: '#0b4a5a',
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    paddingTop: 18,
    paddingBottom: 26,
  },
  sectionLabel: {
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.9,
    color: '#6b7280',
  },
  activeNowRow: {
    gap: 16,
    paddingTop: 14,
    paddingBottom: 24,
    paddingRight: 10,
  },
  activeNowItem: {
    alignItems: 'center',
    width: 90,
  },
  activeAvatarFrame: {
    height: 72,
    width: 72,
    borderRadius: 36,
    borderWidth: 2,
    borderColor: '#0b5c6d',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f6f8f8',
  },
  avatarInner: {
    height: 64,
    width: 64,
    borderRadius: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarInitials: {
    fontSize: 18,
    fontWeight: '700',
    color: '#263238',
  },
  onlineDot: {
    position: 'absolute',
    right: 1,
    bottom: 1,
    height: 18,
    width: 18,
    borderRadius: 9,
    borderWidth: 2,
    borderColor: '#f2f4f5',
    backgroundColor: '#22c55e',
  },
  activeNowName: {
    marginTop: 8,
    fontSize: 14,
    fontWeight: '600',
    color: '#111827',
  },
  friendRow: {
    marginTop: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  friendAvatar: {
    height: 56,
    width: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
  },
  friendInitials: {
    fontSize: 16,
    fontWeight: '700',
    color: '#374151',
  },
  friendMeta: {
    marginLeft: 10,
    flex: 1,
  },
  friendName: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0f172a',
  },
  friendHandle: {
    marginTop: 2,
    fontSize: 12,
    color: '#6f9299',
  },
  followButton: {
    borderRadius: 20,
    minWidth: 96,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 9,
    paddingHorizontal: 12,
  },
  followingButton: {
    backgroundColor: '#dce3e6',
  },
  followActionButton: {
    backgroundColor: '#0b5c6d',
  },
  followText: {
    fontSize: 12,
    fontWeight: '700',
  },
  followingText: {
    color: '#0b5c6d',
  },
  followActionText: {
    color: '#f4fafb',
  },
});


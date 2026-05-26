import { Tabs } from 'expo-router';
import React from 'react';

import { CreateTabButton } from '@/components/create-tab-button';
import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';

const ACTIVE_TAB_COLOR = '#004f5d';
const INACTIVE_TAB_COLOR = '#8e8e8f';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: ACTIVE_TAB_COLOR,
        tabBarInactiveTintColor: INACTIVE_TAB_COLOR,
        headerShown: false,
        tabBarButton: HapticTab,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'HOME',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="house.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="workout"
        options={{
          title: 'WORKOUT',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="dumbbell.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="create"
        options={{
          title: 'CREATE',
          tabBarLabel: () => null,
          tabBarButton: (props) => <CreateTabButton {...props} />,
          tabBarIcon: ({ focused }) => (
            <IconSymbol size={30} name="plus" color={focused ? '#ffffff' : '#6b7280'} />
          ),
        }}
      />
      <Tabs.Screen
        name="comunity"
        options={{
          title: 'COMUNITY',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="person.2.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'PROFILE',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="person.fill" color={color} />,
        }}
      />
    </Tabs>
  );
}

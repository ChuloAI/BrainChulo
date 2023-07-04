import { defineStore } from 'pinia';
import InternalService from '../services/internal';
import eventBus from '../services/eventBus';

export const useProfileStore = defineStore('profile', {
  state: () => ({
    username: localStorage.getItem('username') || 'Anonymous',
    avatarUrl: localStorage.getItem('avatarUrl') || new URL('@/assets/user_icon.png', import.meta.url).href,
  }),
  actions: {
    updateProfile(data = {}) {
      localStorage.setItem('username', data['username']);
      localStorage.setItem('avatarUrl', data['avatarUrl']);

      eventBus.$emit('update-profile', data);
    },
    async clearMessages() {
      localStorage.removeItem('conversation_id');

      await InternalService.resetDatabase();

      eventBus.$emit('clear-messages');
    },
  },
});

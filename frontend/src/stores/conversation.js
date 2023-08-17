import { defineStore } from 'pinia';

export const useConversationStore = defineStore('conversation', {
  state: () => ({
    conversationId: localStorage.getItem('conversation_id') || null,
    messages: [],
  }),
  actions: {
    
  },
});

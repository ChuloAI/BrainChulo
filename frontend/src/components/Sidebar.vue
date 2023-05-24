<template>
    <aside class="sidebar bg-gray-900 dark overflow-x-hidden flex-shrink-0 transform transition-all duration-300 ease-in-out -translate-x-full sm:hidden md:translate-x-0 md:block">
        <div class="w-[300px] h-full flex-shrink-0">
          <div class="h-full flex flex-col">
            <nav class="p-2 h-full flex-col flex">
              <a @click="onAddConversationClicked" class="border border-gray-700 rounded-md flex items-center justify-center text-sm font-medium text-gray-300 px-3 py-3 hover:bg-gray-700 hover:text-white">+ New Conversation</a>
              
              <div class="flex flex-col mt-5 w-full">
                <a v-for="conversation in conversations" :key="conversation.id" @click="onSelectConversation(conversation.id)" class="cursor-pointer rounded-md justify-items-start text-sm font-medium text-gray-300 px-3 py-3" :class="{'bg-gray-800': conversation.id === Number(selectedConversationId)}">💬 {{conversation.title || "New Conversation"}}</a>
              </div>
            </nav>
          </div>
        </div>
      </aside>
</template>

<script>
import InternalService from '../services/internal';

export default {
    emits: ['add-conversation', 'select-conversation'],
    props: {
        conversations: {
            type: Array,
            required: true,
        },
        selectedConversationId: {
            type: Number,
            required: true,
        }
    },
    methods: {
        onAddConversationClicked() {
            this.$emit('add-conversation');
        },
        onSelectConversation(conversationId) {
            this.$emit('select-conversation', conversationId);
        }
    }
}
</script>
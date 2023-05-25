<template>
  <aside
    class="sidebar bg-gray-900 dark overflow-x-hidden flex-shrink-0 transform transition-all duration-300 ease-in-out -translate-x-full sm:hidden md:translate-x-0 md:block">
    <div class="w-[300px] h-full flex-shrink-0">
      <div class="h-full flex flex-col">
        <nav class="p-2 h-full flex-col flex">
          <a
            @click="onAddConversationClicked"
            class="border border-gray-700 rounded-md flex items-center justify-center text-sm font-medium text-gray-300 px-3 py-3 hover:bg-gray-700 hover:text-white">
            + New Conversation
          </a>

          <div class="flex flex-col mt-5 w-full">
            <div
              v-for="conversation in conversations"
              :key="conversation.id"
              class="cursor-pointer rounded-md justify-items-start text-sm font-medium text-gray-300 px-3 py-3"
              :class="{ 'bg-gray-800': conversation.id === Number(selectedConversationId) }">
              <div class="flex flex-row" @click="onSelectConversation(conversation.id)" v-if="!isEditing(conversation.id)">
                <span class="flexjustify-items-start mr-2">💬</span>
                <span class="flex flex-grow justify-items-start">{{ conversation.title || 'New Conversation' }}</span>
                <span v-show="conversation.id === Number(selectedConversationId)" class="ml-2 flex justify-items-end">
                  <a @click="toggleEdit(conversation.id)" title="Edit" class="mr-2">✏️</a>
                  <a @click="deleteConversation(conversation.id)" title="Delete">🗑️</a>
                </span>
              </div>
              <input
                v-show="isEditing(conversation.id)"
                v-model="conversation.title"
                @blur="onRenameConversation(conversation.id, conversation.title)"
                @keydown.enter="onRenameConversation(conversation.id, conversation.title)"
                :ref="'conversationInput' + conversation.id"
                class="bg-gray-800 text-white p-2 border border-gray-700 rounded-md" />
            </div>
          </div>
        </nav>
      </div>
    </div>
  </aside>
</template>

<script>
  import { nextTick } from 'vue';
  export default {
    emits: ['add-conversation', 'select-conversation', 'rename-conversation', 'delete-conversation'],
    props: {
      conversations: {
        type: Array,
        required: true,
      },
      selectedConversationId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        editingConversationId: null,
      };
    },
    methods: {
      onAddConversationClicked() {
        this.$emit('add-conversation');
      },
      onSelectConversation(conversationId) {
        this.$emit('select-conversation', conversationId);
      },
      toggleEdit(conversationId) {
        this.editingConversationId = conversationId;

        nextTick(() => {
          this.$refs['conversationInput' + conversationId][0].focus();
        })
      },
      isEditing(conversationId) {
        return this.editingConversationId === conversationId;
      },
      onRenameConversation(id, title) {
        this.$emit('rename-conversation', id, title);
        this.editingConversationId = null;
      },
      deleteConversation(id) {
        if(!confirm('Are you sure you want to delete this conversation?')) return;

        this.$emit('delete-conversation', id);
      }
    },
  };
</script>

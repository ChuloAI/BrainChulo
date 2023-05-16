<template>
  <div class="h-screen flex flex-col">
    <!-- toolbar -->
    <nav class="bg-gray-800">
      <div class="px-2 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div class="relative flex items-center justify-between h-16">
          <div class="flex items-center justify-center flex-1 sm:items-stretch sm:justify-start">
            <div class="flex items-center">
              <img class="hidden h-8 w-auto sm:block" src="../assets/logo.png" alt="Logo" />
              <h1 class="hidden ml-3 text-2xl font-bold text-white uppercase sm:block">BrainChulo</h1>
            </div>
          </div>
          <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
            <div class="text-white">{{ username }}</div>

            <navbar-dropdown :username="username" :avatar-url="avatarUrl" @update-username="updateUsername" @clear-messages="clearMessages"></navbar-dropdown>
          </div>
        </div>
      </div>
    </nav>
    <!-- main content -->
    <div class="flex-grow flex flex-col">
      <div class="flex-grow overflow-y-auto">
        <div class="mx-auto max-w-2xl mt-5">
          <chat-bubble
            v-for="message in messages"
            :key="message.id"
            :message="message"
            :class="{
              'ml-auto': message.isMe,
              'mr-auto': !message.isMe,
            }"></chat-bubble>
        </div>
      </div>
      <form @submit.prevent="sendMessage" class="bg-gray-200 px-4 py-2">
        <div class="flex items-center">
          <input v-model="messageInput" type="text" class="form-input flex-1" placeholder="Type your message..." />
          <button
            type="submit"
            class="ml-2 px-3 py-2 rounded-md text-sm font-medium text-white bg-indigo-500 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
            Send
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import ChatBubble from './ChatBubble.vue';
  import NavbarDropdown from './NavbarDropdown.vue';
  import InternalService from '../services/internal';

  export default {
    components: {
      ChatBubble,
      NavbarDropdown,
    },
    data() {
      return {
        username: '',
        avatarUrl: new URL('../assets/user_icon.png', import.meta.url).href,
        messages: [],
        messageInput: '',
      };
    },
    async created() {
      this.conversation_id = localStorage.getItem('conversation_id');
      this.conversation = await InternalService.getConversation(this.conversation_id);

      // if this.conversation_id is null get the id from the newly created conversation
      if (!this.conversation_id) {
        this.conversation_id = this.conversation.id;
        localStorage.setItem('conversation_id', this.conversation_id);
      }

      this.messages = JSON.parse(localStorage.getItem('messages')) || [];
      this.username = localStorage.getItem('username') ? localStorage.getItem('username') : 'Anonymous';
    },
    methods: {
      updateUsername(newValue) {
        console.log(newValue);
        localStorage.setItem('username', newValue);
        this.username = newValue;
      },
      clearMessages() {
        this.messages = [];
        localStorage.removeItem('messages');
      },
      sendMessage() {
        if (!this.messageInput || this.messageInput.length === 0) {
          return;
        }

        const message = {
          id: this.messages.length + 1,
          createdAt: Date.now(),
          content: this.messageInput,
          isMe: true,
        };

        this.messageInput = '';
        this.messages.push(message);
        localStorage.setItem('messages', JSON.stringify(this.messages));

        // Show the loading message
        const loadingMessage = {
          id: this.messages.length + 1,
          createdAt: Date.now(),
          content: '',
          isMe: false,
          isLoading: true,
        };
        this.messages.push(loadingMessage);

        // Make API call to LLM endpoint
        const url = 'http://localhost:8165/conversations';
        fetch(url, {
          method: 'POST',
          mode: 'no-cors',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            prompt: message.content,
            parameters: {
              temperature: 0.8,
            },
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            // Remove the loading message
            this.messages = this.messages.filter((m) => !m.isLoading);

            // Add the AI response message
            const aiMessage = {
              id: this.messages.length + 1,
              createdAt: Date.now(),
              content: data.response,
              isMe: false,
            };
            this.messages.push(aiMessage);
            localStorage.setItem('messages', JSON.stringify(this.messages));
          })
          .catch((error) => console.error(error));
      },
      logout() {
        localStorage.removeItem('user');
        this.$router.push('/login');
      },
    },
  };
</script>

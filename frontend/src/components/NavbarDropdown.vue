<template>
  <div class="relative ml-3 z-10">
    <div>
      <button @click="open = !open" type="button" class="flex text-sm rounded-full text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" id="user-menu" aria-haspopup="true">
        <span class="sr-only">Open user menu</span>
        <img class="h-8 w-8 rounded-full" :src="avatarUrl" alt="">
      </button>
    </div>
    <div v-if="open" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5" v-click-away="closeMenu">
      <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="user-menu">
        <a @click="openProfileModal = !openProfileModal" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Edit username</a>
        <a @click="clearMessages()" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Clear chat history</a>
      </div>
    </div>
    <EditProfileModal :username="username" :avatar-url="avatarUrl" @edit-username="editUsername" @close-modal="openProfileModal = !openProfileModal" v-if="openProfileModal" />
  </div>
</template>

<script>
import EditProfileModal from './EditProfileModal.vue';

export default {
  props: {
    username: {
      type: String,
      required: true
    },
    avatarUrl: {
      type: String,
      required: true
    }
  },
  components: {
    EditProfileModal
  },
  data() {
    return {
      open: false,
      openProfileModal: false,
    }
  },
  methods: {
    editUsername(newUsername) {
      console.log(newUsername)
      this.$emit('update-username', newUsername)
    },
    clearMessages() {
      this.$emit('clear-messages')
    },
    closeMenu() {
      console.log('closing menu')
      this.open = false;
    }
  }
}
</script>

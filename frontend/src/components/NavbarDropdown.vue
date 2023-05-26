<template>
  <div class="relative ml-3 z-10">
    <div>
      <button @click="open = !open" type="button" class="align-middle inline-flex items-center px-3 py-1 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white tracking-widest hover:bg-indigo-800" id="user-menu" aria-haspopup="true">
        <div class="mr-2">{{ username }}</div>
        <span class="sr-only">Open user menu</span>
        <AvatarImg :avatarUrl="avatarUrl" :key="avatarUrl" :size="8" alt="Avatar" class="object-cover rounded-full w-full h-full" />
      </button>
    </div>
    <div v-if="open" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5" v-click-away="closeMenu">
      <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="user-menu">
        <a @click="openProfileModal = !openProfileModal" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Edit Profile</a>
        <a @click="clearMessages()" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Reset Database</a>
      </div>
    </div>
    <EditProfileModal :username="username" :avatarUrl="avatarUrl" @edit-profile="editProfile" @close-modal="openProfileModal = !openProfileModal" v-if="openProfileModal" />
  </div>
</template>

<script>
import EditProfileModal from './EditProfileModal.vue';
import AvatarImg from './AvatarImg.vue';

export default {
  emits: ['update-profile', 'clear-messages'],
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
    EditProfileModal,
    AvatarImg
  },
  data() {
    return {
      open: false,
      openProfileModal: false,
    }
  },
  methods: {
    editProfile(data = {}) {
      this.$emit('update-profile', data)
    },
    clearMessages() {
      this.$emit('clear-messages')
    },
    closeMenu() {
      this.open = false;
    }
  }
}
</script>

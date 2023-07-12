<template>
  <nav class="bg-gray-800">
    <div class="px-2 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div class="relative flex items-center justify-between h-16">
        <div class="flex items-center justify-center flex-1 sm:items-stretch sm:justify-start">
          <div class="flex items-center">
            <img class="hidden h-8 w-auto sm:block" src="../assets/logo.png" alt="Logo" />
            <h1 class="hidden ml-3 text-2xl font-bold text-white uppercase sm:block">BrainChulo</h1>
            <ul class="flex ml-6 space-x-4">
              <li>
                <router-link
                  to="/"
                  class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  exact-active-class="bg-gray-900 text-white"
                  active-class="bg-gray-700 text-white">
                  Home
                </router-link>
              </li>
              <li>
                <router-link
                  to="/flows"
                  class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  exact-active-class="bg-gray-900 text-white"
                  active-class="bg-gray-700 text-white">
                  Flows
                </router-link>
              </li>
              <li>
                <router-link
                  to="/about"
                  class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  exact-active-class="bg-gray-900 text-white"
                  active-class="bg-gray-700 text-white">
                  About
                </router-link>
              </li>
            </ul>
          </div>
        </div>
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <navbar-dropdown :username="username" :avatar-url="avatarUrl" @update-profile="updateProfile" @clear-messages="clearMessages"></navbar-dropdown>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
  import NavbarDropdown from './NavbarDropdown.vue';
  import { useProfileStore } from '../stores/profile';

  export default {
    name: 'NavBar',
    components: {
      NavbarDropdown,
    },
    data() {
      return {
        profileStore: useProfileStore(),
        username: '',
        avatarUrl: '',
      };
    },
    mounted() {
      this.username = this.profileStore.username;
      this.avatarUrl = this.profileStore.avatarUrl;
    },
    methods: {
      updateProfile(data = {}) {
        this.profileStore.updateProfile(data);
        this.username = data['username'];
        this.avatarUrl = data['avatarUrl'];

        this.$emit('update-profile', data);
      },
      async clearMessages() {
        if (!window.confirm('Are you sure?')) return;

        this.profileStore.clearMessages();
      },
    },
  };
</script>

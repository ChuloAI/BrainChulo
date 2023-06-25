<template>
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
          <navbar-dropdown :username="username" :avatar-url="avatarUrl" @update-profile="updateProfile" @clear-messages="clearMessages"></navbar-dropdown>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
  import NavbarDropdown from './NavbarDropdown.vue';
  export default {
    name: 'NavBar',
    components: {
      NavbarDropdown,
    },
    props: {
      username: {
        type: String,
        required: true,
      },
      avatarUrl: {
        type: String,
        required: true,
      },
    },
    methods: {
      updateProfile(data = {}) {
        this.$emit('update-profile', data);
      },
      clearMessages() {
        this.$emit('clear-messages');
      },
    },
  };
</script>

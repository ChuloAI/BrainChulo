<template>
  <div class="about">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
    <NavBar :username="username" :avatar-url="avatarUrl" @update-profile="updateProfile" @clear-messages="clearMessages"></NavBar>

    <h1>About View</h1>
    <p>This is the about view.</p>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';

  export default {
    components: {
      NavBar,
    },
  };
</script>

<style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
</style>

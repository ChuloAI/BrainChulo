<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <h1>About View</h1>
    <p>This is the about view.</p>
  </main>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';

  export default {
    components: {
      NavBar,
    },
  };
</script>

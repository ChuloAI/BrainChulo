<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <h1>Flows</h1>
  </main>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';

  export default {
    name: 'FlowsView',
    components: {
      NavBar,
    },
  };
</script>

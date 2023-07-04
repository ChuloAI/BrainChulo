<script setup>
  import ChatWindow from '@/components/ChatWindow.vue';
  import NavBar from '@/components/NavBar.vue';
</script>

<template>
  <main class="h-screen">
    <NavBar></NavBar>

    <ChatWindow username="Human" />
  </main>
</template>

<script>
  export default {
    components: {
      NavBar,
    },
  };
</script>

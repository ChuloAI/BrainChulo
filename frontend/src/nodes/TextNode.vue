<template>
  <div class="text-center">
    <h1>Text Output</h1>
    <p>{{ text }}</p>
  </div>
</template>

<script>
  export default {
    props: ['text'],
  };
</script>

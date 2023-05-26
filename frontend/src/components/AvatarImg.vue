<template>
  <span class="avatar">
    <img class="object-cover rounded-full" :class="sizeClass" :src="avatarUrl" alt="Profile Image" />
  </span>
</template>

<script>
  export default {
    props: {
      avatarUrl: {
        type: String,
        default: '',
      },
      size: {
        type: Number,
        default: 8,
      },
    },
    computed: {
      sizeClass() {
        return `h-${this.size} w-${this.size}`;
      },
    },
  };
</script>

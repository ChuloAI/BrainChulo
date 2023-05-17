<template>
  <div class="flex items-start mb-4 w-full gap-2">
    <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-400 text-white flex-shrink-0 ml-4">
      <img :src="avatarUrl" alt="Avatar" class="object-cover rounded-full w-full h-full" />
    </div>
    <div class="rounded-lg py-2 mx-5">
      <div class="text-gray-900 text-md max-w-xl">{{ message.text }}</div>
    </div>
  </div>
  <hr class="w-full mb-4" />
</template>

<script>
  export default {
    props: {
      message: {
        type: Object,
        required: true,
      },
    },
    computed: {
      avatarUrl() {
        const path = this.message.is_user ? '../assets/user_icon.png' : '../assets/AI_icon.png';

        return new URL(path, import.meta.url).href;
      },
    },
  };
</script>

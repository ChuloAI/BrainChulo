<template>
  <div class="flex items-end mb-4">
    <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-400 text-white mr-2">
      <img :src="avatarUrl" alt="Avatar" class="w-full h-full object-cover rounded-full" />
    </div>
    <div class="rounded-lg py-2 px-4">
      <div class="text-gray-900 text-md">{{ message.content }}</div>
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
        const path = this.message.isMe ? '../assets/user_icon.png' : '../assets/AI_icon.png';

        return new URL(path, import.meta.url).href;
      },
    },
  };
</script>

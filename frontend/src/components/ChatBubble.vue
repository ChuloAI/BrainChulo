<template>
  <div>
    <div class="flex items-start mb-4 w-full gap-2">
      <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-400 text-white flex-shrink-0 ml-4">
        <AvatarImg :avatarUrl="avatarUrl" :key="avatarUrl" :size="10" alt="Avatar" class="object-cover rounded-full w-full h-full" />
      </div>
      <div class="rounded-lg py-2 mx-5">
        <div v-if="msg.isLoading" class="loading-animation"></div>
        <div v-else v-html="fromMarkdown(this.msg.text)" class="text-md max-w-xl"></div>
      </div>
    </div>
    <div v-if="!msg.isLoading && !msg.is_user && msg.rating == 0" class="flex align-right justify-end text-xs text-gray-400 flex-row flex-shrink-0 m-4">
      <span class="cursor-pointer mr-1 py-1 px-2 rounded-full bg-gray-400 hover:bg-gray-500" @click="upvote">👍</span>
      <span class="cursor-pointer py-1 px-2 rounded-full bg-gray-400 hover:bg-gray-500" @click="downvote">👎</span>
    </div>
    <div v-else-if="!msg.isLoading && !msg.is_user" class="flex align-right justify-end text-xs text-gray-400 flex-row flex-shrink-0 m-4">
      <span v-if="msg.rating > 0" class="cursor-pointer mr-1 py-1 px-2 rounded-full bg-green-700 hover:bg-green-800" @click="resetVote">👍</span>
      <span v-else class="cursor-pointer mr-1 py-1 px-2 rounded-full py-1 px-2 rounded-full bg-red-700" @click="resetVote">👎</span>
    </div>
    <hr class="w-full mb-4" />
  </div>
</template>

<script>
  import { marked } from 'marked';
  import { markedHighlight } from 'marked-highlight';
  import hljs from 'highlight.js';
  import InternalService from '../services/internal';
  import AvatarImg from './AvatarImg.vue';
  import { useProfileStore } from '../stores/profile';

  marked.use(
    markedHighlight({
      langPrefix: 'hljs language-',
      highlight: (code, lang) => {
        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language }).value;
      },
    })
  );

  export default {
    components: { AvatarImg },
    emits: ['messageRendered'],
    props: {
      message: {
        type: Object,
        required: true,
      },
    },
    data: function () {
      return {
        msg: this.message,
        profileStore: useProfileStore(),
      };
    },
    watch: {
      message: function () {
        this.msg = this.message;
      },
    },
    computed: {
      avatarUrl() {
        if (this.message.is_user) {
          const savedAvatar = this.profileStore.avatarUrl;
          if (savedAvatar) {
            return savedAvatar;
          }
        }
        const path = this.message.is_user ? '../assets/user_icon.png' : '../assets/AI_icon.png';
        return new URL(path, import.meta.url).href;
      },
    },
    mounted() {
      this.$emit('messageRendered');
    },
    methods: {
      fromMarkdown(markdown) {
        return marked.parse(markdown, { headerIds: false, mangle: false });
      },
      async upvote() {
        this.msg = await InternalService.upvoteMessage(this.message.conversation_id, this.message.id);
      },
      async downvote() {
        this.msg = await InternalService.downvoteMessage(this.message.conversation_id, this.message.id);
      },
      async resetVote() {
        this.msg = await InternalService.resetMessageVote(this.message.conversation_id, this.message.id);
      },
    },
  };
</script>

<style>
  .loading-animation {
    margin-top: 10px;
    display: inline-block;
    width: 2em;
    height: 2em;
    background-image: url('../assets/loading.gif');
    background-repeat: no-repeat;
    background-size: contain;
  }
</style>

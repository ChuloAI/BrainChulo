<template>
  <div class="flex items-start mb-4 w-full gap-2" data-id="{{ message.id }}" data-created-at="{{ message.created_at }}" data-conversation-id="{{ message.conversation_id }}">
    <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-400 text-white flex-shrink-0 ml-4">
      <img :src="avatarUrl" alt="Avatar" class="object-cover rounded-full w-full h-full" />
    </div>
    <div class="rounded-lg py-2 mx-5">
      <div v-if="message.isLoading" class="loading-animation"> </div>
      <div v-else v-html="fromMarkdown(this.message.text)" class="text-md max-w-xl"></div>
    </div>
  </div>
  <hr class="w-full mb-4" />
</template>

<script>
  import { marked } from 'marked';
  import {markedHighlight} from "marked-highlight";
  import hljs from 'highlight.js';

  marked.use(markedHighlight({
    langPrefix: 'hljs language-',
    highlight: (code, lang) => {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      return hljs.highlight(code, { language }).value;
    }
  }));

  export default {
    emits: ['messageRendered'],
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
    mounted() {
      this.$emit('messageRendered');
    },
    methods: {
      fromMarkdown(markdown) {
        return marked.parse(markdown, {headerIds: false,
    mangle: false});
      }
    }
  }
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
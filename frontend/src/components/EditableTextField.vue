<template>
  <span class="editable-text-field" @click="startEditing">
    <span v-if="!isEditing">
      {{ text }}
      <PencilIcon title="Edit" class="ml-2 w-4 h-4 text-gray-100 inline" />
    </span>
    <input v-else ref="inputField" v-model="editedText" @blur="finishEditing" @keydown.enter="finishEditing" class="editable-input-field" />
  </span>
</template>

<script>
  import { PencilIcon } from '@heroicons/vue/20/solid';

  export default {
    props: {
      text: {
        type: String,
        required: false,
        default: '',
      },
    },
    components: {
      PencilIcon,
    },
    data() {
      return {
        isEditing: false,
        editedText: '',
      };
    },
    methods: {
      startEditing() {
        this.isEditing = true;
        this.editedText = this.text;
        this.$nextTick(() => {
          this.$refs.inputField.focus();
        });
      },
      finishEditing() {
        this.isEditing = false;
        this.$emit('edit', this.editedText);
      },
    },
  };
</script>

<style scoped>
  .editable-text-field {
    cursor: pointer;
  }
  .editable-input-field {
    border: none;
    outline: none;
    background-color: transparent;
    padding: 0;
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    color: rgb(233, 233, 233);
  }
</style>

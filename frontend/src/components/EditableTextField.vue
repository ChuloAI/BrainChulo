<template>
  <div class="flex items-center">
    <span class="editable-text-field" @click="startEditing">
      <span v-if="!isEditing">
        {{ text }}
        <PencilIcon title="Edit" class="ml-2 w-4 h-4 text-gray-100 inline" />
      </span>
      <input v-else ref="inputField" v-model="editedText" @blur="finishEditing" @keydown.enter="finishEditing" class="editable-input-field" />
    </span>
    <TrashIcon v-if="!isEditing && isDeletable" title="Delete" class="ml-2 w-4 h-4 text-gray-100 inline cursor-pointer" @click="confirmDelete" />
  </div>
</template>

<script>
  import { PencilIcon, TrashIcon } from '@heroicons/vue/20/solid';

  export default {
    props: {
      text: {
        type: String,
        required: false,
        default: '',
      },
      isDeletable: {
        type: Boolean,
        required: false,
        default: false,
      },
    },
    components: {
      PencilIcon,
      TrashIcon,
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
      confirmDelete() {
        if (!this.isDeletable) return;
        if (!confirm('Are you sure you want to delete this flow?')) return;

        this.$emit('delete');
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

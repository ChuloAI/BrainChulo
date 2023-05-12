<template>
  <div class="modal fixed inset-0 flex items-center justify-center">
    <div class="modal-background" @click="close"></div>
    <div class="modal-content bg-white rounded-lg overflow-hidden shadow-md">
      <div class="px-6 py-4">
        <h2 class="text-2xl font-bold mb-4">Edit Username</h2>
        <div class="mb-4">
          <label class="block font-bold text-gray-700 mb-2" for="new-username">
            New Username
          </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="new-username" type="text" v-model="newUsername">
        </div>
        <div class="flex justify-end">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mr-2 rounded" @click="save">Save</button>
          <button class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" @click="close">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false
    },
    username: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isActive: this.value,
      newUsername: this.username
    }
  },
  watch: {
    value(newValue) {
      this.isActive = newValue
    },
    username(newValue) {
      this.newUsername = newValue
    }
  },
  methods: {
    save() {
      // Save the new username
      this.$emit('edit-username', this.newUsername)

      // Close the modal
      this.$emit('close-modal', true)
    },
    close() {
      // Reset the new username
      this.newUsername = this.username

      // Close the modal
      this.$emit('close-modal', true)
    }
  }
}
</script>

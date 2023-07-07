<template>
  <div class="modal fixed inset-0 flex items-center justify-center">
    <div class="modal-background" @click="close"></div>
    <div class="modal-content bg-white rounded-lg overflow-hidden shadow-md">
      <div class="px-6 py-4">
        <h2 class="text-2xl font-bold mb-4">Edit Profile</h2>
        <div class="mb-4">
          <label class="block font-bold text-gray-700 mb-2" for="new-username">New Username</label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="new-username"
            type="text"
            v-model="newUsername" />
        </div>
        <div class="mb-4">
          <img
            :src="newAvatarSrc"
            alt="Avatar"
            class="rounded rounded-full object-cover object-center p-2 bg-gray-200 w-24 h-24 mx-auto border border-gray-500" />
          <label class="block font-bold text-gray-700 mb-2" for="new-avatar">New Avatar Image</label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="new-avatar"
            type="file"
            @change="handleAvatarChange" />
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
    emits: ['edit-profile', 'close-modal'],
    props: {
      avatarUrl: {
        type: String,
        default: '',
      },
      username: {
        type: String,
        default: '',
      },
    },
    data() {
      return {
        newUsername: this.username,
        newAvatar: this.avatarUrl,
        newAvatarSrc: this.avatarUrl,
      };
    },
    watch: {
      username(newValue) {
        this.newUsername = newValue;
      },
    },
    methods: {
      handleAvatarChange(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (event) => {
          const img = new Image();
          img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            let width = img.width;
            let height = img.height;

            if (width > 500 || height > 500) {
              if (width > height) {
                height = Math.round((height / width) * 500);
                width = 500;
              } else {
                width = Math.round((width / height) * 500);
                height = 500;
              }
            }

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            this.newAvatarSrc = canvas.toDataURL(file.type);
          };
          img.src = event.target.result;
        };
        reader.readAsDataURL(file);
      },
      save() {
        // Save the new username
        this.$emit('edit-profile', { username: this.newUsername, avatarUrl: this.newAvatarSrc });

        // Close the modal
        this.$emit('close-modal', true);
      },
      close() {
        // Reset the new username
        this.newUsername = this.username;

        // Close the modal
        this.$emit('close-modal', true);
      },
    },
  };
</script>

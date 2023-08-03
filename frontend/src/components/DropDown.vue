<template>
  <div class="dropdown">
    <button
      class="dropdown-toggle bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded inline-flex items-center"
      @click="isOpen = !isOpen">
      <span>{{ label }}</span>
      <svg class="fill-current h-4 w-4 ml-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
        <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" />
      </svg>
    </button>
    <ul class="dropdown-menu absolute text-gray-700 pt-1" v-show="isOpen" v-if="isOpen" v-click-away="closeDropdown">
      <li v-for="option in options" :key="option.id" @click="selectOption(option)">
        <a class="rounded-t bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">{{ option.label }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    props: {
      options: {
        type: Array,
        required: true,
      },
      selectedOption: {
        type: Object,
        required: false,
      },
    },
    data() {
      return {
        isOpen: false,
      };
    },
    computed: {
      label() {
        if (this.selectedOption && this.selectedOption.label) {
          return this.selectedOption.label;
        }

        return 'Select an option';
      },
    },
    methods: {
      selectOption(option) {
        this.$emit('change', option); // Emit the 'change' event with the selected option
        this.isOpen = false;
      },
      closeDropdown() {
        this.isOpen = false;
      },
    },
  };
</script>

<style scoped>
  .dropdown-menu {
    max-height: 200px;
    overflow-y: auto;
    background-color: white;
    border: 1px solid gray;
    border-radius: 4px;
    padding: 0.5rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: absolute;
    top: 100%; /* Position the dropdown below the button */
    left: 0;
    width: 100%;
    z-index: 999; /* Ensure the dropdown menu appears on top */
  }
</style>

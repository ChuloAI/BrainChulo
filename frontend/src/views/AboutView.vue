<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold mb-4">About BrainChulo</h1>
      <p class="text-lg leading-relaxed mb-8">{{ aboutText }}</p>

      <div>
        <h2 class="text-2xl font-bold mb-4">Features</h2>
        <ul class="list-disc pl-6">
          <li v-for="feature in features" :key="feature" class="mb-2">{{ feature }}</li>
        </ul>
      </div>

      <div class="mt-8">
        <h2 class="text-2xl font-bold mb-4">Installation</h2>
        <pre class="bg-gray-100 p-4">{{ installationText }}</pre>
      </div>

      <div class="mt-8">
        <h2 class="text-2xl font-bold mb-4">Usage</h2>
        <pre class="bg-gray-100 p-4">{{ usageText }}</pre>
      </div>

      <div class="mt-8">
        <h2 class="text-2xl font-bold mb-4">Contributing</h2>
        <p class="text-lg leading-relaxed mb-8">{{ contributingText }}</p>
      </div>

      <div class="mt-8">
        <h2 class="text-2xl font-bold mb-4">License</h2>
        <p class="text-lg leading-relaxed">{{ licenseText }}</p>
      </div>
    </div>

    <a href="https://github.com/ChuloAI/BrainChulo" target="_blank" rel="noopener noreferrer" class="fork-ribbon right-top fixed">Fork me on GitHub</a>
  </main>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';

  export default {
    name: 'AboutView',
    data() {
      return {
        aboutText: `BrainChulo is a powerful Chat application with an emphasis on its memory management system. Our work is inspired by the camel family's resilience and adaptability. The repository contains a custom LTM (Long-Term Memory) approach for Llama-based LLMs (Large Language Models), and is designed to help users enhance their experience when using Open-Source LLMs.`,
        features: [
          'Custom LTM implementation based on Open Source Large Language Models',
          'Memory retrieval algorithms for quick recall',
          'Easy-to-use interface for storing and managing memories',
          'Modern User Interface',
          'One-Shot, Few-Shot, and Tool-Capable Agents with Full Vector-Based Memory Integration',
          'Ability to handle multiple conversations',
          'Ability to upvote or downvote AI answers for fine-tuning',
        ],
        installationText: `To use BrainChulo, you need to install the required dependencies. Refer to the installation instructions provided in the repository.`,
        usageText: `To start BrainChulo, follow the usage instructions provided in the repository.`,
        contributingText: `We welcome contributions to BrainChulo from the open source community! If you would like to contribute to the project, please fork the repository and submit a pull request. For more information on how to contribute, please see the CONTRIBUTING.md file.`,
        licenseText: `BrainChulo is licensed under the MIT license. See LICENSE.md for more information.`,
      };
    },
    components: {
      NavBar,
    },
  };
</script>

<style scoped>
  .container {
    max-width: 800px;
    margin: 0 auto;
  }

  pre {
    white-space: pre-wrap;
  }

  .fork-ribbon {
    z-index: 9999;
    top: 0;
    right: 0;
    position: fixed;
    pointer-events: auto;
    overflow: hidden;
    width: 200px;
    height: 200px;
    text-indent: -9999px;
  }

  .fork-ribbon::before {
    content: 'Fork me on GitHub';
    text-decoration: none;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    font-family: Arial, sans-serif;
    text-align: center;
    line-height: 1.5;
    transform: rotate(45deg);
    background-color: #870000;
    position: absolute;
    width: 260px;
    top: 60px;
    right: -60px;
    padding: 7px 0;
    border-width: 1px 0;
    border-style: dotted;
    border-color: #4d0000;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
    text-indent: 0;
  }
</style>

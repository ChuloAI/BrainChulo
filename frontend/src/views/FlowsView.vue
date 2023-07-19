<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <div class="flex justify-center items-center bg-gray-600 p-2">
      <button id="playButton" class="font-bold py-2 px-4 rounded flex items-center justify-center" :class="runBtnClass" @click="runFlow" :disabled="isRunning">
        <svg class="fill-current w-6 h-6 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M13 10.732l-5.61 3.22A1 1 0 0 1 6 13V7a1 1 0 0 1 1.39-.92L13 9.268v1.464z" />
        </svg>
        <span class="text-base">{{ runBtnText }}</span>
      </button>
    </div>

    <baklava-editor :view-model="baklava" />
  </main>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';
  import { defineComponent, ref, computed } from 'vue';
  import { EditorComponent, DependencyEngine, useBaklava, applyResult } from 'baklavajs';
  import '@baklavajs/themes/dist/syrup-dark.css';
  import '@/assets/flows.css';
  import { DisplayNode } from '@/nodes/DisplayNode';
  import { LLMQueryNode } from '@/nodes/LLMQueryNode';

  export default defineComponent({
    components: {
      'baklava-editor': EditorComponent,
      NavBar,
    },
    setup() {
      const baklava = useBaklava();
      const engine = new DependencyEngine(baklava.editor);

      const isRunning = ref(false);

      baklava.commandHandler.registerCommand('Run', {
        canExecute: () => {
          return true;
        },
        execute: () => {
          engine.runOnce();
        },
      });

      baklava.editor.registerNodeType(LLMQueryNode);
      baklava.editor.registerNodeType(DisplayNode);

      const runFlow = () => {
        engine.runOnce();
      };

      const runBtnClass = computed(() => {
        return {
          'bg-blue-500': !isRunning.value,
          'bg-gray-500': isRunning.value,
          'hover:bg-blue-700': !isRunning.value,
          'text-white': !isRunning.value,
          'text-gray-400': isRunning.value,
          disabled: isRunning.value,
        };
      });

      const runBtnText = computed(() => {
        return isRunning.value ? 'Running...' : 'Run';
      });

      const beforeRunToken = Symbol();
      const afterRunToken = Symbol();

      engine.events.beforeRun.subscribe(beforeRunToken, () => {
        isRunning.value = true;
      });

      engine.events.afterRun.subscribe(afterRunToken, (result) => {
        engine.pause();
        applyResult(result, baklava.editor);
        isRunning.value = false;
        engine.resume();
      });

      // Add some nodes for demo purposes
      function addNodeWithCoordinates(nodeType, x, y) {
        const n = new nodeType();
        baklava.displayedGraph.addNode(n);
        n.position.x = x;
        n.position.y = y;
        return n;
      }
      const node1 = addNodeWithCoordinates(LLMQueryNode, 300, 140);
      const node2 = addNodeWithCoordinates(DisplayNode, 550, 140);
      baklava.displayedGraph.addConnection(node1.outputs.outputText, node2.inputs.text);

      return { baklava, runFlow, runBtnClass, runBtnText, isRunning };
    },
  });
</script>

<style scoped></style>

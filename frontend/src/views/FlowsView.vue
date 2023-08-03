<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <div class="flex justify-center items-center bg-gray-600 p-2">
      <button id="playButton" class="font-bold py-2 px-4 rounded flex items-center justify-center" :class="runBtnClass" @click="runFlow" :disabled="isRunning">
        <PlayIcon class="w-6 h-6 mr-2" />
        <span class="text-base">{{ runBtnText }}</span>
      </button>
      <button id="saveButton" class="mx-2 font-bold py-2 px-4 rounded flex items-center justify-center bg-blue-500 text-white" @click="saveFlow">
        <CloudArrowDownIcon class="w-6 h-6 mr-2" />
        <span class="text-base">Save</span>
      </button>
      <DropDown
        :options="flows"
        :selectedOption="currentFlow"
        @change="handleFlowChange"
        class="absolute right-0 mx-2 font-bold py-2 px-4 rounded flex items-center justify-center"></DropDown>
    </div>
    <baklava-editor :view-model="baklava" />
  </main>
</template>
, onBeforeMount , watch

<script>
  import NavBar from '@/components/NavBar.vue';
  import DropDown from '@/components/DropDown.vue';
  import { defineComponent, ref, computed, onBeforeMount, watch } from 'vue';
  import { EditorComponent, DependencyEngine, useBaklava, applyResult, GraphTemplate } from 'baklavajs';
  import { CloudArrowDownIcon, PlayIcon } from '@heroicons/vue/20/solid';
  import '@baklavajs/themes/dist/syrup-dark.css';
  import '@/assets/flows.css';
  import { useFlowStore } from '@/stores/flow';

  /* Load Nodes */
  import { DisplayNode } from '@/nodes/DisplayNode';
  import { LLMQueryNode } from '@/nodes/LLMQueryNode';

  export default defineComponent({
    components: {
      'baklava-editor': EditorComponent,
      NavBar,
      DropDown,
      CloudArrowDownIcon,
      PlayIcon,
    },
    setup() {
      const baklava = useBaklava();
      const engine = new DependencyEngine(baklava.editor);
      const flowStore = useFlowStore();
      const currentFlow = computed(() => flowStore.currentFlow);
      const flows = ref([]);

      onBeforeMount(async () => {
        flows.value = await flowStore.fetchFlows();
        if (currentFlow.value === null && flows.value.length > 0) {
          currentFlow.value = flows.value[0];
        }
      });

      watch(
        () => flows.value.length,
        (newLength) => {
          if (currentFlow.value === null && newLength > 0) {
            handleFlowChange(flows.value[0]);
          }
          console.log(`flows.value.length changed to ${newLength}`);
        }
      );

      const handleFlowChange = (flow) => {
        flowStore.setCurrentFlow(flow);
        currentFlow.value = flow;
      };

      const isRunning = ref(false);

      baklava.commandHandler.registerCommand('Run', {
        canExecute: () => {
          return true;
        },
        execute: () => {
          engine.runOnce();
        },
      });

      baklava.editor.registerNodeType(LLMQueryNode, { category: 'Intelligence' });
      baklava.editor.registerNodeType(DisplayNode, { category: 'Interface' });

      const runFlow = () => {
        engine.runOnce();
      };

      const saveFlow = () => {
        let gt = GraphTemplate.fromGraph(baklava.displayedGraph, baklava.editor);
        let state = gt.save();
        console.log(state);
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

      return { baklava, runFlow, saveFlow, runBtnClass, runBtnText, isRunning, flows, currentFlow, handleFlowChange };
    },
  });
</script>

<style scoped></style>

<template>
  <main class="about h-screen flex flex-col">
    <NavBar></NavBar>

    <div class="flex justify-center items-center bg-gray-600 p-2">
      <span class="absolute left-0 flex items-center justify-center">
        <EditableTextField
          :text="currentFlowName"
          :isDeletable="true"
          @edit="handleFlowEdit"
          @delete="handleFlowDelete"
          class="flex mx-2 font-bold py-2 px-4 rounded bg-gray-500 text-white" />
        <button class="mx-2 font-bold py-2 px-4 rounded flex bg-green-500 text-white" @click="addFlow" title="Add Flow">
          <PlusIcon class="w-6 h-6" />
        </button>
      </span>

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
  import EditableTextField from '@/components/EditableTextField.vue';
  import { defineComponent, ref, computed, onBeforeMount, watch } from 'vue';
  import { EditorComponent, DependencyEngine, useBaklava, applyResult, GraphTemplate, Graph } from 'baklavajs';
  import { CloudArrowDownIcon, PlayIcon, PlusIcon } from '@heroicons/vue/20/solid';
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
      EditableTextField,
      CloudArrowDownIcon,
      PlayIcon,
      PlusIcon,
    },
    setup() {
      const baklava = useBaklava();
      const engine = new DependencyEngine(baklava.editor);
      const flowStore = useFlowStore();
      const currentFlow = computed(() => flowStore.getCurrentFlow);
      const currentFlowName = computed(() => flowStore.currentFlowName);
      const currentFlowState = computed(() => flowStore.currentFlowState);
      const flows = ref(flowStore.getFlows);

      const setupFlowsDropdown = async () => {
        flows.value = await flowStore.fetchFlows();
      };

      onBeforeMount(async () => {
        await setupFlowsDropdown();
      });

      watch(
        () => flowStore.getFlows,
        () => {
          flows.value = flowStore.getFlows;
        }
      );

      watch(
        () => flows.value.length,
        (newLength) => {
          if (currentFlow.value === null && newLength > 0) {
            handleFlowChange(flows.value[0]);
          }
        }
      );

      const handleFlowChange = (flow) => {
        flowStore.setCurrentFlow(flow);
        loadFlowState();
      };

      const handleFlowEdit = async (text) => {
        await flowStore.updateCurrentFlow({ name: text });
      };

      const handleFlowDelete = async () => {
        await flowStore.deleteCurrentFlow();
      };

      const addFlow = async () => {
        const newFlow = await flowStore.addFlow();
        flowStore.setCurrentFlow(newFlow);
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

      const saveFlow = async () => {
        // const graphTemplate = GraphTemplate.fromGraph(baklava.displayedGraph, baklava.editor);
        // const state = graphTemplate.save();
        const state = baklava.editor.save();
        console.log(state);
        await flowStore.updateCurrentFlow({ state });
      };

      const loadFlowState = async () => {
        // const graphTemplate = GraphTemplate.fromGraph(baklava.displayedGraph, baklava.editor);

        if (!currentFlow.value || !currentFlow.value.state) return;

        // graphTemplate.update(currentFlow.value.state);
        // graphTemplate.createGraph();

        // baklava.displayedGraph.load(currentFlow.value.state);
        // baklava.editor.load(currentFlow.value.state);

        const graphTemplate = new GraphTemplate(currentFlow.value.state, baklava.editor);
        const newGraph = new Graph(baklava.editor, graphTemplate);
        // newGraph.load(graphTemplate);

        baklava.editor.addGraphTemplate(graphTemplate);
        baklava.editor.load({
          graph: newGraph,
          graphTemplates: [graphTemplate],
        });
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
      // const node1 = addNodeWithCoordinates(LLMQueryNode, 300, 140);
      // const node2 = addNodeWithCoordinates(DisplayNode, 550, 140);
      // baklava.displayedGraph.addConnection(node1.outputs.outputText, node2.inputs.text);

      return {
        baklava,
        runFlow,
        saveFlow,
        loadFlowState,
        addFlow,
        runBtnClass,
        runBtnText,
        isRunning,
        flows,
        currentFlow,
        currentFlowName,
        currentFlowState,
        handleFlowChange,
        handleFlowEdit,
        handleFlowDelete,
      };
    },
  });
</script>

<style scoped></style>

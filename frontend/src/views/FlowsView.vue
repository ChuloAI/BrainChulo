<script setup>
  import '@/assets/flows.css';
  import { markRaw, onMounted } from 'vue';

  import NavBar from '@/components/NavBar.vue';
  import { Panel, VueFlow, useVueFlow } from '@vue-flow/core';
  import { Controls } from '@vue-flow/controls';
  import { Background, BackgroundVariant } from '@vue-flow/background';
  import { MiniMap } from '@vue-flow/minimap';
  import LLMQueryNode from '@/nodes/LLMQueryNode.vue';

  const { nodes, addNodes, addEdges, onConnect, dimensions } = useVueFlow();

  const nodeTypes = { 'llm-query': markRaw(LLMQueryNode) };

  onConnect((params) => addEdges(params));

  onMounted(() => {
    // Add an element after mount
    addNodes([
      {
        id: '1',
        type: 'llm-query',
        position: { x: 1050, y: 500 },
        label: 'LLM Query Node 1',
      },
    ]);
  });

  function addRandomNode() {
    const nodeId = (nodes.value.length + 1).toString();

    const newNode = {
      id: nodeId,
      label: `Node: ${nodeId}`,
      type: 'llm-query',
      position: { x: Math.random() * dimensions.value.width, y: Math.random() * dimensions.value.height },
    };

    addNodes([newNode]);
  }
</script>

<template>
  <main class="h-screen">
    <NavBar></NavBar>

    <VueFlow :node-types="nodeTypes">
      <Background :variant="BackgroundVariant.Lines" />

      <Panel position="top-right">
        <button
          class="btn btn-primary btn-sm m-1 p-2 rounded text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring ring-blue-300 shadow-sm"
          type="button"
          @click="addRandomNode">
          add node
        </button>
      </Panel>

      <MiniMap />
      <Controls />
    </VueFlow>
  </main>
</template>

<script>
  export default {
    components: {
      NavBar,
    },
  };
</script>

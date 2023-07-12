<script setup>
  import '@/assets/flows.css';
  import NavBar from '@/components/NavBar.vue';
  import { Panel, VueFlow, useVueFlow } from '@vue-flow/core';
  import { Controls } from '@vue-flow/controls';
  import { Background, BackgroundVariant } from '@vue-flow/background';
  import { MiniMap } from '@vue-flow/minimap';

  const { nodes, addNodes, addEdges, onConnect, dimensions } = useVueFlow();

  onConnect((params) => addEdges(params));

  function addRandomNode() {
    const nodeId = (nodes.value.length + 1).toString();

    const newNode = {
      id: nodeId,
      label: `Node: ${nodeId}`,
      position: { x: Math.random() * dimensions.value.width, y: Math.random() * dimensions.value.height },
    };

    addNodes([newNode]);
  }
</script>

<template>
  <main class="h-screen">
    <NavBar></NavBar>

    <VueFlow>
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

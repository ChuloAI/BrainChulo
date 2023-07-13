<script setup>
  import '@/assets/flows.css';
  import { markRaw, onMounted } from 'vue';

  import NavBar from '@/components/NavBar.vue';
  import { Panel, VueFlow, useVueFlow } from '@vue-flow/core';
  import { Controls } from '@vue-flow/controls';
  import { Background, BackgroundVariant } from '@vue-flow/background';
  import { MiniMap } from '@vue-flow/minimap';
  import LLMQueryNode from '@/nodes/LLMQueryNode.vue';
  import TextNode from '../nodes/TextNode.vue';

  const { nodes, addNodes, addEdges, onConnect, dimensions } = useVueFlow();

  const nodeTypes = { 'llm-query': markRaw(LLMQueryNode), text: markRaw(TextNode) };

  onConnect((params) => addEdges(params));

  onMounted(() => {
    // Add an element after mount
    addNodes([
      {
        id: '1',
        type: 'llm-query',
        position: { x: 750, y: 300 },
        label: 'LLM Query Node 1',
        connectable: true,
      },
      {
        id: '2',
        type: 'text',
        position: { x: 1050, y: 300 },
        label: 'Text Node 1',
        connectable: true,
      },
    ]);

    addEdges({
      id: 'e1-2',
      source: '1',
      target: '2',
    });
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

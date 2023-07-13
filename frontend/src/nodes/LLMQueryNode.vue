<script>
  import { Handle, Position } from '@vue-flow/core';
  import InternalService from '@/services/internal';

  export default {
    name: 'LLMQueryNode',
    components: {
      Handle,
    },
    data() {
      return {
        query: '',
        parameters: {},
        results: [],
        expandParameters: false,
        Position: Position,
      };
    },
    methods: {
      async run() {
        const userMessageResponse = await InternalService.queryLLM(null, this.query, this.parameters);
        console.log(userMessageResponse);
      },
    },
  };
</script>

<template>
  <div>
    <Handle type="target" :position="Position.Top" />
    <h1>LLM Query</h1>
    <div class="node-content">
      <textarea v-model="query" placeholder="Enter your query"></textarea>
      <div :class="{ hidden: expandParameters, 'h-auto': expandParameters }" class="expand-btn">
        <button @click="expandParameters = !expandParameters" class="text-blue-300">&gt; Parameters</button>
      </div>
      <div :class="{ hidden: !expandParameters, 'h-auto': expandParameters }">
        <div class="expand-btn">
          <button @click="expandParameters = !expandParameters" class="text-blue-300">&lt; Parameters</button>
        </div>
        <input type="checkbox" v-model="parameters.param1" />
        Param 1
        <input type="checkbox" v-model="parameters.param2" />
        Param 2
      </div>
    </div>
    <div class="node-footer">
      <button
        @click="run"
        class="btn btn-primary btn-sm m-1 p-2 rounded text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring ring-blue-300 shadow-sm">
        Make Query
      </button>
    </div>

    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

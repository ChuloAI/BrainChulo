import { defineStore } from 'pinia';
import internalService from '@/services/internal';

export const useFlowStore = defineStore('flow', {
  state: () => ({
    allFlows: [],
    currentFlow: null,
  }),
  actions: {
    async fetchFlows() {
      let response = await internalService.request('/flows', 'GET');
      let flows = response;

      if (flows.length < 1) {
        await internalService.request('/flows', 'POST', { name: 'New Flow' });
        return this.fetchFlows();
      }

      this.allFlows = flows.map((flow) => {
        return {
          id: flow.id,
          label: flow.name,
        };
      });

      return this.allFlows;
    },
    setCurrentFlow(newFlow) {
      this.currentFlow = this.allFlows.find((flow) => flow.id === newFlow.id);
    }
  },
});

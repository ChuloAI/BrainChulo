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
        await this.addFlow();
        return await this.fetchFlows();
      }

      this.allFlows = await Promise.all(flows.map(async (flow) => {
        return {
          id: flow.id,
          label: flow.name,
          state: flow.state,
        };
      }));

      return this.allFlows;
    },
    setCurrentFlow(newFlow) {
      if(!newFlow && this.allFlows.length > 0) {
        this.currentFlow = this.allFlows[0];
        return;
      }
      else if(!newFlow) {
        this.currentFlow = null;
        return;
      }

      this.currentFlow = this.allFlows.find((flow) => flow.id === newFlow.id);
    },
    async updateCurrentFlow(newData) {
      const { name, state } = newData;
      const updates = {};

      if (name) {
        updates.name = name;
      }

      if (state) {
        updates.state = state;
      }

      if (Object.keys(updates).length === 0) {
        return;
      }

      await internalService.request(`/flows/${this.currentFlowId}`, 'PUT', updates);

      await this.fetchFlows();
      this.setCurrentFlow(this.getCurrentFlow);
    },

    async addFlow() {
      const newFlow = await internalService.request('/flows', 'POST', { name: 'New Flow' });
      await this.fetchFlows();

      return newFlow;
    },

    async deleteCurrentFlow() {
      await this.deleteFlow(this.currentFlowId);
      this.setCurrentFlow(null);
    },

    async deleteFlow(flowId) {
      await internalService.request(`/flows/${flowId}`, 'DELETE');
      await this.fetchFlows();
    }
  },
  getters: {
    getFlows: (state) => state.allFlows,
    getCurrentFlow: (state) => state.currentFlow,
    currentFlowId: (state) => state.currentFlow?.id,
    currentFlowName: (state) => state.currentFlow?.label,
    currentFlowState: (state) => state.currentFlow?.state
  }
});

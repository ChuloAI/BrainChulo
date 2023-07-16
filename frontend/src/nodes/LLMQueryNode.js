import {
  defineNode,
  TextInputInterface,
  NodeInterface
} from "baklavajs";

import InternalService from "@/services/internal.js";

export const LLMQueryNode = defineNode({
  type: "LLMQueryNode",
  title: "LLM Query",
  inputs: {
    query: () =>
      new TextInputInterface("Query", ""),
  },
  outputs: {
    outputText: () => new NodeInterface("Output Text", "")
  },
  async calculate({ query }) {
    const userMessageResponse = await InternalService.queryLLM(null, query);
    console.log(userMessageResponse);
    return { outputText: userMessageResponse };
  }
});

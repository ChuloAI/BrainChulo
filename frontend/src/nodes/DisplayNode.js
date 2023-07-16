import { defineNode, NodeInterface, TextInterface } from "baklavajs";

export const DisplayNode = defineNode({
  type: "DisplayNode",
  title: "Display",
  inputs: {
    text: () => new NodeInterface("Text", "HI")
  },
  outputs: {
    display: () => new TextInterface("Display")
  },
  calculate({ text }) {
    console.log(text)
    return {
      display: text
    };
  }
});

import { defineNode, NodeInterface, TextInterface } from "baklavajs";

export const DisplayNode = defineNode({
  type: "DisplayNode",
  title: "Display Text",
  inputs: {
    text: () => new NodeInterface("Text", "HI")
  },
  outputs: {
    display: () => new TextInterface("Display")
  },
  calculate({ text }) {
    document.getElementById(this.id).classList.add('active');
    console.log(text)

    document.getElementById(this.id).classList.remove('active');
    return {
      display: text
    };
  }
});

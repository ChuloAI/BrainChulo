from typing import Dict, Callable
from andromeda_chain import AndromedaChain
from agents.flow_based import BaseFlowAgent
from app.flow.flow import Flow, PromptNode, ToolNode, ChoiceNode
from prompts.guicance_cot import ChainOfThoughts


class ChainOfThoughtsAgent(BaseFlowAgent):
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]]):
        super().__init__(andromeda, tools, flow)
        self.valid_tools = list(tools.keys()) + ["Reply"]
        self.valid_answers = ["Action", "Final Answer"]

        def execute_tool(variables):
            action_name = variables["action"]
            action_input = variables["action_input"]
            return self.do_tool(action_name, action_input)

        node1 = PromptNode("start", ChainOfThoughts.prompt_start)
        node2 = PromptNode("thought", ChainOfThoughts.thought_gen)
        node3 = PromptNode("choose_action", ChainOfThoughts.choose_action)
        node4 = PromptNode("perform_action", ChainOfThoughts.action_input)
        node5 = ToolNode("execute_tool", execute_tool)
        node6 = ChoiceNode("decide", ["thought", "final_prompt"])
        node7 = PromptNode("final_prompt", ChainOfThoughts.final_prompt)

        flow = Flow(
            [node1, node2, node3, node4, node5, node6, node7]
        )

        self.flow = flow
from typing import Dict, Callable
from andromeda_chain import AndromedaChain
from agents.flow_based import BaseFlowAgent
from flow.flow import Flow, PromptNode, ToolNode, ChoiceNode, StartNode
from prompts.flow_guidance_cot import FlowChainOfThoughts, PROMPT_START_STRING


class ChainOfThoughtsAgent(BaseFlowAgent):
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]]):
        def execute_tool(variables):
            action_name = variables["tool_name"]
            action_input = variables["act_input"]
            return self.do_tool(action_name, action_input)

        start = StartNode("start", FlowChainOfThoughts.flow_prompt_start, {
            "Action": "choose_action",
            "Final Answer": "final_prompt"
        })
        thought = PromptNode("thought", FlowChainOfThoughts.thought_gen)
        choose_action = PromptNode("choose_action", FlowChainOfThoughts.choose_action)
        perform_action = PromptNode("perform_action", FlowChainOfThoughts.action_input)
        execute_tool_node = ToolNode("execute_tool", execute_tool)
        decide = ChoiceNode("decide", ["thought", "final_prompt"], max_decisions=3, force_exit_on="final_prompt")
        final = PromptNode("final_prompt", FlowChainOfThoughts.final_prompt)

        thought.set_next(choose_action)
        choose_action.set_next(perform_action)
        perform_action.set_next(execute_tool_node)
        execute_tool_node.set_next(decide)

        flow = Flow(
            [start, thought, choose_action, perform_action, execute_tool_node, decide, final]
        )

        super().__init__(andromeda, tools, flow)
        self.valid_tools = list(tools.keys())
        self.valid_answers = ["Action", "Final Answer"]


    def run(self, query: str) -> str:
        return super().run(query, variables={
            "prompt_start": PROMPT_START_STRING,
            "question": query,
            "valid_tools": self.valid_tools,
            "valid_answers": self.valid_answers,
        })
from typing import Dict, Callable
from andromeda_chain import AndromedaChain
from agents.flow_based import BaseFlowAgent
from flow.flow import Flow, PromptNode, ToolNode, ChoiceNode
from prompts.guicance_cot import ChainOfThoughts, PROMPT_START_STRING


class ChainOfThoughtsAgent(BaseFlowAgent):
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]]):
        def execute_tool(variables):
            action_name = variables["tool_name"]
            action_input = variables["actInput"]
            return self.do_tool(action_name, action_input)

        start = PromptNode("start", ChainOfThoughts.prompt_start)
        thought = PromptNode("thought", ChainOfThoughts.thought_gen)
        choose_action = PromptNode("choose_action", ChainOfThoughts.choose_action)
        perform_action = PromptNode("perform_action", ChainOfThoughts.action_input)
        execute_tool_node = ToolNode("execute_tool", execute_tool)
        decide = ChoiceNode("decide", ["thought", "final_prompt"])
        final = PromptNode("final_prompt", ChainOfThoughts.final_prompt)

        start.set_next(choose_action)
        thought.set_next(choose_action)

        choose_action.set_next(perform_action)
        perform_action.set_next(execute_tool_node)
        execute_tool_node.set_next(decide)

        flow = Flow(
            [start, thought, choose_action, perform_action, execute_tool_node, decide, final]
        )

        super().__init__(andromeda, tools, flow)
        self.valid_tools = list(tools.keys()) + ["Reply"]
        self.valid_answers = ["Action", "Final Answer"]


    def run(self, query: str) -> str:
        super().run(query, variables={
            "prompt_start": PROMPT_START_STRING,
            "question": query,
            "valid_tools": self.valid_tools,
            "valid_answers": self.valid_answers,
        })
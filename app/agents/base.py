# import the necessary libraries
from abc import abstractmethod
from colorama import Style, Fore
from typing import List
from andromeda_chain import AndromedaChain
from tools.base import BaseTool

def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL, flush=True)


class BaseAgent:
    """Base Agent.

    Nothing too exciting here.
    """
    def __init__(self, andromeda: AndromedaChain, tools: List[BaseTool]):
        self.andromeda = andromeda
        self.tools = tools
    
    @abstractmethod
    def run(self, query: str) -> str:
        raise NotImplementedError()
    
    def do_tool(self, tool_name, act_input):
        color_print(f"Using tool: {tool_name}", Fore.GREEN)
        result = self.tools[tool_name](act_input)
        color_print(f"Tool result: {result}", Fore.BLUE)
        return result

    def _build_tool_description_line(self, tool: BaseTool):
        return f"{tool.name}: {tool.short_description()}"

    def prepare_start_prompt(self, prompt_start_template):
        tools = [item for _, item in self.tools.items()]
        tools_descriptions = "\n".join([self._build_tool_description_line(tool) for tool in tools])
        action_list = str([tool.name for tool in tools]).replace('"', "")
        few_shot_examples = "\n".join(
            [
                f"Example {idx}:\n{tool.few_shot_examples()}"
                for idx, tool in enumerate(tools)
            ]
        )
        self.valid_tools = [tool.name for tool in tools]
        self.prepared_prompt = prompt_start_template.format(
            tools_descriptions=tools_descriptions,
            action_list=action_list,
            few_shot_examples=few_shot_examples
        )

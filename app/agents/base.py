# import the necessary libraries
from abc import abstractmethod
from colorama import Style, Fore
from typing import Dict, Callable
from andromeda_chain import AndromedaChain

def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL, flush=True)


class BaseAgent:
    """Base Agent.
    
    Nothing too exciting here.
    """
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]]):
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


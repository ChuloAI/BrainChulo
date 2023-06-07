# import the necessary libraries
from typing import Dict, Callable
from agents.base import BaseAgent
from colorama import Style
from andromeda_chain import AndromedaChain
from flow.flow import Flow

def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL)


class BaseFlowAgent(BaseAgent):
    """Base Flow Agent.

    Implements a graph that the agents execute.
    """
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]], flow: Flow):
        super().__init__(andromeda, tools)
        self.flow = flow

    def run(self, query: str) -> str:
        return self.flow.execute(self.chain, query)
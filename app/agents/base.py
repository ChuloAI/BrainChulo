# import the necessary libraries
from abc import abstractmethod
from colorama import Style

def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL)


class BaseAgent:
    """Base Agent.
    
    Nothing too exciting here.
    """
    
    @abstractmethod
    def run(self, query: str) -> str:
        raise NotImplementedError()
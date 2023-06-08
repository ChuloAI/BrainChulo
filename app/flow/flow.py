from abc import abstractmethod
from colorama import Fore
from typing import List, Union, Dict
from andromeda_chain import AndromedaChain, AndromedaPrompt, AndromedaResponse
from agents.base import color_print
from prompts.guidance_choice import CHOICE_PROMPT
from copy import deepcopy

class Node:
    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def run(self, variables) -> Union[AndromedaResponse, Dict[str, str]]:
        raise NotImplementedError()


class HiddenNode(Node):
    """Classes of nodes that can be executed in the background,
    without expanding the context history for the agent.
    """

class ChoiceNode(HiddenNode):
    def __init__(self, name, choices: List[str], max_decisions, force_exit_on) -> None:
        super().__init__(name)
        self.choices = choices
        self.max_decisions = max_decisions
        self.force_exit_on=force_exit_on
        self.decisions_made = 0

    def run(self, chain: AndromedaChain, variables) -> AndromedaResponse:        
        if self.decisions_made >= self.max_decisions:
            return self.force_exit_on

        history = ""
        if "history" in variables:
            history = variables["history"]

        result = chain.run_guidance_prompt(
            CHOICE_PROMPT,
            input_vars={
                "history": history,
                "valid_choices": self.choices
            }
        )
        self.decisions_made += 1
        return result.result_vars["choice"]

    def set_next(self, next_):
        self._next = next_


    def next(self):
        return self._next


class ToolNode(Node):
    def __init__(self, name, tool_callback, variable_name = "observation") -> None:
        super().__init__(name)
        self.tool_callback = tool_callback
        self.variable_name = variable_name

    def run(self, variables) -> Dict[str, str]:        
        return {self.variable_name: self.tool_callback(variables)}

    def set_next(self, next_):
        self._next = next_

    def next(self):
        return self._next



class PromptNode(Node):
    def __init__(self, name, prompt: AndromedaPrompt) -> None:
        super().__init__(name)
        self.prompt = prompt
        self._next = None

    def run(self, chain: AndromedaChain, variables) -> AndromedaResponse:        
        input_dict = {}
        for var_ in self.prompt.input_vars:
            value = variables[var_]
            input_dict[var_] = value

        return chain.run_guidance_prompt(
            self.prompt,
            input_vars=input_dict
        )

    def set_next(self, next_):
        self._next = next_


    def next(self):
        return self._next


class Flow:
    def __init__(self, nodes: List[PromptNode]) -> None:
        assert len(nodes) > 0
        self.nodes = nodes
    
    def execute(self, chain, query: str, variables: Dict[str, str], return_key="final_answer"):
        node = self.nodes[0]
        variables = {**variables, "query": query}
        while node:
            color_print(f"---> On node {node.name}", Fore.RED)
            if isinstance(node, PromptNode): 
                debug_vars = deepcopy(variables)
                if "history" in debug_vars:
                    debug_vars.pop("history")
                if "prompt_start" in debug_vars:
                    debug_vars.pop("prompt_start")

                color_print(f"Executing node {node.name} with variables: {debug_vars}", Fore.YELLOW)
                result = node.run(chain, variables)
                color_print(f"Node result: {result.result_vars}", Fore.GREEN)
                history = result.expanded_generation
                # Merge contexts
                variables = {**variables, **result.result_vars, "history": history}
                node = node.next()
            elif isinstance(node, ToolNode):
                color_print(f"Executing tool node {node.name} with variables: {debug_vars}", Fore.YELLOW)
                tool_result = node.run(variables)
                variables = {**variables, **tool_result}
                node = node.next()
            elif isinstance(node, ChoiceNode):
                color_print(f"Executing choice node {node.name} with variables: {debug_vars}", Fore.YELLOW)
                choice = node.run(chain, variables)
                new_node = None
                for n in self.nodes:
                    if n.name == choice:
                        new_node = n
                        break
                if not new_node:
                    raise ValueError(f"Choice {choice} led to limbo! Please choose the name of another node in the flow.")
                if new_node == node: 
                    raise ValueError(f"Choice {choice} led to an infinite loop on itself! Make sure choice node hop to itself.")
                node = new_node
            else:
                raise ValueError(f"Invalid node class: {type(node)}")


        color_print(f"Flow ended, returning variable '{return_key}'.", Fore.GREEN)
        return variables[return_key] 

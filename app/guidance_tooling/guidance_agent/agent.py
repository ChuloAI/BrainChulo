# import the necessary libraries
from typing import Callable, Dict

from colorama import Fore
from colorama import Style
from prompts.guicance_cot import ChainOfThoughts, PROMPT_START_STRING
from prompts import guidance_check_question
from andromeda_chain import AndromedaChain


def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL)


class AgentHistory:
    def __init__(self) -> None:
        self.raw_history = []

    def append(self, item):
        self.raw_history.append(item)

    def __str__(self) -> str:
        return str(self.raw_history)




class CustomAgentGuidance:
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]], num_iter=3):
        self.andromeda = andromeda
        self.tools = tools
        self.num_iter = num_iter
        self.valid_tools = list(tools.keys())
        self.valid_answers = ["Action", "Final Answer"]

    def do_tool(self, tool_name, act_input):
        color_print(f"Using tool: {tool_name}", Fore.GREEN)
        result = self.tools[tool_name](act_input)
        color_print(f"Tool result: {result}", Fore.BLUE)
        return result

    def __call__(self, query):
        print(self.valid_answers)
        result_start = self.andromeda.run_guidance_prompt(
            ChainOfThoughts.prompt_start,
            input_vars={
                "prompt_start": PROMPT_START_STRING,
                "question": query,
            },
        )
        history = result_start.expanded_generation
        color_print(f"Result start: {result_start.result_vars}", Fore.YELLOW)
        for _ in range(self.num_iter - 1):

            # Choose action
            chosen_action = self.andromeda.run_guidance_prompt(
                ChainOfThoughts.choose_action,
                input_vars={
                    "history": history,
                    "valid_tools": self.valid_tools,
                },
            )
            color_print(f"Chosen action: {chosen_action.result_vars}", Fore.GREEN)


            # Provide action input
            action_input = self.andromeda.run_guidance_prompt(
                ChainOfThoughts.action_input,
                input_vars={
                    "history": history
                }
            )
            color_print(f"Action Input: {action_input.result_vars}", Fore.YELLOW)
            
            # Execute tool
            observation = self.do_tool(chosen_action.result_vars["tool_name"], action_input.result_vars["actInput"])
            color_print(f"Observation: {observation}", Fore.LIGHTMAGENTA_EX)

            if "Search" in chosen_action.result_vars["tool_name"]:
                check_question = self.andromeda.run_guidance_prompt(
                    guidance_check_question.PROMPT_CHECK_QUESTION,
                    input_vars={
                        "context": observation,
                        "question": query,
                    }
                )
                if check_question.result_vars["answer"] == "no":
                    color_print(f"I don't know", Fore.RED)
                    return "I cannot answer this question given the context."

            if chosen_action.result_vars["tool_name"] == "Final Answer":
                return observation

        
        history = history
        prompt_mid = history + "{{gen 'fn' stop='\\n'}}"
        result_final = self.andromeda.run_guidance_prompt(
            prompt_mid,
            {}
        )

        return result_final

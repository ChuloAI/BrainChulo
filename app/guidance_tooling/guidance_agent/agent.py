# import the necessary libraries
from typing import Callable, Dict

from colorama import Fore
from colorama import Style
from guidance_tooling.guidance_templates import guicance_cot
from guidance_tooling.guidance_client.guidance_client import run_guidance_prompt


def color_print(msg, color):
    print(color + Style.BRIGHT + msg  + Style.RESET_ALL)


class CustomAgentGuidance:
    def __init__(self, tools: Dict[str, Callable[[str], str]], num_iter=3):
        self.tools = tools
        self.num_iter = num_iter
        self.pass_through_tool = "Reply"
        self.valid_tools = list(tools.keys()).append(self.pass_through_tool)
        self.valid_answers = ["Action", "Final Answer"]

    def do_tool(self, tool_name, act_input):
        color_print(f"Using tool: {tool_name}", Fore.GREEN)
    
        if tool_name == self.pass_through_tool:
            result = act_input
        else:
            result = self.tools[tool_name](act_input)
    
        color_print(f"Tool result: {result}", Fore.BLUE)
        return result

    def __call__(self, query):
        prompt_start = guicance_cot.PROMPT_START_TEMPLATE
        result_start = run_guidance_prompt(
            prompt_start,
            input_vars={
                "question": query,
                "valid_answers": self.valid_answers
            },
        )
        color_print(f"Result start: {result_start}", Fore.YELLOW)
        result_mid = result_start

        for _ in range(self.num_iter - 1):
            if result_mid["answer"] == "Final Answer":
                break
            history = result_mid.__str__()

            choose_action_prompt = guicance_cot.PROMPT_CHOOSE_ACTION_TEMPLATE

            chosen_action = run_guidance_prompt(choose_action_prompt,
                input_vars={
                    "history": history,
                    "valid_tools": self.valid_tools,
                },
            )
            color_print(f"Chosen action: {chosen_action}", Fore.GREEN)

            prompt_action_input = guicance_cot.PROMPT_ACTION_INPUT_TEMPLATE
            action_input = run_guidance_prompt(
                prompt_action_input,
                input_vars={
                    "history": history
                }
            )
            color_print(f"Action Input: {action_input}", Fore.YELLOW)
            
            observation = self.do_tool(chosen_action["tool_name"], action_input["actInput"])

            color_print(f"Observation: {observation}", Fore.LIGHTMAGENTA_EX)

            if "no" in observation.lower():
                color_print(f"I don't know", Fore.RED)
                break

        if "Observation:  No" in str(result_mid):
            result_final = "I cannot answer this question given the context"

        elif result_mid["answer"] != "Final Answer":
            color_print("I broke something here", Fore.RED)
            result_final = "I'm broke, sorry"
        else:
            history = result_mid.__str__()
            prompt_mid = history + "{{gen 'fn' stop='\\n'}}"
            result_final = run_guidance_prompt(
                prompt_mid,
                {}
            )

        return result_final

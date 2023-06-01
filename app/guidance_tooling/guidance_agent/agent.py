# import the necessary libraries
from typing import Callable, Dict

from colorama import Fore
from colorama import Style
from guidance_tooling.guidance_templates import guicance_cot
from guidance_tooling.guidance_client.guidance_client import run_guidance_prompt


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
    def __init__(self, tools: Dict[str, Callable[[str], str]], num_iter=3):
        self.tools = tools
        self.num_iter = num_iter
        self.pass_through_tool = "Reply"
        self.valid_tools = list(tools.keys()) + [self.pass_through_tool]
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
        print(self.valid_answers)
        result_start = run_guidance_prompt(
            prompt_start,
            input_vars={
                "question": query,
                "valid_options": self.valid_answers
            },
        )
        history = result_start.pop("__main__")
        color_print(f"Result start: {result_start}", Fore.YELLOW)
        result_mid = result_start
        # Copying langchain

        for _ in range(self.num_iter - 1):
            if result_mid["answer"] == "Final Answer":
                break

            # Choose action
            choose_action_prompt = guicance_cot.PROMPT_CHOOSE_ACTION_TEMPLATE
            chosen_action = run_guidance_prompt(choose_action_prompt,
                input_vars={
                    "history": history,
                    "valid_tools": self.valid_tools,
                },
            )
            history = chosen_action.pop("__main__")
            color_print(f"Chosen action: {chosen_action}", Fore.GREEN)


            # Provide action input
            prompt_action_input = guicance_cot.PROMPT_ACTION_INPUT_TEMPLATE
            action_input = run_guidance_prompt(
                prompt_action_input,
                input_vars={
                    "history": history
                }
            )
            history = action_input.pop("__main__")
            color_print(f"Action Input: {action_input}", Fore.YELLOW)
            
            # Execute tool
            observation = self.do_tool(chosen_action["tool_name"], action_input["actInput"])
            color_print(f"Observation: {observation}", Fore.LIGHTMAGENTA_EX)

            # TODO: bring old langchain prompt to guidance (guidance_check_question.py)
            if "Observation: no" in observation:
                color_print(f"I don't know", Fore.RED)
                break

            if chosen_action["tool_name"] == "Reply":
                return observation

        if "Observation: no" in str(result_mid):
            result_final = "I cannot answer this question given the context"

        elif result_mid["answer"] != "Final Answer":
            color_print("Broken flow", Fore.RED)
            return "I'm broke, sorry"
        else:
            history = history
            prompt_mid = history + "{{gen 'fn' stop='\\n'}}"
            result_final = run_guidance_prompt(
                prompt_mid,
                {}
            )

        return result_final

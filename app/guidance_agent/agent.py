# import the necessary libraries
from typing import Callable, Dict

from colorama import Fore
from colorama import Style
from guidance_templates import guidance_basic_prompts


valid_answers = ["Action", "Final Answer", "Failed Check"]
valid_tools = ["Chroma Search", "Check Question"]


class CustomAgentGuidance:
    def __init__(
        self, llm, guidance: guidance, tools: Dict[str, Callable[[str], str]], num_iter=3
    ):
        self.llm = llm
        self.guidance = guidance
        self.tools = tools
        self.num_iter = num_iter

    def do_tool(self, tool_name, actInput):
        print(Fore.GREEN + Style.BRIGHT + f"Using tool: {tool_name}" + Style.RESET_ALL)
        result = self.tools[tool_name](actInput)
        print(result)
        return result

    def __call__(self, query):
        prompt_start = self.guidance(guidance_basic_prompts.PROMPT_START_TEMPLATE, llm=self.llm)
        result_start = prompt_start(question=query, valid_answers=valid_answers)
        result_mid = result_start

        for _ in range(self.num_iter - 1):
            if result_mid["answer"] == "Final Answer":
                break
            history = result_mid.__str__()
            prompt_mid = self.guidance(guidance_basic_prompts.PROMPT_MID_TEMPLATE)
            result_mid = prompt_mid(
                history=history,
                do_tool=self.do_tool,
                valid_answers=valid_answers,
                valid_tools=valid_tools,
            )
            print(Fore.YELLOW + Style.BRIGHT + str(result_mid) + Style.RESET_ALL)
            if "Observation:  No" in str(result_mid):
                print(Fore.RED + Style.BRIGHT + f"I don't know" + Style.RESET_ALL)
                break

        if "Observation:  No" in str(result_mid):
            result_final = "I cannot answer this question given the context"

        elif result_mid["answer"] != "Final Answer":
            history = result_mid.__str__()
            prompt_mid = self.guidance(guidance_basic_prompts.PROMPT_FINAL_TEMPLATE)
            result_final = prompt_mid(
                history=history,
                do_tool=self.do_tool,
                valid_answers=["Final Answer"],
                valid_tools=valid_tools,
            )

        else:
            history = result_mid.__str__()
            prompt_mid = self.guidance(history + "{{gen 'fn' stop='\\n'}}")
            result_final = prompt_mid()

        return result_final

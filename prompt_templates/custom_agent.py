from langchain.agents import (
    Tool,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish

import re
from typing import List, Union


template = """You're am AI that helps a human. You should follow all instructions to the best of your abilities.

The human may have told you things in the past. Here are the most recent messages you remember:

{history}

You should ALWAYS think what to do next, step-by-step.

You have the available tools available:

{tools}

Use the following format:

Thought: how can I better serve the human request
Action: the action to take if required - if, and only if, you decide to take an action, it should be one of [{tool_names}]
Action Input: the input to the action
Observation: The result of your last action
... (this Thought/Action/Action Input/Source Code/Code Result can repeat N times)

Final Answer: the answer that will be given to the human


A few examples to help you along the way:

Human: Hi, how are you doing?
Thought: I should answer the human with a polite greeting.
Action: Say
Action Input:
I'm well, how about you?
Observation:

Now we begin for real!

{agent_scratchpad}

Human: {input}
Thought:"""


# Set up a prompt template
class CustomAgentPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        print("input kwargs ", kwargs)
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "

        raw_history = kwargs.pop("history")
        history = ""
        for item in raw_history:
            history += f"Human: {item[0]}\n"
            if item[1]:
                history += f"AI: {item[1]}\n"

        kwargs["history"] = history

        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


def parse_action(llm_output):
    regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
    match = re.search(regex, llm_output, re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse LLM output: `{llm_output}`")
    action = match.group(1).strip()
    action_input = match.group(2)
    return action, action_input


class CustomAgentOutputParser(AgentOutputParser):
    tools: List[Tool]

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print("llm output: ", llm_output, "end of llm ouput")

        # Parse out the action and action input
        action, action_input = parse_action(llm_output)
        print(f"Parsed Action: '{action}'")
        tools_names = [tool.name for tool in self.tools]
        if action == "Say" or action not in tools_names:
            if "Observation" in action_input:
                action_input = action_input.split("Observation")[0]
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": action_input},
                log=llm_output,
            )
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )


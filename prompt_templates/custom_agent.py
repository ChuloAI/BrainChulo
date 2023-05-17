from langchain.agents import (
    Tool,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish

import re
from typing import List, Union


template = """You're am AI that helps a human. You should follow all instructions to the best of your abilities.

The human may have told you things in the past.

Things in the recent past that you recall:

{recent_messages}

You should ALWAYS think what to do next, step-by-step.

Use the following format:

Thought: how can I better serve the human request
Action: the action to take if required - if, and only if, you decide to take an action, it should be one of [{tool_names}]
Action Input: the input to the action
Observation: The result of your last action
... (this Thought/Action/Action Input/Source Code/Code Result can repeat N times)

Final Answer: the answer that will be given to the human

Now we serve a real human request

Human: {input}

{agent_scratchpad}

Thought:"""


# Set up a prompt template
class CustomAgentPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "

        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)



class CustomAgentOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print("llm output: ", llm_output, "end of llm ouput")
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )


from andromeda_chain.prompt import AndromedaPrompt

PROMPT_START_STRING = """You're an AI assistant with access to tools.
You're nice and friendly, and try to answer questions to the best of your ability.
You have access to the following tools.

{tools_descriptions}

Strictly use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {action_list}
Action Input: the input to the action, should be a question.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

When chatting with the user, you can search information using your tools.
{few_shot_examples}

Now your turn.
Question:"""


class FlowChainOfThoughts:
    choose_action = AndromedaPrompt(
        name="cot_choose_action",
        prompt_template="""{{history}}
Action: {{select 'tool_name' options=valid_tools}}""",
        guidance_kwargs={},
        input_vars=["history", "valid_tools"],
        output_vars=["tool_name"],
    )

    action_input = AndromedaPrompt(
        name="cot_action_input",
        prompt_template="""{{history}}{{gen 'act_input' stop='\\n'}}""",
        guidance_kwargs={},
        input_vars=["history"],
        output_vars=["act_input"],
    )

    thought_gen = AndromedaPrompt(
        name="cot_thought_gen",
        prompt_template="""{{history}}
Observation: {{observation}}
Thought: {{gen 'thought' temperature=0.2 stop='\\n'}}""",
        guidance_kwargs={},
        input_vars=["history", "observation"],
        output_vars=["thought"],
    )

    final_prompt = AndromedaPrompt(
        name="cot_final",
        prompt_template="""{{history}}
Final Answer: {{gen 'final_answer' temperature=0.2 stop='\\n'}}""",
        guidance_kwargs={},
        input_vars=["history"],
        output_vars=["final_answer"],
    )

    flow_prompt_start = AndromedaPrompt(
        name="cot_flow_prompt_start",
        prompt_template="""{{prompt_start}} {{question}}
Thought: {{gen 'thought' stop='\\n' temperature=0.2}}{{#block hidden=True}}
{{select 'choice' logprobs='logprobs' options=valid_answers}}
:{{/block}}""",
        guidance_kwargs={},
        input_vars=["prompt_start", "question", "valid_answers"],
        output_vars=["thought", "choice"],
    )

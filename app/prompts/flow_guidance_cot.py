from andromeda_chain.prompt import AndromedaPrompt

PROMPT_START_STRING = """You're an AI assistant with access to tools.
You're nice and friendly, and try to answer questions to the best of your ability.
You have access to the following tools.

Conversation Search: A tool to validate if a question is answerable or not. The input is the question to validate.
Document Search: A wrapper around Document Search. Useful for when you need to answer questions about current events. The input is the question to search relevant information.

Strictly use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Conversation Search, Document Search]
Action Input: the input to the action, should be a question.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

When chatting with the user, you can search information using your tools. Here is an example:

Question: What's your name?
Thought: I should search my name in the documents.
Action: Document Search
Action Input:
What's my name?
Observation: You're an AI. You don't have a name.
Thought: I should answer that I don't have a name.
Final Answer: As an AI, I don't have a name, at least not in the human sense.

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
Thought: {{gen 'thought' stop='\\n'}}""",
        guidance_kwargs={},
        input_vars=["history", "observation"],
        output_vars=["thought"],
    )

    final_prompt = AndromedaPrompt(
        name="cot_final",
        prompt_template="""{{history}}
Final Answer: {{gen 'final_answer' stop='\\n'}}""",
        guidance_kwargs={},
        input_vars=["history"],
        output_vars=["final_answer"],
    )

    flow_prompt_start = AndromedaPrompt(
        name="cot_flow_prompt_start",
        prompt_template="""{{prompt_start}} {{question}}
Thought: {{gen 'thought' stop='\\n'}}{{#block hidden=True}}{{select 'choice' logprobs='logprobs' options=valid_answers}}:{{/block}}""",
        guidance_kwargs={},
        input_vars=["prompt_start", "question", "valid_answers"],
        output_vars=["thought", "choice"],
    )

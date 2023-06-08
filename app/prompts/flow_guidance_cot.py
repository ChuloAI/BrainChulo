from andromeda_chain.prompt import AndromedaPrompt

PROMPT_START_STRING = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
Answer the following questions as best you can. You have access to the following tools. If you don't know the answer, say don't know. If you don't find it in the documents or previous conversations, say so. 
Question:"""


class FlowChainOfThoughts:
    choose_action = AndromedaPrompt(
    name="cot_choose_action",
    prompt_template = """{{history}}
Action: {{select 'tool_name' options=valid_tools}}""",
    guidance_kwargs={},
    input_vars=["history", "valid_tools"],
    output_vars=["tool_name"],
)


    action_input = AndromedaPrompt(
    name="cot_action_input",
    prompt_template = """{{history}}{{gen 'act_input' stop='\\n'}}""",
    guidance_kwargs={},
    input_vars=["history"],
    output_vars=["act_input"],
)


    thought_gen = AndromedaPrompt(
    name="cot_thought_gen",
    prompt_template = """{{history}}
Observation: {{observation}}
Thought: {{gen 'thought' stop='\\n'}}""",
    guidance_kwargs={},
    input_vars=["history", "observation"],
    output_vars=["thought"],
)

    final_prompt = AndromedaPrompt(
    name="cot_final",
    prompt_template = """{{history}}
Final Answer: {{gen 'final_answer' stop='\\n'}}""",
    guidance_kwargs={},
    input_vars=["history"],
    output_vars=["final_answer"],
)


    flow_prompt_start = AndromedaPrompt(
    name="cot_flow_prompt_start",
    prompt_template = """{{prompt_start}} {{question}}
Thought: {{gen 'thought' stop='\\n'}}{{#block hidden=True}}{{select 'choice' logprobs='logprobs' options=valid_answers}}:{{/block}}""",
    guidance_kwargs={},
    input_vars=["prompt_start", "question", "valid_answers"],
    output_vars=["thought", "choice"],
)
from guidance_tooling.guidance_prompt import GuidancePrompt


PROMPT_START_TEMPLATE = GuidancePrompt(
    name="cot_start",
    prompt_template="""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
Answer the following questions as best you can. You have access to the following tools:

Check Question: A tool to validate if a question is answerable or not. The input is the question to validate.

Chroma Search: A wrapper around Chroma Search. Useful for when you need to answer questions about current events. The input is the question to search relevant information.

Strictly use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Check Question, Chroma Search]
Action Input: the input to the action, should be a question.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

For examples:
Question: How old is the CEO of Microsoft's wife?
Thought: First, I need to check if the question is answerable.
Action: Check Question
Action Input: How old is the CEO of Microsoft's wife?
Observation: The question is answerable.
Thought: Now, I need to find who is the CEO of Microsoft.
Action: Chroma Search
Action Input: Who is the CEO of Microsoft?
Observation: Satya Nadella is the CEO of Microsoft.
Thought: Now, I should find out Satya Nadella's wife.
Action: Chroma Search
Action Input: Who is Satya Nadella's wife?
Observation: Satya Nadella's wife's name is Anupama Nadella.
Thought: Then, I need to check Anupama Nadella's age.
Action: Chroma Search
Action Input: How old is Anupama Nadella?
Observation: Anupama Nadella's age is 50.
Thought: I now know the final answer.
Final Answer: Anupama Nadella is 50 years old.

### Input:
{{question}}

### Response:
Question: {{question}}
Thought: {{gen 't1' stop='\\n'}}
{{select 'answer' logprobs='logprobs' options=valid_answers}}: """,
    guidance_kwargs={},
    input_vars=["question", "valid_answers"],
    output_vars=["t1","answer"],
)

PROMPT_CHOOSE_ACTION_TEMPLATE = GuidancePrompt(
    name="cot_choose_action",
    prompt_template = """{{history}}
Action: {{select 'tool_name' options=valid_tools}}
""",
    guidance_kwargs={},
    input_vars=["valid_tools"],
    output_vars=["tool_name"],
)


PROMPT_ACTION_INPUT_TEMPLATE = GuidancePrompt(
    name="cot_action_input",
    prompt_template = """{{history}}
Action Input: {{gen 'actInput' stop='\\n'}}
Observation:
""",
    guidance_kwargs={},
    input_vars=["history"],
    output_vars=["actInput"],
)


PROMPT_THOUGHT_TEMPLATE = GuidancePrompt(
    name="cot_thought_gen",
    prompt_template = """{{history}}
Observation: {{observation}}
Thought: {{gen 'thought' stop='\\n'}}
{{select 'answer' logprobs='logprobs' options=valid_answers}}: """,
    guidance_kwargs={},
    input_vars=["history", "observation"],
    output_vars=["thought", "answer"],
)


PROMPT_FINAL_TEMPLATE = GuidancePrompt(
    name="cot_final",
    prompt_template = """{{history}}{{select 'tool_name' options=valid_tools}}
Action Input: {{gen 'actInput' stop='\\n'}}
Observation: {{do_tool tool_name actInput}}
Thought: {{gen 'thought' stop='\\n'}}
{{select 'answer' options=valid_answers}}: {{gen 'fn' stop='\\n'}}""",
    guidance_kwargs={},
    input_vars=["input"],
    output_vars=["output", "tool_name"],
)
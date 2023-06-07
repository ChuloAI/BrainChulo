from andromeda_chain.prompt import AndromedaPrompt

PROMPT_START_STRING = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
Answer the following questions as best you can. You have access to the following tools:

Check Question: A tool to validate if a question is answerable or not. The input is the question to validate.

Chroma Search: A wrapper around Chroma Search. Useful for when you need to answer questions about current events. The input is the question to search relevant information.

Strictly use the following format:

Question: the input question you must answerA
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

### Input:"""
 

class ChainOfThoughts:
    choose_action = AndromedaPrompt(
    name="cot_choose_action",
    prompt_template = """{{history}}
Action: {{select 'tool_name' options=valid_tools}}
""",
    guidance_kwargs={},
    input_vars=["history", "valid_tools"],
    output_vars=["tool_name"],
)


    action_input = AndromedaPrompt(
    name="cot_action_input",
    prompt_template = """{{history}}
Action Input: {{gen 'actInput' stop='\\n'}}
Observation:
""",
    guidance_kwargs={},
    input_vars=["history"],
    output_vars=["actInput"],
)

    prompt_start = AndromedaPrompt(
    name="cot_prompt_start",
    prompt_template = """{{prompt_start}}{{question}}
###RESPONSE:
Thought: {{gen 'thought' stop='\\n'}}
{{select 'answer' logprobs='logprobs' options=valid_answers}}: """,
    guidance_kwargs={},
    input_vars=["prompt_start", "question", "valid_answers"],
    output_vars=["thought", "answer"],
)


    thought_gen = AndromedaPrompt(
    name="cot_thought_gen",
    prompt_template = """{{history}}
Observation: {{observation}}
Thought: {{gen 'thought' stop='\\n'}}
{{select 'answer' logprobs='logprobs' options=valid_answers}}: """,
    guidance_kwargs={},
    input_vars=["history", "observation", "valid_answers"],
    output_vars=["thought", "answer"],
)


    final_prompt = AndromedaPrompt(
    name="cot_final",
    prompt_template = """{{history}}
Final Answer: {{gen 'final_answer' stop='\\n'}}""",
    guidance_kwargs={},
    input_vars=["history"],
    output_vars=["final_answer"],
)
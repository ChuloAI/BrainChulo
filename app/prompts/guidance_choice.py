from andromeda_chain.prompt import AndromedaPrompt


CHOICE_PROMPT =  AndromedaPrompt(
    name="choice_prompt",
    prompt_template = """{{history}}
{{select 'choice' logprobs='logprobs' options=valid_choices}}: """,
    input_vars=["history", "valid_choices"],
    output_vars=["choice"],
)
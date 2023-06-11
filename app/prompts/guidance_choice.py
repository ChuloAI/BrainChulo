from andromeda_chain.prompt import AndromedaPrompt


CHOICE_PROMPT =  AndromedaPrompt(
    name="choice_prompt",
    prompt_template = """{{history}}
You must now choose an option out of the {{valid_choices}}.
Remember that it must be coherent with your last thought.
{{select 'choice' logprobs='logprobs' options=valid_choices}}: """,
    input_vars=["history", "valid_choices"],
    output_vars=["choice"],
)
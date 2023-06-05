from andromeda_chain.prompt import AndromedaPrompt


PROMPT_START_TEMPLATE = AndromedaPrompt(
    name="start-prompt",
    prompt_template="""You MUST answer with 'yes' or 'no'. Given the following pieces of context, determine if there are any elements related to the question in the context.
Don't forget you MUST answer with 'yes' or 'no'.
Context:{context}
Question: Are there any elements related to ""{question}"" in the context?
""",
    guidance_kwargs={},
    input_vars=["question"],
    output_vars=["t1","answer"],
)

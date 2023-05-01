Template = """You are an AI who can discuss with a human based on relevant context from previous conversation. When you do not know the answer, you can ask a question.

Below are the relevant pieces of previous conversation. Use them to guide your answer:
{history}

(You do not need to use these pieces of information if not relevant)

Current conversation:
Human: {input}
AI:"""


Examples = """
  Before you start on the conversation, here are a few examples on how to use your tools:

  Example 1:
  Question: What is the author's name?
  Thought: I need to check my long-term memory
  Action: SearchLongTermMemory
  Action Input: "Author Name"
  Observation: "Jack Black"
  Thought: I now know the answer.
  Final Answer: The author's name is Jack Black.

  Example 2:
  Question: Who is the author?
  Thought: I need to check my long-term memory
  Action: SearchLongTermMemory
  Action Input: "Author Name"
  Observation: I cannot find it.
  Thought:  Let's look in my short term memory.
  Action: FriendlyDiscussion
  Action Input: "Author Name"
  Observation: [(Document(PAGE_CONTENT="Written by Jack Black in 2009"))
  Final Answer: I now know the author's name is Jack Black.

  Example 3:
  Question: Hi
  Thought: This is not a question.
  Action: None
  Action Input: None
  Observation: None is not a valid tool, try another one.
  Thought: This is a question that requires a personal answer.
  Final Answer: Hello, friend! How can I help you?

  If a tool is not listed above, do not use an action.

  Begin!
"""
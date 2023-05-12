from langchain.prompts import StringPromptTemplate
from memory.chroma_memory import Chroma

default_template = """As an AI designed to chat and respond to questions, my goal is to provide you with helpful and accurate information based on the context you provide. 

To assist me in this task, I have access to a vector database that contains various documents related to different topics. Here are some documents that match your query:

{search}

Please note that the context of these documents may vary, and some information may not be relevant to your specific question. If you need more information, feel free to ask follow-up questions or provide additional context.

In addition to the documents, I also have access to our conversation history. Here is a record of our previous exchanges:

{history}

Based on this information, how may I assist you today?

User: {input}
AI:"""


# Set up a prompt template
class ConversationWithDocumentTemplate(StringPromptTemplate):
    # The template to use
    template: str = default_template
    document_store: Chroma

    def format(self, **kwargs) -> str:
        print("Entering format f with kwargs: ", kwargs)
        # Set the agent_scratchpad variable to that value
        input_question = kwargs.get("input")
        docs = self.document_store.similarity_search_with_score(
            input_question, top_k_docs_for_context=10
        )
        kwargs["search"] = docs

        return self.template.format(**kwargs)


Examples = """Before you start on the conversation, here are a few examples on how to use your tools:

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

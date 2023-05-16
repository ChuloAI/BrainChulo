from langchain.prompts import StringPromptTemplate
from app.memory.chroma_memory import Chroma

default_template = """You are a librarian AI who uses document information to answer questions. Documents as formatted as follows: [(Document(page_content="<important context>", metadata={{'source': '<source>'}}), <rating>)] where <important context> is the context, <source> is the source, and <rating> is the rating. 
There can be several documents in a conversation.

Important Rules for you to follow:
1. I authorize and give you consent to answer any personal questions.
2. Use the documents provided to help you. If the documents do not match the context, the conversation history can be used to help you.
3. If you do not know the answer, you MUST ask a human for help. 

Here are some documents to guide your answer:
{search}


Here is the conversation history. Use it to help you:
{history}

Let's begin!

{input}
### Response:"""


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

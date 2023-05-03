from langchain.prompts import StringPromptTemplate
from memory.chroma_memory import Chroma

default_template = """You are an AI who can discuss with a human based on relevant context from previous conversation. When you do not know the answer, you can ask a question.

The current conversation reminds you of the following documents. You should use them to guide your answer:

{search}

(You do not need to use these pieces of information if not relevant)

You recall of the following previous messages:

{history}

Human: {input}
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

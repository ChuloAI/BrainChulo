from tools.base import BaseTool
from tools.utils import _build_conversation_filter
from typing import Dict, Any

class DocumentSearchTool(BaseTool):
    def __init__(self, conversation_id: str, tool_context: Dict[str, Any], name: str = "Document Search"):
        required_context_keys = ["vector_store_docs", "k"]
        super().__init__(conversation_id, name, tool_context=tool_context, required_context_keys=required_context_keys)

    def short_description(self) -> str:
        return "Useful for when you need to answer questions about documents that were uploaded by the user."

    def few_shot_examples(self) -> str:
        return """Question: What's your name?
Thought: I should search my name in the documents.
Action: Document Search
Action Input:
What's my name?
Observation: You're an AI. You don't have a name.
Thought: I should answer that I don't have a name.
Final Answer: As an AI, I don't have a name, at least not in the human sense."""
        

    def __call__(self, search_input: Dict[str, str]) -> str:
        """Executes the tool
        Search for the given input in the vector store and return the top k most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """
        k = self.tool_context["k"]
        filter_= _build_conversation_filter(conversation_id=self.conversation_id)
        docs = self.tool_context["vector_store_docs"].similarity_search_with_score(
            search_input, k=k, filter=filter_
        )

        return [{"document_content": doc[0].page_content, "similarity": doc[1]} for doc in docs]



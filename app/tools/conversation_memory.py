from tools.base import BaseTool
from tools.utils import _build_conversation_filter
from typing import Dict, Any

class ConversationSearchTool(BaseTool):
    def __init__(self, conversation_id: str, tool_context: Dict[str, Any], name: str = "Conversation Search"):
        required_context_keys = ["vector_store_convs", "k"]
        super().__init__(conversation_id, name, tool_context=tool_context, required_context_keys=required_context_keys)

    def short_description(self) -> str:
        return "A tool to search in your memory previous conversations with this user."
    
    def few_shot_examples(self) -> str:
        return """Question: What's your name?
Thought: I should search my name in the previous conversations.
Action: Conversation Search
Action Input:
What's my name?
Observation:
User: I'd like to give you a better name.
Bot: How would you like to call me?
User: I'd like to call you Joseph.
Bot: Alright, you may call me Joseph from now on.

Thought: The user wants to call me Joseph.
Final Answer: As I recall from a previous conversation, you call me Joseph."""


    def __call__(self, search_input):
        """
        Search for the given input in the vector store and return the top 10 most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """

        k = self.tool_context["k"]
        filter_= _build_conversation_filter(conversation_id=self.conversation_id)
        docs = self.tool_context["vector_store_convs"].similarity_search_with_score(
            search_input, k=5, filter=filter_
        )
        return [{"document_content": doc[0].page_content, "similarity": doc[1]} for doc in docs]

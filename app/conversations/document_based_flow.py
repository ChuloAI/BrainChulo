from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from andromeda_chain import AndromedaChain
from agents import ChainOfThoughtsFlowAgent
from tools.base import ToolFactory
from tools.document_memory import DocumentSearchTool
from tools.conversation_memory import ConversationSearchTool

from settings import load_config, logger

config = load_config()


class DocumentBasedConversationFlowAgent:
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=20, length_function=len)

        self.vector_store_docs = Chroma(collection_name="docs_collection")
        self.vector_store_convs = Chroma(collection_name="convos_collection")
        self.tools = [DocumentSearchTool, ConversationSearchTool]
        self.andromeda = AndromedaChain(config.andromeda_url)

        self.active_agent_class = ChainOfThoughtsFlowAgent
        self.tool_context = {
            "vector_store_docs": self.vector_store_docs,
            "vector_store_convs": self.vector_store_convs,
            "k": 5,
        }


    def load_document(self, document_path, conversation_id=None):
        """
        Load a document from a file and add its contents to the vector store.

        Args:
          document_path: A string representing the path to the document file.

        Returns:
          None.
        """
        text_loader = TextLoader(document_path, encoding="utf8")
        documents = text_loader.load()
        documents = self.text_splitter.split_documents(documents)

        if conversation_id is not None:
            for doc in documents:
                doc.metadata["conversation_id"] = conversation_id

        self.vector_store_docs.add_documents(documents)


    def predict(self, input: str, conversation_id: str):
        """
        Predicts a response based on the given input.

        Args:
          input (str): The input string to generate a response for.

        Returns:
          str: The generated response string.

        Raises:
          OutputParserException: If the response from the conversation agent could not be parsed.
        """
        logger.info("Defined tools: %s", self.tools)
        loaded_tools = ToolFactory(self.tools).build_tools(conversation_id, self.tool_context)

        logger.info("Loaded tools: %s", loaded_tools)
        loaded_agent = self.active_agent_class(self.andromeda, loaded_tools)

        final_answer = loaded_agent.run(input)
        if isinstance(final_answer, dict):
            final_answer = {'answer': str(final_answer), 'function': str(final_answer['fn'])}
        else:
            # Handle the case when final_answer is not a dictionary.
            final_answer = {'answer': str(final_answer)}

        return final_answer["answer"]

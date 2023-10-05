from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from colorama import Fore, Style
from llama_cpp import Llama
from settings import logger, load_config
import os

config = load_config()
dict_tools = None

def get_llama_model():
    print("Loading main model...")
    llm = Llama(model_path=config.model_path, n_ctx=2048)
    print("Finished loading main model...")

    return llm

class LlamaBasedConversation:
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=20, length_function=len)
        self.llama_model = get_llama_model()
        
        self.vector_store_docs = Chroma(collection_name="docs_collection")
        self.vector_store_convs = Chroma(collection_name="convos_collection")

        tools = {
            "Search Documents": self.search_documents,
            "Search Conversations": self.search_conversations,
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

    def search_documents(self, search_input, conversation_id=None):
        """
        Search for the given input in the vector store and return the top 10 most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """

        logger.info(f"Searching for: {search_input} in LTM")
        docs = self.vector_store_docs.similarity_search_with_score(
            search_input, k=5, filter=filter
        )
        return [{"document_content": doc[0].page_content, "similarity": doc[1]} for doc in docs]
        
    def search_conversations(self, search_input, conversation_id=None):
        """
        Search for the given input in the vector store and return the top 10 most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """
        if conversation_id is not None:
            filter = {"conversation_id": conversation_id}
        else:
            filter = {}

        logger.info(f"Searching for: {search_input} in LTM")
        docs = self.vector_store_convs.similarity_search_with_score(
            search_input, k=5, filter=filter
        )
        return [{"document_content": doc[0].page_content, "similarity": doc[1]} for doc in docs]

    def predict(self, input, history):
        context = []
        i=0
        for message in history:
            if i % 2 == 0:
                context.append("Q:" + message.text)
            else:
                context.append("A:" + message.text)
            i+=1

        context = "\n".join(context) + " A:"
        output = self.llama_model(context, max_tokens=500, stop=["Q:", "\n"], echo=True)
        response = output['choices'][0]['text']
        response = response.replace(context, "")

        return response



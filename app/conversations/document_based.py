from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from andromeda_chain import AndromedaChain
from agents import ChainOfThoughtsAgent

from settings import logger, load_config
import guidance 
config = load_config()

dict_tools = None


llama_model = None

def get_llama_model():
    global llama_model
    if llama_model is None:
        print("Loading qa model...")
        llama_model = guidance.llms.LlamaCpp(
            model = "/home/karajan/Downloads/guanaco-33B.ggmlv3.q5_0.bin",
            tokenizer = "openaccess-ai-collective/manticore-13b-chat-pyg",
            before_role = "<|",
            after_role = "|>",
            n_gpu_layers=300,
            n_threads=12,
            caching=False, )
        guidance.llm = llama_model
    return llama_model

class DocumentBasedConversation:
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=20, length_function=len)
        self.llama = get_llama_model()
        guidance.llm = self.llama
        self.vector_store_docs = Chroma(collection_name="docs_collection")
        self.vector_store_convs = Chroma(collection_name="convos_collection")
        tools = {
            "Search Documents": self.search_documents,
            "Search Conversations": self.search_conversations,
        }
        self.andromeda = AndromedaChain(config.andromeda_url)
        self.document_qa_agent = ChainOfThoughtsAgent(guidance, tools)


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

    def predict(self, input):
        global dict_tools
        """
        Predicts a response based on the given input.

        Args:
          input (str): The input string to generate a response for.

        Returns:
          str: The generated response string.

        Raises:
          OutputParserException: If the response from the conversation agent could not be parsed.
        """
        final_answer = self.document_qa_agent.run(input)
        if isinstance(final_answer, dict):
            final_answer = {'answer': str(final_answer), 'function': str(final_answer['fn'])}
        else:
            # Handle the case when final_answer is not a dictionary.
            final_answer = {'answer': str(final_answer)}

        return final_answer["answer"]

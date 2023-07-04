from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from colorama import Fore, Style
from guidance_tooling.guidance_programs.tools import clean_text
from transformers import BertTokenizerFast, BertForSequenceClassification

from andromeda_chain import AndromedaChain
from agents import ChainOfThoughtsAgent
from settings import logger, load_config
import guidance 
import os

config = load_config()
dict_tools = None
llama_model = None
llama_model2 = None
bert = None
bert_tokenizer = None
bert_model = None
guidance_reasoning_model_path = config.guidance_reasoning_model_path
guidance_extraction_model_path = config.guidance_extraction_model_path

TEST_MODE = os.getenv("TEST_MODE")
GUIDANCE_MODEL = os.getenv("GUIDANCE_MODEL_PATH")

def get_llama_model():
    global llama_model
    if llama_model is None:
        print("Loading main guidance model...")
        llama_model = guidance.llms.LlamaCpp(
            model = guidance_reasoning_model_path,
            tokenizer = "openaccess-ai-collective/manticore-13b-chat-pyg",
            before_role = "<|",
            after_role = "|>",
            n_gpu_layers=300,
            n_threads=12,
            caching=False, )
        print("Loading main guidance model...")
        guidance.llm = llama_model
    return llama_model

def get_llama_model2():
    global llama_model2
    if llama_model2 is None and guidance_extraction_model_path is not None: 
        print("Loading guidance model...")
        llama_model2 = guidance.llms.LlamaCpp(
            model = guidance_extraction_model_path,
            tokenizer = "openaccess-ai-collective/manticore-13b-chat-pyg",
            before_role = "<|",
            after_role = "|>",
            n_gpu_layers=300,
            n_threads=12,
            caching=False, )
        print("Loading second guidance model...")
    return llama_model2


def load_bert():
    print("Loading u-bert node...")
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('/home/karajan/labzone/ChatGPT_Automation/results/checkpoint-13500')
    print("u-bert node loaded!")
    return {"tokenizer": tokenizer, "model": model}

class DocumentBasedConversation:
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """
        self.bert = load_bert()
        self.bert_tokenizer=self.bert["tokenizer"]
        self.bert_model = self.bert["model"]
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=20, length_function=len)
        self.llama_model = get_llama_model()
        if llama_model2 is not None:
            self.llama_model2 = get_llama_model2()
        guidance.llm = self.llama_model
        self.vector_store_docs = Chroma(collection_name="docs_collection")
        self.vector_store_convs = Chroma(collection_name="convos_collection")
        tools = {
            "Search Documents": self.search_documents,
            "Search Conversations": self.search_conversations,
        }
        self.andromeda = AndromedaChain(config.andromeda_url)
        self.document_qa_agent = ChainOfThoughtsAgent(guidance, llama_model,llama_model2, bert_tokenizer, bert_model)


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
      context = self.search_documents(input)
      
      str_context = str(context)
      print(Fore.GREEN + Style.BRIGHT + "Printing vector search context..." + Style.RESET_ALL)
      print(Fore.GREEN + Style.BRIGHT + str_context + Style.RESET_ALL)
      final_answer = self.document_qa_agent.run(input, context, history)

      print(Fore.CYAN + Style.BRIGHT + "Printing full thought process..." + Style.RESET_ALL)
      print(Fore.CYAN + Style.BRIGHT + str(final_answer) + Style.RESET_ALL)

      if isinstance(final_answer, dict):
          final_answer = {'answer': str(final_answer), 'function': str(final_answer['fn'])}
      else:
          # Handle the case when final_answer is not a dictionary.
          final_answer = {'answer': str(final_answer)}

          # Check if 'Final Answer:' key exists in the dictionary
      if 'Final Answer:' in final_answer['answer']:
          # Find the index of 'Final Answer:' and extract everything after it
          answer_start_index = final_answer['answer'].index('Final Answer:') + len('Final Answer:')
          final_answer_text = final_answer['answer'][answer_start_index:]
          return final_answer_text.strip()
      else:
          return final_answer["answer"]



from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from llms.oobabooga_llm import OobaboogaLLM
from prompt_templates.document_based_conversation import Template
from settings import logger

class DocumentBasedConversation():
  def __init__(self):
    """
    Initializes the object with necessary components for conversation chain generation.

    Args:
      - self: the object itself

    Returns:
      - None

    Components:
      - llm: an instance of the OobaboogaLLM class
      - text_splitter: an instance of the CharacterTextSplitter class, with specified chunk size and overlap
      - embeddings: an instance of the HuggingFaceEmbeddings class, with specified model name
      - prompt: a PromptTemplate object with input variables and template
      - memory: None, to be initialized later
      - convo: a ConversationChain object with specified components and verbosity level
    """
    self.llm = OobaboogaLLM()
    self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    self.prompt = PromptTemplate(input_variables=["history", "input"], template=Template)
    self.refresh_store()


  def load_document(self, document_path):
    """Load and process a document file.

    Args:
      document_path (str): Path to the document file to load.

    Returns:
      None.

    Side effects:
      - Loads the contents of the document file located at `document_path`.
      - Splits the loaded documents into smaller chunks using `self.text_splitter`.
      - Creates a vector store using `Chroma.from_documents()` with the loaded documents
        and `self.embeddings`.
      - Creates a retriever from the vector store using `vector_store.as_retriever()`
        with `search_kwargs=dict(k=20)`.
      - Initializes `self.memory` with a new `VectorStoreRetrieverMemory` instance
        using the retriever created above.
      - Initializes `self.convo` with a new `ConversationChain` instance using
        `self.llm`, `self.prompt`, `self.memory`, and `verbose=False`.

    Raises:
      Any exceptions raised by `TextLoader.load()` or any of the methods called during
      processing of the loaded document (e.g. `self.text_splitter.split_documents()`).
    """
    text_loader = TextLoader(document_path, encoding="utf8")
    documents = text_loader.load()
    documents = self.text_splitter.split_documents(documents)

    self.refresh_store(documents)
  
  def refresh_store(self, documents = None):
    if documents is None:
      memory = None

    else:
      vector_store = Chroma.from_documents(
        documents, self.embeddings,
        metadatas=[{"source": str(i)} for i in range(len(documents))]
      )
      retriever = vector_store.as_retriever(search_kwargs=dict(k=20))
      memory = VectorStoreRetrieverMemory(retriever=retriever)

    self.convo = ConversationChain(
      llm=self.llm,
      prompt=self.prompt,
      verbose=True
    )

    if memory:
      logger.info("Initializing memory")
      self.convo.memory = memory
  
  def add_exchange_to_memory(self, input, output):
    if self.convo.memory:
      logger.info("Adding exchange to memory")
      self.convo.memory.save_context(input, output)


  def predict(self, input):
    print(f"Input: {input}")
    return self.convo.predict(input=input)

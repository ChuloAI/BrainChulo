import os
from typing import Any, Iterable, List, Optional, Type
from memory.base import BaseMemory
from langchain import vectorstores
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from settings import load_config, logger

config = load_config()

class Chroma(BaseMemory):
  vector_store: Optional[Type[vectorstores.Chroma]]
  
  def __init__(self):
    super().__init__()
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    logger.info(f"Embeddings: {embeddings}")
    persist_directory = os.path.join(os.getcwd(), "data", config.memories_path)
    # Create directory if it doesn't exist
    os.makedirs(persist_directory, exist_ok=True)
    

    self.vector_store = vectorstores.Chroma(
      collection_name="brainchulo",
      embedding_function=embeddings,
      persist_directory=persist_directory
    )

    self.setup_index()

  def setup_index(self):
    self.add_texts(["Hello", "world!", "this", "is", "a", "test"], ids=["1", "2", "3", "4", "5", "6"])


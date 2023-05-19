import os
from typing import Any, Iterable, List, Optional, Type
from memory.base import BaseMemory
from langchain import vectorstores
from langchain.embeddings import (
    HuggingFaceInstructEmbeddings,
    HuggingFaceEmbeddings,
)
from langchain.docstore.document import Document
from settings import load_config, logger

config = load_config()

instruct_embeddings = ["hkunlp/instructor-xl", "hkunlp/instructor-large"]
sentence_transformers_embeddings = ["all-MiniLM-L6-v2", "sentence-t5-xxl"]


class Chroma(BaseMemory):
    vector_store: Optional[Type[vectorstores.Chroma]]
    collection_name: Optional[str]

    embeddings_map = {
        **{name: HuggingFaceInstructEmbeddings for name in instruct_embeddings},
        **{
            name: HuggingFaceEmbeddings
            for name in sentence_transformers_embeddings
        },
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        EmbeddingsModel = self.embeddings_map.get(config.embeddings_model)
        if EmbeddingsModel is None:
            raise ValueError(
                f"Invalid embeddings model: {config.embeddings_model}"
            )

        kwargs = {"model_name": config.embeddings_model}
        if EmbeddingsModel == HuggingFaceInstructEmbeddings:
            kwargs["model_kwargs"] = {"device": "cuda"}

        embeddings = EmbeddingsModel(**kwargs)

        persist_directory = os.path.join(
            os.getcwd(), "data", config.memories_path
        )
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        self.vector_store = vectorstores.Chroma(
            collection_name=self.collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )

        self.setup_index()

    def setup_index(self):
        collection = self.vector_store._client.get_collection(
            self.collection_name
        )
        if len(collection.get()['ids']) < 6:
            self.add_texts(
                ["Hello", "world!", "this", "is", "a", "test"],
                ids=["1", "2", "3", "4", "5", "6"],
            )

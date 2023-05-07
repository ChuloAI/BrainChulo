
from typing import Any, Dict, List
from pydantic import BaseModel, Extra, root_validator
from langchain.embeddings.base import Embeddings
from chromadb.utils import embedding_functions


class ChromaMiniLM(BaseModel, Embeddings):
    # Per https://huggingface.co/blog/mteb all-MiniLM-L6-v2 provides a good balance between speed and performance
    # The model will be downloaded on first run
    client: Any = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2")

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values = {
            **values,
            "client": embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2")}

        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client([text])[0]

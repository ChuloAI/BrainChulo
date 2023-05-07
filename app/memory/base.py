from typing import Any, Iterable, List, Optional, Dict, Tuple, Type
from pydantic import BaseModel
from pyparsing import abstractmethod
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore


class BaseMemory(BaseModel):
    collection_name: Optional[str]
    vector_store: Optional[Type[VectorStore]]

    def __init__(self, collection_name: str = "default_collection"):
        # init super class
        super().__init__()
        self.collection_name = collection_name

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        response = self.vector_store.add_texts(texts, metadatas, ids, **kwargs)
        self.vector_store._client.persist()

        return response

    def add_documents(self, documents: list[Document]):
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        return self.add_texts(texts, metadatas)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k, **kwargs)

    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        return self.vector_store.similarity_search_by_vector(
            embedding, k=k, **kwargs)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        return self.vector_store.similarity_search_with_score(
            query, k=k, **kwargs)

    def max_marginal_relevance_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        return self.vector_store.max_marginal_relevance_search_by_vector(
            embedding, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult, **kwargs)

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        return self.vector_store.max_marginal_relevance_search(
            query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult, **kwargs)

    def delete_collection(self) -> None:
        return self.vector_store.delete_collection()

    def persist(self) -> None:
        return self.vector_store.persist()

    def update_document(self, document_id: str, document: Document) -> None:
        return self.vector_store.update_document(document_id, document)

    def get_store(self) -> Document:
        return self.vector_store

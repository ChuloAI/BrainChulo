from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from embeddings.chroma_mini_llm import ChromaMiniLM
from chromadb.utils import embedding_functions
from vicuna_llm import VicunaLLM
import settings

config = settings.load_config()

loader = TextLoader('./data/paul_graham_essay.txt', encoding="utf8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
documents = text_splitter.split_documents(documents)

embeddings = ChromaMiniLM()
vectorstore = Chroma.from_documents(documents, embeddings)

# define custom QuestionAnswerPrompt
query_str = "What did the author do growing up?"


qna = ConversationalRetrievalChain.from_llm(
    VicunaLLM(), vectorstore.as_retriever())

response = qna({"question": query_str, "chat_history": []})

print(response)

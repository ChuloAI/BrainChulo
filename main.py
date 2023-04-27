from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from vicuna_llm import VicunaLLM
import settings

config = settings.load_config()

loader = TextLoader('./data/paul_graham_essay.txt', encoding="utf8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vectorstore = Chroma.from_documents(documents, embeddings, metadatas=[
    {"source": str(i)} for i in range(len(documents))])

# define custom QuestionAnswerPrompt
query_str = "Where did the author grow up?"

qna = ConversationalRetrievalChain.from_llm(
    VicunaLLM(), vectorstore.as_retriever())

chat_history = []
response = qna({"question": query_str, "chat_history": chat_history})

chat_history.append((query_str, response['answer']))

response = qna({"question": 'Who is the author in love with?',
               "chat_history": chat_history})

print(response)

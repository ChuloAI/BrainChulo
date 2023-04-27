from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from vicuna_llm import VicunaLLM
from prompt_templates.friendly_conversation import Template
import settings

config = settings.load_config()

loader = TextLoader('./data/paul_graham_essay.txt', encoding="utf8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vectorstore = Chroma.from_documents(documents, embeddings, metadatas=[
    {"source": str(i)} for i in range(len(documents))])
retriever = vectorstore.as_retriever(search_kwargs=dict(k=20))
memory = VectorStoreRetrieverMemory(retriever=retriever)


PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=Template
)

# define custom QuestionAnswerPrompt
query_str = "Where did the author grow up?"

convo = ConversationChain(
    llm=VicunaLLM(),
    prompt=PROMPT,
    memory=memory,
    verbose=False
)


response = convo.predict(input=query_str)
print(f"Response from AI: {response}")

response = convo.predict(input="Who did the author marry?")
print(f"Response from AI: {response}")

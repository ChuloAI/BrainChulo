import os
import re

from colorama import Fore
from colorama import Style
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def clean_text(text):
    # Remove line breaks
    text = text.replace("\n", " ")

    # Remove special characters
    text = re.sub(r"[^\w\s]", "", text)

    return text


def load_unstructured_document(document: str) -> list[Document]:
    with open(document, "r") as file:
        text = file.read()
    title = os.path.basename(document)
    return [Document(page_content=text, metadata={"title": title})]


def split_documents(
    documents: list[Document], chunk_size: int = 100, chunk_overlap: int = 0
) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)


def checkQuestion(llm, question: str, retriever):
    QUESTION_CHECK_PROMPT_TEMPLATE = """You MUST answer with 'yes' or 'no'. Given the following pieces of context, determine if there are any elements related to the question in the context.
Don't forget you MUST answer with 'yes' or 'no'.
Context:{context}
Question: Are there any elements related to ""{question}"" in the context?
"""
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )

    # Answer the question
    answer_data = qa({"query": question})

    # Check if 'answer' is in answer_data, if not print it in bold red
    if "result" not in answer_data:
        print(f"\033[1;31m{answer_data}\033[0m")
        return "Issue in retrieving the answer."

    context_documents = answer_data["source_documents"]

    # Combine all contexts into one
    context = " ".join([clean_text(doc.page_content) for doc in context_documents])
    # Formulate the prompt for the LLM
    question_check_prompt = QUESTION_CHECK_PROMPT_TEMPLATE.format(
        context=context, question=question
    )
    print(Fore.GREEN + Style.BRIGHT + question_check_prompt + Style.RESET_ALL)
    # Submit the prompt to the LLM directly
    answerable = llm(question_check_prompt)
    print(Fore.GREEN + Style.BRIGHT + answerable + Style.RESET_ALL)
    return answerable[-3:]


def load_tools(llm_model, settings):
    def ingest_file(file_path):
        # Load unstructured document
        documents = load_unstructured_document(file_path)

        # Split documents into chunks
        documents = split_documents(documents, chunk_size=100, chunk_overlap=20)

        # Determine the embedding model to use
        EmbeddingsModel = settings.embeddings_map.get(settings.embeddings_model)
        if EmbeddingsModel is None:
            raise ValueError(f"Invalid embeddings model: {settings.embeddings_model}")

        model_kwargs = (
            {"device": "cuda:0"}
            if EmbeddingsModel == HuggingFaceInstructEmbeddings
            else {}
        )
        embedding = EmbeddingsModel(
            model_name=settings.embeddings_model, model_kwargs=model_kwargs
        )

        # Store embeddings from the chunked documents
        vectordb = Chroma.from_documents(documents=documents, embedding=embedding)

        retriever = vectordb.as_retriever(search_kwargs={"k": 4})

        return retriever, file_path

    file_path = settings.test_file
    retriever, _ = ingest_file(file_path)

    def searchChroma(key_word):
        qa = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
        )

        print(qa)
        res = qa.run(key_word)
        print(res)
        return res

    dict_tools = {
        "Chroma Search": searchChroma,
        "File Ingestion": ingest_file,
        "Check Question": lambda question: checkQuestion(
            llm_model, question, retriever
        ),
    }

    return dict_tools

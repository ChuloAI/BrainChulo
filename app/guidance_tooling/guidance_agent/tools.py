import os
import re

from colorama import Fore
from colorama import Style
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from llms.guidance_llm import ModelBehindGuidance


def clean_text(text):
    # Remove line breaks
    text = text.replace("\n", " ")

    # Remove special characters
    text = re.sub(r"[^\w\s]", "", text)

    return text


def split_documents(
    documents: list[Document], chunk_size: int = 100, chunk_overlap: int = 0
) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)


def checkQuestion(question: str, retriever):
    QUESTION_CHECK_PROMPT_TEMPLATE = """You MUST answer with 'yes' or 'no'. Given the following pieces of context, determine if there are any elements related to the question in the context.
Don't forget you MUST answer with 'yes' or 'no'.
Context:{context}
Question: Are there any elements related to ""{question}"" in the context?
"""
    llm = ModelBehindGuidance()
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


def load_tools(docs_retriever):
    llm = ModelBehindGuidance()

    def searchChroma(key_word):
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=docs_retriever,
            return_source_documents=False,
        )

        print(qa)
        res = qa.run(key_word)
        print(res)
        return res

    dict_tools = {
        "Chroma Search": searchChroma,
        "Check Question": lambda question: checkQuestion(
            question, docs_retriever
        ),
    }

    return dict_tools

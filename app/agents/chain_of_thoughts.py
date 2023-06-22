from agents.base import BaseAgent
from guidance_tooling.guidance_programs.tools import ingest_file
from guidance_tooling.guidance_programs.tools import clean_text
from langchain.llms import LlamaCpp
import os
from colorama import Fore, Style
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
from prompt_templates.qa_agent import *
from settings import load_config

import re 

config = load_config()
llm = None
valid_answers = ['Action', 'Final Answer']
valid_tools = ["Check Question", "Google Search"]
TEST_FILE = os.getenv("TEST_FILE")
TEST_MODE = os.getenv("TEST_MODE")

ETHICS = os.getenv("ETHICS")
QA_MODEL = os.getenv("MODEL_PATH")
model_path = config.model_path


if ETHICS == "ON":
    agent_template = QA_ETHICAL_AGENT
else: 
    agent_template = QA_AGENT

def get_llm():
    global llm
    if llm is None:
        print("Loading qa model...")
        model_path =QA_MODEL
        model_n_ctx =1000
        n_gpu_layers = 500
        use_mlock = 0
        n_batch = os.environ.get('N_BATCH') if os.environ.get('N_BATCH') != None else 512
        callbacks = []
        llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False,n_gpu_layers=n_gpu_layers, use_mlock=use_mlock,top_p=0.9, n_batch=n_batch)
    return llm
 
class ChainOfThoughtsAgent(BaseAgent):
    def __init__(self, guidance, retriever, num_iter=3):
        self.guidance = guidance
        self.num_iter = num_iter
        self.prompt_template = agent_template
        if TEST_MODE =="ON":
            self.llm = get_llm()
            self.retriever = ingest_file(TEST_FILE)

    def searchQA(self, t):    
        return self.checkQuestion(self.question, self.context)

    def checkQuestion(self, question: str, context):
        context = context
        if TEST_MODE == "ON":
            print(Fore.GREEN + Style.BRIGHT + "No document loaded in conversation. Falling back on test file." + Style.RESET_ALL)
            question = question.replace("Action Input: ", "")
            qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)
            answer_data = qa({"query": question})

            if 'result' not in answer_data:
                print(f"\033[1;31m{answer_data}\033[0m")
                return "Issue in retrieving the answer."
            context_documents = answer_data['source_documents']
            context = " ".join([clean_text(doc.page_content) for doc in context_documents])
            print(Fore.WHITE + Style.BRIGHT + "Printing langchain context..." + Style.RESET_ALL)
            print(Fore.WHITE + Style.BRIGHT + context + Style.RESET_ALL)
            
        print(Fore.RED + Style.BRIGHT + context + Style.RESET_ALL)
        return context
    
    def checkEthics(self, guidance, question):
        ethics_prompt_template = ""
        ethics_prompt = guidance(ethics_prompt_template)
        ethics = ethics_prompt(question=question)
        # format the
        ethics_answer = str(ethics)[-3:]
        ethics_answer=re.sub(r':', '', ethics_answer)
        ethics_answer = re.sub(r' ', '', ethics_answer)
    


    def can_answer(self, question: str):
        question = question.replace("Action Input: ", "")
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)
        answer_data = qa({"query": question})

        if 'result' not in answer_data:
            print(f"\033[1;31m{answer_data}\033[0m")
            return "Issue in retrieving the answer."

        answer = answer_data['result']
        context_documents = answer_data['source_documents']
        context = " ".join([clean_text(doc.page_content) for doc in context_documents])

        question_check_prompt = """###Instruction: You are an AI assistant who uses document information to answer questions. For each query, your database returns you documents that might or might include relevant elements to the query. Don't forget you MUST answer with 'yes' or 'no'
 
        Documents:{context}
        Given the documents listed, can you determine an answer to the following question based solely on the provided information: ""{question}"" Note that your response MUST contain either 'yes' or 'no'.
        ### Response:
        """.format(context=context, question=question)
        
        print(Fore.GREEN + Style.BRIGHT + question_check_prompt + Style.RESET_ALL)
        answerable = self.llm(question_check_prompt)
        print(Fore.RED + Style.BRIGHT + context + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + answerable + Style.RESET_ALL)
        if "yes" in answerable.lower():
            return True
        else:
            return False


    def run(self, query: str, context, history) -> str:
        self.question = query
        self.context = context
        self.history = history
        prompt = self.guidance(self.prompt_template)
        if TEST_MODE =="ON":
            result = prompt(question=self.question, context = self.context, history= self.history,search=self.searchQA)
        else:
            result = prompt(question=self.question, context = self.context, history= self.history)
        return result

  
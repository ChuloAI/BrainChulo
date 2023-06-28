from agents.base import BaseAgent
from guidance_tooling.guidance_programs.tools import ingest_file
from guidance_tooling.guidance_programs.tools import clean_text
from langchain.llms import LlamaCpp
import os
import time
import guidance
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
  
    def __init__(self, guidance, llama_model, llama_model2):
        self.guidance = guidance
         # We first load the model in charge of reasoning along the guidance program
        self.llama_model = llama_model
        # We then load the model in charge of correctly identifying the data within the context and provide an answer
        self.llama_model2 = llama_model2

    
    def print_stage(self, stage_name, message):
        print(Fore.CYAN + Style.BRIGHT + f"Entering {stage_name} round" + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL)
    
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
        return context
    
    def ethics_check(self, question, ethics_prompt):
        ethics_program = self.guidance(ethics_prompt)
        return ethics_program(question=question)

    def query_identification(self, question, conversation_prompt):
        guidance.llm = self.llama_model
        conversation_program = self.guidance(conversation_prompt) 
        return conversation_program(question=question)

    def phatic_answer(self, question, history, phatic_prompt):
        phatic_program = self.guidance(phatic_prompt)
        return phatic_program(question=question, history=history)

    def data_retrieval(self, question):
        if self.llama_model2 is not None:
            guidance.llm = self.llama_model2
        referential_program = self.guidance(referential_prompt)
        referential_round = referential_program(question=question, search=self.searchQA)
        return referential_round

    def answer_question(self, question, answer_prompt):
        if self.llama_model2 is not None:
            guidance.llm = self.llama_model2
        answer_program = self.guidance(answer_prompt)
        answer_round = answer_program(question=question, search=self.searchQA)
        return answer_round["final_answer"] 

    def run(self, query: str, context, history) -> str:

        self.question = query 
        self.context = context
        self.history = history
        print(Fore.GREEN + Style.BRIGHT + "Starting guidance agent..." + Style.RESET_ALL)
        conversation_round= self.query_identification(self.question , conversation_prompt)

        if conversation_round["query_type"] == "Phatic": 
            self.print_stage("answering", "User query identified as phatic")
            phatic_round = self.phatic_answer(self.question , history, phatic_prompt)
            return phatic_round["phatic_answer"]  

        self.print_stage("data retrieval", "User query identified as referential")
        referential_round = self.data_retrieval(self.question )

        if referential_round["answerable"] == "Yes":
            self.print_stage("answering", "Matching information found")
            return self.answer_question(self.question, answer_prompt)
        else:
            return "I don't have enough information to answer."



  
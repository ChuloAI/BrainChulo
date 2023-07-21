from agents.base import BaseAgent
from guidance_tooling.guidance_programs.tools import ingest_file, clean_text, classify_sentence, classify_question, generate_subject, generate_summary, predict_match, test_search_documents
from langchain.llms import LlamaCpp
import os
import time
import guidance
from colorama import Fore, Style
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
from prompt_templates.qa_agent import *
from prompt_templates.exllama import *
from settings import load_config
import requests  # Add requests for the API
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
HOST = '86.242.95.136:449'  # API details
URI = f'http://{HOST}/api/v1/generate'


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
  
    def __init__(self, guidance, llama_model2):
        self.guidance = guidance
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

    def query_classification(self, question):
        print(Fore.RED + Style.BRIGHT + "Classifying query..." + Style.RESET_ALL)
        prediction = classify_sentence(question)
        print(Fore.RED + Style.BRIGHT + str(prediction)+ Style.RESET_ALL)
        return prediction
    
    def query_identification(self, question):
        print(Fore.RED + Style.BRIGHT + "Classifying question..." + Style.RESET_ALL)
        prediction = classify_question(question)
        print(Fore.RED + Style.BRIGHT + str(prediction)+ Style.RESET_ALL)
        return prediction

    def phatic_answer(self, question, history, phatic_prompt):
        phatic_program = self.guidance(phatic_prompt)
        return phatic_program(question=question, history=history)

    def topic_extraction(self, question):
        subject= generate_subject(question)
        return subject
    
    def data_summary(self, context):
        print("STARTING SUMMARY")
        summary = generate_summary(context)
        return summary
    
    def data_matching(self, subject, summary):
        subject= predict_match(subject, summary)
        return subject
    
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
    
    def questions_listing(self, question, context):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Make a list of 5 questions you should ask yourself to infer the answer to '{question}' from a piece of text.

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
        
    def questions_answering(self, question, context, questions):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Answer '{questions}' relatively to '{context}'

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 400,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result

    def api_data_matching(self, question, context, questions):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Infer the answer to '{question}' from: "{context}".
Here are the questions you should ask yourself: {questions}

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
    
    def api_data_evaluation(self, question, context):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Evaluate if the answer to '{question}' is found or can be inferred from: "{context}".

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
        
    def phatic_api_answer(self, question, history, context):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions taking into accounrt their chat history.
### Human:
History: {history}  
Context: {context}
Latest user's message: '{question}

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result

    def run(self, query: str, context, history) -> str:
        self.question = query 
        self.context = context
        self.history = history
        print(Fore.GREEN + Style.BRIGHT + "Starting guidance agent..." + Style.RESET_ALL)
        classification_round= self.query_classification(query)
        self.print_stage("query classification", "User query identified as " + classification_round)
        topic_extraction_round = self.topic_extraction(query)
        data_summary_round = self.data_summary(context) ##generate the summary immediately as well just in case
        print(Fore.GREEN + Style.BRIGHT + data_summary_round + Style.RESET_ALL)
        data_matching_round = self.data_matching(str(topic_extraction_round), str(data_summary_round))
        if "declarative" in classification_round:
            self.print_stage("answering", "User query is not a question")
            phatic_round = self.phatic_api_answer(self.question , history)
            return phatic_round
         
        conversation_round= self.query_identification(self.question)

        if "phatic" in conversation_round: 
            self.print_stage("answering", "User query identified as phatic")
            phatic_round = self.phatic_api_answer(self.question , history)
            return phatic_round
        
        self.print_stage("data retrieval", "User query identified as referential")
  
        time.sleep(1)
        if data_matching_round == 1:
            questions_listing_round = self.questions_listing(self.question, str(context))
            questions_answer_round =self.questions_answering(self.question, str(context), str(questions_listing_round))
            api_matching_round = self.api_data_matching(self.question, str(questions_answer_round), str(questions_listing_round))
            print(Fore.CYAN + Style.BRIGHT  + str(api_matching_round) + Style.RESET_ALL)

            return api_matching_round
        else:
            api_matching_eval= self.api_data_evaluation(self.question, str(context))
            print(Fore.CYAN + Style.BRIGHT  + str(api_matching_eval) + Style.RESET_ALL)
            return api_matching_eval

  
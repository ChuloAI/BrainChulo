from typing import Dict, Callable
from andromeda_chain import AndromedaChain
from agents.flow_based import BaseAgent, BaseFlowAgent
from flow.flow import Flow, PromptNode, ToolNode, ChoiceNode, StartNode
from prompts.flow_guidance_cot import FlowChainOfThoughts, PROMPT_START_STRING
from guidance_tooling.guidance_programs.tools import ingest_file
from guidance_tooling.guidance_programs.tools import clean_text
from guidance_tooling.guidance_programs.tools import load_tools

import os
from langchain.llms import LlamaCpp
from dotenv import load_dotenv
import os
from chromadb.config import Settings
from colorama import Fore, Style
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp

llm = None
valid_answers = ['Action', 'Final Answer']
valid_tools = ["Check Question", "Google Search"]
TEST_FILE = os.getenv("TEST_FILE")

def get_llm():
    global llm
    if llm is None:
        print("Loading guidance model...")
        model_type = "LlamaCpp"
        model_path ="/home/karajan/Downloads/airoboros-13b-gpt4.ggmlv3.q8_0.bin"
        model_n_ctx =1000
        target_source_chunks = 4
        n_gpu_layers = 500
        use_mlock = 0
        n_batch = os.environ.get('N_BATCH') if os.environ.get('N_BATCH') != None else 512
        callbacks = []
        qa_prompt = ""
        llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False,n_gpu_layers=n_gpu_layers, use_mlock=use_mlock,top_p=0.9, n_batch=n_batch)
    return llm

class ChainOfThoughtsFlowAgent(BaseFlowAgent):
    def __init__(self, andromeda: AndromedaChain, tools: Dict[str, Callable[[str], str]]):
        def execute_tool(variables):
            action_name = variables["tool_name"]
            action_input = variables["act_input"]
            return self.do_tool(action_name, action_input)

        start = StartNode("start", FlowChainOfThoughts.flow_prompt_start, {
            "Action": "choose_action",
            "Final Answer": "final_prompt"
        })
        thought = PromptNode("thought", FlowChainOfThoughts.thought_gen)
        choose_action = PromptNode("choose_action", FlowChainOfThoughts.choose_action)
        perform_action = PromptNode("perform_action", FlowChainOfThoughts.action_input)
        execute_tool_node = ToolNode("execute_tool", execute_tool)
        decide = ChoiceNode("decide", ["thought", "final_prompt"], max_decisions=3, force_exit_on="final_prompt")
        final = PromptNode("final_prompt", FlowChainOfThoughts.final_prompt)

        thought.set_next(choose_action)
        choose_action.set_next(perform_action)
        perform_action.set_next(execute_tool_node)
        execute_tool_node.set_next(decide)

        flow = Flow(
            [start, thought, choose_action, perform_action, execute_tool_node, decide, final]
        )

        super().__init__(andromeda, tools, flow)
        self.valid_tools = list(tools.keys())
        self.valid_answers = ["Action", "Final Answer"]


    def run(self, query: str) -> str:
        return super().run(query, variables={
            "prompt_start": PROMPT_START_STRING,
            "question": query,
            "valid_tools": self.valid_tools,
            "valid_answers": self.valid_answers,
        })

class ChainOfThoughtsAgent(BaseAgent):
    def __init__(self, guidance, retriever, num_iter=3):
        self.guidance = guidance
        self.retriever = ingest_file(TEST_FILE)
        self.llm = get_llm()

        self.num_iter = num_iter
        self.prompt_template = """
        {{#system~}}
        Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
        ### Instruction:
        Answer the following questions as best you can. You have access to the following tools:
        Google Search: A wrapper around Google Search. Useful for when you need to answer questions about current events. The input is the question to search relevant information.
        {{~/system}}

        {{#user~}}
        Question: {{question}}
        {{~/user}}

        {{#assistant~}}
        Thought: Let's first check our database.
        Action: Check Question
        Action Input: {{question}}
        {{~/assistant}}

        {{#user~}}
        Here are the relevant documents from our database:{{search question}}
        {{~/user}}address?

        {{#assistant~}}
        Observation: Based on the documents, I think I can reach a conclusion.
        {{#if (can_answer)}} 
        Thought: I believe I can answer the question based on the information contained in the returned documents.
        Final Answer: {{gen 'answer' temperature=0.7 max_tokens=50}}
        {{else}}
        Thought: I don't think I can answer the question based on the information contained in the returned documents.
        Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.
        {{/if}}

        {{~/assistant}}
        """

    def searchQA(self, t):    
        return self.checkQuestion(self.question)

    def checkQuestion(self, question: str):
        question = question.replace("Action Input: ", "")
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)
        answer_data = qa({"query": question})

        if 'result' not in answer_data:
            print(f"\033[1;31m{answer_data}\033[0m")
            return "Issue in retrieving the answer."

        context_documents = answer_data['source_documents']
        context = " ".join([clean_text(doc.page_content) for doc in context_documents])
        return context

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


    def run(self, query: str) -> str:
        self.question = query
        prompt = self.guidance(self.prompt_template)
        result = prompt(question=self.question, search=self.searchQA, can_answer=self.can_answer(self.question),valid_answers=valid_answers, valid_tools=valid_tools)
        return result

  
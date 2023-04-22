import os
from llama_index import GPTListIndex, SimpleDirectoryReader, PromptHelper, QuestionAnswerPrompt
from llama_index import LLMPredictor, ServiceContext
from vicuna_llm import VicunaLLM
import settings

config = settings.load_config()

# define prompt helper
# set maximum input size
max_input_size = 2048
# set number of output tokens
num_output = 256
# set maximum chunk overlap
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

# Define our LLM
llm_predictor = LLMPredictor(llm=VicunaLLM())

service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, prompt_helper=prompt_helper)

# Create or load index
# Check if index.json exists
if os.path.exists(config.index_path):
  index = GPTListIndex.load_from_disk(
    "index.json", service_context=service_context)
else:
  documents = SimpleDirectoryReader('data').load_data()
  index = GPTListIndex.from_documents(
    documents, service_context=service_context)
  index.save_to_disk(config.index_path)

# define custom QuestionAnswerPrompt
query_str = "What did the author do growing up?"

QA_PROMPT_TMPL = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n"
    "### Instruction:\nGiven the context information, please answer the following question: {query_str}\n"
    "### Response:\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)


response = index.query(query_str, text_qa_template=QA_PROMPT)
print(response)

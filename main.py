from dotenv import load_dotenv
from llama_index import GPTListIndex, SimpleDirectoryReader, PromptHelper
from llama_index import LLMPredictor, ServiceContext
from vicuna_llm import VicunaLLM

load_dotenv()

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

documents = SimpleDirectoryReader('data').load_data()
index = GPTListIndex.from_documents(documents, service_context=service_context)
index.save_to_disk('index.json')

response = index.query("What did the author do growing up?")
print(response)

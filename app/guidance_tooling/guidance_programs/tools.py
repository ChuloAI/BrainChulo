from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain import HuggingFacePipeline
from colorama import Fore, Style
from transformers import BertTokenizerFast, BertForSequenceClassification
from transformers import BartTokenizer, BartForSequenceClassification, BartForConditionalGeneration

from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.llms import LlamaCpp
from torch import nn
import gc
import torch
import re
import os
import json


load_dotenv()
QUESTION_BERT= os.getenv("QUESTION_BERT_MODEL_PATH")
PHATIC_BERT= os.getenv("PHATIC_BERT_MODEL_PATH")
TOPIC_BART= os.getenv("TOPIC_BART_MODEL_PATH")
SYNTHESIS_BART= os.getenv("SYNTHESIS_BART_MODEL_PATH")
MATCHING_BART= os.getenv("MATCHING_BART_MODEL_PATH")

TEST_FILE = os.getenv("TEST_FILE")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")
EMBEDDINGS_MAP = {
    **{name: HuggingFaceInstructEmbeddings for name in ["hkunlp/instructor-xl", "hkunlp/instructor-large"]},
    **{name: HuggingFaceEmbeddings for name in ["all-MiniLM-L6-v2", "sentence-t5-xxl"]}
}

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx =1000
target_source_chunks = os.environ.get('TARGET_SOURCE_CHUNKS')
n_gpu_layers = os.environ.get('N_GPU_LAYERS')
use_mlock = os.environ.get('USE_MLOCK')
n_batch = os.environ.get('N_BATCH') if os.environ.get('N_BATCH') != None else 512
callbacks = []
qa_prompt = ""

CHROMA_SETTINGS = {}  # Set your Chroma settings here

def clean_text(text):
    # Remove line breaksRetrievalQA
    text = text.replace('\n', ' ')

    # Remove special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    return text

def load_unstructured_document(document: str) -> list[Document]:
    with open(document, 'r') as file:
        text = file.read()
    title = os.path.basename(document)
    return [Document(page_content=text, metadata={"title": title})]

def split_documents(documents: list[Document], chunk_size: int = 250, chunk_overlap: int = 20) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

 

def ingest_file(file_path):
        # Load unstructured document
        documents = load_unstructured_document(file_path)

        # Split documents into chunks
        documents = split_documents(documents, chunk_size=250, chunk_overlap=100)

        # Determine the embedding model to use
        EmbeddingsModel = EMBEDDINGS_MAP.get(EMBEDDINGS_MODEL)
        if EmbeddingsModel is None:
            raise ValueError(f"Invalid embeddings model: {EMBEDDINGS_MODEL}")

        model_kwargs = {"device": "cuda:0"} if EmbeddingsModel == HuggingFaceInstructEmbeddings else {}
        embedding = EmbeddingsModel(model_name=EMBEDDINGS_MODEL, model_kwargs=model_kwargs)

        # Store embeddings from the chunked documents
        vectordb = Chroma.from_documents(documents=documents, embedding=embedding)

        retriever = vectordb.as_retriever(search_kwargs={"k":4})

        print(file_path)
        print(retriever)

        return retriever

def classify_sentence(sentence):
    # Prepare the sentence for BERT by tokenizing, padding and creating attention mask
    print("FUNCTION STARTED")
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(QUESTION_BERT)
    encoding = tokenizer.encode_plus(
      sentence,
      truncation=True,
      padding='max_length',
      max_length=128,
      return_tensors='pt'  # Return PyTorch tensors
    )
    # Get the input IDs and attention mask in tensor format
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    # No gradient needed for inference, so wrap in torch.no_grad()
    with torch.no_grad():
        # Forward pass, get logit predictions
        outputs = model(input_ids, attention_mask=attention_mask)
    print(outputs)
    # Get the predicted class
    _, predicted = torch.max(outputs.logits, 1)
    del model
    torch.cuda.empty_cache()  # clear unused memory in PyTorch
    gc.collect()  # enforce garbage collection

    # Return the predicted class (0 for 'declarative', 1 for 'interrogative')
    return "declarative" if predicted.item() == 0 else "interrogative"


def classify_question(sentence):
    # Prepare the sentence for BERT by tokenizing, padding and creating attention mask
    print("FUNCTION STARTED")
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(PHATIC_BERT)
    encoding = tokenizer.encode_plus(
      sentence,
      truncation=True,
      padding='max_length',
      max_length=128,
      return_tensors='pt'  # Return PyTorch tensors
    )
    # Get the input IDs and attention mask in tensor format
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    # No gradient needed for inference, so wrap in torch.no_grad()
    with torch.no_grad():
        # Forward pass, get logit predictions
        outputs = model(input_ids, attention_mask=attention_mask)
    print(outputs)
    # Get the predicted class
    _, predicted = torch.max(outputs.logits, 1)
    del model
    torch.cuda.empty_cache()  # clear unused memory in PyTorch
    gc.collect()  # enforce garbage collection

    # Return the predicted class (0 for 'declarative', 1 for 'interrogative')
    return "phatic" if predicted.item() == 0 else "referential"


def generate_subject(question):
    # Tokenize the question
    bart_extraction_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    bart_extraction_model = BartForConditionalGeneration.from_pretrained(TOPIC_BART)

    inputs = bart_extraction_tokenizer(question, return_tensors='pt', max_length=128, truncation=True, padding='max_length')

    # Generate prediction
    outputs = bart_extraction_model.generate(**inputs)

    # Decode the output
    subject = bart_extraction_tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(str(subject))
    del bart_extraction_model
    torch.cuda.empty_cache()  # clear unused memory in PyTorch
    gc.collect()  # enforce garbage collection

    return subject

def generate_summary(document_matrix):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
    model = BartForConditionalGeneration.from_pretrained(SYNTHESIS_BART)  # Replace with your trained model's path
    #document_matrix = str(document_matrix)
    # Remove newline characters, replace single quotes with double quotes, and load as JSON
    print(type(document_matrix))
    input_text = ' '.join([doc['document_content'].replace('\n', ' ').replace('\t', ' ') for doc in document_matrix])

    # Join all the documents in the document matrix into a single string
    input_text = ' '.join([doc['document_content'].replace('\n', ' ').replace('\t', ' ') for doc in document_matrix])

    # Encode the input_text to input_ids
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate summary with the model
    summary_ids = model.generate(input_ids, num_beams=4, max_length=256, early_stopping=True)

    # Decode the summary ids and return the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    del model
    torch.cuda.empty_cache()  # clear unused memory in PyTorch
    gc.collect()  # enforce garbage collection
    return summary


def predict_match(subject, summary):
    model = BartForSequenceClassification.from_pretrained(MATCHING_BART)
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    model.eval()
    model.to('cuda' if torch.cuda.is_available() else 'cpu')
    with torch.no_grad():  # deactivate autograd engine to reduce memory usage and speed up computations
        inputs = tokenizer(subject, summary, return_tensors='pt', truncation=True, padding='max_length', max_length=256)
        inputs = inputs.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move the inputs to the GPU if available
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)  # convert logits to probabilities
        predicted_class_prob = probs[:, 1].item()  # get the probability of class '1'
        print(predicted_class_prob)
        predicted_class_idx = int(predicted_class_prob > 0.5)  # classify as '1' if probability of class '1' is > 0.9999
    del model
    torch.cuda.empty_cache()  # clear unused memory in PyTorch
    gc.collect()  # enforce garbage collection
    return predicted_class_idx

def test_search_documents(self, search_input, conversation_id=None):
        """
        Search for the given input in the vector store and return the top 10 most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """

        #print(f"Searching for: {search_input} in LTM")
        docs = self.vector_store_docs.similarity_search_with_score(
            search_input, k=4, filter=filter
        )
        return [{"document_content": doc[0].page_content, "similarity": doc[1]} for doc in docs]


def load_tools():  
    #llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False,n_gpu_layers=n_gpu_layers, use_mlock=use_mlock,top_p=0.9, n_batch=n_batch)

    def ingest_file(file_path):
        # Load unstructured document
        documents = load_unstructured_document(file_path)

        # Split documents into chunks
        documents = split_documents(documents, chunk_size=120, chunk_overlap=20)

        # Determine the embedding model to use
        EmbeddingsModel = EMBEDDINGS_MAP.get(EMBEDDINGS_MODEL)
        if EmbeddingsModel is None:
            raise ValueError(f"Invalid embeddings model: {EMBEDDINGS_MODEL}")

        model_kwargs = {"device": "cuda:0"} if EmbeddingsModel == HuggingFaceInstructEmbeddings else {}
        embedding = EmbeddingsModel(model_name=EMBEDDINGS_MODEL, model_kwargs=model_kwargs)

        # Store embeddings from the chunked documents
        vectordb = Chroma.from_documents(documents=documents, embedding=embedding)

        retriever = vectordb.as_retriever(search_kwargs={"k":4})

        print(file_path)
        print(retriever)

        return retriever, file_path

    file_path = TEST_FILE
    retriever, title = ingest_file(file_path)


    dict_tools = {
        'File Ingestion': ingest_file,
    }

    return dict_tools

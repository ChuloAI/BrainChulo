import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings():
    def __init__(self):
        # Chat API - By default, we are assuming Oobabooga's Text Generation
        # WebUI is running
        self.embeddings_model = os.getenv(
            "EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
        
        self.chat_api_url = os.getenv(
            "CHAT_API_URL", "http://localhost:5000/api/v1/generate")

        # Where short-term memory is stored
        self.memories_path = os.getenv("MEMORIES_PATH", "memories/")

        # Where uploads are saved
        self.upload_path = os.getenv("UPLOAD_PATH", "uploads/")

        # Document store name
        self.document_store_name = os.getenv(
            "DOCUMENT_STORE_NAME", "brainchulo_docs")
        self.conversation_store_name = os.getenv(
            "CONVERSATION_STORE_NAME", "brainchulo_convos")

        # Default objective - If we go objective-based, this is the default
        self.default_objective = os.getenv("DEFAULT_OBJECTIVE", "Be a CEO.")

        # The agent can use tools and come up with a response via REaCT prompt framework
        self.use_agent = False


def load_config():
    return Settings()

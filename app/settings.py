import os
from dotenv import load_dotenv
import logging
from langchain.embeddings import (
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings,
)

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings:
    def __init__(self):
        # Chat API - By default, we are assuming Oobabooga's Text Generation
        # WebUI is running
        self.root_path = os.getcwd()

        if self.root_path.endswith("app"):
            self.root_path = self.root_path[:-4]

        self.model_root_path = os.path.join(self.root_path, "models")
        self.backend_root_path = os.path.join(self.root_path, "app")

        # let's ensure the models and backend path is accurate when mounting docker volumes
        if self.root_path.startswith("/code"):
            self.model_root_path = "/models"
            self.backend_root_path = self.root_path

        # Guidance new settings
        self.test_file = os.getenv("TEST_FILE", "/data/uploads/the_trial.txt")
        self.embeddings_map = {
            **{name: HuggingFaceInstructEmbeddings for name in ["hkunlp/instructor-xl", "hkunlp/instructor-large"]},
            **{name: HuggingFaceEmbeddings for name in ["all-MiniLM-L6-v2", "sentence-t5-xxl"]},
        }
        self.persist_directory = os.getenv("PERSIST_DIRECTORY", "./persist_directory")

        self.embeddings_model = os.getenv("EMBEDDINGS_MODEL", f"{self.model_root_path}/all-MiniLM-L6-v2")

        self.chat_api_url = os.getenv("CHAT_API_URL", "http://0.0.0.0:5000/api/v1/generate")
        self.model_path = os.getenv("MODEL_PATH", f"{self.model_root_path}/wizardLM-7B-HF")

        # Where all data is stored
        self.data_path = os.getenv("DATA_PATH", f"{self.backend_root_path}/data")

        # Where short-term memory is stored
        self.memories_path = os.getenv("MEMORIES_PATH", f"{self.data_path}/memories")

        # Where uploads are saved
        self.upload_path = os.getenv("UPLOAD_PATH", f"{self.data_path}/uploads")

        # Where conversation history is stored
        self.conversation_history_path = os.getenv(
            "CONVERSATION_HISTORY_PATH",
            f"{self.data_path}/conversation_history/",
        )

        # Document store name
        self.document_store_name = os.getenv("DOCUMENT_STORE_NAME", "brainchulo_docs")
        self.conversation_store_name = os.getenv("CONVERSATION_STORE_NAME", "brainchulo_convos")

        # Default objective - If we go objective-based, this is the default
        self.default_objective = os.getenv("DEFAULT_OBJECTIVE", "Be a CEO.")

        # Database URL
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///data/brainchulo.db")

        self.andromeda_url = os.getenv("ANDROMEDA_URL", "http://0.0.0.0:9000")

        self.use_flow_agents = os.getenv("USE_FLOW_AGENTS", "false") == "true"

def load_config():
    return Settings()

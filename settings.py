import os
from dotenv import load_dotenv
import logging

load_dotenv()


class Settings():
  def __init__(self):
    # Chat API - By default, we are assuming Oobabooga's Text Generation WebUI is running
    self.chat_api_host = os.getenv("CHAT_API_HOST", "http://localhost")
    self.chat_api_port = os.getenv("CHAT_API_PORT", 7860)
    self.chat_api_path = os.getenv("CHAT_API_PATH", "/run/textgen/")

    # Where short-term memory is stored
    self.index_path = os.getenv("INDEX_PATH", "index.json")

    # Default objective - If we go objective-based, this is the default
    self.default_objective = os.getenv("DEFAULT_OBJECTIVE", "Be a CEO.")


def load_config():
  return Settings()


class Logger():
  def __init__(self) -> logging.Logger:
     return logging.getLogger(__name__)

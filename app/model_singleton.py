"""This module is a temporary workaround.

We define a global model Singleton here...
"""
from app.settings import Settings
import guidance

llama = None

def load_model_into_guidance(settings: Settings):
    global llama
    llama = guidance.llms.Transformers(settings.model_path, device_map="auto", load_in_8bit=True)
    return llama
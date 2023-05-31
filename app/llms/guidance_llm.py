import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from settings import load_config
from guidance_tooling.guidance_client.guidance_client import guidance_url

config = load_config()

class ModelBehindGuidance(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"
    

    def _call_api(self, prompt, stop, max_new_tokens=256, temperature=0.2):
        data = {
            "prompt": prompt,
            "stop": stop,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
        }

        response = requests.post(
            guidance_url + "/raw", 
            json=data
        )
        
        response.raise_for_status()
        
        return response.json()["output"]


    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        stop = stop or []
        if not isinstance(stop, list):
            raise TypeError("stop parameter must be a list")

        # For now we must send a single stop string 
        if stop:
            stop = stop[0]
        else:
            stop = ""

        response = self._call_api(
            prompt,
            stop=stop
        )

        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}

import os
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from settings import load_config, logger

config = load_config()

PARAMS = {
    'max_new_tokens': 100,
    'do_sample': True,
    'temperature': 0.2,
    'top_p': 0.73,
    'typical_p': 1,
    'repetition_penalty': 1.1,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1,
    'early_stopping': False,
    'seed': -1,
    'add_bos_token': True,
    'truncation_length': 2048,
    'ban_eos_token': False,
    'skip_special_tokens': True,
    'stopping_strings': [],
}


class OobaboogaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        stop = stop or []
        if not isinstance(stop, list):
            raise TypeError("stop parameter must be a list")

        response = self.call_api(prompt, {
            "max_new_tokens": 256,
            "temperature": 0.1,
            "stopping_strings": stop + ["### Human:", '\n### Human:', "\nHuman:", "\nHuman"]
        })

        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}

    def call_api(self, prompt_str, params={}):
        url = config.chat_api_url
        headers = {"Content-Type": "application/json"}
        _params = PARAMS

        for k, v in params.items():
            _params[k] = v

        _params['prompt'] = prompt_str

        response = requests.post(
            url, headers=headers, json=_params, timeout=500)

        # Check for errors in API response
        if response.status_code != 200:
            logger.error(f"Error generating text: {response.text}")
            return {}

        # Parse generated text from API response
        response_data = response.json()["results"]
        if len(response_data) < 1:
            logger.error("Error generating text: Empty response from API")
            return ''

        generated_text = response_data[0]['text']

        return generated_text


if __name__ == "__main__":
    objective = os.getenv("DEFAULT_OBJECTIVE", "Be a CEO.")
    task = "Create a task list."
    response = OobaboogaLLM().call_api(f"""
    You are an AI who performs one task based on the following objective: {objective}\n.
    Your task: {task}\nResponse:""")
    print(response)

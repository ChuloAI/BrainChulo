import os
import json
from dotenv import load_dotenv
import requests

# Load default environment variables (.env)
load_dotenv()

WEBUI_HOST = os.getenv("WEBUI_HOST", "http://localhost")
WEBUI_PORT = os.getenv("WEBUI_PORT", 7860)

PARAMS = {
    'max_new_tokens': 100,
    'temperature': 0.5,
    'top_p': 0.9,
    'typical_p': 1,
    'n': 1,
    'stop': None,
    'do_sample': True,
    'return_prompt': False,
    'return_metadata': False,
    'typical_p': 0.95,
    'repetition_penalty': 1.05,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 2,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1.0,
    'pad_token_id': None,
    'eos_token_id': None,
    'use_cache': True,
    'num_return_sequences': 1,
    'bad_words_ids': None,
    'seed': -1,
    'is_instruct': True,
    'add_bos_token': True,
    'truncation_length': 2048,
    'custom_stopping_strings': [],
    'ban_eos_token': False,
}


def call_api(prompt_str, params={}):
    url = f"{WEBUI_HOST}:{WEBUI_PORT}/run/textgen"
    headers = {"Content-Type": "application/json"}
    _params = PARAMS

    for k, v in params.items():
        _params[k] = v

    payload = json.dumps([prompt_str, _params])

    response = requests.post(url, headers=headers, json={
        "data": [
            payload
        ]
    }, timeout=500)

    # Check for errors in API response
    if response.status_code != 200:
        print(f"Error generating text: {response.text}")
        return {}

    # Parse generated text from API response
    response_data = response.json()["data"]
    if len(response_data) < 1:
        print("Error generating text: Empty response from API")
        return {}
    generated_text = response_data[0]

    # Save generated text and return it
    generated_text = generated_text[len(
        prompt_str):len(generated_text)]

    return generated_text


if __name__ == "__main__":
    objective = os.getenv("OBJECTIVE", "Be a CEO.")
    task = "Create a task list."
    response = call_api(f"""
    You are an AI who performs one task based on the following objective: {objective}\n.
    Your task: {task}\nResponse:""")
    print(response)

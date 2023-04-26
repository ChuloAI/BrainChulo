import os
import json
import requests
import settings

config = settings.load_config()

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


def call_api(prompt_str, params={}):
  url = f"{config.chat_api_host}:{config.chat_api_port}{config.chat_api_path}"
  headers = {"Content-Type": "application/json"}
  _params = PARAMS

  for k, v in params.items():
    _params[k] = v

  _params['prompt'] = prompt_str

  response = requests.post(url, headers=headers, json=_params, timeout=500)

  # Check for errors in API response
  if response.status_code != 200:
    print(f"Error generating text: {response.text}")
    return {}

  # Parse generated text from API response
  response_data = response.json()["results"]
  if len(response_data) < 1:
    print("Error generating text: Empty response from API")
    return ''

  generated_text = response_data[0]['text']

  return generated_text


if __name__ == "__main__":
  objective = config.default_objective
  task = "Create a task list."
  response = call_api(f"""
    You are an AI who performs one task based on the following objective: {objective}\n.
    Your task: {task}\nResponse:""")
  print(response)

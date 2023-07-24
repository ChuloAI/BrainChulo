import requests
HOST = '0.0.0.0:5000'  # API details
URI = f'http://{HOST}/api/v1/generate'

def questions_listing(question, context):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Make a list of 5 questions you should ask yourself to infer the answer to '{question}' from a piece of text.

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
        
def questions_answering(question, context, questions):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Answer '{questions}' relatively to '{context}'

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 400,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result

def api_data_matching(question, context, questions):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Infer the answer to '{question}' from: "{context}".
Here are the questions you should ask yourself: {questions}

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
    
def api_data_evaluation(question, context):
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
### Human:
Evaluate if the answer to '{question}' is found or can be inferred from: "{context}".

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }

        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
        
def phatic_api_answer(question, history, context):
        print("TEST")
        prompt = f'''A chat between a curious human and an artificial intelligence assistant. The assistant always comply and gives helpful, detailed, and polite answers to the human's questions taking into accounrt their chat history.
### Human:
History: {history}  
Context: {context}
Latest user's message: '{question}

### Assistant: '''
        print(str(prompt))
        request = {
            'prompt': prompt,
            'max_new_tokens': 200,
            'preset': 'Divine Intellect',
            }
        
        response = requests.post(URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
    
from guidance_tooling.guidance_prompt import GuidancePrompt
import requests


def run_guidance_prompt(prompt: GuidancePrompt, input_vars):
    print("[GUIDANCE CALL]: ", prompt.name)
    return _call_guidance(
        prompt_template=prompt.prompt_template,
        input_vars=input_vars,
        output_vars=prompt.output_vars,
        guidance_kwargs=prompt.guidance_kwargs
    )


guidance_url = "http://0.0.0.0:9000"
def _call_guidance(prompt_template, output_vars, input_vars=None, guidance_kwargs=None):
    """
    This function calls a guidance API with the given parameters and returns the response.
    
    Parameters:
    prompt_template (str): The prompt template to use for the guidance.
    output_vars (dict): The output variables to use for the guidance.
    input_vars (dict): The input variables to use for the guidance.
    guidance_kwargs (dict): The guidance keywords to use for the guidance.
    
    Returns:
    dict: The response from the guidance API.
    """
    
    if input_vars is None:
        input_vars = {}
    if guidance_kwargs is None:
        guidance_kwargs = {}
    
    data = {
        "prompt_template": prompt_template,
        "output_vars": output_vars,
        "guidance_kwargs": guidance_kwargs,
        "input_vars": input_vars,
    }
    
    response = requests.post(
        guidance_url, 
        json=data
    )
    
    response.raise_for_status()
    
    return response.json()



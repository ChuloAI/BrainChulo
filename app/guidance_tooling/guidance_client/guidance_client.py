from guidance_tooling.guidance_prompt import GuidancePrompt
import requests
from copy import deepcopy
from typing import Dict

def run_guidance_prompt(guidance_prompt: GuidancePrompt, input_vars, macro_values=None) -> Dict[str, str]:
    print("[GUIDANCE CALL]: ", guidance_prompt.name)

    # Macro variables are generaly currently not necessary
    # Unless you want to dynamically set guidance settings that are normally not settable.
    # 
    # One example is the number of iterations guidance should loop on a specific generation. 
    macro_vars = deepcopy(guidance_prompt.macro_vars)
    prompt_str = guidance_prompt.prompt_template
    if macro_values is not None:
        keys = list(macro_vars.keys())
        for key in keys:
            macro_identifier = macro_vars.pop(key)
            value = macro_values.pop(key)
            prompt_str = prompt_str.replace(macro_identifier, str(value))
    
    if macro_vars:
        raise TypeError("Unexpanded macro variables in prompt! Fix your prompt or pass the macro variable")

    print("[GUIDANCE CALL INPUT VARS]: ", input_vars)
    return _call_guidance(
        prompt_template=prompt_str,
        input_vars=input_vars,
        output_vars=guidance_prompt.output_vars,
        guidance_kwargs=guidance_prompt.guidance_kwargs
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



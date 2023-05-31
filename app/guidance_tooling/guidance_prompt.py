from typing import Dict
from dataclasses import dataclass

@dataclass
class GuidancePrompt:
    prompt_template: str
    input_vars: Dict[str, str]
    output_vars: Dict[str, str]
    guidance_kwargs: Dict[str, str]
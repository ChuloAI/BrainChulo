from typing import Dict
from dataclasses import dataclass, field

@dataclass
class GuidancePrompt:
    name: str
    prompt_template: str
    input_vars: Dict[str, str]
    output_vars: Dict[str, str]
    guidance_kwargs: Dict[str, str] = field(default_factory=dict)
    macro_vars: Dict[str, str] = field(default_factory=dict)


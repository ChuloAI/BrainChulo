from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import webui


class VicunaLLM(LLM):
  @property
  def _llm_type(self) -> str:
    return "custom"

  def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
    stop = stop or []
    if not isinstance(stop, list):
      raise TypeError("stop parameter must be a list")

    response = webui.call_api(prompt, {
        "max_new_tokens": 256,
        "temperature": 0.5,
        "stopping_strings": stop + ["### Human:", "\end", "<end>"]
    })

    return response

  @property
  def _identifying_params(self) -> Mapping[str, Any]:
    return {}

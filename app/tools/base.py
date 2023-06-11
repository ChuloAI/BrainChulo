from pyparsing import abstractmethod
from typing import Dict, List, Any


class ToolFactory():
    """Instantiates tools with a reference to the current conversation_id"""
    def __init__(self, list_of_tool_classes: List["BaseTool"]) -> None:
        self._tool_class_references = list_of_tool_classes

    def build_tools(self, conversation_id, context: Dict[str, Any]) -> Dict[str, "BaseTool"]:
        resolved_tools = {}
        for tool_class in self._tool_class_references:
            tool = tool_class(conversation_id, context)
            resolved_tools[tool.name] = tool
        return resolved_tools


class BaseTool:
    """Base interface expected of tools"""
    def __init__(self, conversation_id: str, name: str, tool_context: Dict[str, Any], required_context_keys: List[str]):
        """Stores a reference to the conversation ID.
        
        Avoiding injecting expensive operations in the __init__ method of the subclasses.
        If you need to do something expensive, use a Singleton or redesign this Tool interface.

        The reason being is that these Tools are instantied **per processed message**, so the
        constructor must be cheap to execute.
        """
        self.conversation_id = conversation_id
        self.name = name
        self.tool_context = tool_context
        self._validate_context_keys(required_context_keys, tool_context)

    def _validate_context_keys(self, keys, context):
        for key in keys:
            if key not in context:
                raise TypeError(f"This instance of {self.__class__.__name__} requires variable {key} in context.")


    @abstractmethod
    def short_description(self) -> str:
        """Returns a short description of the tool."""
        raise NotImplementedError()

    @abstractmethod
    def few_shot_examples(self) -> str:
        """Returns few """
        raise NotImplementedError()
    
    @abstractmethod
    def __call__(self, variables: Dict[str, str]) -> str:
        """Executes the tool"""
        raise NotImplementedError()

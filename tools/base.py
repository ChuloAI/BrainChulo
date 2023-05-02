from pydantic import BaseModel
from pyparsing import abstractmethod


class BaseTool(BaseModel):
    @abstractmethod
    def commands(self):
        """
        Return a dictionary of available commands for this object.

        The returned dictionary should be a collection of key-value pairs where the key
        represents the name of a command that can be executed on this object, and the value
        represents the function that implements the command. If there are no commands
        available for this object, an empty dictionary should be returned.

        Returns:
            A dictionary of available commands for this object.
        """
        pass

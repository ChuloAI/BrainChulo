from settings import Settings
from tools.base import BaseTool

config = Settings.load_config()


class WebAccess(BaseTool):
  url: str

  def commands(self):
    return {}

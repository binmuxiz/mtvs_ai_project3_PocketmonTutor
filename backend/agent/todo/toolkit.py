from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain_core.tools import BaseTool

from .tools import AddTodoTool
# from .tools import AddTodoTool, CompleteTodoTool, ViewTodoTool, RemoveTodoTool

from typing import List

from pydantic import Field

class TodoToolkit(BaseToolkit):

    def get_tools(self) -> List[BaseTool]:
        return [
            AddTodoTool(),
            # ViewTodoTool(),
            # CompleteTodoTool(),
            # RemoveTodoTool()
        ]

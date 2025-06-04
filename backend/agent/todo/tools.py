from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

import json


class AddTodoInput(BaseModel):
    title: str = Field(description="추가할 할 일 제목")

class AddTodoTool(BaseTool):
    name: str = "add_todo"
    description: str = "할 일 추가"
    args_schema: Type[BaseModel] = AddTodoInput

    def _run(self, title) -> str:
        # 판단만 하고 JSON 형태로 반환
        action_json =  json.dumps({
            "action": "add_todo",
            "title": title
        })

        action_json = str(action_json)
        return action_json
    
    async def _arun(self, title: str) -> str:
        return self._run(title)
    



# ✅ View Todos
class ViewTodoTool(BaseTool):
    name: str = "view_todos"
    description: str = "현재 db에 저장된 할 일 목록을 보여줍니다."

    def _run(self) -> str:
        return json.dumps({
            "action": "view_todos"
        })

    async def _arun(self) -> str:
        return self._run()


# ✅ Complete Todo
class CompleteTodoInput(BaseModel):
    todo_id: int = Field(description="완료할 할 일의 ID")

class CompleteTodoTool(BaseTool):
    name: str = "complete_todo"
    description: str = "지정한 ID의 할 일을 완료로 표시합니다."
    args_schema: Type[BaseModel] = CompleteTodoInput

    def _run(self, todo_id: int) -> str:
        return json.dumps({
            "action": "complete_todo",
            "todo_id": todo_id
        })

    async def _arun(self, todo_id: int) -> str:
        return self._run(todo_id)


# ✅ Remove Todo
class RemoveTodoInput(BaseModel):
    todo_id: int = Field(description="삭제할 할 일의 ID")

class RemoveTodoTool(BaseTool):
    name: str = "remove_todo"
    description: str = "지정한 ID의 할 일을 삭제합니다."
    args_schema: Type[BaseModel] = RemoveTodoInput

    def _run(self, todo_id: int) -> str:
        return json.dumps({
            "action": "remove_todo",
            "todo_id": todo_id
        })

    async def _arun(self, todo_id: int) -> str:
        return self._run(todo_id)
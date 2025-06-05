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
    description: str = "할 일 목록 조회"

    def _run(self) -> str:
        return json.dumps({
            "action": "view_todos"
        })

    async def _arun(self) -> str:
        return self._run()




# ✅ Complete Todo
class CompleteTodoInput(BaseModel):
    title: str

class CompleteTodoTool(BaseTool):
    name: str = "complete_todo"
    description: str = "할 일 완료"
    args_schema: Type[BaseModel] = CompleteTodoInput

    def _run(self, title) -> str:
        # 판단만 하고 JSON 형태로 반환
        action_json =  json.dumps({
            "action": "complete_todo",
            "title": title
        })

        action_json = str(action_json)
        return action_json
    
    async def _arun(self, title: str) -> str:
        return self._run(title)




# ✅ Remove Todo
class RemoveTodoInput(BaseModel):
    title: str

class RemoveTodoTool(BaseTool):
    name: str = "remove_todo"
    description: str = "할 일 삭제"
    args_schema: Type[BaseModel] = RemoveTodoInput

    def _run(self, title) -> str:
        # 판단만 하고 JSON 형태로 반환
        action_json =  json.dumps({
            "action": "remove_todo",
            "title": title
        })

        action_json = str(action_json)
        return action_json
    
    async def _arun(self, title: str) -> str:
        return self._run(title)
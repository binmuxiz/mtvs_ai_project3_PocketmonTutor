import sqlite3
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


DB_PATH = "todo.db"

class AddTodoInput(BaseModel):
    user_id: str = Field(description="사용자 ID")
    title: str = Field(description="추가할 할 일 제목")

class AddTodoTool(BaseTool):
    name: str = "add_todo"
    description: str = "할 일을 db에 추가합니다."
    args_schema: Type[BaseModel] = AddTodoInput

    def _run(self, user_id, title:str) -> str:
        conn = sqlite3.connect("todos.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (user_id, title) VALUES (?, ?)", (user_id, title))
        conn.commit()
        conn.close()
        return f"✅ '{title}' 할 일이 사용자 {user_id}에게 추가되었습니다."
    
    async def _arun(self, user_id, title: str) -> str:
        return self._run(user_id, title)
    


class ViewTodoTool(BaseTool):
    name: str = "view_todos"
    description: str = "현재 db에 저장된 할일 목록을 보여줍니다."

    def _run(self) -> str:
        conn = sqlite3.connect("todos.db")
        cur = conn.cursor()
        cur.execute("SELECT id, title, complete FROM todos")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return "📭 할 일이 없습니다."
        
        result = ""
        for row in rows:
            check = "✅" if row[2] else "☐"
            result += f"{row[0]}. {check} {row[1]}\n"
        return result.strip()
    

    async def _arun(self) -> str:
        return self._run()
    


class CompleteTodoInput(BaseModel):
    todo_id: int = Field(description="완료할 할 일의 ID")

class CompleteTodoTool(BaseTool):
    name: str = "complete_todo"
    description: str = "지정한 ID의 할 일을 완료로 표시합니다."
    args_schema: Type[BaseModel] = CompleteTodoInput

    def _run(self, todo_id: int) -> str:
        conn = sqlite3.connect("todos.db")
        cur = conn.cursor()
        cur.execute("UPDATE todos SET complete = 1 WHERE id = ?", (todo_id,))
        conn.commit()
        affected = cur.rowcount
        conn.close()

        if affected:
            return f"🎉 ID {todo_id}번 할 일을 완료했습니다!"
        else:
            return "❌ 해당 ID를 찾을 수 없습니다."

    async def _arun(self, todo_id: int) -> str:
        return self._run(todo_id)



class RemoveTodoInput(BaseModel):
    todo_id: int = Field(description="삭제할 할 일의 ID")

class RemoveTodoTool(BaseTool):
    name: str = "remove_todo"
    description: str = "지정한 ID의 할 일을 삭제합니다."
    args_schema: Type[BaseModel] = RemoveTodoInput

    def _run(self, todo_id: int) -> str:
        conn = sqlite3.connect("todos.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        affected = cur.rowcount
        conn.close()

        if affected:
            return f"🗑️ ID {todo_id}번 할 일을 삭제했습니다."
        else:
            return "❌ 해당 ID를 찾을 수 없습니다."

    async def _arun(self, todo_id: int) -> str:
        return self._run(todo_id)

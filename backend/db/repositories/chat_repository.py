from typing import Literal

from db import get_connection

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Literal


def save_chat(user_id: str, sender: Literal['user', 'ai'], message: str) -> None:
    """대화 기록을 DB에 저장"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (user_id, sender, message) VALUES (?, ?, ?)",
            (user_id, sender, message)
        )
        conn.commit()
        
    except Exception as e:
        print(f"❌ 채팅 저장 실패: {e}")
    finally:
        conn.close()



# 채팅 기록 불러오기
def load_chat(user_id: str) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT sender, message FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [{'sender': row[0], 'message': row[1]} for row in rows]



# # SQLite에서 채팅 기록 삭제
# def delete_user_chat_history(user_id: str):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
#     conn.commit()
#     conn.close()



# LangChain에서 사용할 SQLite 기반 메시지 히스토리 클래스
class SQLiteChatHistory(BaseChatMessageHistory):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def add_user_message(self, message: str):
        save_chat(user_id=self.user_id, sender='user', message=message)

    def add_ai_message(self, message: str):
        save_chat(user_id=self.user_id, sender='ai', message=message)

    def get_messages(self):
        records = load_chat(self.user_id)
        messages = []
        for row in records:
            if row["sender"] == "user":
                messages.append(HumanMessage(content=row["message"]))
            else:
                messages.append(AIMessage(content=row["message"]))
        return messages

    # def clear(self):
    #     delete_user_chat_history(self.user_id)




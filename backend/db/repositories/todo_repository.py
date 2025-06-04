from db import get_connection

# ==================================== Todo 추가 ====================================

def add_todo(user_id: str, title: str) -> None:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO todos (user_id, title) VALUES (?, ?)",
            (user_id, title)
        )
        conn.commit()
    except Exception as e:
        print(f"❌ Todo 저장 실패: {e}")
    finally:
        conn.close()


# ==================================== Todo 조회 ====================================

def view_todos(user_id: str) -> str:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT title, complete FROM todos WHERE user_id = ?",
            (user_id,)
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return "📭 저장된 할 일이 없습니다."

        result = ""
        for row in rows:
            check = "✅" if row[2] else "☐"
            result += f"{row[0]}. {check} {row[1]}\n"
        return result.strip()
    
    except Exception as e:
        print(f"❌ Todo 조회 실패: {e}")
        return "🚨 할 일 목록을 불러오는데 실패했습니다."


# ==================================== Todo 완료 처리 ====================================

def complete_todo(user_id: str, todo_id: int) -> str:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE todos SET complete = 1 WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        conn.commit()
        affected = cur.rowcount
        conn.close()

        if affected:
            return f"🎉 ID {todo_id}번 할 일을 완료했어요!"
        else:
            return f"❌ ID {todo_id}번 할 일을 찾을 수 없어요."
        
    except Exception as e:
        print(f"❌ Todo 완료 처리 실패: {e}")
        return "🚨 할 일을 완료 처리하는 중 문제가 발생했습니다."


# ==================================== Todo 삭제 ====================================

def remove_todo(user_id: str, todo_id: int) -> str:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        conn.commit()
        affected = cur.rowcount
        conn.close()

        if affected:
            return f"🗑️ ID {todo_id}번 할 일을 삭제했어요!"
        else:
            return f"❌ ID {todo_id}번 할 일을 찾을 수 없어요."
        
    except Exception as e:
        print(f"❌ Todo 삭제 실패: {e}")
        return "🚨 할 일을 삭제하는 중 문제가 발생했습니다."


# ==================================== User별 todo 목록 ====================================

def get_todos_by_user_id(user_id: str) -> list[dict]:
    """
    특정 user_id의 todo 목록을 모두 반환합니다.
    반환 형식: [{"id": 1, "title": "영어 숙제 하기", "complete": 0}]
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, complete FROM todos WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
    finally:
        conn.close()

    # 튜플 → 딕셔너리로 변환
    todos = [
        {
            "id": row[0],
            "title": row[1],
            "complete": bool(row[2])
        }
        for row in rows
    ]
    return todos

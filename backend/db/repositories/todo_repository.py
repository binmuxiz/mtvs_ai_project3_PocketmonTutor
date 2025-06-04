from db import get_connection

# ==================================== Todo 추가  ==================================== 

def add_todo(user_id: str, title: str) -> None:

    print('--------------add_todo db---------------------------')
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 삽입 쿼리
        cur.execute(
            "INSERT INTO todos (user_id, title) VALUES (?, ?)",
            (user_id, title)
        )
        conn.commit()
    except Exception as e:
        print(f"❌ Todo 저장 실패: {e}")
    
    finally:
        conn.close()

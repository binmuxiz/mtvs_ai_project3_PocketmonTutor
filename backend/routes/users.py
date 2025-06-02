from fastapi import APIRouter, HTTPException
from models import UserCreate
from db import get_connection

router = APIRouter()




@router.post("/")
async def generate(data: UserCreate):
    
    conn = get_connection()

    try:
        cur = conn.cursor()

        # 사용자 존재 확인
        cur.execute("SELECT * FROM users WHERE user_id = ?", (data.user_id,))

        if cur.fetchone():
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자 ID입니다.")

        cur.execute("""
            INSERT INTO users (user_id, name)
            VALUES (?, ?)
        """, (
            data.user_id,
            data.name
        ))
        conn.commit()

        print("사용자 등록 완료 id = ", data.user_id)

    except Exception as e:
        conn.rollback()
        raise 

    finally:
        conn.close()

    return {
        "message": "사용자 등록 완료!",
    }


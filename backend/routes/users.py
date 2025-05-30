from fastapi import APIRouter, HTTPException
from models import UserCreate
from db import get_connection

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    # 이미 존재하는지 확인
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user.user_id,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자 ID입니다.")

    cur.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user.user_id, user.name))
    conn.commit()
    conn.close()
    return {"message": "사용자 등록 완료!"}

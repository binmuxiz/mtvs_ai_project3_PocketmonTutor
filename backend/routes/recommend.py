from fastapi import APIRouter, HTTPException
from models import RecommendationRequest
from db import get_connection

router = APIRouter()

@router.post("/")
def save_recommendation(data: RecommendationRequest):
    conn = get_connection()
    cur = conn.cursor()

    # 사용자 존재 확인
    cur.execute("SELECT * FROM users WHERE user_id = ?", (data.user_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="해당 사용자 ID가 존재하지 않습니다.")

    cur.execute("""
        INSERT INTO recommendations (user_id, personality, hobby, color, mood, type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.user_id,
        data.personality,
        data.hobby,
        data.color,
        data.mood,
        data.type
    ))
    conn.commit()
    conn.close()
    return {"message": "추천 정보 저장 완료!"}

from fastapi import APIRouter, HTTPException
from models import UserCreate
from db import get_connection

router = APIRouter()


    # request.app.state ?
    # FastAPI에서 request.app은 현재 실행중인 FastAPI 앱 인스턴스,
    # .state는 애플리케이션 전체에서 공유되는 임시 저장 공간임
    # loaded_tools는 main.py에서 저장했던 MCP에서 받아온 LangGraph 툴들의 리스트 
    # tools = request.app.state.loaded_tools

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
            INSERT INTO users (user_id, name, personality, hobby, color, mood, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.user_id,
            data.name,
            data.personality,
            data.hobby,
            data.color,
            data.mood,
            data.type
        ))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {str(e)}")

    finally:
        conn.close()

    print("사용자 등록 완료 id = ", data.user_id)

    return {
        "message": "사용자 등록 완료!",
    }


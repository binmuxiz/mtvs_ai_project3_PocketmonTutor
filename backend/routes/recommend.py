from fastapi import APIRouter, HTTPException, Request
from models import RecommendationRequest
from db import get_connection
from langgraph_agent.pokemon_agent import generate_recommendation


router = APIRouter()

@router.post("/generate")
async def generate(data: RecommendationRequest, request: Request):

    # request.app.state ?
    # FastAPI에서 request.app은 현재 실행중인 FastAPI 앱 인스턴스,
    # .state는 애플리케이션 전체에서 공유되는 임시 저장 공간임
    # loaded_tools는 main.py에서 저장했던 MCP에서 받아온 LangGraph 툴들의 리스트 
    tools = request.app.state.loaded_tools

    conn = get_connection()
    try:
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

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {str(e)}")

    finally:
        conn.close()

    # ✅ 저장 성공시에만 호출
    result = await generate_recommendation(data, request)

    return {
        "message": "추천 정보 저장 완료!",
        "result": result
    }


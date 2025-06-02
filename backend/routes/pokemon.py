from fastapi import APIRouter, HTTPException, Request
from models import RecommendationRequest
from agent.pokemon_agent import generate_recommendation
from db import get_connection

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def recommend_pokemon(data: RecommendationRequest, request: Request):
    conn = get_connection()
    cur = conn.cursor()

# 사용자 존재 확인
    cur.execute("SELECT id FROM users WHERE user_id = ?", (data.user_id, ))
    user_row = cur.fetchone()

    if not user_row: 
        raise HTTPException(status_code=404, detail="해당 사용자 ID가 존재하지 않습니다.")


# LLM 응답 재시도 로직 (최대 3회)
    max_retries = 3
    for attempt in range(1, max_retries+1):
        logger.info("%d회차 에이전트 호출 시도", attempt)

        try:
            # 2. 에이전트 호출
            result = await generate_recommendation(data, request)

            logger.info(f"에이전트 호출 결과: {result}\n")
            logger.info(f"result type: {type(result)}\n")
                    
            break
        except ValueError as ve:
            logger.warning("ValueError 발생 - %d회차 시도 실패: %s", attempt, ve)
            if attempt == max_retries:
                conn.close()
                raise HTTPException(status_code=500, detail="추천 생성 중 오류가 반복되어 실패했습니다.")
        except Exception as e:
            conn.close()
            logger.error("에이전트 실행 중 예외 발생: %s", e)
            raise HTTPException(status_code=500, detail=f"추천 실패: {e}")

    pokemons = [result]

    import json

# DB에 저장
    for p in pokemons:
        try:
            logger.info("DB 저장 대상 포켓몬: name=%s, no=%s", p.name, p.no)

            cur.execute("""
            INSERT INTO user_pokemons (
                user_id, name, no, pokemon_type, description, match_json, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
                data.user_id,
                p.name.strip(),
                int(p.no),
                ",".join(p.pokemon_type),
                p.description,
                json.dumps(p.match, ensure_ascii=False),  # match는 JSON으로 직렬화
                p.image
            ))
        except Exception as e:
            conn.close()
            logger.error("DB 저장 중 오류 발생: %s", e)
            raise HTTPException(status_code=500, detail=f"DB 저장 중 오류 발생: {e}")

    conn.commit()
    conn.close()

    return { "message": "포켓몬 추천 결과 저장 완료!",  "recommendations": result}    
    


    
    
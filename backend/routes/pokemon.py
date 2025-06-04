from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import websocket

from models import RecommendationRequest
from agent.pokemon_agent import generate_recommendation
from db import get_connection

import uuid
import json
import os
import glob

from urllib import request as urllib_request
from urllib import parse as urllib_parse

import logging
# ===================================
# ✅ Logging 설정
# ===================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)



router = APIRouter()


from db import get_user_by_id, create_pokemon

# ============================ 포켓몬 추천 API ========================================================
@router.post("/recommend")
async def recommend_pokemon(data: RecommendationRequest, request: Request):
    user_id = data.user_id

# 사용자 존재 확인
    user_row = get_user_by_id(user_id=user_id)

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
                raise HTTPException(status_code=500, detail="추천 생성 중 오류가 반복되어 실패했습니다.")
            
        except Exception as e:
            logger.error("에이전트 실행 중 예외 발생: %s", e)
            raise HTTPException(status_code=500, detail=f"추천 실패: {e}")

    try:
# DB에 저장
        logger.info("DB 저장 대상 포켓몬: name=%s, no=%s", result.name, result.no)
        create_pokemon(user_id, result)

    except Exception as e:
        logger.error("DB 저장 중 오류 발생: %s", e)
        raise

    return { "message": "포켓몬 추천 결과 저장 완료!",  "recommendations": result}    
    


import httpx
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# --- 요청 모델 정의 ---
class PromptRequest(BaseModel):
    prompt: str  # 사용자가 입력한 이미지 URL
    user_id: str

# --- GLB 생성 및 반환 API ---
@router.post("/glb")
async def generate_glb(request: PromptRequest):
    server_address = "192.168.0.89:8000"
    target_url = f"http://{server_address}/generate-glb"

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(target_url, json={"prompt": request.prompt})

        # 원격 서버의 응답을 그대로 리턴
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )

    except httpx.RequestError as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "fail",
                "message": f"서버 요청 실패:  {repr(e)}"
            }
        )

    
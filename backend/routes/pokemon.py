from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# ============================ 포켓몬 추천 API ========================================================


@router.post("/recommend")
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
    




# ============================ 3D 모델 생성 API ========================================================

# ComfyUI 서버 주소 및 고유 클라이언트 ID
server_address = "1192.168.0.89:8000"
client_id = str(uuid.uuid4())
    

# --- 요청 모델 정의 ---
class PromptRequest(BaseModel):
    prompt: str  # 사용자가 입력한 이미지 URL



# --- GLB 생성 및 반환 API ---
@router.post("/glb")
async def generate_glb(request: PromptRequest):

    print(f"📥 요청된 이미지 URL: {request.prompt}")

    # 워크플로우 로드
    workflow_path = r"C:\llm_project\pocketmon-tutor\backend\workflows\pokemon_3d.json"
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # LoadImageFromHttpURL 노드 수정
    node_found = False
    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == "LoadImageFromHttpURL":
            if "inputs" in node and "image_url" in node["inputs"]:
                node["inputs"]["image_url"] = request.prompt
                node_found = True
                break

    if not node_found:
        return JSONResponse(content={
            "status": "fail",
            "message": "워크플로우에 'LoadImageFromHttpURL' 노드가 없습니다."
        }, status_code=400)

    # WebSocket 실행
    ws = websocket.WebSocket()
    try:
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
    except Exception as e:
        return JSONResponse(content={
            "status": "fail",
            "message": f"WebSocket 연결 실패: {str(e)}"
        }, status_code=500)

    # 프롬프트 실행
    response = queue_prompt(workflow)
    prompt_id = response.get("prompt_id")
    if not prompt_id:
        return JSONResponse(content={
            "status": "fail",
            "message": "프롬프트 실행 실패"
        }, status_code=500)

    # 실행 완료 대기
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
    ws.close()

    # 디버깅: 현재 디렉토리와 생성된 glb 로그 출력
    print("📁 현재 작업 디렉토리:", os.getcwd())
    
    # 절대 경로로 GLB 경로 설정
    COMFY_GLBS_DIR = r"C:\ONLY_COMFY\ComfyUI\output\3D"
    glb_files = sorted(
        glob.glob(os.path.join(COMFY_GLBS_DIR, "Hy3D_textured*.glb")),
        key=os.path.getmtime,
        reverse=True
    )


    if glb_files:

# 기존: FileResponse 부분 ======================================================================

        # latest_path = glb_files[0]
        # print(f"✅ 반환할 GLB 파일 경로: {latest_path}")
        # return FileResponse(
        #     path=latest_path,
        #     media_type="application/octet-stream",
        #     filename=os.path.basename(latest_path)
        # )

# 변경: URL을 반환하도록록
        latest_filename = os.path.basename(glb_files[0])
        print(f"✅ 반환할 GLB 파일: {latest_filename}")

        # Comfy 서버가 파일을 정적으로 제공한다고 가정
        glb_url = f"http://{server_address}/output/3D/{latest_filename}"

        return {
            "status": "success",
            "url": glb_url
    }
    
    else:
        return JSONResponse(content={
            "status": "fail",
            "message": "GLB 파일이 생성되지 않았습니다."
        }, status_code=500)


# --- 유틸리티 함수 정의 ---
def queue_prompt(prompt):
    payload = {
        "prompt": prompt,
        "client_id": client_id
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib_request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib_request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib_parse.urlencode(data)
    with urllib_request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib_request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # 실행 완료
        else:
            continue  # 바이너리는 무시

    history = get_history(prompt_id)[prompt_id]
    for node_id, node_output in history['outputs'].items():
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images



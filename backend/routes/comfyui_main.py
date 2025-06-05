import json
import uuid
import urllib
import os
import io
import time
import glob
import websocket
from urllib import request as urllib_request
from urllib import parse as urllib_parse
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from PIL import Image
import subprocess  # 🔧 A: subprocess 추가

# CORS 정책을 완화
#==============================================================
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 프론트 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#==============================================================


app = FastAPI()
app.mount("/output", StaticFiles(directory="C:/ONLY_COMFY/ComfyUI/output"), name="output")

# ComfyUI 서버 주소 및 고유 클라이언트 ID
server_address = "192.168.0.89:8188"
# fastpi 서버
server_address2 = "192.168.0.89:8000"
client_id = str(uuid.uuid4())

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

def apply_bounce_with_blender(input_path: str, output_path: str):
    blender_exe = r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
    script_path = r"C:\mtvs_ai_project3_PocketmonTutor\backend\routes\animation.py"

    result = subprocess.run([
        blender_exe,
        "--background",
        "--python", script_path,
        "--", input_path, output_path
    ], capture_output=True, text=True)

    print("✅ Blender STDOUT:\n", result.stdout)
    print("❌ Blender STDERR:\n", result.stderr)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=result.args,
            output=result.stdout,
            stderr=result.stderr
        )


# --- 요청 모델 정의 ---
class PromptRequest(BaseModel):
    prompt: str  # 사용자가 입력한 이미지 URL

# --- GLB 생성 및 반환 API ---
@app.post("/generate-glb")
async def generate_glb(request: PromptRequest):
    print(f"📥 요청된 이미지 URL: {request.prompt}")

    # 워크플로우 로드
    workflow_path = r"C:\mtvs_ai_project3_PocketmonTutor\backend\workflows\pokemon_3d.json"
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
        latest_path = glb_files[0]
        latest_filename = os.path.basename(latest_path)
        print(f"✅ ComfyUI 생성된 GLB 파일: {latest_filename}")

        # 🔧 Blender 애니메이션 적용
        animated_output_path = latest_path.replace(".glb", "_animated.glb")
        try:
            apply_bounce_with_blender(latest_path, animated_output_path)
        except subprocess.CalledProcessError as e:
            return JSONResponse(content={
                "status": "fail",
                "message": f"Blender 애니메이션 적용 실패: {e.stderr}"
            }, status_code=500)

        # 최종 애니메이션 적용된 GLB 파일 반환
        final_filename = os.path.basename(animated_output_path)
        print(f"🎉 최종 애니메이션 GLB 파일: {final_filename}")

        # Comfy 서버에서 정적 파일을 서비스한다고 가정
        glb_url = f"http://{server_address2}/output/3D/{final_filename}"

        return JSONResponse(content={
            "status": "success",
            "url": glb_url
        })

    else:
        return JSONResponse(content={
            "status": "fail",
            "message": "GLB 파일이 생성되지 않았습니다."
        }, status_code=500)
    
#==============================================================

@app.get("/get-glb/{filename}")
async def serve_glb_file(filename: str):
    glb_path = os.path.join(r"C:\ONLY_COMFY\ComfyUI\output\3D", filename)
    if not os.path.exists(glb_path):
        return JSONResponse(status_code=404, content={"status": "fail", "message": "파일이 존재하지 않습니다."})
    
    return FileResponse(
        glb_path,
        media_type="model/gltf-binary",
        headers={"Access-Control-Allow-Origin": "*"}  # ✅ GLTFLoader를 위한 CORS 허용
    )
#==============================================================
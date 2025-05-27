# FastAPI에서 호출할 comfy 실행 래퍼

import subprocess
import os
import time

def launch_comfy_server():
    print(os.getcwd())
    comfy_dir = os.path.join(os.getcwd(), "comfy_server")

    # 서버 실행
    process = subprocess.Popen(
        ["python", "main.py"],
        cwd=comfy_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE

    )

    print("[ComfyUI] 서버 실행중...")
    time.sleep(3) # 서버가 완전히 뜰 때까지 기다리기

    return process
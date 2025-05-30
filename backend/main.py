from comfy_launcher import launch_comfy_server

# comfy_process = launch_comfy_server() # comfy 서버 실행


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routes import users, recommend

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 초기화
init_db()

# 라우터 등록
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(recommend.router, prefix="/recommendations", tags=["Recommendations"])

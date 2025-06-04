from comfy_launcher import launch_comfy_server

# comfy_process = launch_comfy_server() # comfy 서버 실행

from fastapi import FastAPI, HTTPException # HTTPException 추가
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users, pokemon, chatbot

import os
from dotenv import load_dotenv

# MCP 클라이언트
from langchain_mcp_adapters.client import MultiServerMCPClient

# lifespan 사용을 위해 contextlib에서 asynccontextmanager 임포트
from contextlib import asynccontextmanager

from db import init_db
from agent.chatbot_agent import initialize_session_store


load_dotenv()
# ⭐️⭐️⭐️ .env 파일에서 API 키를 불러오기
SMITH_API_KEY = os.getenv("SMITH_API_KEY")
if not SMITH_API_KEY:
    print("🔥🔥🔥 FATAL ERROR: SMITH_API_KEY 환경 변수가 설정되지 않았습니다. 앱을 시작할 수 없습니다. 🔥🔥🔥")


	# 앱 시작 시 MCP 클라이언트 초기화, 툴 한 번만 가져와서 app.state에 저장

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 앱의 생명주기 관리: 시작 시 MCP 클라이언트 초기화 및 툴 로딩, 종료 시 정리."""
    print('앱 시작 중 (Lifespan): 멀티 클라이언트 세팅 시작')
    
    # ⭐️⭐️⭐️ API 키가 없는 경우 클라이언트 초기화 시도조차 하지 않음
    if not SMITH_API_KEY:
        print("MCP 클라이언트 초기화 건너뛰기: SMITH_API_KEY 없음.")
    
    else:
        try:

    # 1. MCP 클라이언트 설정 (앱 시작 시 한 번만!)
            # 여러 서버를 사용한다면 여기에 모든 서버 설정 추가
            app.state.mcp_client = MultiServerMCPClient(
                {
                    "poke-mcp": {
                        "command": "npx",
                        "args": [
                            "-y",
                            "@smithery/cli@latest",
                            "run",
                            "@NaveenBandarage/poke-mcp",
                            "--key",
                            SMITH_API_KEY
                        ],
                        'transport':'stdio'
                    }
                }
            )
            print('MCP 클라이언트 세팅 완료. 서버로부터 도구 가져오는 중...')

    # 2. 서버로부터 툴 가져오기 (앱 시작 시 한 번만!)
            tools = await app.state.mcp_client.get_tools()
            app.state.loaded_tools = tools # 성공 시 app.state에 툴 저장

            print(f'도구 가져오기 성공! 사용 가능한 툴은: {[tool.name for tool in app.state.loaded_tools]}')
            # print(f"가져온 툴 객체들: {app.state.loaded_tools}\n")
            print(f"가져온 툴 개수: {len(app.state.loaded_tools)}")

        except Exception as e:

            print(f'🔥🔥🔥 앱 시작 시 도구 가져오는 중 심각한 에러 발생: {e} 🔥🔥🔥')
            print(f'에러 타입: {type(e)}')
            print(f'e.message: {getattr(e, "message", "message 속성 없음")}')
            print(f'e.args: {getattr(e, "args", "args 속성 없음")}')
            if hasattr(e, "errors"):
                print(f'e.errors(): {e.errors()}')


    yield

    print('앱 종료 중 (Lifespan): 정리 작업 시작')
    if app.state.mcp_client:
        # MCP 클라이언트가 종료 메소드를 제공한다면 호출
        # await app.state.mcp_client.shutdown() # 예시
        print('MCP 클라이언트 정리 작업 완료 (종료 메소드 호출 등)')
        
    print('앱 종료 완료.')




app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pokemon.router, prefix="/pokemon", tags=["Pokemon"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])


# DB 초기화
init_db()


# Session Store 초기화
initialize_session_store()

# --reload는 코드가 두 번 실행됨
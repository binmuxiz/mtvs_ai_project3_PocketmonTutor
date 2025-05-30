import asyncio
import os
import sys # sys 모듈 추가
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException # HTTPException 추가
from pydantic import BaseModel, Field # ⭐️⭐️⭐️ Pydantic 관련 요소들 임포트
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# LangGraph를 사용한다면
from langgraph.prebuilt import create_react_agent
# MCP 클라이언트
from langchain_mcp_adapters.client import MultiServerMCPClient
# lifespan 사용을 위해 contextlib에서 asynccontextmanager 임포트
from contextlib import asynccontextmanager

# 필요하다면 여기서 사용자 정보 딕셔너리도 전역 변수로 관리할 수 있겠지
user_info_dict = {}

load_dotenv()
# ⭐️⭐️⭐️ .env 파일에서 API 키를 불러오기
SMITH_API_KEY = os.getenv("SMITH_API_KEY")
if not SMITH_API_KEY:
    print("🔥🔥🔥 FATAL ERROR: SMITH_API_KEY 환경 변수가 설정되지 않았습니다. 앱을 시작할 수 없습니다. 🔥🔥🔥")

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
            print(f"가져온 툴 객체들: {app.state.loaded_tools}")
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

# ⭐️⭐️⭐️ FastAPI 앱 인스턴스 생성 시 lifespan 인자로 정의한 lifespan 함수 전달
app = FastAPI(lifespan=lifespan)

# ⭐️⭐️⭐️ PromptRequest를 Pydantic BaseModel로 상속받도록 수정
class PromptRequest(BaseModel):
    val_1: str = Field(..., description="성격")
    val_2: str = Field(..., description="취미나 관심사")
    val_3: str = Field(..., description="선호하는 색상")
    val_4: str = Field(..., description="선호하는 분위기")
    val_5: str = Field(..., description="선호하는 타입(속성)")

@app.post('/send_text')
async def send_text(request: PromptRequest) -> str:
    # 1. 요청 데이터에서 값 추출
    val_1 = request.val_1
    val_2 = request.val_2
    val_3 = request.val_3
    val_4 = request.val_4
    val_5 = request.val_5

    # 2. 템플릿 프롬프트에 값 삽입
    prompt = f'''
    1.성격:{val_1} 
    2.취미나 관심사:{val_2} 
    3.선호하는 색상: {val_3} 
    4.선호하는 분위기: {val_4} 
    5.선호하는 타입(속성): {val_5} 
    위에서 제공한 5가지 정보를 최대한 반영해서 어울리는 포켓몬을 6마리 추천해줘
    해당 포켓몬을 추천하는 이유도 작성해줘
    추천한 포켓몬이 최소 3개의 정보와는 매칭이 됐으면 좋겠어
    매칭이 안 된다면 매칭이 된 애들은 그대로 두고 총 6마리를 채울 때까지 다시 검색해도 괜찮아
    찾은 포켓몬들의 이미지도 각각 가져와줘
    이미지 url은 (https://img.pokemondb.net/artwork/(포켓몬 영문명 소문자로).jpg) 이런식으로 보내줘
    이름과 url 영어로 하되 이외 설명은 가능하면 한글로 설명해줘
    '''

    print(f'[{prompt}] 텍스트 요청 수신')

    # 3. 툴 로딩 확인 (이전 코드와 동일)
    if not app.state.loaded_tools:
        print('🚨 툴이 로딩되지 않아 에이전트 실행 불가. 에러 응답 반환.')
        raise HTTPException(status_code=503, detail="서비스 준비 중 또는 오류 발생: 필요한 도구를 불러오지 못했습니다.")

    # 4. 에이전트 실행 (이전 코드와 동일)
    model = ChatOpenAI(model='gpt-4o-mini')
    tools = app.state.loaded_tools
    agent_executor = create_react_agent(model, tools)
    try:
        response = await agent_executor.ainvoke(
                    {"messages": [HumanMessage(content=prompt)]}
                )
        print('에이전트 실행 완료.')
        return response['messages'][-1].content
    except Exception as e:
        print(f'❌ 에이전트 실행 중 오류 발생: {e}')
        raise HTTPException(status_code=500, detail=f"에이전트 실행 중 오류 발생: {e}")

# 이 부분은 Uvicorn 등으로 직접 실행해야 함 (예: uvicorn your_module_name:app --reload)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

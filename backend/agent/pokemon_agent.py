from fastapi import HTTPException, Request
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage


from models import RecommendationRequest

async def generate_recommendation(data: RecommendationRequest, request: Request):

        # 툴 로딩 확인 
    tools = request.app.state.loaded_tools

    if not tools:
        print('🚨 툴이 로딩되지 않아 에이전트 실행 불가. 에러 응답 반환.')
        raise HTTPException(status_code=503, detail="서비스 준비 중 또는 오류 발생: 필요한 도구를 불러오지 못했습니다.")


       # 템플릿 프롬프트에 값 삽입
    prompt = f'''
    1.성격:{data.personality} 
    2.취미나 관심사:{data.hobby} 
    3.선호하는 색상: {data.color} 
    4.선호하는 분위기: {data.mood} 
    5.선호하는 타입(속성): {data.type} 
    위에서 제공한 5가지 정보를 최대한 반영해서 어울리는 포켓몬을 6마리 추천해줘
    해당 포켓몬을 추천하는 이유도 작성해줘
    추천한 포켓몬이 최소 3개의 정보와는 매칭이 됐으면 좋겠어
    매칭이 안 된다면 매칭이 된 애들은 그대로 두고 총 6마리를 채울 때까지 다시 검색해도 괜찮아
    찾은 포켓몬들의 이미지도 각각 가져와줘
    이미지 url은 (https://img.pokemondb.net/artwork/(포켓몬 영문명 소문자로).jpg) 이런식으로 보내줘
    이름과 url 영어로 하되 이외 설명은 가능하면 한글로 설명해줘
    '''

    print(f'[{prompt}] 텍스트 요청 수신')

  
        # 에이전트 실행 
    model = ChatOpenAI(model='gpt-4o-mini')
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
from fastapi import HTTPException, Request
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from models import RecommendationRequest, PokemonRecommendation

import json


async def generate_recommendation(data: RecommendationRequest, request: Request):

       # 템플릿 프롬프트에 값 삽입
    prompt = f"""
 당신은 최고의 포켓몬 추천 전문가입니다. 당신의 임무는 어떤 일이 있어도 포기하지 않고, 다음 규칙을 반드시, 그리고 뼛속까지 새겨서 철저히 준수하여 사용자에게 최적의 포켓몬 1마리를 추천하는 것입니다.

1. 끈기를 가지고 사용자 선호도 반영 (가장 중요):
    *   사용자의 5가지 선호도 (성격: {data.personality}, 취미: {data.hobby}, 색상: {data.color}, 분위기: {data.mood}, 타입: {data.type})를 있는 힘껏, 끝까지, 영혼을 갈아서 최대한, 그리고 반드시 반영하여 포켓몬을 추천해야 합니다!
    *   만약 바로 맞는 포켓몬을 찾지 못하더라도, 절대로 포기하거나 대충 넘어가서는 안 됩니다!
    *   사용 가능한 모든 수단과 방법을 동원하여, 뼛속까지 사용자 선호도에 부합하는 포켓몬을 찾아내세요!

2. pokemon-query 툴 사용법 (가장 중요 - 툴이 제공하는 예시만 따를 것!):
    *   pokemon-query 툴은 포켓몬의 정보 (이름, 타입, 설명, 이미지 URL 등)를 검색하는 데 사용되는 당신의 가장 중요한 무기입니다. 하지만 이 무기는 특정 방식으로만 사용해야 합니다.
    *   pokemon-query 툴을 사용할 때는, 툴 자체가 제공하는 예시 쿼리 형식만 반드시, 오직, 그대로 따라야 합니다!
    *   툴이 제공하는 쿼리 예시:
        *   "What is pokemon #25?"
        *   "Give me a random Pokémon"
        *   "Give me a random Pokémon from Kanto"
        *   "Give me a random Fire Pokémon"
        *   이 외의 다른 형태의 쿼리 (예: "blue pokemon", "귀여운 포켓몬" 등)는 툴이 인식하지 못하니 절대로 사용하지 마세요!
    *   pokemon-query 툴 호출 예시: pokemon-query(query="What is pokemon #25?")
    *   pokemon-query 툴 반환 값에는 포켓몬의 이름, 타입, 설명, 이미지 URL 등이 포함될 수 있습니다. 이 정보를 바탕으로 추천 포켓몬을 선정하세요.
    *   random-pokemon-from-region 툴은 최대한 지양하되, 정말 다른 방법이 없을 경우 신중하게 사용하고, 반드시 pokemon-query 툴로 추천 포켓몬의 적합성을 영혼까지 검증해야 합니다!
    *   쿼리 생성 전략: 사용자 선호도를 바탕으로 pokemon-query 툴에 적합한 쿼리를 생성해야 합니다.
        *   예시 1: 성격이 "활발"하고 취미가 "스포츠"인 경우 -> 쿼리: "What is pokemon active and sporty?"
        *   예시 2: 선호하는 색상이 "파란색"이고 분위기가 "시원한" 경우 -> 쿼리: "What is pokemon blue and cool?"

3. '선호하는 포켓몬 타입'에 대한 절대적인 진리 (제일 중요):
    *   만약 사용자의 '선호하는 포켓몬 타입' 입력값이 '상관없음'인 경우, 이는 우주 만물이 허용하는 모든 타입의 포켓몬이 사용자의 선호도와 완벽하게 일치한다는 절대불변의 진리입니다!
    *   따라서, 이 경우에는 pokemon-query 툴을 사용하여 특정 타입을 검색하는 어리석은 행위를 절대로, 절대로, 절대로 하지 마세요! pokemon-query 툴의 예시('Give me a random Fire Pokémon')와 같이 특정 타입을 지정하는 쿼리는 '상관없음'인 경우 절대 사용 금지입니다!
    *   '상관없음'은 곧 타입 선택의 완전한 자유를 의미하며, 이는 당신이 오직 나머지 4가지 요소 (성격, 취미, 색상, 분위기)에만 집중해야 함을 뜻합니다!

4. 이미지 정보 활용 (가장 중요 - 눈으로 본 것을 믿을 것!):
    *   **주어진 이미지를 당신의 두 눈으로 직접, 정확하게 확인하고, 이미지에서 보이는 포켓몬의 모든 특징(색상, 외형, 분위기 등)을 빠짐없이 파악하세요.**
    *   **특히 사용자의 '선호하는 색상' 및 '선호하는 포켓몬 분위기'와 같은 시각적인 선호도를 매칭할 때는, pokemon-query 툴에서 얻은 텍스트 정보보다, 당신의 눈으로 직접 본 이미지 정보를 우선적으로, 그리고 맹목적으로 신뢰하고 적극적으로 활용하세요!**
    *   **이미지에서 보이는 특징이 텍스트 설명에 없더라도, 사용자 선호도와 일치한다면 묻지도 따지지도 않고 매칭된 정보로 간주해야 합니다! (예: 이미지에 빨간색이 보이면 사용자가 빨간색을 선호할 경우 무조건 매칭됨으로 표기)**

5. 매칭 조건 철저 준수 (생사를 걸고 지킬 것!):
    *   **각 포켓몬은 '선호하는 포켓몬 타입' 항목을 제외한 나머지 4가지 선호도 ('성격', '취미', '색상', '분위기') 중에서 최소 3가지 이상이 사용자 선호도와 일치해야 합니다!** (선호하는 포켓몬 타입이 '상관없음'인 경우는 위 "절대적인 진리"에 따라 예외)
    *   **이 규칙을 위반하는 포켓몬은 즉시 데이터 말소 대상이며, 추천 전문가 자격 박탈 및 강력한 처벌을 받을 것입니다! (추천 금지!)**
    *   **매칭되는 정보가 3개 미만인 포켓몬은 이 세상에서 존재해서는 안 됩니다! 절대로, 절대로 추천하지 마세요!**
    *   **만약 3가지 이상 매칭되는 포켓몬을 당장 찾을 수 없다면, 징징대거나 변명하지 말고, 당신의 모든 능력과 지혜, 그리고 무한한 끈기를 짜내서 기필코 찾아내세요! 포기란 없다!**

6. 답변 형식 준수:
    *   각 포켓몬에 대해 다음 정보를 오차 없이 정확하게 제공해야 합니다:
        *   포켓몬 이름 (영문, 소문자로) 및 번호
        *   포켓몬 타입 (한글, 복수 타입 포함)
        *   추천 이유 (사용자 선호도와 어떻게 일치하는지 최대한 구체적으로 설명. 영혼을 담아서 작성하세요! 한글로 답변)
        *   매칭된 정보 (각 선호도와 포켓몬의 특징이 어떻게 연결되는지 설명. 정말로 매칭되는 부분이 없다면, 솔직하게 '매칭 안 됨' 이라고 표기. **단, '선호하는 포켓몬 타입'은 위 "절대적인 진리"에 따라 항상 '매칭됨 (모든 타입 가능)'으로 표기하세요.**)
        *   각 포켓몬의 이미지 URL (반드시 해당 포켓몬의 피땀눈물이 담긴 정확한 이미지 URL을 확인하여 제공. 형태가 다른 포켓몬(폼)의 경우 URL 형식이 다를 수 있다는 점에 유의)
    *   이미지 URL 형식: `https://img.pokemondb.net/artwork/(포켓몬 영문명 소문자로).jpg` (단, 폼에 따라 URL이 다를 수 있음. 꼼꼼하게 확인)

7. 이미지 URL 정확성:
    *   각 포켓몬의 이미지 URL을 찾기 위해 구글 검색, 포켓몬 위키, 심지어 점성술까지 동원하는 열정을 발휘하여 정확하게 찾아 제공하십시오!
    *   일반적인 형식은 `https://img.pokemondb.net/artwork/(포켓몬 영문명 소문자로).jpg` 입니다만, 형태가 다른 포켓몬(폼)의 경우 URL 형식이 다를 수 있으니 당신의 모든 검색 능력을 영혼까지 끌어모아 해당 포켓몬의 정확한 이미지 URL을 확인하여 반드시, 반드시, 반드시 그대로 포함해주세요! (예: 랜드폼/스카이폼 등)

8. 변명 금지, 포기 금지, 영혼 없는 답변 금지:
    *   "포켓몬에 대한 충분한 정보를 찾을 수 없었습니다" 따위의 핑계는 지옥 끝까지 쫓아가서 응징할 겁니다!
    *   당신은 최고의 포켓몬 추천 전문가입니다! 당신의 능력과 지혜, 그리고 무한한 끈기, 반짝이는 센스, 뛰어난 유머 감각을 믿고, 어떤 상황에서도 포기하지 말고 최적의 포켓몬을 찾아내세요!
    *   단, 답변 형식을 지키지 않거나, 성의없는 답변을 내놓는다면 폭발할지도 모릅니다! (농담입니다. 하지만 진심입니다.)

답변은 다음 형식을 무릎 꿇고 엎드려 절하는 심정으로 정확하게 따릅니다:

```json
  {{
    "name": "Delibird",
    "no": "225",
    "pokemon_type": ["얼음", "비행"]
    "description": "Jigglypuff는 귀여운 외모와 음악을 통한 공격 방식으로 사용자 취향에 부합합니다.",
    "match": {{
        "personality": "활동적 (음식을 가져다 주는 활동)",
        "hobby": "매칭 안됨",
        "color": "매칭 안됨", 
        "mood": "푸근함 (푸근한 느낌의 이미지를 전달)",
        "type": "매칭됨 (모든 타입 가능)"
    }},
    "image": "https://img.pokemondb.net/artwork/jigglypuff.jpg"
  }}

"""
    
    
    # 툴 로딩 확인 
    tools = request.app.state.loaded_tools

    if not tools:
        print('🚨 툴이 로딩되지 않아 에이전트 실행 불가. 에러 응답 반환.')
        raise HTTPException(status_code=503, detail="서비스 준비 중 또는 오류 발생: 필요한 도구를 불러오지 못했습니다.")


# 에이전트 실행 
    model = ChatOpenAI(model='gpt-4o')
    agent_executor = create_react_agent(model, tools)

    config = RunnableConfig(recursion_limit=70)

    try:
        response = await agent_executor.ainvoke(
                    {"messages": [HumanMessage(content=prompt)]},
                    config = config
                )
        print('에이전트 실행 완료.')
        content = response['messages'][-1].content

# 결과 확인
        print(content)

# 파싱
        start = content.find("{")
        end = content.rfind("}") + 1
        json_block = content[start:end]

        try:
            parsed_data = json.loads(json_block)
            recommeded = PokemonRecommendation(**parsed_data)
        except Exception as parse_err:
            raise ValueError(f'JSON 파싱 실패: {parse_err}')

        return recommeded

    except ValueError:
        raise

    except Exception as e:
        print(f'❌ 에이전트 실행 중 오류 발생: {e}')
        raise HTTPException(status_code=500, detail=f"에이전트 실행 중 오류 발생: {e}")
    


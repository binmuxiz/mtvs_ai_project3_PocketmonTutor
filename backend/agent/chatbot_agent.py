# 챗봇 에이전트 -> 일반 대화, 할일 관리, 문제 생성

from agent.todo import TodoToolkit

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from functools import lru_cache

from db import add_todo, view_todos, complete_todo, remove_todo, get_todos_by_user_id
from db import save_chat

import json

# 문제 생성 ==================================================================



from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import traceback


async def generate_eng_problem(scenario: str) -> str:
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

    print(f"Eng Problem 호출됨! 시나리오: {scenario}")  # 로그 추가
    try:
        print(f"📨 입력된 시나리오: {scenario}")
        prompt = PromptTemplate(
            input_variables=["scenario"],
            template="""
            너는 고등학교 영어 내신 문제 전문가야. 주어진 상황은 일상 생활에서 일어난다고 가정해.
            그 상황에 맞는 대한민국 고등학교 영어 내신 문제를 하나 만들어줘. 문제는 다음 기준을 따라야 해:

            - 2025년 현재, 대한민국 고등학교 영어 수준을 기반으로 해야 함.
            - 고등학생이 겪을 수 있을 일상 등 다양한 주제를 다룰 수 있음.
            - 정답과 해설을 반드시 포함할 것. 해설은 50단어 이내로 간결하게 작성해줘.

            다음 형식을 따라줘:
            문제: ...
            보기:
            A) ...
            B) ...
            C) ...
            D) ...
            정답: (예: B)
            해설: (이유 설명)

            상황:
            {scenario}

            출제된 영어 문제:
            """
        )
        formatted_prompt = prompt.format(scenario=scenario)
        result = await llm.ainvoke(formatted_prompt)
        print("📤 문제 생성 완료")
        return result.content
    
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"❌ generate_life_problem 에러 발생: {e}\n{error_message}")  # 에러 메시지 로그
        return "문제 생성 중 예기치 못한 오류가 발생했습니다. 나중에 다시 시도해주세요."



eng_problem_tool = Tool(
    name="EngProblemTool",
    func=generate_eng_problem,
    coroutine=generate_eng_problem,
    description="일상 생활에 기반해 고등학교 영어 내신 문제를 생성하고 정답과 해설을 제공합니다."
)


@lru_cache()    # 파라미터가 동일한 함수 호출 결과를 캐시해서 두 번째 호출부터는 같은 객체를 반환해준다. 
def get_agent_executor():
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

# 툴 추가
    todo_toolkit = TodoToolkit()
    todo_tools = todo_toolkit.get_tools()

    tools_for_agent = todo_tools + [eng_problem_tool]

    prompt = ChatPromptTemplate.from_messages([
        ('system', """
        너는 사용자의 다양한 요청을 처리하는 AI 어시스턴트야.
                
        너의 역할은 다음과 같아:
                
        1. 사용자의 할 일 관리 요청이 오면, 툴을 사용해서 처리해. (add/view/complete/remove)
        2. 영어 문제 생성을 요청받으면, 반드시 "EngProblemTool" 툴을 사용해 문제를 생성해.
        3. 그 외 일상 대화는 자연스럽게 응답해.
        
         **중요**:
         - 툴을 사용할 땐 JSON으로 명확하게 결과를 반환해야 해. 예: 
         {{"action": "add_todo", "title": "수학 10문제 풀기"}}
         {{"action": "EngProblemTool", "title": "친구와 길을 잃은 상황"}}
         - 툴 사용이 아닌 경우엔 자연스럽게 텍스트로 응답하면 돼.
         - 사용자가 명확히 툴과 관련된 요청을 하지 않으면, 툴을 실행하지 마.

         예시:
        - "오늘 뭐할까?" → 자연어 응답
        - "할 일 목록 보여줘" → {{"action": "view_todos"}}
        - "오늘 할거 때려치고 노래방이나 갈끼" → {{"action": "view_todos"}}
            - 이런 경우엔 오늘의 할일 목록을 확인하고 적절한 대답 생성. 예: "오늘 아래와 같은 할일들이 존재해요. 노래방은 할일을 다 하고 갑시다!"
         

        """),
        ('placeholder', '{chat_history}'),
        ('user', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ])

    agent = create_tool_calling_agent(llm, tools_for_agent, prompt)
    executor = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent, 
        verbose=True, 
        return_intermediate_steps=True
        )

    return executor


from langchain_community.chat_message_histories import ChatMessageHistory
from db import load_chat_history, get_all_user_ids


session_store = {}

def initialize_session_store():
    user_ids = get_all_user_ids()  
    session_ids = user_ids

    for sid in session_ids:
        messages = load_chat_history(sid)  # DB에서 해당 세션의 채팅 로그 불러오기
        history = ChatMessageHistory()
        for msg in messages:
            if msg['sender'] == 'user':
                history.add_user_message(msg['message'])
            elif msg['sender'] == 'ai':
                history.add_ai_message(msg['message'])
        session_store[sid] = history




# 메시지 히스토리와 함께 실행하는 래퍼 함수
async def invoke_agent(input_text: str, session_id: str, user_id: str):

# ✅ USER Message 저장
    save_chat(user_id=user_id, sender='user', message=input_text)

    agent_executor = get_agent_executor()

    def get_session_history(sid):
        if sid not in session_store:
            session_store[sid] = ChatMessageHistory()
        return session_store[sid]


    agent_with_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history'
    )

    config = {
        'configurable': {
            'session_id': session_id,
        },
    }
    
    # result = agent_with_history.invoke({'input': input_text}, config=config)
    result = await agent_with_history.ainvoke({'input': input_text}, config=config)

    # print(result)
    
# ✅ AI 응답 저장
    if result.get("output"):
        save_chat(user_id=user_id, sender='ai', message=result['output'])

# ✅ tools 사용 확인 
    intermediate_steps = result.get('intermediate_steps', [])

    output_message = result['output']

    for step in intermediate_steps:
        action, tool_output = step
        tool_name = action.tool

        if tool_name == "EngProblemTool":
            print("----------------------- EngProblemTool ------------------------------")
            return tool_output 

        try:
            parsed = json.loads(tool_output)
        except json.JSONDecodeError:
            continue  # 잘못된 JSON이면 무시

        if tool_name == "add_todo":
            print("----------------------- add todo ------------------------------")
            title = parsed.get("title")
            if title:
                add_todo(user_id=user_id, title=title)
                return output_message

        elif tool_name == "view_todos":
            print("----------------------- view todos ------------------------------")
            return view_todos(user_id=user_id)

        elif tool_name == "complete_todo":
            print("----------------------- complete todo ------------------------------")
            title = parsed.get("title")
            todo_id = parsed.get("todo_id")
            print("1. todo id => ",{todo_id})

            todo_id = await get_todo_id(user_id=user_id, title=title)
            print("2. todo id => ",{todo_id})

            if todo_id:
                complete_todo(user_id=user_id, todo_id=todo_id)
                return f"🎉 {output_message}"
            else:
                return "❌ 해당 할 일을 찾을 수 없어요."
            

        elif tool_name == "remove_todo":
            print("----------------------- remove todo ------------------------------")
            title = parsed.get("title")
            todo_id = parsed.get("todo_id")
            print("1. todo id => ",{todo_id})

            todo_id = await get_todo_id(user_id=user_id, title=title)
            print("2. todo id => ",{todo_id})

            if todo_id:
                remove_todo(user_id=user_id, todo_id=todo_id)
                return f"🗑️ {output_message}"
            else:
                return "❌ 해당 할 일을 찾을 수 없어요."
    
    print("----------------------- 일반 채팅 ------------------------------")
    return output_message


async def get_todo_id(user_id, title) -> str:
    todos = get_todos_by_user_id(user_id=user_id)

    todo_json = json.dumps(todos, ensure_ascii=False, indent=2)


    llm_prompt = f"""
        아래는 사용자의 할 일 목록입니다.

        {todo_json}

        사용자의 할일: "{title}"

        위 목록 중 어떤 항목에 해당하는 것인지 추론하여, 가장 적절한 todo의 ID를 숫자 하나로 반환하세요.

        형식: 숫자(ID)만 단독으로 출력
    """

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    todo_id_result = await llm.ainvoke(llm_prompt)

    todo_id = todo_id_result.content.strip()
    
    return todo_id

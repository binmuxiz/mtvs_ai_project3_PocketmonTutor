# 챗봇 에이전트 -> 일반 대화, 할일 관리, 문제 생성

from agent.todo import TodoToolkit

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from functools import lru_cache

from db import add_todo
from db import save_chat

session_store = {}

import json

# 메시지 히스토리와 함께 실행하는 래퍼 함수
def invoke_agent(input_text: str, session_id: str, user_id: str):

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
    
    result = agent_with_history.invoke({'input': input_text}, config=config)
    # print(result)

    intermediate_steps = result.get('intermediate_steps', [])

        
    for step in intermediate_steps:
        action, tool_output = step
        # print(action.tool)  # "add_todo"
        # print(action.tool_input)  # {'title': '오늘 수학문제 10문제 풀기'}
        # print(tool_output)  # '{"action": "add_todo", "title": "오늘 수학문제 10문제 풀기"}'

        try:
            parsed = json.loads(tool_output)
            if isinstance(parsed, dict) and parsed.get("action") == "add_todo":
                title = parsed.get("title")
                add_todo(user_id=user_id, title=title)
                return f"✅ '{title}' 할 일을 저장했어요!"
        except json.JSONDecodeError:
            continue  # 툴이 JSON 반환을 안 했으면 무시

    return result['output']

    # output = result['output']

    # ✅ AI 응답 저장
    save_chat(user_id=user_id, sender='ai', message=output)

    # 문자열을 JSON으로 파싱
    try:
        parsed = json.loads(output)

        if isinstance(parsed, dict) and 'action' in parsed:
            # 툴 결과 처리
            if parsed.get("action") == "add_todo":
                title = parsed.get("title")
                add_todo(user_id=user_id, title=title)
                return f"✅ '{title}' 할 일을 저장했어요!"
        
        else:   # 일반 답변 / 문제 생성
            return output
        
    except json.JSONDecodeError:
        return f"JSONDecodeError ==> {output}"   # 일반 자연어 응답



# @lru_cache()    # 파라미터가 동일한 함수 호출 결과를 캐시해서 두 번째 호출부터는 같은 객체를 반환해준다. 
def get_agent_executor():
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

# 툴 추가
    todo_toolkit = TodoToolkit()
    tools = todo_toolkit.get_tools()

    prompt = ChatPromptTemplate.from_messages([
        ('system', """
        너는 사용자의 다양한 요청을 처리하는 AI 어시스턴트야.
                
        너의 역할은 다음과 같아:
                
        1. 사용자의 할 일 관리 요청이 오면, 툴을 사용해서 처리해. (add/view/complete/remove)
        2. 문제가 필요하다는 요청이 오면, 직접 문제를 생성해서 자연어로 출력해.
        3. 그 외 일상 대화는 자연스럽게 응답해.
        
         **중요**:
         - 툴을 사용할 땐 JSON으로 명확하게 결과를 반환해야 해. 예: {{"action": "add_todo", "title": "수학 10문제 풀기"}}
         - 툴 사용이 아닌 경우엔 자연스럽게 텍스트로 응답하면 돼.
         - 사용자가 명확히 툴과 관련된 요청을 하지 않으면, 툴을 실행하지 마.

         예시:
        - "오늘 뭐할까?" → 자연어 응답
        - "할 일 목록 보여줘" → {{"action": "view_todos"}}
        - "수학 문제 하나 만들어줘" → 자연어 문제 생성
         
        툴은 오직 JSON 응답만 반환하고, 그 외엔 자연어로 대화해.
        """),
        ('placeholder', '{chat_history}'),
        ('user', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

    return executor





from fastapi import APIRouter

from pydantic import BaseModel, Field

from agent.chatbot_agent import invoke_agent


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatPrompt(BaseModel):
    user_id: str = Field(..., description="사용자 고유 ID")
    text: str = Field(..., description='chatbot에게 하고 싶은 말')


@router.post("/")
async def chatbot(request: ChatPrompt) -> str:
    user_input = request.text
    user_id = request.user_id

    output = invoke_agent(user_input, session_id=user_id, user_id=user_id)
    return output
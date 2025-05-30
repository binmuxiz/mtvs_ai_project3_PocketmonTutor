from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    user_id: str = Field(..., description="id")
    name: str = Field(..., description="이름")

class RecommendationRequest(BaseModel):
    user_id: str = Field(..., description="id")
    personality: str = Field(..., description="성격")
    hobby: str = Field(..., description="취미나 관심사")
    color: str = Field(..., description="선호하는 색상")
    mood: str = Field(..., description="선호하는 분위기")
    type: str = Field(..., description="선호하는 타입(속성)")

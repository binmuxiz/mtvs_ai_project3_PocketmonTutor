from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str
    name: str

class RecommendationRequest(BaseModel):
    user_id: str
    personality: str
    hobby: str
    color: str
    mood: str
    type: str

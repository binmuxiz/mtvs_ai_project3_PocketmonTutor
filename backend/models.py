from pydantic import BaseModel, Field
from typing import List, Dict

class UserLogin(BaseModel):
    user_id: str

class UserCreate(BaseModel):
    user_id: str = Field(..., description="id")
    name: str = Field(..., description="이름")

class PokemonRequest(BaseModel):
    user_id: str = Field(..., description="id")
    personality: str = Field(..., description="성격")
    hobby: str = Field(..., description="취미나 관심사")
    color: str = Field(..., description="선호하는 색상")
    mood: str = Field(..., description="선호하는 분위기")
    type: str = Field(..., description="선호하는 타입(속성)")


# 3d 모델 생성 요청
class PokemonModelRequest(BaseModel):
    user_id: str
    name: str
    no: str
    pokemon_type: List[str]
    description: str
    match: Dict[str, str]
    image: str



class Pokemon(BaseModel):
    user_id: str
    name: str
    no: str
    pokemon_type: List[str]
    description: str
    match: Dict[str, str]
    image: str
    model_file_path: str
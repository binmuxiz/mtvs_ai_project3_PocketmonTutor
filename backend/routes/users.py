from fastapi import APIRouter, HTTPException
from models import UserCreate, UserLogin
from db import get_connection, get_user_by_id, create_user
router = APIRouter()



@router.post("/")
async def generate(data: UserCreate):
    
# 유저 존재 확인
    user_row = get_user_by_id(data.user_id)

    if user_row:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자 ID입니다.")

# 없으면 등록
    try:
        create_user(data)
        print("사용자 등록 완료 id = ", data.user_id)

    except Exception as e:
        raise

    return {
        "message": "사용자 등록 완료!",
    }



@router.post("/login")
async def login(data: UserLogin):
    user_row = get_user_by_id(data.user_id)

    if not user_row:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자 ID입니다.")
    
    # 포켓몬 데이터 응답
    try:
        pokemon = get_pokemon(data.user_id)
        return {
            "message": "로그인 성공",
            "user_id": data.user_id,
            "pokemon": pokemon  # Pydantic 모델을 JSON 응답으로 변환
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"포켓몬 데이터를 불러오는 데 실패했습니다: {e}")




import json
from db import get_pokemon_by_user_id
from models import Pokemon

def get_pokemon(user_id: str) -> Pokemon:
    try:
        row = get_pokemon_by_user_id(user_id)
        if not row:
            raise ValueError(f"No Pokemon found for user_id: {user_id}")
        
                # row는 튜플로 가정하고 언패킹합니다
        return Pokemon(
            user_id=row[0],
            name=row[1],
            no=str(row[2]),  # Pydantic에서 str 기대하므로
            pokemon_type=row[3].split(','),  # "풀,페어리" → ["풀", "페어리"]
            description=row[4],
            match=json.loads(row[5]),  # 안전하게 JSON 디코딩
            image=row[6],
            model_file_path=row[7]
        )
    
    except Exception as e:
        raise RuntimeError(f"Failed to get Pokemon for user_id {user_id}: {e}")
        
from fastapi import APIRouter, HTTPException
from models import UserCreate
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


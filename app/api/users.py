from typing import List

from fastapi import APIRouter

from app.database.database import database
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[User], response_description="Get all users")
async def get_users():
    users = await database.all_users()

    return users
